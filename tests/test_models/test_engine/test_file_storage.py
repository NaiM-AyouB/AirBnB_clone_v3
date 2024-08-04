#!/usr/bin/python3
"""
Contains the TestFileStorageDocs classes
"""

from datetime import datetime
import inspect
import models
from models.engine import file_storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import json
import os
import pep8
import unittest
FileStorage = file_storage.FileStorage
classes = {"Amenity": Amenity, "BaseModel": BaseModel, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


class TestFileStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of FileStorage class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.fs_f = inspect.getmembers(FileStorage, inspect.isfunction)

    def test_pep8_conformance_file_storage(self):
        """Test that models/engine/file_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/engine/file_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_file_storage(self):
        """Test tests/test_models/test_file_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_engine/\
test_file_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_file_storage_module_docstring(self):
        """Test for the file_storage.py module docstring"""
        self.assertIsNot(file_storage.__doc__, None,
                         "file_storage.py needs a docstring")
        self.assertTrue(len(file_storage.__doc__) >= 1,
                        "file_storage.py needs a docstring")

    def test_file_storage_class_docstring(self):
        """Test for the FileStorage class docstring"""
        self.assertIsNot(FileStorage.__doc__, None,
                         "FileStorage class needs a docstring")
        self.assertTrue(len(FileStorage.__doc__) >= 1,
                        "FileStorage class needs a docstring")

    def test_fs_func_docstrings(self):
        """Test for the presence of docstrings in FileStorage methods"""
        for func in self.fs_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestFileStorage(unittest.TestCase):
    """Test the FileStorage class"""

    def setUp(cls):
        """reset file storage"""
        storage = FileStorage()
        storage.reset()

    def tearDown(cls):
        """reset file storage"""
        storage = FileStorage()
        storage.reset()

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_reload_with_no_existing_file_storage(self):
        """test reload with no file storage"""
        storage = FileStorage()
        storage.reload()
        self.assertEqual(storage.all(), {})

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_reload_with_file_storage(self):
        """test reload with file storage"""
        storage = FileStorage()
        storage._FileStorage__file_path = 'tests/test_file.json'
        NUMBER_OF_OBJECTS = 8   # in test_file.json
        storage.reload()
        self.assertIs(len(storage.all()), NUMBER_OF_OBJECTS)

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_all_returns_dict(self):
        """Test that all returns the FileStorage.__objects attr"""
        storage = FileStorage()
        storage.reload()
        new_dict = storage.all()
        self.assertIs(new_dict, storage._FileStorage__objects)

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_new(self):
        """test that new adds an object to the FileStorage.__objects attr"""
        storage = FileStorage()
        storage.reload()
        test_dict = {}
        for value in classes.values():
            instance = value()
            instance_key = instance.__class__.__name__ + "." + instance.id
            storage.new(instance)
            test_dict[instance_key] = instance
            self.assertEqual(test_dict, storage._FileStorage__objects)

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_delete(self):
        """test that delete remove an object
        from the FileStorage.__objects attr"""
        storage = FileStorage()
        storage.reload()
        for value in classes.values():
            instance = value()
            storage.new(instance)
            storage.delete(instance)
            self.assertEqual({}, storage._FileStorage__objects)

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_get(self):
        """test that get return an object from the file storage"""
        storage = FileStorage()
        storage.reload()
        for value in classes.values():
            instance = value()
            storage.new(instance)
            self.assertIsNotNone(
                storage.get(instance.__class__.__name__, instance.id)
                )

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_count(self):
        """test that count return the number of objects"""
        storage = FileStorage()
        storage.reload()
        for value in classes.values():
            instance = value()
            storage.new(instance)
        self.assertEqual(storage.count(), len(storage.all()))

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_save(self):
        """Test that save properly saves objects to file.json"""
        storage = FileStorage()
        new_dict = {}
        for value in classes.values():
            instance = value()
            storage.new(instance)
            instance_key = instance.__class__.__name__ + "." + instance.id
            new_dict[instance_key] = instance.to_dict()
        storage.save()
        string = json.dumps(new_dict)
        with open("file.json", "r") as f:
            js = f.read()
        self.assertEqual(json.loads(string), json.loads(js))
