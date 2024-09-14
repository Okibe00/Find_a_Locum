from models.base_model import BaseModel
import mysql.connector
from mysql.connector import errorcode
from mysql.connector import Error
from utils.create_tables import TABLES
from models.profession import Profession
from models.state import State
from models.city import City
from models.user import User
from models.job import Job
from mysql.connector import pooling
from os import getenv

'''A database engine
Name:
   db_storage.py

Description:
    The module provides a database engine that interacts with
    mysql database,its core functions is the conversion
    of objects into dictionary for storage
    this dictionary values into the database.
    it also handles fetching and
    converting database records back into python objects.

Attributes:

Usage:
    To use this module import it and call the available functions and classes.

Example:
    To get a list of states objects in the database.

    import db_storage

    state_list = db.storage.all(states)

Author:
    Okibe Ogomola Onmeje

Date:
2024-06-23
'''

"""
TODO:
    01: Merge the new and save functions (done)
    02: 
"""


classes = {
    'State': State,
    'Profession': Profession,
    'City': City,
    'Job': Job,
    'User': User
}

DB_TABLES = {
    'State': 'states',
    'Profession': 'profession',
    'User': 'users',
    'City': 'cities',
    'Job': 'jobs'
}

class DB_storage(BaseModel):
    '''creates a database engine

    Establish connection to a database and perform,
    operations(CRUD)

    Attributes:
        __cnx (obj): connection object
        __session (dict): current session objects

    '''
    __cnx = None

    def __init__(self, host=None, user=None,
                 password=None, db=None, port=None):
        '''creates a connection to  a database.

        Args:
            host (str): database host.
            user (str): databasse user (optional).
            password (str): database password (optional)
            port (str): database host port (optional)

        Return:
            None
        '''
        config = {
            'password': getenv("PASSWORD"),
            'host': getenv("HOST"),
            'user': getenv("USER"),
            'db': getenv("DB"),
            'port': getenv("PORT"),
        }
        try:
            if None in config.values():
                config = {k: v for k, v in config.items() if v is not None}
            self.__cnx = pooling.MySQLConnectionPool(
                pool_name="pool01",
                pool_size=32,
                **config
            )
            if self.is_connected():
                print('connection successful')
        except Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Bad username or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)

    def delete(self, cls,  o_id):
        '''Delete a record
        Argument:
            o_id: record id
            cls: table
        Return: 1(succes) or 0(error)
        
        '''
        table = DB_TABLES[cls]
        query = f'DELETE FROM {cls} WHERE id = %s'
        conn = self.__cnx.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(query, (o_id,))
        except Error as err:
            print(err)
        finally:
            cursor.close()
            conn.close()
        return 1

    def all(self, cls):
        '''get all record of a class
        Attribute:
            cls(str): class to fetch
        Return:
            list of dictionary or None
        '''
        if classes.get(cls) is None:
            print("** class does not exist **")
            return
        try:
            conn = self.__cnx.get_connection()
            cursor = conn.cursor(dictionary=True)
            table = DB_TABLES[cls]
            query = f"SELECT * FROM {table};"
            cursor.execute(query)
            return cursor.fetchall()
        except Error as err:
            print('Failed to get connection')
            print(err)

    def get(self, cls, name=None, o_id=None):
        '''
        fetch records from the database and convert them
        back into Python objects or dictionaries
        A single record, multiple records, or all records from a table

        Arguments:
            cls (str): class name to fetch
            id(str): class id

        Return: list of dictionaries or []
        '''
        result = []
        conn = self.__cnx.get_connection()
        if conn.is_connected():
            pass
        else:
            conn.ping(reconnect=True, attempts=3, delay=2)
            if conn.is_connected() is False:
                print("Unable to connect to database")
                return

        cursor = conn.cursor(dictionary=True)
        table = DB_TABLES[cls]
        if cls in classes:
            try:
                if name:
                    query = f"SELECT * FROM {table} WHERE name=%s;"
                    cursor.execute(query, (name,))
                    data = cursor.fetchall()
                    if len(data):
                        #data[0]['__class__'] = cls
                        #result = result + data
                        pass
                    else:
                        print("** name does not exist **")
                elif o_id:
                    query = f"SELECT * FROM {table} WHERE id=%s;"
                    cursor.execute(query, (o_id,))
                    data = cursor.fetchall()
                    if len(data) == 0:
                        print("** Invalid ID **")
                    #for obj in data:
                    #    obj['___class__'] = cls
                    #result = result + data
            except Error as err:
                print(err)
                cursor.close()
                conn.close()
            finally:
                cursor.close()
                conn.close()
        else:
            print("** class does not exist **")

        for obj in data:
            obj['___class__'] = cls
        #result = result + data
        return data

    def reload(self):
        '''creates database tables'''
        KEYS = ['profession', 'state', 'city', 'user', 'jobs']
        print("Creating tables..")
        for key in KEYS:
            self.create_table(key, TABLES[key])
        print("Tables created")

    def save(self, obj):
        '''saves session objs to the database'''
        data = obj.to_dict()
        table_name = DB_TABLES[f"{data['__class__']}"]
        del data['__class__']
        columns = ', '.join(data.keys())
        values = tuple(data.values())
        plholder = ', '.join(['%s'] * len(values))
        query = f'INSERT INTO {table_name} ({columns}) VALUES({plholder});'
        print(query)
        self.execute(query, values)

    def create_table(self, table_name=None, query=None):
        '''
        creates database tables
        '''
        '''this is just to guarantee the order of table creation'''
        conn = self.__cnx.get_connection()
        cursor = conn.cursor()
        try:
            '''check if database exist if it doesnt create it and use it'''
            print(f'Creating: {table_name}')
            cursor.execute(query)
            print(f'{table_name} created')
            conn.commit()
        except Exception as e:
            '''cursor.execute("SHOW ENGINE INNODB STATUS;")'''
            """ raise reasonable exception """
            raise Exception("Failed to create database table") from e
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    def create_database(self, name):
        '''creates the databases'''
        conn = self.__cnx.get_connection()
        query = """ CREATE DATABASE %s;"""
        cursor = conn.cursor()
        try:
            cursor.execute(query, (name,))
        except Error as err:
            print(err)
            cursor.close()
            conn.close()

    def execute(self, query=None, param=None):
        '''Execute a database query

        Arguments(str):
            query: prepared statement
            param: tuple of argument to subst into query
        '''
        conn = self.__cnx.get_connection()
        try:
            conn.ping(reconnect=True, attempts=3, delay=2)
        except Error as err:
            print("Error: ", err)
        cursor = conn.cursor()
        try:
            if param:
                cursor.execute(query, param)
            else:
                cursor.execute(query)
        except Error as err:
            print(err)
            return None
        result = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        return result

    def begin_transaction(self, queries):
        """
        Executes a series of SQL queries.
        Handles both parameterized and non-parameterized queries.

        :param queries: A list of tuples, where each tuple contains:
            - SQL query string
            - Optional tuple of parameters
            (or None for non-parameterized queries)
            -  Example: [("SELECT * FROM table_name", None), ...]
        Return:
            list of query result
        """
        if type(queries) is not list:
            print(
                "Usage: Example: [(SELECT * FROM table_name, None),\
                (SELECT * FROM table_name WHERE id=%s, (id,)),...]"
            )
        conn = self.__cnx.get_connection()
        result = list()
        try:
            conn.ping(reconnect=True, attempts=3, delay=2)
            print('connection active')
        except Error as err:
            print("Error: ", err)
        conn.autocommit = False
        cursor = conn.cursor(dictionary=True)

        try:
            for query, param in queries:
                if param:
                    cursor.execute(query, param)
                else:
                    cursor.execute(query)
                if cursor.with_rows:
                    result = result + cursor.fetchall()

            conn.commit()
        except Error as err:
            print("Error: ", err)
            if conn.is_connected():
                conn.rollback()
                cursor.close()
                conn.close()
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()
                print("connection to MySQL closed")
        return result

    def is_connected(self):
        '''check is a connection is active'''
        conn = self.__cnx.get_connection()
        return (conn is not None and conn.is_connected())
