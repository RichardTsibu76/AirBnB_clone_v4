#!/usr/bin/python3
"""
initialize the models package
"""

import sys
from os import getenv

# set the default name for the file storage, the name changes with the
# environment.
if any('unittest' in arg for arg in sys.argv) or getenv('HBNB_ENV'):
    FILE_PATH = 'dummy_test_file.json'
else:
    FILE_PATH = "file.json"

storage_t = getenv("HBNB_TYPE_STORAGE")

if storage_t == "db":
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()
storage.reload()
