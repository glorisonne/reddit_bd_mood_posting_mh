# Code accompanying the paper "An exploratory analysis of posting patterns in peer online support forums and their associations with emotions and mood in bipolar disorder" 

This repository contains the code to reproduce all results from the paper Jagfeld, G., Lobban, F., Davies, R., Boyd, R. L., Rayson, P., & Jones, S. H. (submitted for publication) An exploratory analysis of posting patterns in peer online support forums and their associations with emotions and mood in bipolar disorder.

The data provided in the data/ directory is only made-up example data to show the structure of the data and test the code release. To obtain the actual data, please contact Glorianna Jagfeld <g.jagfeld@lancaster.ac.uk> or Professor Steven Jones <s.jones7@lancaster.ac.uk>. You will be provided with a Data Usage Agreement outlining ethical terms of use for the data that you need to sign before getting access to the data. Please note, that access to the data will only be granted for non-commercial research purposes.

By default, the repository expects that the actual data is stored in the data/ subdirectory in the files posts.csv, users.csv, and posts_LIWC.csv.
To run the code on the provided example data, use the optional demo flag for each of the scripts.

For portability reasons, the dataset is provided in .csv format. However, reading the csv file of 21M posts can take up to 30 minutes. To speed this up, the data could be pickled and read from the .pkl instead of .csv file:

posts = pd.read_csv(c.data + "posts.csv")
posts.to_pickle(c.data + "posts.pkl")
posts = pd.read_pickle(c.data + "posts.pkl")

## Requirements
python 3.9.5, pandas 1.3.0, numpy 1.20.3
R 4.1.0, car 3.0 (including carData 3.0), languageR 1.5.0, caret 6.0 (including ggplot2 3.3.5, lattice 0.2.0), ROCR 1.0

## Subreddit topics
The file data/subreddit_topics.csv contains the categorisation of 30,867 subreddits that was created in this project based on snoopsnoo*s subreddit categorisation (https://github.com/orionmelt/sherlock/blob/master/subreddits.csv)

The 158 MH subreddits are identified by the category label "Mental Health" assigned in the column "third level".
Among these, the 37 BD subreddits are identified by the category label "bipolar" assigned in the column "fourth level".

## RQ1: What proportion of Reddit users with a BD diagnosis posts in MH and non-MH subreddits?

  python RQ1.py [demo]

### Expected output

> At least 1 (1 for both MH and non-MH) post(s):<br>
1369 users (7.0%) only posted in MH subreddits<br>
4666 users (23.7%) only posted in non-MH subreddits<br>
13650 users (69.3%) posted both in MH and non-MH subreddits<br>
At least 8 (4 for both MH and non-MH) post(s):<br>
364 users (1.8%) only posted in MH subreddits<br>
3650 users (18.5%) only posted in non-MH subreddits<br>
10770 users (54.7%) posted both in MH and non-MH subreddits

## RQ2: What differences exist in the emotions that Reddit users with a BD diagnosis express in MH and non-MH subreddit posts?

<python>
  python RQ2.py [demo]
</python>

### Expected output
>Reading posts from data/posts_LIWC.csv<br>
Read in 21407593 posts by 19685 users<br>
Selected 9821 users (49.9%) with 6493626 posts (11.4% in MH subreddits) with at least 4 posts with at least 25 words in MH and non-MH subreddits<br>
variable; mean MH posts; SD MH posts; mean non-MH posts; SD non-MH posts;p; p<0.001?; Cohen's d;Cohen's d interpretation<br>
posemo;3.48;1.08;3.64;0.93;0.0000;True;-0.20;Small<br>
anx;0.67;0.42;0.37;0.22;0.0000;True;0.97;Large<br>
anger;0.75;0.49;0.78;0.44;0.0000;True;-0.07;No effect<br>
sad;0.81;0.44;0.45;0.24;0.0000;True;1.11;Large<br>
i;8.82;2.28;6.39;1.96;0.0000;True;1.63;Very large<br>


## RQ3: How does trait mood differ between users who post in MH subreddits and those who only post in non-MH subreddits?

### Select users
python RQ3.py [demo]

This creates the files data/users_rq3.csv and data/users_rq3_gender_balanced.csv.
The gender-balanced users are selected based on user_ids_rq3_gender_balanced.csv to reproduce the results of the paper, as random variation in the subsampling of the users would yield slightly different results otherwise.

### Expected output

>Reading posts from data/posts_LIWC.csv<br>
Read in 21407593 posts by 19685 users<br>
Selected 9821 users (54.2%) with 6493626 posts (11.4% in MH subreddits) with at least 4 posts with at least 25 words in MH and non-MH subreddits<br>
0 posts in MH subreddits and at least 4 posts in non-MH subreddits: 3650<br>
Selected 10202 users for RQ 3 (13471 before selecting only users with age+gender<br>
2356 posted only in non-MH subreddits)<br>
avg_posting_age;29.22;9.31;29.41;9.80;3.5170;False;-0.02;No effect;independent t<br>
gender;0.40;0.49;0.61;0.49;0.0000;True;-0.43;Small;independent t<br>
active_days;1292.08;883.97;1114.15;890.21;0.0000;True;0.20;Small;independent t<br>
activity;1.44;2.52;1.84;4.76;0.0010;True;-0.16;Very small;Welchs-t<br>
posemo;3.63;0.88;5.62;2.40;0.0000;True;-2.26;Huge;Welchs-t<br>
anx;0.36;0.19;0.30;0.18;0.0000;True;0.35;Small;Welchs-t<br>
anger;0.79;0.41;1.09;0.63;0.0000;True;-0.74;Medium;Welchs-t<br>
sad;0.44;0.21;0.44;0.24;4.9625;False;0.01;No effect;independent t<br>
i;6.35;1.86;5.57;1.81;0.0000;True;0.42;Small;independent t<br>
Outcome variable posted_MH by gender before gender balancing<br>
posted_MH  gender<br>
0          1.0       1446<br>
           0.0        910<br>
1          0.0       4696<br>
           1.0       3150<br>
Name: gender, dtype: int64<br>
Outcome variable posted_MH by gender after gender balancing<br>
posted_MH  gender<br>
0          0.0        910<br>
           1.0        910<br>
1          0.0       3150<br>
           1.0       3150<br>
Name: gender, dtype: int64

### Logistic regression model + analyses:
<R>
	RScript RQ3.R
</R>

### Expected output
The output of RQ3.R is provided in data/RQ3R_output.txt.
Note that this is the output obtained from running RQ3.R in the RStudio console.
Running RQ3.R from a bash terminal results in a more parsimonious output.
