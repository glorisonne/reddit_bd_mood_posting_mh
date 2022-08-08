# -*- coding: utf-8 -*-
import pandas as pd
from scipy import stats
import numpy as np

import config as c


def identify_mh_subreddits(posts):
    subreddits = pd.read_csv(c.data + "subreddit_topics.csv")
    mh_subreddits = subreddits[subreddits["third level"] == "Mental Health"].subreddit
    posts["in_mh_subreddit"] = posts.subreddit_name.str.lower().isin(mh_subreddits.str.lower())
    print("%d posts by %d users in %d MH subreddits" % (len(posts[posts.in_mh_subreddit]),
                                                        posts[posts.in_mh_subreddit].user_id.nunique(),
                                                        len(mh_subreddits)))
    return posts


def mean_comparison_test(series_left, series_right, n_comparisons, dependent):
    """
    Statistical comparison of the means of two series
    :param series_left: series to compare
    :param series_right: series to compare with
    :param n_comparisons: total number of comparisons that are run for the same data to calculate Bonferroni correction
    (set to 1 if do not want correction for multiple comparisons)
    :param dependent: whether the series are dependent or independent
    :returns: p value, p value significant at 0.001, effect size, adjective to describe effect size, name of test
    """
    if dependent:
        test_name = "dependent t"
        result = stats.ttest_rel(series_left, series_right, nan_policy="omit")
        effect_size = cohens_d(series_left, series_right, result.statistic)

    else:
        # could test for normality first - then use Bartlett's test instead of Levene to check for variance homogeneity
        # but can ignore non-normality for sample sizes > 30
        # first run Levene's test to check if variances are equal or not
        # null-hypothesis: variances are equal
        # trimmed is best option for heavy-tailed distribution
        var_equal = stats.levene(series_left, series_right, center="trimmed") # trimmed, mean
        # print(var_equal)

        if is_significant(var_equal.pvalue, n_comparisons):
            # unequal variances -> Welch's test for significance and Glass's delta for effect size
            test_name = "Welchs-t"
            result = stats.ttest_ind(series_left, series_right, equal_var=False, nan_policy="omit")
            effect_size = glass_delta(series_left, series_right)
        else:
            # equal variances -> t-test for significance, Cohen's d for effect size
            test_name = "independent t"
            result = stats.ttest_ind(series_left, series_right, equal_var=True, nan_policy="omit")
            effect_size = cohens_d(series_left, series_right, result.statistic)

    effect_size_interpretation = interpret_effect_size(effect_size)

    return result.pvalue * n_comparisons, is_significant(result.pvalue,
                                         n_comparisons), effect_size, effect_size_interpretation, test_name

def cohens_d(group1, group2, statistics):
    """
    statistics = t-value of (Welch's-)t-test
    """
    # Effect size
    # Cohen's d

    # Calculated using t(statistics)*square root(1/group1_n + 1/group2_n)
    if group1.count() == 0.0 or group2.count() == 0:
        return 0.0
    else:
        return statistics * np.sqrt(1 / group1.count() + 1 / group2.count())

def glass_delta(group1, group2):
    # Glass's delta
    return (group1.mean() - group2.mean()) / group1.std()

def interpret_effect_size(effect_size):
    """
    https://en.wikipedia.org/wiki/Effect_size#Cohen's_d
    https://digitalcommons.wayne.edu/cgi/viewcontent.cgi?referer=https://scholar.google.com/&httpsredir=1&article=1536&context=jmasm
    Determines text interpretation of effect size given Cohen's d value
    :param effect_size: float of Cohen's d or Glass delta value
    :returns: effect_size_interpretation: adjective to describe magnitude of effect size
    """
    effect_size = np.abs(effect_size)
    # print("Cohen's d %.2f" %cohens_d)
    if 0 <= effect_size < 0.1:
        effect_size_interpretation = "No effect"
    elif 0.1 <= effect_size < 0.2:
        effect_size_interpretation = "Very small"
    elif 0.2 <= effect_size < 0.5:
        effect_size_interpretation = "Small"
    elif 0.5 <= effect_size < 0.8:
        effect_size_interpretation = "Medium"
    elif 0.8 <= effect_size < 1.2:
        effect_size_interpretation = "Large"
    elif 1.2 <= effect_size < 2.0:
        effect_size_interpretation = "Very large"
    elif effect_size >= 2.0:
        effect_size_interpretation = "Huge"
    else:
        return pd.NA
    return effect_size_interpretation

def is_significant(p_value, correction=1, threshold=0.001):
    return (p_value * correction) < threshold