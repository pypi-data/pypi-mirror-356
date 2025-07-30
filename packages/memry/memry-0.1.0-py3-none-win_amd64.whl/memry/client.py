import json
import socket
import io
import pandas as pd
import pyarrow as pa
import pyarrow.ipc
from .exceptions import ConnectionError, ServerError

# --- CHANGED to a TCP Address ---
SERVER_ADDRESS = ("127.0.0.1", 56789)
BUFFER_SIZE = 8192

class MemryConnection:
    """Manages a persistent connection to the Memry daemon."""
    def __init__(self):
        self.sock = None
        self.reader = None

    def connect(self):
        if self.sock and self.is_connected():
            return
        try:
            # --- CHANGED to an INET (TCP) socket ---
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect(SERVER_ADDRESS)
            self.reader = self.sock.makefile('rb')
        except (socket.error, ConnectionRefusedError) as e:
            self.sock = None
            self.reader = None
            raise ConnectionError(
                f"Could not connect to Memry daemon at {SERVER_ADDRESS[0]}:{SERVER_ADDRESS[1]}. "
                "Is the server running?"
            ) from e
            
    def is_connected(self):
        try:
            # Create a temporary connection to check status without disrupting the main one
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as test_sock:
                test_sock.settimeout(0.5) # Don't wait forever
                test_sock.connect(SERVER_ADDRESS)
            return True
        except (socket.error, ConnectionRefusedError):
            return False

    def close(self):
        if self.sock:
            try:
                self.sock.close()
            except socket.error:
                pass
            self.sock = None
            self.reader = None

    def _ensure_connection(self):
        if not self.sock:
            self.connect()
        # Ping to check if the connection is still alive
        try:
            self._send_command_on_socket({'action': 'Ping'})
            response = self._receive_response_from_reader()
            if response.get('message') != 'pong':
                raise ConnectionError("Connection lost")
        except (socket.error, BrokenPipeError, ConnectionError):
            # If ping fails, reconnect and try again
            self.connect()

    def _send_command_on_socket(self, cmd_dict):
        payload = (json.dumps(cmd_dict) + '\n').encode('utf-8')
        self.sock.sendall(payload)
        
    def _receive_response_from_reader(self):
        line = self.reader.readline()
        if not line:
            raise ConnectionError("Daemon closed the connection unexpectedly.")
        
        resp = json.loads(line)
        if resp.get('status') == 'Error':
            raise ServerError(resp.get('message', 'Unknown server error'))
        return resp

    def _read_data(self, data_len):
        return self.reader.read(data_len)

# Global connection object for simple API
_connection = MemryConnection()

def put(df: pd.DataFrame) -> str:
    _connection._ensure_connection()
    if not isinstance(df, pd.DataFrame):
        raise TypeError("Input must be a pandas DataFrame")

    table = pa.Table.from_pandas(df, preserve_index=False)
    sink = io.BytesIO()
    with pa.ipc.new_stream(sink, table.schema) as writer:
        writer.write_table(table)
    
    data_bytes = sink.getvalue()
    
    cmd = {"action": "Put", "data_len": len(data_bytes)}
    _connection._send_command_on_socket(cmd)
    _connection.sock.sendall(data_bytes)
    
    response = _connection._receive_response_from_reader()
    return response['message']

def get(key: str) -> pd.DataFrame:
    _connection._ensure_connection()
    cmd = {"action": "Get", "key": key}
    _connection._send_command_on_socket(cmd)
    
    response = _connection._receive_response_from_reader()
    data_len = response['data_len']
    
    data_bytes = _connection._read_data(data_len)

    with pa.ipc.open_stream(data_bytes) as reader:
        table = reader.read_all()
    
    return table.to_pandas()

def delete(key: str):
    _connection._ensure_connection()
    cmd = {"action": "Delete", "key": key}
    _connection._send_command_on_socket(cmd)
    _connection._receive_response_from_reader()

def list_keys() -> list:
    _connection._ensure_connection()
    cmd = {"action": "ListKeys"}
    _connection._send_command_on_socket(cmd)
    response = _connection._receive_response_from_reader()
    return response.get('keys', [])

def shutdown_server():
    print("Sending shutdown command to Memry daemon...")
    try:
        _connection._ensure_connection()
        cmd = {"action": "Shutdown"}
        _connection._send_command_on_socket(cmd)
        _connection._receive_response_from_reader()
        print("Shutdown successful.")
    except ConnectionError:
        print("Could not connect to server. It might already be stopped.")
    finally:
        _connection.close()

def close():
    _connection.close()