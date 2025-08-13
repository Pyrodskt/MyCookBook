import subprocess
import os
import sys
import time

project_root = os.path.dirname(os.path.abspath(__file__))
front_path = os.path.join(project_root, 'front')
back_path = os.path.join(project_root, 'back')

def get_venv_python_executable(base_path):
    """Determines the path to the python executable within a venv."""
    if sys.platform == "win32":
        return os.path.join(base_path, 'venv', 'Scripts', 'python.exe')
    else:
        return os.path.join(base_path, 'venv', 'bin', 'python')

def run_command(command, cwd, env=None):
    print(f"Running command: {' '.join(command)} in {cwd}")
    process = subprocess.Popen(command, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
    return process

if __name__ == "__main__":
    # Get venv python executables
    back_python = get_venv_python_executable(back_path)
    front_python = get_venv_python_executable(front_path)

    # Check if venv executables exist
    if not os.path.exists(back_python):
        print(f"Error: Backend virtual environment not found at {back_python}. Please create it and install dependencies.")
        sys.exit(1)
    if not os.path.exists(front_python):
        print(f"Error: Frontend virtual environment not found at {front_python}. Please create it and install dependencies.")
        sys.exit(1)

    print("Starting backend API...")
    backend_env = os.environ.copy()
    backend_env['FLASK_APP'] = 'app.py'
    backend_process = run_command([back_python, '-m', 'flask', 'run', '--port', '5001'], cwd=back_path, env=backend_env)

    time.sleep(2) # Give backend a moment to start

    print("Starting frontend application...")
    frontend_env = os.environ.copy()
    frontend_env['FLASK_APP'] = 'app.py'
    frontend_process = run_command([front_python, '-m', 'flask', 'run', '--port', '5000'], cwd=front_path, env=frontend_env)

    print("\nBoth frontend and backend are starting...")
    print("Frontend: http://127.0.0.1:5000/")
    print("Backend API: http://127.0.0.1:5001/")
    print("Press Ctrl+C to stop both processes.")

    try:
        # Keep the main script alive until processes are terminated
        backend_process.wait()
        frontend_process.wait()
    except KeyboardInterrupt:
        print("\nStopping processes...")
        backend_process.terminate()
        frontend_process.terminate()
        backend_process.wait()
        frontend_process.wait()
        print("Processes stopped.")
