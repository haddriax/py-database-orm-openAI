from openai import OpenAI
from dotenv import load_dotenv, dotenv_values
from database_py.models.db_model import Posts

load_dotenv()


class PostDetails:
    """
    Data class that holds information about the creation process for a post.
    """
    no_hashtag: bool
    """ Ensure the generation does not include hashtag at the end of the post."""
    is_info_true: bool
    """ Hint for generated information to be either true or false."""
    force_title: str
    """ Pass a value that will be used as title. If none, a random one will be generated. """

    def __init__(self, is_info_true, no_hashtag, force_title=None, min_char=200, max_char=400):
        self.is_info_true = is_info_true
        self.no_hashtag = no_hashtag
        self.force_title = force_title
        self.min_char = min_char
        self.max_char = max_char
        pass


def generate_post(post_details: PostDetails) -> Posts:
    """
    Uses OpenAI API to generate a post with random content and matching title.
    :param post_details: PostDetails that holds information about the post creation.
   :return: A newly created and filled Post
   """
    ai_instruction_title = (
        (post_details.force_title if (post_details.force_title is not None)
         else
         "Generate the title, and only the title, of a social media post. The content must be {is_true}. The post "
         "must be informative.".format(is_true=post_details.is_info_true)))

    role = ""
    print("Title prompt: {}".format(ai_instruction_title))
    client = OpenAI()

    completion_headline = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": role},
            {"role": "user", "content": ai_instruction_title},
        ]
    )
    print(completion_headline.choices[0].message.content)

    ai_instruction_content = ((
        "Generate the content of a social media post based on this title: {title}. The "
        "content must be {is_true}. The post"
        "must be informative. Limit the size from {min_char} to {max_char} characters. Do not add any "
        "hashtag '#' at the end. Avoid repeating the title in the content.").format(
        title=completion_headline.choices[0].message.content,
        is_true=post_details.is_info_true,
        min_char=post_details.min_char,
        max_char=post_details.max_char)
    )

    completion_content = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": role},
            {"role": "user", "content": ai_instruction_content},
        ]
    )
    print("\n")
    print("Content prompt: {}".format(ai_instruction_content))
    print(completion_content.choices[0].message.content)

    post_model = Posts(
        ms_id='0',
        fk_linked_study=1,
        headline=completion_headline.choices[0].message.content,
        content=completion_content.choices[0].message.content,
        is_true_fact=post_details.is_info_true,
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


post = generate_post(PostDetails(is_info_true=False, no_hashtag=False))
print("\nPost headline:  "+post.headline)
print("Post content: "+post.content)
