from dotenv import load_dotenv, dotenv_values
import psycopg2
from psycopg2 import OperationalError
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ai.post_generator import Posts, generate_post


def create_connection(db_name, db_user, db_password, db_host, db_port):
    connection = None
    try:
        connection = psycopg2.connect(
            database=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
        )
        print("Connection to PostgreSQL DB successful")
    except OperationalError as e:
        print(f"The error '{e}' occurred")
    return connection


load_dotenv()


def execute_query(connection, query):
    connection.autocommit = True
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Query executed successfully")
    except OperationalError as e:
        print(f"The error '{e}' occurred")


db_engine = create_engine('postgresql://postgres:password@localhost/database_2')
Session = sessionmaker(bind=db_engine)
session = Session()

post_to_upload = generate_post()

session.add(post_to_upload)
session.commit()
session.close()
