import json
import subprocess
import os
import shutil
import zipfile
import streamlit as st
import platform


def create_react_app(payload_json):
    # ...existing code...
    try:
        # Check if npm is available
        if shutil.which("npm") is None:
            return None, "'npm' is not installed or not found in PATH."
        else:
            print("'npm' is available in PATH.")

        # Get current working directory
        cwd = os.getcwd()

        print("Received payload:", payload_json)
        payload = json.loads(payload_json)
        project_name = payload.get("project_name", "default_project").lower()
        framework = payload.get("framework", "react").lower()
    except json.JSONDecodeError as e:
        return None, f"Invalid JSON payload: {e}"

    try:
        # Get current working directory
        cwd = os.getcwd()
        project_dir = os.path.join(cwd, project_name)

        # Step 1: Run Vite create command
        print(
            f"Creating React app with framework '{framework}' and project name '{project_name}'...")

        print(f"Current working directory: {cwd}")
        print(f"Project directory: {project_dir}")

        # Create command based on OS
        npm_cmd = "npm.cmd" if platform.system() == "Windows" else "npm"

        result = subprocess.run(
            [
                npm_cmd, "create", "vite@latest", project_name,
                "--", "--template", f"{framework}"
            ],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        print("Vite output:", result.stdout)
        if result.stderr:
            print("Vite errors:", result.stderr)

        # Verify the project directory exists
        if not os.path.exists(project_dir):
            return None, f"Project directory not created: {project_dir}"

        # Step 2: Zip the project
        zip_filename = f"{project_name}.zip"
        if framework.endswith("-ts"):
            zip_filename = f"{project_name}-ts.zip"

        zip_path = os.path.join(cwd, zip_filename)
        print(f"Zipping project to {zip_path}")

        # Remove existing zip if it exists
        if os.path.exists(zip_path):
            os.remove(zip_path)

        print(f"Creating zip archive for {project_name}...")

        # Create zip archive using the ZipFile module instead of shutil
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Walk through all files and directories in the project folder
            for root, dirs, files in os.walk(project_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    # Calculate relative path for zip structure
                    relative_path = os.path.relpath(file_path, cwd)
                    # Use os.path.normpath to handle path separators correctly across platforms
                    relative_path = os.path.normpath(relative_path)
                    zipf.write(file_path, relative_path)

        print(f"Zip archive created at {zip_path}")

        # Step 3: Clean up the project directory
        print(f"Cleaning up project directory: {project_dir}")
        shutil.rmtree(project_dir, ignore_errors=True)
        print(f"Project directory {project_dir} cleaned up.")

        # Verify the zip file exists
        if not os.path.exists(zip_path):
            return None, f"Failed to create zip file: {zip_path}"

        return zip_path, f"React app '{project_name}' created and zipped successfully."

    except subprocess.CalledProcessError as e:
        return None, f"Command failed: {e}"
    except Exception as e:
        import traceback
        # Print full error traceback for debugging
        print(traceback.format_exc())
        return None, f"An error occurred: {str(e)}"
