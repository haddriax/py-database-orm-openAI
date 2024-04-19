from dotenv import dotenv_values
from sqlalchemy import create_engine

# __CONFIG__ = dotenv_values(".env")
#
# engine = "postgres://{user}{password}@{host}/{db_name}".format(
#     user=__CONFIG__["DATABASE_USER"],
#     password=__CONFIG__["DATABASE_PASSWORD"],
#     host=__CONFIG__["DATABASE_HOST"],
#     db_name=__CONFIG__["DATABASE_NAME"],
# )

# if db_engine is None:
#     db_engine = create_engine(engine)
# else:
#     raise RuntimeError("db_engine has already been created.")

