import os
from pathlib import Path

os.chdir(str(Path(__file__).resolve().parents[1]))

MAPPING = {
    "PySide2": "PyQt5",
    "Signal": "pyqtSignal",
    "Slot": "pyqtSlot",
    "pyside2client": "pyqt5client"
}


def main():
    src = "./clients/pyside2client"
    dst = "./clients/pyqt5client"
    for dirpath, dirnames, filenames in os.walk(src):
        for filename in filenames:
            src_file_path = Path(dirpath, filename)
            dst_file_path = Path(dirpath.replace(src, dst), filename)
            if src_file_path.suffix == ".py":
                with open(src_file_path, "r") as f:
                    content = f.read()
                    for key, value in MAPPING.items():
                        content = content.replace(key, value)
                os.makedirs(dst_file_path.parent, exist_ok=True)
                with open(dst_file_path, "w") as f:
                    f.write(content)


if __name__ == "__main__":
    main()
