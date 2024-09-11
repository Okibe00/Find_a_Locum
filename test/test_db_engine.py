"""
Name:
    test_db_engine.py

Description:
    Test the database engine functionality.

Usage:
    Same directory:
        python -m unittest test_db_engine
    Project root directory:
        python -m unittest discover test_directory

Author:
    Okibe Ogomola Onmeje

Date:
    2024-06-06
"""

import unittest
from models.engine.db_storage import DB_storage
from models import storage
from models.profession import Profession
from models.state import State
from models.job import Job


class TestDBEngine(unittest.TestCase):
    '''
    Test the database engine
    '''

    def test_connection(self):
        '''
        test wether database is connected
        '''
        self.assertTrue(storage)

    def test_create_table(self):
        '''Test the create table'''
        table_name = "my_s"
        query = 'CREATE TABLE IF NOT EXISTS my_s (name varchar(5));'
        storage.create_table(table_name, query)
        t_exist = f"SHOW TABLES LIKE '{table_name}'"
        res = storage.execute(t_exist)
        self.assertTrue(len(res) > 0)

    def test_bad_query(self):
        '''test bad query string to create table'''
        query = "creat TABLE ;"
        storage.create_table(query)

    def test_save(self):
        '''Test the save method'''
        p1 = Profession()
        obj_id = p1.id
        storage.new(p1)
        storage.save()
        query = f"SELECT * from profession where id = %s"
        res = storage.execute(query, (obj_id,))
        self.assertEqual(obj_id, res[0][0])

    def test_get(self):
        '''Fetch records from the database'''
        '''fetch single record'''
        new_obj = Profession(name="Doctor")
        obj_id = new_obj.id
        storage.new(new_obj)
        storage.save()
        res = storage.get("Profession", obj_id)
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]['id'], obj_id)
        self.assertEqual("Doctor", res[0]['name'])
        '''test fetch entire record'''
        new_data = storage.get('Profession')
        self.assertTrue(len(new_data) > 1)
        """test failure behaviour"""

    def test_begin_transaction(self):
        '''test transaction handling'''
        query = [
            ("SELECT * FROM profession LIMIT 5;", None),
            ('SELECT * FROM profession WHERE name="Pharmacist";', None)
        ]
        res = storage.begin_transaction(query)
        self.assertTrue(len(res) > 0)
