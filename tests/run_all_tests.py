if __name__ == "__main__":
    import os
    from pathlib import Path
    import sys

    project_root = str(Path(__file__).resolve().parents[1])
    sys.path.append(project_root)
    os.chdir(project_root)

import unittest
from tests.tservices.tdocuments.all import *
from tests.tservices.tstorage.all import *
from tests.tservices.test_service_provider import *
unittest.main()
