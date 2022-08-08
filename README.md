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
R 4.1.0


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
><br>

## RQ3: How does trait mood differ between users who post in MH subreddits and those who only post in non-MH subreddits?

### Select users:
python RQ3.py [demo]

### Logistic regression model + analyses:
Rscript RQ3.R

### Expected output
><br>
