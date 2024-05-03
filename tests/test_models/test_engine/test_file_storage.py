#!/usr/bin/python3
"""
Contains the TestFileStorageDocs classes
"""

import inspect
import json
import unittest
from random import choice
import pep8
import models
from models import FILE_PATH
from models.engine import file_storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import lazy_methods


FileStorage = file_storage.FileStorage
classes = {
    "Amenity": Amenity,
    "BaseModel": BaseModel,
    "City": City,
    "Place": Place,
    "Review": Review,
    "State": State,
    "User": User,
}


class TestFileStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of FileStorage class"""

    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.fs_f = inspect.getmembers(FileStorage, inspect.isfunction)

    def test_pep8_conformance_file_storage(self):
        """Test that models/engine/file_storage.py conforms to pep8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(["models/engine/file_storage.py"])
        self.assertEqual(
            result.total_errors, 0, "Found code style errors (and warnings)."
        )

    def test_pep8_conformance_test_file_storage(self):
        """
        Test tests/test_models/test_file_storage.py conforms to pep8.
        """
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(
            ["tests/test_models/test_engine/test_file_storage.py"]
        )
        self.assertEqual(
            result.total_errors, 0, "Found code style errors (and warnings)."
        )

    def test_file_storage_module_docstring(self):
        """Test for the file_storage.py module docstring"""
        self.assertIsNot(
            file_storage.__doc__, None, "file_storage.py needs a docstring"
        )
        self.assertTrue(
            len(file_storage.__doc__) >= 1, "file_storage.py needs a docstring"
        )

    def test_file_storage_class_docstring(self):
        """Test for the FileStorage class docstring"""
        self.assertIsNot(
            FileStorage.__doc__, None, "FileStorage class needs a docstring"
        )
        self.assertTrue(
            len(FileStorage.__doc__) >= 1,
            "FileStorage class needs a docstring"
        )

    def test_fs_func_docstrings(self):
        """Test for the presence of docstrings in FileStorage methods"""
        for func in self.fs_f:
            self.assertIsNot(
                func[1].__doc__, None,
                "{} method needs a docstring".format(func[0])
            )
            self.assertTrue(
                len(func[1].__doc__) >= 1,
                "{} method needs a docstring".format(func[0]),
            )


@unittest.skipIf(models.storage_t == "db", "file storage")
class TestFileStorage(unittest.TestCase):
    """Test the FileStorage class"""

    def setUp(self) -> None:
        lazy_methods.empty_object_dictionary(models.storage.all())

    def test_all_returns_dict(self):
        """Test that all returns the FileStorage.__objects attr"""
        storage = FileStorage()
        new_dict = storage.all()
        self.assertEqual(type(new_dict), dict)
        self.assertIs(new_dict, storage.all())

    def test_new(self):
        """test that new adds an object to the FileStorage.__objects attr"""
        test_dict = {}

        for key, value in classes.items():
            with self.subTest(key=key, value=value):
                instance = value()
                instance_key = instance.__class__.__name__ + "." + instance.id
                models.storage.new(instance)
                test_dict[instance_key] = instance
                self.assertEqual(test_dict, models.storage.all())

    def test_save(self):
        """Test that save properly saves objects to file.json"""
        new_dict = {}

        for key, value in classes.items():
            instance = value()
            instance_key = instance.__class__.__name__ + "." + instance.id
            new_dict[instance_key] = instance
            models.storage.new(instance)

        models.storage.save()
        for key, value in new_dict.items():
            new_dict[key] = value.to_dict()
        string = json.dumps(new_dict)
        with open(FILE_PATH, "r", encoding="utf-8") as f:
            js = f.read()
        self.assertEqual(json.loads(string), json.loads(js))

    def test_count_when_empty(self):
        """Test that the `count` method returns zero when nothing exist."""
        self.assertTrue(models.storage.count() == 0)

    def test_count_all_objects(self):
        """Test that the `count` method returns the right number of objects."""
        for model in classes.values():
            models.storage.new(model())

        self.assertEqual(models.storage.count(), len(classes))

    def test_count_with_model_name(self):
        """Test that the `count` method returns the right number of objects for
        a particular class."""
        for key, instance in classes.items():
            with self.subTest(key=key, model=instance):
                num_of_instances = choice(range(1, 20))
                for _ in range(num_of_instances):
                    instance_obj = instance()
                    models.storage.new(instance_obj)

                self.assertEqual(models.storage.count(
                    instance_obj.__class__.__name__), num_of_instances)

    def test_get_with_non_existent(self):
        """Test that `get` method returns None for non-existent objects."""
        self.assertIsNone(models.storage.get(User, 'abcd-1234-test-5678'))

    def test_get_with_class_only(self):
        """Test that the `get` method operates correctly when only the class
        argument is passed."""
        self.assertIsNone(models.storage.get(User))

    def test_get_with_valid_class(self):
        """Test that `get` method returns the right object."""
        for key, instance in classes.items():
            with self.subTest(key=key, model=instance):
                instance_obj = instance()
                models.storage.new(instance_obj)

                self.assertEqual(models.storage.get(
                    instance, instance_obj.id), instance_obj)
