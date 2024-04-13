from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_py.models.db_model import Base

db_engine = create_engine('postgresql://postgres:password@localhost/database_2')
Base.metadata.create_all(db_engine)

Session = sessionmaker(bind=db_engine)
session = Session()
session.commit()
session.close()
