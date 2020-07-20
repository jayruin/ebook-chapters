import shutil
import unittest

from services.storage.all import FilesystemStorage
from tests.tservices.tstorage.test_abstract_storage import TestAbstractStorage


class TestFilesystemStorage(TestAbstractStorage, unittest.TestCase):

    def setUp(self):
        root = self.config["Filesystem"]["ROOT_DIRECTORY"]
        misc = self.config["Filesystem"]["MISC_DIRECTORY"]
        self.storage = FilesystemStorage(root, misc)

    def tearDown(self):
        shutil.rmtree(self.config["Filesystem"]["ROOT_DIRECTORY"])
        shutil.rmtree(self.config["Filesystem"]["MISC_DIRECTORY"])
