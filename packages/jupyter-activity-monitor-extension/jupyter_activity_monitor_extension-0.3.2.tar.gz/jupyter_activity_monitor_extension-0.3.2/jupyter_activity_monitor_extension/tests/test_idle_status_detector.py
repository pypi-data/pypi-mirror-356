import unittest
import os
from datetime import datetime
from tempfile import NamedTemporaryFile
from jupyter_activity_monitor_extension.idle_status_detector import (
    LocalFileActiveTimestampChecker,
)


class TestLocalFileActiveTimestampChecker(unittest.TestCase):

    def setUp(self):
        self.local_file_checker = LocalFileActiveTimestampChecker()

    def test_valid_timestamp(self):
        with NamedTemporaryFile(mode="w+", delete=False) as tmp:
            tmp.write("2025-06-12T18:35:59.751000Z")
            tmp_path = tmp.name

        result = self.local_file_checker.read_last_active_timestamp(tmp_path)
        expected = datetime(2025, 6, 12, 18, 35, 59, 751000)
        self.assertEqual(result, expected)

        os.remove(tmp_path)

    def test_file_not_exists(self):
        result = self.local_file_checker.read_last_active_timestamp(
            "/tmp/nonexistent_file"
        )
        self.assertIsNone(result)

    def test_invalid_content(self):
        with NamedTemporaryFile(mode="w+", delete=False) as tmp:
            tmp.write("not-a-timestamp")
            tmp_path = tmp.name

        result = self.local_file_checker.read_last_active_timestamp(tmp_path)
        self.assertIsNone(result)

        os.remove(tmp_path)


if __name__ == "__main__":
    unittest.main()
