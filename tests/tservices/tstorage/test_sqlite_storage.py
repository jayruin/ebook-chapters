import os
import unittest

from services.storage.all import SqliteStorage
from tests.tservices.tstorage.test_abstract_storage import TestAbstractStorage


class TestSqliteStorage(TestAbstractStorage, unittest.TestCase):

    def setUp(self):
        with open("./services/storage/sql_init/sqlite.sql", "r") as f:
            init = f.read()
        with open("./services/storage/sql_destroy/sqlite.sql", "r") as f:
            destroy = f.read()
        connection = self.config["Sqlite"]["CONNECTION_STRING"]
        self.storage = SqliteStorage(connection, init, destroy)

    def tearDown(self):
        os.remove(self.config["Sqlite"]["CONNECTION_STRING"])
