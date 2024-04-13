CREATE TABLE "study_ui_settings" (
  "id" SERIAL PRIMARY KEY,
  "display_posts_in_feed" bool,
  "display_followers" bool,
  "display_credibility" bool,
  "display_progress" bool,
  "display_number_of_reactions" bool,
  "allow_multiple_reactions" bool,
  "post_enabled_reactions" bool,
  "comment_enabled_reactions" bool
);

CREATE TABLE "study_basic_settings" (
  "id" SERIAL PRIMARY KEY,
  "name" varchar,
  "description" text,
  "prompt" varchar,
  "length" integer,
  "require_reactions" bool,
  "require_comments" bool,
  "require_identification" bool
);

CREATE TABLE "study_advanced_settings" (
  "id" SERIAL PRIMARY KEY,
  "minimum_comment_length" integer,
  "prompt_delay_seconds" integer,
  "react_delay_seconds" integer,
  "gen_completion_code" integer,
  "completion_code_digits" integer,
  "gen_random_default_avatars" integer
);

CREATE TABLE "study_pages_settings" (
  "id" SERIAL PRIMARY KEY,
  "pre_intro" varchar,
  "pre_intro_delay_seconds" integer,
  "rules" varchar,
  "rules_delay_seconds" integer,
  "post_intro" varchar,
  "post_intro_delay_seconds" integer,
  "debrief" varchar
);

CREATE TABLE "admin_users" (
  "id" SERIAL PRIMARY KEY,
  "access_right" integer,
  "created_at" timestamp DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE "studies" (
  "id" SERIAL PRIMARY KEY,
  "fk_ui_settings" integer,
  "fk_basic_settings" integer,
  "fk_advanced_settings" integer,
  "fk_pages_settings" integer,
  "fk_opened_by" integer,
  "fk_closed_by" integer,
  "opened_at" timestamp ,
  "closed_at" timestamp ,
  "result_last_download_time" timestamp ,
  "result_last_download_by" integer,
  "created_at" timestamp,
  CONSTRAINT fk_basic_settings FOREIGN KEY(id)
      REFERENCES study_basic_settings(id),
  CONSTRAINT fk_ui_settings FOREIGN KEY(id)
      REFERENCES study_ui_settings(id),
  CONSTRAINT fk_advanced_settings FOREIGN KEY(id)
      REFERENCES study_advanced_settings(id),
  CONSTRAINT fk_pages_settings FOREIGN KEY(id)
      REFERENCES study_pages_settings(id),
  CONSTRAINT fk_opened_at FOREIGN KEY(id)
      REFERENCES admin_users(id),
  CONSTRAINT fk_closed_at FOREIGN KEY(id)
      REFERENCES admin_users(id)
);

CREATE TABLE "sources" (
  "id" SERIAL PRIMARY KEY,
  "ms_id" varchar,
  "name" varchar,
  "style" bytea,
  "max_posts" integer,
  "true_post_percentage" integer,
  "avatar" bytea,
  "created_at" timestamp
);

CREATE TABLE "participants" (
  "id" SERIAL PRIMARY KEY,
  "ms_id" integer,
  "fk_linked_study" integer,
  "session_id" varchar,
  "avatar" bytea,
  "username" varchar,
  "nb_follower" integer,
  "credibility_score" integer,
  "game_start_time" timestamp,
  "game_finish_time" timestamp,
  "created_at" timestamp,
  CONSTRAINT fk_linked_study FOREIGN KEY(id)
      REFERENCES admin_users(id)
);

CREATE TABLE "posts" (
  "id" SERIAL PRIMARY KEY,
  "ms_id" varchar,
  "fk_linked_study" integer,
  "headline" varchar,
  "content" text,
  "is_true_fact" bool,
  "changes_to_follower_on_like" integer,
  "changes_to_follower_on_dislike" integer,
  "changes_to_follower_on_share" integer,
  "changes_to_follower_on_flag" integer,
  "changes_to_credibility_on_like" integer,
  "changes_to_credibility_on_dislike" integer,
  "changes_to_credibility_on_share" integer,
  "changes_to_credibility_on_flag" integer,
  "number_of_reactions" integer,
  "fk_source_id" integer,
  "created_at" timestamp,
  CONSTRAINT fk_linked_study FOREIGN KEY(id)
      REFERENCES admin_users(id),
  CONSTRAINT fk_source_id FOREIGN KEY(id)
      REFERENCES sources(id)
);

CREATE TABLE "posts_interactions" (
  "id" SERIAL PRIMARY KEY,
  "order" integer,
  "fk_participant_id" integer,
  "fk_post_id" integer,
  "reaction_type" varchar,
  "flagged" bool,
  "shared" bool,
  "first_time_to_interact_ms" integer,
  "last_interaction_time_ms" integer,
  "user_follower_before" integer,
  "user_follower_after" integer,
  "user_credibility_before" integer,
  "user_credibility_after" integer,
  "created_at" timestamp,
  CONSTRAINT fk_participant_id FOREIGN KEY(id)
      REFERENCES participants(id),
  CONSTRAINT fk_post_id FOREIGN KEY(id)
      REFERENCES posts(id)
);

CREATE TABLE "comments" (
  "id" SERIAL PRIMARY KEY,
  "fk_source_id" integer,
  "fk_post_id" integer,
  "content" varchar,
  "created_at" timestamp,
  CONSTRAINT fk_source_id FOREIGN KEY(id)
      REFERENCES sources(id),
  CONSTRAINT fk_linked_post FOREIGN KEY(id)
      REFERENCES posts(id)
);

CREATE TABLE "comments_interactions" (
  "id" SERIAL PRIMARY KEY,
  "fk_comment_id" integer,
  "fk_participant_id" integer,
  "reaction_type" varchar,
  "first_time_to_interact_ms" integer,
  "last_interaction_time_ms" integer,
  "created_at" timestamp,
  CONSTRAINT fk_comment_id FOREIGN KEY(id)
      REFERENCES comments(id),
  CONSTRAINT fk_participant_id FOREIGN KEY(id)
      REFERENCES participants(id)
);
