import os
import subprocess
import sys
import venv
from pathlib import Path
import argparse

REPO_URL = "https://github.com/MattSouzaDev/unichat.git"
PROJECT_DIR = Path("unichat")
VENV_DIR = PROJECT_DIR / "venv"

def run(cmd, cwd=None):
    subprocess.check_call(cmd, cwd=cwd, shell=(os.name == "nt"))

def main(username, email, password):
    if not PROJECT_DIR.exists():
        run(["git", "clone", REPO_URL])

    if not VENV_DIR.exists():
        venv.create(VENV_DIR, with_pip=True)

    if os.name == "nt":
        pip_path = VENV_DIR / "Scripts" / "pip.exe"
        python_path = VENV_DIR / "Scripts" / "python.exe"
    else:
        pip_path = VENV_DIR / "bin" / "pip"
        python_path = VENV_DIR / "bin" / "python"

    run([str(pip_path), "install", "--upgrade", "pip"])
    run([str(pip_path), "install", "Django", "Pillow"])
    run([str(python_path), "manage.py", "migrate"], cwd=PROJECT_DIR)

    superuser_cmd = (
        "from django.contrib.auth import get_user_model;"
        "User=get_user_model();"
        f"User.objects.create_superuser('{username}','{email}','{password}') "
        f"if not User.objects.filter(username='{username}').exists() else None"
    )
    run([str(python_path), "manage.py", "shell", "-c", superuser_cmd], cwd=PROJECT_DIR)
    run([str(python_path), "manage.py", "runserver"], cwd=PROJECT_DIR)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--user", default="admin")
    parser.add_argument("--email", default="admin@example.com")
    parser.add_argument("--senha", default="admin123")
    args = parser.parse_args()
    main(args.user, args.email, args.senha)
