# RQ3: How does trait mood differ between users who post in MH subreddits and those who only post in non-MH subreddits?
import pandas as pd
import numpy as np

import config as c
import util as u

def select_users(DV, min_posts, suffix):
    print("Reading posts from %s" % (c.data + "posts_LIWC%s.csv" % suffix))
    posts = pd.read_csv(c.data + "posts_LIWC%s.csv" %suffix)
    n_users = posts.user_id.nunique()
    print("Read in %d posts by %d users" % (len(posts), n_users))

    # posted_MH: at least min_posts with at least 25 words in both MH and non-MH subreddits
    posts_users_posted_MH = posts.groupby("user_id").filter(lambda x:
                                        (len(x[(~x.in_mh_subreddit) & (x.WC >= c.min_words_per_post)]) >= min_posts) &
                                        (len(x[x.in_mh_subreddit & (x.WC >= c.min_words_per_post)]) >= min_posts))
    print("Selected %d users (%.1f%%) with %d posts (%.1f%% in MH subreddits) with at least %d posts with at least %d"
          " words in MH and non-MH subreddits"
          % (posts_users_posted_MH.user_id.nunique(), posts_users_posted_MH.user_id.nunique() / n_users * 100,
             len(posts_users_posted_MH),
             len(posts_users_posted_MH[posts_users_posted_MH.in_mh_subreddit]) / len(posts_users_posted_MH) * 100,
             min_posts, c.min_words_per_post))

    # not_posted_MH: at least min_posts (8) posts with at least 25 words in non-MH subreddits but
    # NO posts (regardless of length) in MH subreddits
    posts_users_not_posted_MH = posts.groupby("user_id").filter(lambda x: (len(x[x.in_mh_subreddit]) == 0) &
                                                     (len(x[(~x.in_mh_subreddit) & (x.WC >= c.min_words_per_post)]) >= (2*min_posts)))
    print("0 posts in MH subreddits and at least %d posts in non-MH subreddits: %d" %(2*min_posts,
                                                                                      posts_users_not_posted_MH.user_id.nunique()))

    # For each user: mean LIWC score, control variables, group
    posts_users_posted_MH[DV] = True
    posts_users_not_posted_MH[DV] = False
    posts = pd.concat([posts_users_posted_MH, posts_users_not_posted_MH], axis=0)

    # select only posts in non-MH subreddits!
    posts = posts[~posts.in_mh_subreddit]

    users_liwc = posts.groupby("user_id")[c.liwc].mean().reset_index().rename(columns={"user_id": "id"})
    users = pd.read_csv(c.data + "users%s.csv" %suffix)
    users = users_liwc.merge(users, left_on="id", right_on="id", how="left")
    users[DV] = np.where(users.id.isin(posts[posts[DV]].user_id.unique()), 1, 0)

    # complete cases only (age + gender)
    n_users_incomplete_cases = len(users)
    users = users[users.gender.notna() & users.avg_posting_age.notna()]

    print("Selected %d users for RQ 3 (%d before selecting only users with age+gender, %d posted"
" only in non-MH subreddits\n)" %(len(users), n_users_incomplete_cases, len(users[users[DV] == 0])))

    users[["id", DV] + c.liwc + c.controls].to_csv(c.data + "users_rq3%s.csv" %suffix)
    return users

def descriptive_statistics(users):
    # descriptive statistics
    users_posted_MH = users[users.posted_MH == 1]
    users_not_posted_MH = users[users.posted_MH == 0]

    for var in c.controls + c.liwc:
        p, sig, effect_size, effect_size_interpretation, test_name = u.mean_comparison_test(users_posted_MH[var],
                                                        users_not_posted_MH[var], n_comparisons=len(c.controls + c.liwc),
                                                                                            dependent=False)
        print("%s;%.2f;%.2f;%.2f;%.2f;%.4f;%s;%.2f;%s;%s" %(var,
            users_posted_MH[var].mean(), users_posted_MH[var].std(),
            users_not_posted_MH[var].mean(), users_not_posted_MH[var].std(),
            p, sig, effect_size, effect_size_interpretation, test_name))

def gender_balance_users(users, DV, suffix, user_id_list=""):
    """
    Select the same number of masculine and feminine users for each outcome of the outcome variable posted_MH
    :param users:
    :param user_id_list: select users according to provided user_id list to reproduce results from paper (otherwise random variation would select other users)
    :return:
    """
    print("Outcome variable posted_MH by gender before gender balancing")
    print(users.groupby(DV).gender.value_counts())
    if user_id_list:
        users_gender_balanced = pd.read_csv(user_id_list).id
    else:
        # determine minimum number of users with a certain gender in each outcome group
        n_not_posted_MH = users[users[DV] == 0].groupby("gender").id.count().min()
        n_posted_MH = users[users[DV] == 1].groupby("gender").id.count().min()

        n_users = [n_not_posted_MH, n_posted_MH]

        # subsample users with each gender in each outcome group
        users_gender_balanced = []
        for posted_MH in [0, 1]:
            for gender in [0, 1]:
                users_gender_balanced.extend(users[(users[DV] == posted_MH) & (users.gender == gender)]
                                             .id.sample(n=n_users[posted_MH], replace=False, random_state=0))

        pd.Series(users_gender_balanced).to_csv(c.data + "user_ids_rq3_gender_balanced.csv", index=False)

    users = users[users.id.isin(users_gender_balanced)]
    users.to_csv(c.data + "users_rq3_gender_balanced%s.csv" %suffix, index=False)
    print("Outcome variable posted_MH by gender after gender balancing")
    print(users.groupby(DV).gender.value_counts())

if __name__ == "__main__":
    DV = "posted_MH"
    min_posts = 4
    suffix = u.get_suffix()
    users = select_users(DV, min_posts, suffix)
    users = pd.read_csv(c.data + "users_rq3.csv")
    descriptive_statistics(users)
    user_id_list = c.data + "user_ids_rq3_gender_balanced.csv"
    if suffix == "_demo":
        user_id_list = ""
    gender_balance_users(users, DV, suffix, user_id_list=user_id_list)