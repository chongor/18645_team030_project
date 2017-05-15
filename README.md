# 18645_team030_project
Reddit subreddit recommendation for 18-645 Fastcode project.

## Code Structure
- hadoop-2.4.0: contains distributed cache implementation of distributed kNN model training
- hadoop-2.7.3: contains all pairs implementation of distributed kNN model training
- original-src: contains the original source code, unmodified
- src: contains the modified source code for logix as our sequential code base
- accuracyTester.py: program for testing accuracy of the three kNN implementations
- prep.py: program for sequentially preprocessing raw reddit data
- trainingCreator.py: program to split preprocessed data into training and test sets
