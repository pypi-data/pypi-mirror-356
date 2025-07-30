import subprocess
import sys
from pathlib import Path

def get_server_binary_path() -> Path:
    """
    Finds the path to the packaged Rust binary ('memryd'), handling
    both installed packages and local development environments. This function
    is platform-aware and looks for '.exe' on Windows.
    """
    # Determine the correct binary name based on the operating system
    if sys.platform == "win32":
        binary_name = "memryd.exe"
    else:
        binary_name = "memryd"

    # 1. Check the standard installation location first.
    install_path = Path(__file__).parent / "bin" / binary_name
    if install_path.exists():
        return install_path

    # 2. If not found, this is a development environment.
    #    The binary is in the project's root `target` directory.
    project_root = Path(__file__).parent.parent
    dev_path = project_root / "target" / "debug" / binary_name
    if dev_path.exists():
        return dev_path

    # Check release as a final fallback
    dev_path_release = project_root / "target" / "release" / binary_name
    if dev_path_release.exists():
        return dev_path_release
    
    # 3. If it's in none of those places, the build is broken.
    raise FileNotFoundError(
        f"Memry server binary ('{binary_name}') could not be found in the installation "
        "or development target directories. Please run 'maturin develop'."
    )

def main():
    """
    Finds and runs the compiled Memry daemon, letting it take over the
    current terminal. Press Ctrl+C in the terminal to stop the server.
    """
    try:
        server_path = get_server_binary_path()
        print(f"--- Launching Memry Server from: {server_path} ---")
        subprocess.run([server_path], check=True)
    except FileNotFoundError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"ERROR: Memry server exited with an error (code {e.returncode}).", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nLauncher interrupted. Server shut down.")
        sys.exit(0)

if __name__ == "__main__":
    main()