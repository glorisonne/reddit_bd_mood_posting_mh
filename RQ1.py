# RQ1: What proportion of Reddit users with a BD diagnosis posts in MH and non-MH subreddits?
import pandas as pd
import math
import config as c
import util as u

posts = pd.read_pickle(c.data + "posts.pkl")

posts = u.identify_mh_subreddits(posts)

posts_by_users = posts.groupby("user_id")
n_users = posts.user_id.nunique()

for min_posts in [1, 8]:
    users_mh_only = posts_by_user.filter(lambda x: (len(x[x.in_mh_subreddit]) >= min_posts) &
                                                   (len(x[~x.in_mh_subreddit]) == 0)).user_id.nunique()
    users_non_mh_only = posts_by_user.filter(lambda x: (len(x[~x.in_mh_subreddit]) >= min_posts) &
                                                       (len(x[x.in_mh_subreddit]) == 0)).user_id.nunique()
    users_both_mh_and_non_mh = posts_by_user.filter(lambda x: (len(x[~x.in_mh_subreddit]) >= math.ceil(min_posts / 2)) &
                                                              (len(x[x.in_mh_subreddit]) >= math.ceil(
                                                                  min_posts / 2))).user_id.nunique()

    print("At least %d (%d for both MH and non-MH) post(s):" % (min_posts, math.ceil(min_posts / 2)))
    print("%d users (%.1f%%) only posted in MH subreddits\n%d users (%.1f%%) only posted in non-MH subreddits\n\
    %d users (%.1f%%) posted both in MH and non-MH subreddits"
          % (users_mh_only, users_mh_only / n_users * 100, users_non_mh_only, users_non_mh_only / n_users * 100,
             users_both_mh_and_non_mh, users_both_mh_and_non_mh / n_users * 100))