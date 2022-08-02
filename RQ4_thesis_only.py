# RQ3: How does trait mood differ between users who post in MH subreddits and those who only post in non-MH subreddits?
import pandas as pd
import math
import config as c
import util as u

def only_previous_post(posts, period, min_posts):
    """
    min_posts: how many target posts a user must have in each subreddit group to be included (typically 1 or 2)
    post_type: post = any (submission or comment), submission = only submissions
    this is only for the target post, pre_posts can be either submission or comment
    """
    # get info of previous post
    posts_by_user = posts.groupby("user_id")
    for col in ["created_at_UTC", "WC", "subreddit_type"] + c.liwc:
        posts["%s_prev" % col] = posts_by_user[col].shift(+1)

    # previous post is from "other" subreddit and has at least 25 words
    posts.loc[:, "WC_prev"] = np.where((posts.WC_prev > 24) &
                                       (posts.subreddit_type_prev == "other") &
                                       ((posts.created_at_UTC - posts.created_at_UTC_prev) < period),
                                       posts.WC_prev, np.nan)

    # pre-filter eligible users (will then filter their posts)
    posts_users_MH_non_MH_pre = posts.groupby("user_id").filter(lambda x:
                                    # at least min_posts MH subreddit posts with previous post
                                    (len(x[x.subreddit_type.isin(["bd", "mh"]) & x.WC_prev.notna()]) >= min_posts) &
                                    # at least min_posts non-MH subreddit post with previous post
                                    (len(x[(x.subreddit_type == "other") & x.WC_prev.notna()]) >= min_posts))
    # from all posts of the eligible users, select only those that have a non-mh pre post
    posts_with_non_mh_pre_post = posts_users_MH_non_MH_pre[posts_users_MH_non_MH_pre.WC_prev.notna()]

    # split into MH and non-MH post instances (the two values of the DV)
    posts_MH = posts_with_non_mh_pre_post[posts_with_non_mh_pre_post.subreddit_type.isin(["bd", "mh"])]
    posts_non_MH = posts_with_non_mh_pre_post[posts_with_non_mh_pre_post.subreddit_type == "other"]
    posts_MH["MH_post"] = True
    posts_non_MH["MH_post"] = False
    posts = pd.concat([posts_MH, posts_non_MH], axis=0)

    instances_MH = len(posts_MH)
    instances_non_MH = len(posts_non_MH)

    print("Selected users: %d" %posts_users_MH_non_MH_pre.user_id.nunique())
    print("All posts of selected users: %d" %len(posts_users_MH_non_MH_pre))
    print("Posts with preceding non-MH post with at least 25 words: %d" %len(posts_with_non_mh_pre_post))
    print("Of which are in MH subreddits: %d" %instances_MH)
    print("Of which are in non-MH subreddits: %d" %instances_non_MH)

    # add user information
    users["activity"] = users.n_posts / users.active_days
    users = users[["id"] + c.controls]

    # broadcast user information to every post
    posts = posts.merge(users, left_on="user_id", right_on="id", how="left")
    posts.rename(columns={"id_x" : "id"}, inplace=True)

    posts[["id", "MH_post", "user_id"] + ["%s_prev" %v for v in c.liwc] + c.controls].to_csv(
        c.data_folder + "posts_users_pre_24h_min_2_posts.csv", index=False)

    return posts_users_MH_non_MH_pre, instances_MH, instances_non_MH


posts = pd.read_pickle(c.data + "posts_LIWC.pkl")

posts.set_index(["user_id", "created_at_UTC"], inplace=True)
posts.sort_index(inplace=True)
posts.reset_index(inplace=True)

users = pd.read_pickle(c.data + "users.pkl")

posts_included_users, instances_MH, instances_non_MH = only_previous_post(posts, period='24h', min_posts=2)

print("period,users,posts,MH posts,non-MH posts,submissions, MH submissions, non-MH submissions,eligible MH posts,"
      "eligible non-MH posts\n%s,%d,%d,%d,%d,%d,%d,%d,%d,%d"
      % (period, posts_included_users.user_id.nunique(),
         len(posts_included_users),
         len(posts_included_users[posts_included_users.subreddit_type.isin(["bd", "mh"])]),
         len(posts_included_users[posts_included_users.subreddit_type == "other"]),
         len(posts_included_users[posts_included_users.type == "s"]),
         len(posts_included_users[
                 (posts_included_users.type == "s") & posts_included_users.subreddit_type.isin(["bd", "mh"])]),
         len(posts_included_users[
                 (posts_included_users.type == "s") & (posts_included_users.subreddit_type == "other")]),
         instances_MH, instances_non_MH))

