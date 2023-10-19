import os
import logging
import threading
import configparser
from flask_restful import Resource, reqparse
from productcatagory.configuration.resource_encryption import FileDecrpytor
from productcatagory.configuration import log_config
from productcatagory.datamodel.db_connector import database_access

# Create a ConfigParser instance and read the config.ini file
config = configparser.ConfigParser()

#config.read(config_file_path)
decrypt_instance = FileDecrpytor()
conn = decrypt_instance.filedecrypt().decode('utf-8')
config.read_string(conn)
db_table_name = config.get('database', 'db_table_name')

# Logging initialization
logger = log_config.configure_logging()

# Create a custom filter to add the class name to the log record
class ClassNameFilter(logging.Filter):
    def __init__(self, name=""):
        super().__init__()
        self.class_name = name
    def filter(self, record):
        record.classname = self.class_name
        return True

class CatagoryValidation():
    current_directory = os.path.abspath(os.path.dirname(__file__))
    category_directory = os.path.join(current_directory, '..', '..', 'productcatagory')
    categoryValidation = os.path.join(category_directory, "scripts/catagoryValidation.sql")
    categoryCreation = os.path.join(category_directory, "scripts/catagoryCreation.sql")
    TABLE_NAME = db_table_name
    def __init__(self, username):
        self.username = username
    @classmethod
    def find_by_catagory(cls, name):
        logger.addFilter(ClassNameFilter(__class__.__name__))
        logger.info("Making a connection to the database")
        connection = database_access()
        cursor = connection.cursor()
        with open(CatagoryValidation.categoryValidation, 'r') as sql_file:
            query = sql_file.read()
            logger.info("Checking if a catagory is already exists in our database or not")
            query = query.format(table=cls.TABLE_NAME)
            logger.info("query = {}".format(query))
            cursor.execute(query, (name,))
            row = cursor.fetchone()
            if row:
                logger.info("catagory found, returning info")
                user = row
            else:
                user = None
        connection.close()
        return user


class CatagoryListing(Resource):
    TABLE_NAME = db_table_name
    parser = reqparse.RequestParser()
    parser.add_argument('catagoryId', type=str, required=True, help="This field cannot be left blank!")
    parser.add_argument('name', type=str, required=True, help="This field cannot be left blank!")
    parser.add_argument('description', type=str, required=True, help="This field cannot be left blank!")
    # Create a logger for the thread
    def post(self):
        logger.addFilter(ClassNameFilter(__class__.__name__))
        logger.info(f"Thread {threading.current_thread().name}: Registering seller")
        data = CatagoryListing.parser.parse_args()
        if CatagoryValidation.find_by_catagory(data['name']):
            logger.error("category {} already exists".format(data['name']))
            return {"message": "category {} already exists.".format(data['name'])}, 400
        # Perform seller registration in a separate thread
        registration_thread = threading.Thread(target=self.list_category, args=(data,))
        try:
            registration_thread.start()
            return {"message": "category {} added successfully".format(data['name'])}, 201
        except Exception as e:
            logging.error(e)
            return {"message": "{}".format(e)}, 400

    def list_category(self, data):
        connection = database_access()
        cursor = connection.cursor()
        with open(CatagoryValidation.categoryCreation, 'r') as sql_file:
            logger.info("adding a new category into our database")
            query = sql_file.read()
            query = query.format(table=self.TABLE_NAME)
            cursor.execute(query, (data['catagoryId'], data['name'], data['description']))
            connection.commit()
        connection.close()
        logger.info(f"catagory {data['name']} successfully added.")