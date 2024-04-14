from dotenv import load_dotenv, dotenv_values
import psycopg2
from psycopg2 import OperationalError
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ai.post_generator import Posts, generate_post


# Load OpenAI API key.
load_dotenv()

# Create database seesion.
db_engine = create_engine('postgresql://postgres:password@localhost/database_2')
Session = sessionmaker(bind=db_engine)
session = Session()

# Generation of content
post_to_upload = generate_post()

# Upload to database
session.add(post_to_upload)
session.commit()
session.close()
