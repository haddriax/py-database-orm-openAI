INSERT INTO posts
 (ms_id, fk_linked_study, headline, content, is_true_fact,
  changes_to_follower_on_like, changes_to_follower_on_dislike, changes_to_follower_on_share,
  changes_to_follower_on_flag, changes_to_credibility_on_like, changes_to_credibility_on_dislike,
  changes_to_credibility_on_share, changes_to_credibility_on_flag, number_of_reactions, source_id, created_at)
 VALUES ('{ms_id}', '{fk_linked_study}', '{headline}', '{content}', '{is_true_fact}',
         '{changes_to_follower_on_like}', '{changes_to_follower_on_dislike}', '{changes_to_follower_on_share}',
         '{changes_to_follower_on_flag}', '{changes_to_credibility_on_like}', '{changes_to_credibility_on_dislike}',
         '{changes_to_credibility_on_share}', '{changes_to_credibility_on_flag}', '{number_of_reactions}',
         '{source_id}', '{created_at}');
