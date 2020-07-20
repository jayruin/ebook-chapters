if __name__ == "__main__":
    import os
    from pathlib import Path
    import sys

    project_root = str(Path(__file__).resolve().parents[2])
    sys.path.append(project_root)
    os.chdir(project_root)

from clients.pyside2client.MainApplication import MainApplication
import sys
sys.exit(MainApplication(sys.argv).exec_())
