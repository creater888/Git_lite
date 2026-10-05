from datetime import datetime
from utils import generate_hash


class Commit:

    def __init__(self, message, parent=None, files=None):

        self.message = message
        self.parent = parent
        self.files = files or {}

        self.timestamp = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        commit_data = {
            "message": self.message,
            "parent": self.parent,
            "files": self.files,
            "timestamp": self.timestamp
        }

        self.commit_id = generate_hash(str(commit_data))

    def to_dict(self):

        return {
            "commit_id": self.commit_id,
            "message": self.message,
            "parent": self.parent,
            "files": self.files,
            "timestamp": self.timestamp
        }