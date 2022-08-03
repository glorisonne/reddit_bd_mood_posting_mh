# RQ3: How does trait mood differ between users who post in MH subreddits and those who only post in non-MH subreddits?
import pandas as pd
import numpy as np
import math
import config as c
import util as u
import RQ2 as rq2

DV = "posted_MH"
min_posts = 4
suffix = "" # "-new" # "-new", ""

posts = pd.read_pickle(c.data + "posts_LIWC.pkl")
posts = u.identify_mh_subreddits(posts, suffix=suffix)

# only posts with at least 25 words
# posts = posts[posts.WC >= c.min_words_per_post]
posts = posts.groupby("user_id").filter(lambda x: x[~x.in_mh_subreddit].WC.sum() > 24)

# posted_MH: at least min_posts in both MH and non-MH subreddits
posts_users_posted_MH = rq2.select_posts_by_users_min_posts(posts, min_posts=min_posts)

# not_posted_MH: at least min_posts (8) posts in non-MH subreddits but NO posts in MH subreddits
posts_users_not_posted_MH = posts.groupby("user_id").filter(lambda x: (len(x[x.in_mh_subreddit]) == 0) &
                                                 (len(x[~x.in_mh_subreddit]) >= (2*min_posts)))
print("0 posts in MH subreddits and at least %d posts in non-MH subreddits: %d" %(min_posts, posts_users_not_posted_MH.user_id.nunique()))

# For each user: mean LIWC score, control variables, group
posts_users_posted_MH[DV] = True
posts_users_not_posted_MH[DV] = False
posts = pd.concat([posts_users_posted_MH, posts_users_not_posted_MH], axis=0)

# select only posts in non-MH subreddits!
posts = posts[~posts.in_mh_subreddit]

users_liwc = posts.groupby("user_id")[c.liwc].mean().reset_index().rename(columns={"user_id": "id"})
users = pd.read_pickle(c.data + "users.pkl")
users = users_liwc.merge(users, left_on="id", right_on="id", how="left")
users[DV] = np.where(users.id.isin(posts[posts[DV]].user_id.unique()), 1, 0)

# complete cases only (age + gender)
n_users_incomplete_cases = len(users)
users = users[users.gender.notna() & users.avg_posting_age.notna()]

print("Selected %d users for RQ 3 (%d before selecting only users with age+gender\n"
      "%d posted only in non-MH subreddits)" %(len(users), n_users_incomplete_cases, len(users[users.DV == 0])))

users[["id", DV] + c.liwc + c.controls].to_csv(c.data + "users_rq3%s.csv" %suffix)

# descriptive statistics
users_posted_MH = users[users.posted_MH == 1]
users_not_posted_MH = users[users.posted_MH == 0]

for var in c.liwc:
    p, sig, effect_size, effect_size_interpretation, test_name = stats.mean_comparison_test(users_posted_MH[var],
                                                    users_not_posted_MH[var], n_comparisons=5, dependent=False)
    print("%s;%.2f;%.2f;%.2f;%.2f;%.4f;%s;%.2f;%s" %(var,
        users_posted_MH[var].mean(), users_posted_MH[var].std(),
        users_not_posted_MH[var].mean(), users_not_posted_MH[var].std(),
        p, sig, effect_size, effect_size_interpretation))
    print(test_name)