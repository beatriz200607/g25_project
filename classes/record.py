import json
import os

class Record:
    FILE_PATH = 'records.json'

    @staticmethod
    def _ensure_file():
        if not os.path.exists(Record.FILE_PATH):
            with open(Record.FILE_PATH, 'w') as f:
                json.dump([], f)

    @staticmethod
    def add(record_type, data):
        Record._ensure_file()

        with open(Record.FILE_PATH, 'r') as f:
            records = json.load(f)

        entry = {'type': record_type, **data}
        records.append(entry)

        with open(Record.FILE_PATH, 'w') as f:
            json.dump(records, f, indent=2)

        return entry
