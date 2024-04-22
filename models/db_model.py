from typing import Type, Optional, TypeVar
from sqlalchemy import Integer, String, Boolean, TIMESTAMP, ForeignKey
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import relationship, mapped_column, Mapped, declarative_base
from datetime import datetime

Base = declarative_base()


class DatabaseBaseClass(Base):
    __abstract__ = True

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    # @TODO add the "created_at" field here. Will allow to track every single entry creation.


# Define a type variable for the model class
ModelType = TypeVar('ModelType', bound=DatabaseBaseClass)


def get_by_id(session, table_class: Type[ModelType], query_id, jointures=None) -> Optional[ModelType]:
    """
    :param session: The active SQLAlchemy session object
    :param table_class: The class representing the database table to query
    :param query_id: The id of the row to be retrieved
    :param jointures: Optional list of tables to join with the main table
    :return: The queried row as an instance of the table_class, or None if an error occurred
    """
    assert query_id > 0, 'id must be greater than 0'
    try:
        query_object = session.query(table_class).filter(table_class.id == query_id)

        if jointures is not None:
            for j in jointures:
                query_object = query_object.join(j)

    except SQLAlchemyError as e:
        error = str(e)
        print(error)
        return None

    return query_object.first()


class StudyUiSettings(DatabaseBaseClass):
    __tablename__ = 'study_ui_settings'

    display_posts_in_feed: Mapped[bool] = mapped_column(Boolean)
    display_followers: Mapped[bool] = mapped_column(Boolean)
    display_credibility: Mapped[bool] = mapped_column(Boolean)
    display_progress: Mapped[bool] = mapped_column(Boolean)
    display_number_of_reactions: Mapped[bool] = mapped_column(Boolean)
    allow_multiple_reactions: Mapped[bool] = mapped_column(Boolean)
    post_enabled_reactions: Mapped[bool] = mapped_column(Boolean)
    comment_enabled_reactions: Mapped[bool] = mapped_column(Boolean)

    @staticmethod
    def get_by_id(session, ui_settings_id):
        return get_by_id(session, StudyUiSettings, ui_settings_id)


class StudyBasicSettings(DatabaseBaseClass):
    __tablename__ = 'study_basic_settings'

    name: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)
    prompt: Mapped[str] = mapped_column(String)
    length: Mapped[int] = mapped_column(Integer)
    require_reactions: Mapped[bool] = mapped_column(Boolean)
    require_comments: Mapped[bool] = mapped_column(Boolean)
    require_identification: Mapped[bool] = mapped_column(Boolean)

    @staticmethod
    def get_by_id(session, basic_settings_id):
        return get_by_id(session, StudyBasicSettings, basic_settings_id)


class StudyAdvancedSettings(DatabaseBaseClass):
    __tablename__ = 'study_advanced_settings'

    minimum_comment_length: Mapped[int] = mapped_column(Integer)
    prompt_delay_seconds: Mapped[int] = mapped_column(Integer)
    react_delay_seconds: Mapped[int] = mapped_column(Integer)
    gen_completion_code: Mapped[int] = mapped_column(Integer)
    completion_code_digits: Mapped[int] = mapped_column(Integer)
    gen_random_default_avatars: Mapped[int] = mapped_column(Integer)

    @staticmethod
    def get_by_id(session, advanced_settings_id):
        return get_by_id(session, StudyAdvancedSettings, advanced_settings_id)


class StudyPagesSettings(DatabaseBaseClass):
    __tablename__ = 'study_pages_settings'

    pre_intro: Mapped[str] = mapped_column(String)
    pre_intro_delay_seconds: Mapped[int] = mapped_column(Integer)
    rules: Mapped[str] = mapped_column(String)
    rules_delay_seconds: Mapped[int] = mapped_column(Integer)
    post_intro: Mapped[str] = mapped_column(String)
    post_intro_delay_seconds: Mapped[int] = mapped_column(Integer)
    debrief: Mapped[str] = mapped_column(String)

    @staticmethod
    def get_by_id(session, pages_settings_id):
        return get_by_id(session, StudyPagesSettings, pages_settings_id)


class AdminUsers(DatabaseBaseClass):
    __tablename__ = 'admin_users'

    access_right: Mapped[int] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.now, nullable=False)

    @staticmethod
    def get_by_id(session, user_id):
        return get_by_id(session, AdminUsers, user_id)


class Studies(DatabaseBaseClass):
    __tablename__ = 'studies'

    fk_ui_settings: Mapped[int] = mapped_column(Integer, ForeignKey('study_ui_settings.id'))
    fk_basic_settings: Mapped[int] = mapped_column(Integer, ForeignKey('study_basic_settings.id'))
    fk_advanced_settings: Mapped[int] = mapped_column(Integer, ForeignKey('study_advanced_settings.id'))
    fk_pages_settings: Mapped[int] = mapped_column(Integer, ForeignKey('study_pages_settings.id'), nullable=True)
    fk_opened_by: Mapped[int] = mapped_column(Integer, ForeignKey('admin_users.id'))
    fk_closed_by: Mapped[int] = mapped_column(Integer, ForeignKey('admin_users.id'))
    opened_at: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=True, default=None)
    closed_at: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=True, default=None)
    result_last_download_time: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=True, default=None)
    fk_result_last_download_by: Mapped[int] = mapped_column(Integer, ForeignKey('admin_users.id'), nullable=True,
                                                            default=None)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.now, nullable=False)

    basic_settings = relationship('StudyBasicSettings')
    advanced_settings = relationship('StudyAdvancedSettings')
    pages_settings = relationship('StudyPagesSettings')
    ui_settings = relationship('StudyUiSettings')
    opened_by = relationship('AdminUsers', foreign_keys=[fk_opened_by])
    closed_by = relationship('AdminUsers', foreign_keys=[fk_closed_by])
    result_last_download_by = relationship('AdminUsers', foreign_keys=[fk_result_last_download_by])

    @staticmethod
    def get_by_id(session, study_id):
        return get_by_id(session, Studies, study_id, {StudyBasicSettings, StudyAdvancedSettings, StudyPagesSettings,
                                                      StudyAdvancedSettings, AdminUsers})


class Sources(DatabaseBaseClass):
    __tablename__ = 'sources'

    ms_id: Mapped[str] = mapped_column(String)
    name: Mapped[str] = mapped_column(String)
    style: Mapped[bytes] = mapped_column(String)
    max_posts: Mapped[int] = mapped_column(Integer)
    true_post_percentage: Mapped[int] = mapped_column(Integer)
    avatar: Mapped[bytes] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.now, nullable=False)

    @staticmethod
    def get_by_id(session, source_id):
        return get_by_id(session, Sources, source_id)


class Participants(DatabaseBaseClass):
    __tablename__ = 'participants'

    ms_id: Mapped[int] = mapped_column(Integer)
    fk_linked_study: Mapped[int] = mapped_column(Integer, ForeignKey('studies.id'))
    session_id: Mapped[str] = mapped_column(String)
    avatar: Mapped[bytes] = mapped_column(String)
    username: Mapped[str] = mapped_column(String)
    nb_follower: Mapped[int] = mapped_column(Integer)
    credibility_score: Mapped[int] = mapped_column(Integer)
    game_start_time: Mapped[datetime] = mapped_column(TIMESTAMP)
    game_finish_time: Mapped[datetime] = mapped_column(TIMESTAMP)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.now, nullable=False)

    linked_study = relationship('Studies')

    @staticmethod
    def get_by_id(session, participant_id):
        return get_by_id(session, Participants, participant_id)


class Posts(DatabaseBaseClass):
    """
    Represents a post in the database. This data is static.

    :param id: The ID of the post.
    :type id: int
    :param ms_id: The Microsoft ID of the post.
    :type ms_id: str
    :param fk_linked_study: The ID of the linked study.
    :type fk_linked_study: int
    :param headline: The headline of the post.
    :type headline: str
    :param content: The content of the post.
    :type content: str
    :param is_true_fact: Indicates whether the post represents a true fact.
    :type is_true_fact: bool
    :param changes_to_follower_on_like: The number of changes to the follower count when the post is liked.
    :type changes_to_follower_on_like: int
    :param changes_to_follower_on_dislike: The number of changes to the follower count when the post is disliked.
    :type changes_to_follower_on_dislike: int
    :param changes_to_follower_on_share: The number of changes to the follower count when the post is shared.
    :type changes_to_follower_on_share: int
    :param changes_to_follower_on_flag: The number of changes to the follower count when the post is flagged.
    :type changes_to_follower_on_flag: int
    :param changes_to_credibility_on_like: The number of changes to the credibility score when the post is liked.
    :type changes_to_credibility_on_like: int
    :param changes_to_credibility_on_dislike: The number of changes to the credibility score when the post is disliked.
    :type changes_to_credibility_on_dislike: int
    :param changes_to_credibility_on_share: The number of changes to the credibility score when the post is shared.
    :type changes_to_credibility_on_share: int
    :param changes_to_credibility_on_flag: The number of changes to the credibility score when the post is flagged.
    :type changes_to_credibility_on_flag: int
    :param number_of_reactions: The number of reactions to the post.
    :type number_of_reactions: int
    :param fk_source_id: The ID of the post's source.
    :type fk_source_id: int
    :param created_at: The datetime when the post was created.
    :type created_at: datetime.datetime
    :param linked_study: The linked study object.
    :type linked_study: study.Studies
    :param source: The source object.
    :type source: source.Sources
    """
    __tablename__ = 'posts'

    # @todo Add a default amount of like/dislike/share/flags
    ms_id: Mapped[str] = mapped_column(String)
    fk_linked_study: Mapped[int] = mapped_column(Integer, ForeignKey('studies.id'))
    headline: Mapped[str] = mapped_column(String)
    content: Mapped[str] = mapped_column(String)
    is_true_fact: Mapped[bool] = mapped_column(Boolean)
    number_of_likes: Mapped[int] = mapped_column(Integer, default=0)  # Likes shown when post is presented
    number_of_dislike: Mapped[int] = mapped_column(Integer, default=0)  # Dislikes shown when post is presented
    number_of_shared: Mapped[int] = mapped_column(Integer, default=0)  # Shares shown when post is presented
    number_of_flagged: Mapped[int] = mapped_column(Integer, default=0)  # Flags shown when post is presented
    changes_to_follower_on_like: Mapped[int] = mapped_column(Integer, default=0)
    changes_to_follower_on_dislike: Mapped[int] = mapped_column(Integer, default=0)
    changes_to_follower_on_share: Mapped[int] = mapped_column(Integer, default=0)
    changes_to_follower_on_flag: Mapped[int] = mapped_column(Integer, default=0)
    changes_to_credibility_on_like: Mapped[int] = mapped_column(Integer, default=0)
    changes_to_credibility_on_dislike: Mapped[int] = mapped_column(Integer, default=0)
    changes_to_credibility_on_share: Mapped[int] = mapped_column(Integer, default=0)
    changes_to_credibility_on_flag: Mapped[int] = mapped_column(Integer, default=0)
    fk_source_id: Mapped[int] = mapped_column(Integer, ForeignKey('sources.id'))
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.now, nullable=False)

    linked_study = relationship('Studies')
    source = relationship('Sources')

    @staticmethod
    def get_by_id(session, post_id):
        return get_by_id(session, Posts, post_id, {Studies, Sources})

    @staticmethod
    def get_all_by_study_id(session, study_id):
        """Retrieve all posts matching a study ID.

        :param session: The database session.
        :param study_id: The id of the study.
        :return: A list of posts.
        """
        try:
            posts_interactions = (session.query(Posts)
                                  .join(Studies)
                                  .join(Sources)
                                  .filter(Posts.fk_linked_study == study_id).all())
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            print(error)
            return None
        return posts_interactions


class PostsInteractions(DatabaseBaseClass):
    __tablename__ = 'posts_interactions'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    order: Mapped[int] = mapped_column(Integer)
    fk_participant_id: Mapped[int] = mapped_column(Integer, ForeignKey('participants.id'))
    fk_post_id: Mapped[int] = mapped_column(Integer, ForeignKey('posts.id'))
    reaction_type: Mapped[str] = mapped_column(String)
    flagged: Mapped[bool] = mapped_column(Boolean)
    shared: Mapped[bool] = mapped_column(Boolean)
    fk_comment_id: Mapped[int] = mapped_column(Integer, ForeignKey('comments.id'), nullable=True, default=None)
    first_time_to_interact_ms: Mapped[int] = mapped_column(Integer, default=-1)
    last_interaction_time_ms: Mapped[int] = mapped_column(Integer, default=-1)
    user_follower_before: Mapped[int] = mapped_column(Integer)
    user_follower_after: Mapped[int] = mapped_column(Integer)
    user_credibility_before: Mapped[int] = mapped_column(Integer)
    user_credibility_after: Mapped[int] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.now, nullable=False)

    participant = relationship('Participants')
    post = relationship('Posts')
    comment = relationship('Comments')

    @staticmethod
    def get_by_id(session, interaction_id):
        return get_by_id(session, PostsInteractions, interaction_id)

    # @TODO refactor this with to get all matching foreign keys for a function.
    @staticmethod
    def get_all_by_post_id(session, post_id):
        """Retrieve all posts interactions matching a post ID.

        :param session: The database session.
        :param post_id: The id of the post.
        :return: A list of posts interactions.
        """
        try:
            posts_interactions = (session.query(PostsInteractions)
                                  .join(Participants)
                                  .join(Posts)
                                  .filter(PostsInteractions.fk_post_id == post_id).all())
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            print(error)
            return None
        return posts_interactions


class Comments(DatabaseBaseClass):
    __tablename__ = 'comments'

    fk_source_id: Mapped[int] = mapped_column(Integer, ForeignKey('sources.id'))
    fk_post_id: Mapped[int] = mapped_column(Integer, ForeignKey('posts.id'))
    content: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.now, nullable=False)

    source = relationship('Sources')
    linked_posts = relationship('Posts')

    @staticmethod
    def get_by_id(session, comments_id):
        return get_by_id(session, Comments, comments_id)


class CommentsInteractions(DatabaseBaseClass):
    __tablename__ = 'comments_interactions'

    fk_comment_id: Mapped[int] = mapped_column(Integer, ForeignKey('comments.id'))
    fk_participant_id: Mapped[int] = mapped_column(Integer, ForeignKey('participants.id'))
    reaction_type: Mapped[str] = mapped_column(String)
    first_time_to_interact_ms: Mapped[int] = mapped_column(Integer)
    last_interaction_time_ms: Mapped[int] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.now, nullable=False)

    comment = relationship('Comments')
    participant = relationship('Participants')

    @staticmethod
    def get_by_id(session, interaction_id):
        return get_by_id(session, CommentsInteractions, interaction_id)
