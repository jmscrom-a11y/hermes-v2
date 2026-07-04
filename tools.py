from pathlib import Path
from datetime import datetime
import shutil
import subprocess
from config import BACKUP_DIR

def backup_file(file_path):
    src = Path(file_path)
    if not src.exists():
        return False

    Path(BACKUP_DIR).mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    dst = Path(BACKUP_DIR) / f"{src.name}.{timestamp}.bak"
    shutil.copy2(src, dst)
    return str(dst)

def read_file(file_path):
    return Path(file_path).read_text(encoding="utf-8")

def write_file(file_path, content):
    backup_file(file_path)
    Path(file_path).write_text(content, encoding="utf-8")
    return True

def compile_check(file_path):
    result = subprocess.run(
        ["python3", "-m", "py_compile", file_path],
        capture_output=True,
        text=True,
    )
    return result.returncode == 0, result.stderr

def restart():
    subprocess.Popen(["bash", "restart.sh"])
