#!/usr/bin/python3
"""
Contains the TestDBStorageDocs and TestDBStorage classes
"""

from datetime import datetime
import inspect
import models
from models.engine import db_storage
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
DBStorage = db_storage.DBStorage
classes = {"Amenity": Amenity, "City": City, "Place": Place,
           "Review": Review, "State": State, "User": User}


class TestDBStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of DBStorage class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.dbs_f = inspect.getmembers(DBStorage, inspect.isfunction)

    def test_pep8_conformance_db_storage(self):
        """Test that models/engine/db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/engine/db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_db_storage(self):
        """Test tests/test_models/test_db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_engine/\
test_db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_db_storage_module_docstring(self):
        """Test for the db_storage.py module docstring"""
        self.assertIsNot(db_storage.__doc__, None,
                         "db_storage.py needs a docstring")
        self.assertTrue(len(db_storage.__doc__) >= 1,
                        "db_storage.py needs a docstring")

    def test_db_storage_class_docstring(self):
        """Test for the DBStorage class docstring"""
        self.assertIsNot(DBStorage.__doc__, None,
                         "DBStorage class needs a docstring")
        self.assertTrue(len(DBStorage.__doc__) >= 1,
                        "DBStorage class needs a docstring")

    def test_dbs_func_docstrings(self):
        """Test for the presence of docstrings in DBStorage methods"""
        for func in self.dbs_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestFileStorage(unittest.TestCase):
    """Test the FileStorage class"""
    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_returns_dict(self):
        """Test that all returns a dictionary"""
        self.assertIs(type(models.storage.all()), dict)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_no_class(self):
        """Test that all returns all rows when no class is passed"""

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_new(self):
        """test that new adds an object to the database"""

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_save(self):
        """Test that save properly saves objects to file.json"""

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_get(self):
        """Test save method returns a single object"""

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_count(self):
        """Test count method returns count of all objects"""

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_get(self):
        """Tests that obtaining an object from file storage"""
        db_storage = DBStorage()
        my_obj = {"name": "AmuElla"}
        instance = State(**my_obj)
        db_storage.new(instance)
        db_storage.save()
        self.assertEqual(db_storage.get(State, instance.id), instance)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_count(self):
        """Tests that return number of objects in file storage"""
        db_storage = DBStorage()
        my_obj = {"name": "AmuElla"}
        state = State(**my_obj)
        db_storage.new(state)
        my_obj = {"name": "Canada"}
        city = City(**my_obj)
        db_storage.new(city)
        db_storage.save()
        self.assertEqual(len(db_storage.all()), db_storage.count())


class TestDBStorage(unittest.TestCase):
    """Test the DBStorage class"""

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db',
                     "not testing db storage")
    def test_get(self):
        """Tests that retrieve an object"""
        storage = models.storage
        my_obj = State(name='California')
        my_obj.save()
        self.assertEqual(my_obj.id, storage.get(State, my_obj.id).id)
        self.assertEqual(my_obj.name, storage.get(State, my_obj.id).name)
        self.assertIsNot(my_obj, storage.get(State, my_obj.id + 'op'))
        self.assertIsNone(storage.get(State, my_obj.id + 'op'))
        self.assertIsNone(storage.get(State, 45))
        self.assertIsNone(storage.get(None, my_obj.id))
        self.assertIsNone(storage.get(int, my_obj.id))
        with self.assertRaises(TypeError):
            storage.get(State, my_obj.id, 'op')
        with self.assertRaises(TypeError):
            storage.get(State)
        with self.assertRaises(TypeError):
            storage.get()

    def test_count(self):
        """Tests that return number of objects"""
        storage = models.storage
        self.assertIs(type(storage.count()), int)
        self.assertIs(type(storage.count(None)), int)
        self.assertIs(type(storage.count(int)), int)
        self.assertIs(type(storage.count(State)), int)
        self.assertEqual(storage.count(), storage.count(None))
        State(name='Ohio').save()
        self.assertGreater(storage.count(State), 0)
        self.assertEqual(storage.count(), storage.count(None))
        ct = storage.count(State)
        State(name='Florida').save()
        self.assertGreater(storage.count(State), ct)
