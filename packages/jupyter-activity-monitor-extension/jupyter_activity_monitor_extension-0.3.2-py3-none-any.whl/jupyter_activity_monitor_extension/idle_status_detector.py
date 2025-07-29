from datetime import datetime
import os


class LocalFileActiveTimestampChecker:
    def read_last_active_timestamp(self, path="/tmp/.sagemaker-last-active-timestamp"):
        """
        Reads and parses the last active timestamp from a file.

        Parameters:
            path (str): The file path to read the timestamp from.

        Returns:
            datetime: Parsed datetime object if the file exists and content is valid.
            None: If the file does not exist, is not accessible, or has invalid content.
        """
        try:
            # Check if file exists
            if not os.path.isfile(path):
                return None

            # Read timestamp string from the file
            with open(path, "r") as f:
                timestamp_str = f.read().strip()

            # Parse timestamp using ISO 8601 format with Zulu time
            return datetime.strptime(timestamp_str, "%Y-%m-%dT%H:%M:%S.%fZ")
        except (OSError, ValueError):
            # Return None for file access errors or invalid format
            return None
