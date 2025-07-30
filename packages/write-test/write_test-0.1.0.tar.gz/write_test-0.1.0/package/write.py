from pathlib import Path
import shutil

def get_user_file():
    user_dir = Path.home() / ".my_package"
    user_dir.mkdir(exist_ok=True)
    user_file = user_dir / "data.txt"

    if not user_file.exists():
        data_path = Path(__file__).parent / "data.txt"
        shutil.copy(data_path, user_file)

    return user_file

def write_to_file():
    file_path = get_user_file()
    print("Writing to:", file_path)
    with open(file_path, "a") as f:
        f.write("asd" + "\n")