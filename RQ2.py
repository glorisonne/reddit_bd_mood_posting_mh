# RQ2: What differences exist in the emotions that Reddit users with a BD diagnosis express in MH and non-MH subreddit posts?
import pandas as pd
import math
import config as c
import util as u


def select_posts_by_users_min_posts(posts, min_posts):
    # select users with at least 4 MH and non-MH subreddit posts each
    n_users = posts.user_id.nunique()

    # posts = posts[posts.WC >= c.min_words_per_post]
    posts = posts.groupby("user_id").filter(lambda x: (len(x[~x.in_mh_subreddit]) >= min_posts) &
                                                      (len(x[x.in_mh_subreddit]) >= min_posts))

    print("Selected %d users (%.1f%%) with %d posts (%.1f%% in MH subreddits) with at least %d posts with at least %d"
          " words in MH and non-MH subreddits"
          % (posts.user_id.nunique(), posts.user_id.nunique() / n_users * 100, len(posts),
             len(posts[posts.in_mh_subreddit]) / len(posts) * 100, min_posts, c.min_words_per_post))
    return posts


def compare_user_means(user_means):
    # run dependent t-tests
    print("variable; mean MH posts; SD MH posts; mean non-MH posts; SD non-MH posts;p; p<0.001?; Cohen's d;\
    Cohen's d interpretation")
    for var in c.liwc:
        p, sig, effect_size, effect_size_interpretation, test_name = u.mean_comparison_test(user_means["%s_MH" % var],
                                                                                            user_means[
                                                                                                "%s_non_MH" % var],
                                                                                            n_comparisons=len(c.liwc),
                                                                                            dependent=True)
        print("%s;%.2f;%.2f;%.2f;%.2f;%.4f;%s;%.2f;%s" % (var,
                                                          user_means["%s_MH" % var].mean(),
                                                          user_means["%s_MH" % var].std(),
                                                          user_means["%s_non_MH" % var].mean(),
                                                          user_means["%s_non_MH" % var].std(),
                                                          p, sig, effect_size, effect_size_interpretation))


if __name__ == "__main__":
    posts = pd.read_pickle(c.data + "posts_LIWC.pkl")
    posts = u.identify_mh_subreddits(posts, suffix="-new")

    min_posts = 4
    posts = select_posts_by_users_min_posts(posts, min_posts)

    # calculate mean LIWC scores for users' MH and non-MH posts
    user_means_MH = posts[posts.in_mh_subreddit].groupby("user_id")[c.liwc].mean()
    user_means_non_MH = posts[~posts.in_mh_subreddit].groupby("user_id")[c.liwc].mean()

    user_means = user_means_MH.merge(user_means_non_MH, left_index=True, right_index=True, suffixes=('_MH', '_non_MH'))

    compare_user_means(user_means)
