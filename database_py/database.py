import psycopg2
from psycopg2 import OperationalError


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


def execute_query(connection, query):
    connection.autocommit = True
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Query executed successfully")
    except OperationalError as e:
        print(f"The error '{e}' occurred")


def create_database(db_connection):
    with open('sql_sources/create-database.sql', 'r') as file:
        sql_command = file.read()  # .replace('\n', '')
    execute_query(db_connection, sql_command)


def create_settings_basic(connection, name, description, prompt, length, require_reactions, require_comments, require_identification):
    table_name = "study_basic_settings"
    sql_instruction = ""
    with open('sql_sources/insertion-queries.sql', 'r') as file:
        sql_instruction = file.read().replace('\n', '')
    print(sql_instruction)
    sql_instruction = sql_instruction.format(name=name,
                                             description=description,
                                             prompt=prompt,
                                             length=length,
                                             require_reactions=require_reactions,
                                             require_comments=require_comments,
                                             require_identification=require_identification)
    print(sql_instruction)
    execute_query(connection, sql_instruction)


def create_post(connection, ms_id, fk_linked_study, headline, content, is_true_fact, changes_to_follower_on_like,
                changes_to_follower_on_dislike, changes_to_follower_on_share, changes_to_follower_on_flag,
                changes_to_credibility_on_like, changes_to_credibility_on_dislike, changes_to_credibility_on_share,
                changes_to_credibility_on_flag, number_of_reactions, source_id, created_at):
    table_name = "posts"
    sql_instruction = ""
    with open('sql_sources/insertion-queries.sql', 'r') as file:
        sql_instruction = file.read().replace('\n', '')

    sql_instruction = sql_instruction.format(ms_id=ms_id,
                                             fk_linked_study=fk_linked_study,
                                             headline=headline,
                                             content=content,
                                             is_true_fact=is_true_fact,
                                             changes_to_follower_on_like=changes_to_follower_on_like,
                                             changes_to_follower_on_dislike=changes_to_follower_on_dislike,
                                             changes_to_follower_on_share=changes_to_follower_on_share,
                                             changes_to_follower_on_flag=changes_to_follower_on_flag,
                                             changes_to_credibility_on_like=changes_to_credibility_on_like,
                                             changes_to_credibility_on_dislike=changes_to_credibility_on_dislike,
                                             changes_to_credibility_on_share=changes_to_credibility_on_share,
                                             changes_to_credibility_on_flag=changes_to_credibility_on_flag,
                                             number_of_reactions=number_of_reactions,
                                             source_id=source_id,
                                             created_at=created_at)

    execute_query(connection, sql_instruction)


db_connection = create_connection(
    "database_01", "postgres", "password", "127.0.0.1", "5432"
)

# create_settings_basic(connection=db_connection,
#                       name="one",
#                       description="description",
#                       prompt="prompt",
#                       length="10",
#                       require_reactions="0",
#                       require_comments="0",
#                       require_identification="0")

create_post(db_connection, 'ms123', 'null', 'Headline', 'Content', True,
            5, 3, 2, 1,
            10, 5, 3,
            2, 15, 'null', '2024-04-11 12:00:00')
