import openai
from openai import OpenAI
import os
from dotenv import load_dotenv, dotenv_values
from database_py.models.db_model import Posts

load_dotenv()


class PostDetails:
    def __init__(self, is_info_true):
        self.is_info_true = is_info_true
        pass


def generate_post() -> Posts:
    """
    Uses OpenAI API to generate a post with random content and matching title.
   :return: A newly created and filled Post
   """
    ai_remove_hashtag = "Do not add '#' at the end of the post."
    ai_instruction_title = (
        "Generate the title, and only the title, of a social media post. The content must be true. The "
        "post must be informative.")
    role = ""
    client = OpenAI()

    completion_title = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": role},
            {"role": "user", "content": ai_instruction_title},
        ]
    )

    is_content_true = True
    ai_instruction_content = ((
                                  "Generate the content of a social media post based on this title: {title}. The "
                                  "content must be {is_true}. The post"
                                  "must be informative. Limit the size to 200 to 500 characters. Do not add any "
                                  "hashtag '#' at the end. Avoid repeating the title in the content.")
                              .format(title=completion_title.choices[0].message, is_true=is_content_true))

    completion_content = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": role},
            {"role": "user", "content": ai_instruction_content},
        ]
    )

    post_model = Posts(
        ms_id='0',
        fk_linked_study=1,
        headline=completion_title.choices[0].message.content,
        content=completion_content.choices[0].message.content,
        is_true_fact=is_content_true,
        changes_to_follower_on_like=10,
        changes_to_follower_on_dislike=10,
        changes_to_follower_on_share=5,
        changes_to_follower_on_flag=15,
        changes_to_credibility_on_like=11,
        changes_to_credibility_on_dislike=12,
        changes_to_credibility_on_share=25,
        changes_to_credibility_on_flag=18,
        number_of_reactions=144,
        fk_source_id=1
    )
    return post_model
