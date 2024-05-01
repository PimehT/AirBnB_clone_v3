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
import pycodestyle
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
        pep8s = pycodestyle.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/engine/db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_db_storage(self):
        """Test tests/test_models/test_db_storage.py conforms to PEP8."""
        pep8s = pycodestyle.StyleGuide(quiet=True)
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


@unittest.skipIf(models.storage_t != 'db', "not testing db storage")
class TestDBStorage(unittest.TestCase):
    """Test the DBStorage class"""
    def test_all_returns_dict(self):
        """Test that all returns a dictionary"""
        self.assertIs(type(models.storage.all()), dict)

    def test_all_no_class(self):
        """Test that all returns all rows when no class is passed"""
        storage = models.storage
        # Create some objects to test
        state1 = State(name="California")
        state2 = State(name="New York")
        state3 = State(name="Texas")
        # Save the objects
        storage.new(state1)
        storage.new(state2)
        storage.new(state3)
        storage.save()
        # Get all rows without passing a class
        all_rows = storage.all()
        # Check if all rows are returned
        self.assertEqual(len(all_rows), 3)

    def test_new(self):
        """Test that new adds an object to the database"""
        storage = models.storage
        # Create an object to test
        state = State(name="California")
        # Save the object
        storage.new(state)
        storage.save()
        # Get the object from the database
        retrieved_state = storage.get(State, state.id)
        # Check if the retrieved object is the same as the original object
        self.assertEqual(retrieved_state, state)

    def test_save(self):
        """Test that save properly saves objects to file.json"""
        storage = models.storage
        # Create an object to test
        state = State(name="California")
        # Save the object
        storage.new(state)
        storage.save()
        # Reload the database
        models.storage.reload()
        # Get the object from the database
        retrieved_state = storage.get(State, state.id)
        # Check if the retrieved object is the same as the original object
        self.assertEqual(retrieved_state, state)

    def test_get(self):
        """Test the get method of DBStorage"""
        storage = models.storage
        new_state = State(name="California")
        storage.new(new_state)
        storage.save()
        state_id = new_state.id
        retrieved_state = storage.get(State, state_id)
        self.assertEqual(retrieved_state, new_state)

    def test_count(self):
        """Test the count method of DBStorage"""
        storage = models.storage
        initial_count = storage.count()
        new_state = State(name="California")
        storage.new(new_state)
        storage.save()
        updated_count = storage.count()
        self.assertEqual(updated_count, initial_count + 1)
