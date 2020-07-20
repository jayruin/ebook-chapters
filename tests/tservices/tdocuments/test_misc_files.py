import unittest

from services.documents.all import MiscFile


class TestMiscFiles(unittest.TestCase):

    def test_json(self):
        f1 = MiscFile("file", bytes("abc", "utf-8"))
        fj = f1.to_json()
        f2 = MiscFile.from_json(fj)

        self.assertEqual(f2.to_json(), fj)
        self.assertIsInstance(f2.raw_data, bytes)
        self.assertEqual(f1, f2)
