from random import randrange

from openai import OpenAI
from dotenv import load_dotenv
from models.db_model import Posts

# Load API-KEY from a .env file.
load_dotenv()


# @todo add a percentage a posts that can be 'list' or 'top 10' style.
class PostDetails:
    """
    Data class that holds information about the creation process for a post.
    """
    ai_model: str
    """ AI Model version."""
    no_hashtag: bool
    """ Ensure the generation does not include hashtag at the end of the post."""
    is_info_true: bool
    """ Hint for generated information to be either true or false."""
    force_title: str
    """ Pass a value that will be used as title. If none, a random one will be generated. """
    is_info_true: bool
    """ Filled at object creation, define if the generated post will be true or fake. """
    available_themes = [
        "Health and Wellness",
        "Environmental Awareness",
        "Technology Trends",
        "Historical Facts",
        "Financial Literacy",
        "Science Education",
        "Cultural Diversity",
        "Global Issues",
        "Travel Tips and Destinations",
        "Education Insights",
        "Self-Improvement",
        "Food and Nutrition",
        "Entrepreneurship",
        "Parenting Tips",
        "Art and Creativity",
        "Work-Life Balance",
        "Human Rights Advocacy",
        "Sports and Fitness",
        "Mental Health Awareness",
        "Automotive Enthusiasm"
    ]
    """ List of themes that are used when no theme is specifically precised."""

    def __init__(self, is_true_percentage, no_hashtag, forced_title=None, specific_theme=None, min_char=300,
                 max_char=600):
        self.is_true_percentage = is_true_percentage
        self.no_hashtag = no_hashtag
        self.force_title = forced_title
        self.min_char = min_char
        self.max_char = max_char
        self.ai_model = "gpt-3.5-turbo"
        self.is_info_true = True if randrange(100) <= is_true_percentage else False
        self.theme = (specific_theme if specific_theme is not None
                      else PostDetails.available_themes[randrange(len(PostDetails.available_themes)-1)]) # @todo check -1
        pass


def generate_post(post_details: PostDetails, verbose=False) -> Posts:
    """
    Uses OpenAI API to generate a post with random content and matching title. This only fill content and headline!
    :param verbose: Print debugging information about the prompts and results.
    :param post_details: PostDetails that holds information about the post creation.
   :return: A newly created and filled Post
   """
    # Preparing the title prompt based on our parameters.
    ai_instruction_title = (
        (post_details.force_title if (post_details.force_title is not None)
         else
         "Generate the title, and only the title, of a social media post. The content must be \033[1m{is_true}\033[0m "
         "and be about\033[1m{theme}\033[0m. The post must be informative. Do not generate title like '10 proven "
         "facts' or '10 proven benefits'"
         "or '10 proven reasons'.".format(
             is_true="true" if post_details.is_info_true else "fake",
             theme=post_details.theme)))

    client = OpenAI()

    # Request for creating the title.
    completion_headline = client.chat.completions.create(
        model=post_details.ai_model,
        messages=[
            {"role": "user", "content": ai_instruction_title},
        ]
    )
    if verbose:
        print("\033[92mTitle prompt:\033[0m\n{}".format(ai_instruction_title))
        print("\033[92mHeadline:\n\033[0m\033[1m{}\033[0m".format(completion_headline.choices[0].message.content))

    # Preparing the content prompt based on our parameters and the result of the title prompt.
    ai_instruction_content = ((
        "Generate the content of a social media post based on this title: \033[1m{title}\033[0m. The "
        "content must be \033[1m{is_true}\033[0m. The post"
        "must be informative. Limit the size from \033[1m{min_char}\033[0m to \033[1m{max_char}\033[0m characters. Do "
        "not add any"
        "hashtag '#' at the end. Avoid repeating the title in the content.").format(
        title=completion_headline.choices[0].message.content,
        is_true=post_details.is_info_true,
        min_char=post_details.min_char,
        max_char=post_details.max_char)
    )

    # Request for creating the content, based on given title.
    completion_content = client.chat.completions.create(
        model=post_details.ai_model,
        messages=[
            {"role": "user", "content": ai_instruction_content},
        ]
    )
    if verbose:
        print("\033[96mContent prompt:\033[0m\n{}".format(ai_instruction_content))
        print("\033[96mContent:\n\033[0m{}".format(completion_content.choices[0].message.content))

    # Create the post with the generated contents. Other values does not matter here.
    post_model = Posts(
        ms_id='0',
        headline=completion_headline.choices[0].message.content,
        content=completion_content.choices[0].message.content,
        is_true_fact=post_details.is_info_true,
        number_of_likes=10,
        number_of_dislike=12,
        number_of_shared=0,
        number_of_flagged=0,
        changes_to_follower_on_like=10,
        changes_to_follower_on_dislike=10,
        changes_to_follower_on_share=5,
        changes_to_follower_on_flag=15,
        changes_to_credibility_on_like=11,
        changes_to_credibility_on_dislike=12,
        changes_to_credibility_on_share=25,
        changes_to_credibility_on_flag=18,
        fk_source_id=1
    )
    return post_model


# Test call of our generation function.
post = generate_post(
    PostDetails(
        is_true_percentage=0,
        no_hashtag=False,
        min_char=600,
        max_char=800,
        specific_theme=None),
    verbose=True)
