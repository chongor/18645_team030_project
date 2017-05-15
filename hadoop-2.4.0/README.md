# 18645_team030_project
Reddit subreddit recommendation for 18-645 Fastcode project.

This folder contains the implementation for using Distributed Cache
To run, build using ant.
Run jar file, give following command line inputs:

program : subreddits
input : specify test data file
input2 : specift training data file
output : specify output file
tmpdir : tmp directory

sample command:
hadoop jar 18645-proj3-0.1-latest.jar -program subreddits -input user_testing1m_1K -input2 user_training_100k -output data/subreddits -tmpdir tmp
