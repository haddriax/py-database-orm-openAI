from datetime import datetime, timezone

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


from database_py.models.db_model import StudyBasicSettings, StudyPagesSettings, StudyAdvancedSettings, StudyUiSettings, \
    Base
from database_py.models.db_model import AdminUsers
from database_py.models.db_model import Studies
from database_py.models.db_model import Sources
from database_py.models.db_model import Participants
from database_py.models.db_model import Posts
from database_py.models.db_model import PostsInteractions
from database_py.models.db_model import Comments
from database_py.models.db_model import CommentsInteractions


db_engine = create_engine('postgresql://postgres:password@localhost/database_2')
# Base.metadata.create_all(db_engine)

Session = sessionmaker(bind=db_engine)
session = Session()

admin_user = AdminUsers(access_right=1)  # Example data
session.add(admin_user)
session.commit()

basic_settings = StudyBasicSettings(name="Example Study", description="Example description", prompt="Example prompt", length=10, require_reactions=True, require_comments=False, require_identification=True)
advanced_settings = StudyAdvancedSettings(minimum_comment_length=50, prompt_delay_seconds=60, react_delay_seconds=30, gen_completion_code=12345, completion_code_digits=6, gen_random_default_avatars=5)
pages_settings = StudyPagesSettings(pre_intro="Welcome to the study!", pre_intro_delay_seconds=10, rules="Study rules here", rules_delay_seconds=20, post_intro="Thank you for participating!", post_intro_delay_seconds=15, debrief="Study debriefing")
ui_settings = StudyUiSettings(display_posts_in_feed=True, display_followers=True, display_credibility=True, display_progress=True, display_number_of_reactions=True, allow_multiple_reactions=True, post_enabled_reactions=True, comment_enabled_reactions=False)
opened_by = session.query(AdminUsers).filter_by(id=1).first()
closed_by = session.query(AdminUsers).filter_by(id=1).first()

session.add_all([basic_settings, advanced_settings, pages_settings, ui_settings])
session.commit()

# Create a Studies object
study = Studies(
    fk_ui_settings=1,
    fk_basic_settings=1,
    fk_advanced_settings=1,
    fk_pages_settings=1,
    fk_opened_by=opened_by.id,
    fk_closed_by=closed_by.id,
    opened_at=datetime.now(timezone.utc),
)

session.add(study)
session.commit()
session.close()
