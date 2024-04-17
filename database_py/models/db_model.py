from sqlalchemy import Integer, String, Boolean, TIMESTAMP, ForeignKey, ForeignKeyConstraint
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import relationship, mapped_column, Mapped, DeclarativeBase
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime


class Base(DeclarativeBase):
    pass


class StudyUiSettings(Base):
    __tablename__ = 'study_ui_settings'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    display_posts_in_feed: Mapped[bool] = mapped_column(Boolean)
    display_followers: Mapped[bool] = mapped_column(Boolean)
    display_credibility: Mapped[bool] = mapped_column(Boolean)
    display_progress: Mapped[bool] = mapped_column(Boolean)
    display_number_of_reactions: Mapped[bool] = mapped_column(Boolean)
    allow_multiple_reactions: Mapped[bool] = mapped_column(Boolean)
    post_enabled_reactions: Mapped[bool] = mapped_column(Boolean)
    comment_enabled_reactions: Mapped[bool] = mapped_column(Boolean)


class StudyBasicSettings(Base):
    __tablename__ = 'study_basic_settings'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)
    prompt: Mapped[str] = mapped_column(String)
    length: Mapped[int] = mapped_column(Integer)
    require_reactions: Mapped[bool] = mapped_column(Boolean)
    require_comments: Mapped[bool] = mapped_column(Boolean)
    require_identification: Mapped[bool] = mapped_column(Boolean)


class StudyAdvancedSettings(Base):
    __tablename__ = 'study_advanced_settings'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    minimum_comment_length: Mapped[int] = mapped_column(Integer)
    prompt_delay_seconds: Mapped[int] = mapped_column(Integer)
    react_delay_seconds: Mapped[int] = mapped_column(Integer)
    gen_completion_code: Mapped[int] = mapped_column(Integer)
    completion_code_digits: Mapped[int] = mapped_column(Integer)
    gen_random_default_avatars: Mapped[int] = mapped_column(Integer)


class StudyPagesSettings(Base):
    __tablename__ = 'study_pages_settings'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    pre_intro: Mapped[str] = mapped_column(String)
    pre_intro_delay_seconds: Mapped[int] = mapped_column(Integer)
    rules: Mapped[str] = mapped_column(String)
    rules_delay_seconds: Mapped[int] = mapped_column(Integer)
    post_intro: Mapped[str] = mapped_column(String)
    post_intro_delay_seconds: Mapped[int] = mapped_column(Integer)
    debrief: Mapped[str] = mapped_column(String)


class AdminUsers(Base):
    __tablename__ = 'admin_users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    access_right: Mapped[int] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.now, nullable=False)


class Studies(Base):
    __tablename__ = 'studies'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
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


class Sources(Base):
    __tablename__ = 'sources'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ms_id: Mapped[str] = mapped_column(String)
    name: Mapped[str] = mapped_column(String)
    style: Mapped[bytes] = mapped_column(String)
    max_posts: Mapped[int] = mapped_column(Integer)
    true_post_percentage: Mapped[int] = mapped_column(Integer)
    avatar: Mapped[bytes] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.now, nullable=False)


class Participants(Base):
    __tablename__ = 'participants'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
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


class Posts(Base):
    __tablename__ = 'posts'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ms_id: Mapped[str] = mapped_column(String)
    fk_linked_study: Mapped[int] = mapped_column(Integer, ForeignKey('studies.id'))
    headline: Mapped[str] = mapped_column(String)
    content: Mapped[str] = mapped_column(String)
    is_true_fact: Mapped[bool] = mapped_column(Boolean)
    changes_to_follower_on_like: Mapped[int] = mapped_column(Integer)
    changes_to_follower_on_dislike: Mapped[int] = mapped_column(Integer)
    changes_to_follower_on_share: Mapped[int] = mapped_column(Integer)
    changes_to_follower_on_flag: Mapped[int] = mapped_column(Integer)
    changes_to_credibility_on_like: Mapped[int] = mapped_column(Integer)
    changes_to_credibility_on_dislike: Mapped[int] = mapped_column(Integer)
    changes_to_credibility_on_share: Mapped[int] = mapped_column(Integer)
    changes_to_credibility_on_flag: Mapped[int] = mapped_column(Integer)
    number_of_reactions: Mapped[int] = mapped_column(Integer)
    fk_source_id: Mapped[int] = mapped_column(Integer, ForeignKey('sources.id'))
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.now, nullable=False)

    linked_study = relationship('Studies')
    source = relationship('Sources')

    @staticmethod
    def get_by_id(session, posts_id):
        post = None
        try:
            post = session.query(Posts).join(Studies).join(Sources).filter(Posts.id == posts_id).first()
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            print(error)
            return None
        return post

    @staticmethod
    def insert(session, study: Studies):
        session.add(study)
        return 1


class PostsInteractions(Base):
    __tablename__ = 'posts_interactions'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    order: Mapped[int] = mapped_column(Integer)
    fk_participant_id: Mapped[int] = mapped_column(Integer, ForeignKey('participants.id'))
    fk_post_id: Mapped[int] = mapped_column(Integer, ForeignKey('posts.id'))
    reaction_type: Mapped[str] = mapped_column(String)
    flagged: Mapped[bool] = mapped_column(Boolean)
    shared: Mapped[bool] = mapped_column(Boolean)
    first_time_to_interact_ms: Mapped[int] = mapped_column(Integer)
    last_interaction_time_ms: Mapped[int] = mapped_column(Integer)
    user_follower_before: Mapped[int] = mapped_column(Integer)
    user_follower_after: Mapped[int] = mapped_column(Integer)
    user_credibility_before: Mapped[int] = mapped_column(Integer)
    user_credibility_after: Mapped[int] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.now, nullable=False)

    participant = relationship('Participants')
    post = relationship('Posts')


class Comments(Base):
    __tablename__ = 'comments'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    fk_source_id: Mapped[int] = mapped_column(Integer, ForeignKey('sources.id'))
    fk_post_id: Mapped[int] = mapped_column(Integer, ForeignKey('posts.id'))
    content: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.now, nullable=False)

    source = relationship('Sources')
    linked_posts = relationship('Posts')


class CommentsInteractions(Base):
    __tablename__ = 'comments_interactions'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    fk_comment_id: Mapped[int] = mapped_column(Integer, ForeignKey('comments.id'))
    fk_participant_id: Mapped[int] = mapped_column(Integer, ForeignKey('participants.id'))
    reaction_type: Mapped[str] = mapped_column(String)
    first_time_to_interact_ms: Mapped[int] = mapped_column(Integer)
    last_interaction_time_ms: Mapped[int] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.now, nullable=False)

    comment = relationship('Comments')
    participant = relationship('Participants')
