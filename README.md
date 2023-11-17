# Code accompanying the paper "Posting Patterns in Peer Online Support Forums and their Associations with Emotions and Mood in Bipolar Disorder: Exploratory Analysis" 

This repository contains the code to reproduce all results from the paper [Jagfeld, G., Lobban, F., Davies, R., Boyd, R. L., Rayson, P., & Jones, S. H. (2023) ‘Posting patterns in peer online support forums and their associations with emotions and mood in bipolar disorder: Exploratory analysis’, PLOS ONE, 18(9), p. e0291369.](https://doi.org/10.1371/journal.pone.0291369).

The data provided in the data/ directory is only made-up example data to show the structure of the data and test the code release.
You can request the actual data [here](https://doi.org/10.17635/lancaster/researchdata/589).
Please note that you will need to provide the [data usage agreement](https://github.com/glorisonne/reddit_bd_mood_posting_mh/blob/main/data/DataUsageAgreement_SBiDDDataset.docx).
Access to the data will only be granted for non-commercial research purposes.

To reproduce the results of this study, you require the files posts_meta.csv, users.csv, and posts_LIWC.csv that 
you need to place in the data/ subdirectory of this repository.
To run the code on the provided example data, use the optional demo flag for each of the scripts.

```

## Requirements
python 3.9.5, pandas 1.3.0, numpy 1.20.3<br>
R 4.1.0, car 3.0 (including carData 3.0), languageR 1.5.0, caret 6.0 (including ggplot2 3.3.5, lattice 0.2.0), ROCR 1.0

## Subreddit topics
The file data/subreddit_topics.csv contains the categorisation of 30,867 subreddits that was created in this project based on snoopsnoo*s subreddit categorisation (https://github.com/orionmelt/sherlock/blob/master/subreddits.csv).

The 158 MH subreddits are identified by the category label "Mental Health" assigned in the column "third level".
Among these, the 37 BD subreddits are identified by the category label "bipolar" assigned in the column "fourth level".

## RQ1: What proportion of Reddit users with a BD diagnosis posts in MH and non-MH subreddits?

```bash
python RQ1.py [demo]
```

### Expected output (with actual input data, not in demo mode)
````{verbatim}
At least 1 (1 for both MH and non-MH) post(s):
1369 users (7.0%) only posted in MH subreddits
4666 users (23.7%) only posted in non-MH subreddits
13650 users (69.3%) posted both in MH and non-MH subreddits
At least 8 (4 for both MH and non-MH) post(s):
364 users (1.8%) only posted in MH subreddits
3650 users (18.5%) only posted in non-MH subreddits
10770 users (54.7%) posted both in MH and non-MH subreddits
````
## RQ2: What differences exist in the emotions that Reddit users with a BD diagnosis express in MH and non-MH subreddit posts?

```bash
python RQ2.py [demo]
```

### Expected output
````{verbatim}
Reading posts from data/posts_LIWC.csv
Read in 21407593 posts by 19685 users
Selected 9821 users (49.9%) with 6493626 posts (11.4% in MH subreddits) with at least 4 posts with at least 25 words in MH and non-MH subreddits
variable; mean MH posts; SD MH posts; mean non-MH posts; SD non-MH posts;p; p<0.001?; Cohen's d;Cohen's d interpretation
posemo;3.48;1.08;3.64;0.93;0.0000;True;-0.20;Small
anx;0.67;0.42;0.37;0.22;0.0000;True;0.97;Large
anger;0.75;0.49;0.78;0.44;0.0000;True;-0.07;No effect
sad;0.81;0.44;0.45;0.24;0.0000;True;1.11;Large
i;8.82;2.28;6.39;1.96;0.0000;True;1.63;Very large
````

## RQ3: How does trait mood differ between users who post in MH subreddits and those who only post in non-MH subreddits?

### Select users
```bash
python RQ3.py [demo]
```

This creates the files data/users_rq3.csv and data/users_rq3_gender_balanced.csv.
The gender-balanced users are selected based on user_ids_rq3_gender_balanced.csv to reproduce the results of the paper, as random variation in the subsampling of the users would yield slightly different results otherwise.

### Expected output
````{verbatim}
Reading posts from data/posts_LIWC.csv
Read in 21407593 posts by 19685 users
Selected 9821 users (49.9%) with 14642641 posts (7.7% in MH subreddits) with at least 4 posts with at least 25 words in MH and non-MH subreddits
0 posts in MH subreddits and at least 8 posts in non-MH subreddits: 3369
Selected 10158 users for RQ 3 (13190 before selecting only users with age+gender, 2312 posted only in non-MH subreddits)

avg_posting_age;29.22;9.31;29.47;9.82;2.2809;False;-0.03;No effect;independent t
gender;0.40;0.49;0.61;0.49;0.0000;True;-0.43;Small;independent t
active_days;1292.08;883.97;1130.44;889.61;0.0000;True;0.18;Very small;independent t
activity;1.44;2.52;1.85;4.79;0.0008;True;-0.16;Very small;Welchs-t
posemo;6.05;2.55;5.61;2.35;0.0000;True;0.17;Very small;Welchs-t
anx;0.33;0.21;0.30;0.16;0.0000;True;0.16;Very small;independent t
anger;1.00;0.60;1.09;0.62;0.0000;True;-0.15;Very small;independent t
sad;0.47;0.25;0.43;0.22;0.0000;True;0.14;Very small;Welchs-t
i;5.90;1.67;5.54;1.75;0.0000;True;0.21;Small;independent t
Outcome variable posted_MH by gender before gender balancing
posted_MH  gender
0          1.0       1416
           0.0        896
1          0.0       4696
           1.0       3150
Name: gender, dtype: int64
Outcome variable posted_MH by gender after gender balancing
posted_MH  gender
0          0.0        896
           1.0        896
1          0.0       3150
           1.0       3150
Name: gender, dtype: int64
````
### Logistic regression model + analyses:
```bash
RScript RQ3.R
```

### Expected output
The output of RQ3.R is provided in data/RQ3R_output.txt.
Note that this is the output obtained from running RQ3.R in the RStudio console.
Running RQ3.R from a bash terminal results in a more parsimonious output.
