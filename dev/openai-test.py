from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from generators.OpenAI.post_generator import generate_post, PostDetails

# Load OpenAI API key.
load_dotenv()

db_engine = create_engine('postgresql://postgres:password@localhost/database_2')


def build_posts(amount: int, upload: bool):
    session_maker = sessionmaker(bind=db_engine)
    session = session_maker()

    for i in range(amount):
        # Generation of content
        post_to_upload = generate_post(PostDetails(is_true_percentage=50, no_hashtag=False), verbose=False)
        post_to_upload.fk_linked_study = 1  # Manually setting is study here, because it cannot be null.
        session.add(post_to_upload)  # Add to the entries that will be sent o the dev.
    session.commit()  # Upload to dev
    session.close()


number_of_post_to_create = 6
build_posts(number_of_post_to_create, True)
