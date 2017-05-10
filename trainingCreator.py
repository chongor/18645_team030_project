
# File to create training and test sets

import sys
import random
import datetime


#setup filenames by arguments
def setup():

    if len(sys.argv) < 2:
        sys.exit("No input data file given.")

    inFile = sys.argv[1]
    return inFile;


# write data to a file
# output format: user [\t] sub1,ascore1;sub2,ascore2; etc.
def writeUserPerRow(data, filename):
    with open(filename, 'w') as fout:
        for user in data:
            record = user + "\t"
            for sub in data[user]:
                record += sub + "," + data[user][sub] + ";"
            fout.write(record[:-1] + "\n")


# write data to a file
# output format: user,subreddit,ascore
def writeOneScorePerRow(data, filename):
    with open(filename, 'w') as fout:
        for user in data:
            for sub in data[user]:
                fout.write(user + "," + sub + "," + data[user][sub] + "\n")


# Takes in dictionary of all users with subreddits and ascores
# Splits the data randomly into a training and testing set
# 80% become training data and 20% become testing data
def splitData(data):
    test = dict()

    # for each user
    for user in data:
        #don't turn users who have only 1 subscription into test data
        if len(data[user]) == 1:
            continue
        else:
            # get list of the subs user has
            subs = list(data[user].keys())
            removed_subs = list()

            # we have to ensure that the user exists in both
            # training and testing data at least once

            # get 20% of the number of subs
            test_num = round(len(subs) * 0.2)
            # if less than 1, set to 1
            if test_num < 1:
                test_num = 1

            # get data into test set first
            for i in range(test_num):
                # get random sub from subs
                r = random.randint(0, len(subs)-1)
                sub = subs.pop(r)
                removed_subs.append(sub)

                if user in test:
                    test[user][sub] = data[user][sub]
                else:
                    test[user] = {sub: data[user][sub]}

            # for the remaining subs, remove it from the original data
            for sub in removed_subs:
                del data[user][sub]


    return [data, test]


# Takes in affinity score file
# Generates a dictionary with all data
def getData(inFile):
    d = dict()
    #read the affinity score data
    with open(inFile, "r") as fin:
        for line in fin:
            data = line.strip().split(",")
            user = data[0]
            sub = data[1]
            ascore = data[2]

            # if author exists
            if user in d:
                # if subreddit not subscribed yet
                if sub not in d[user]:
                    # insert new subscription
                    d[user][sub] = ascore
            # if author doesn't exist, create new author in dict
            # with subreddit and its ascore
            else:
                d[user] = {sub: ascore}

    return d

def main():
    print("Starting...")
    t = datetime.datetime.now().time()
    print(t)
    sys.stdout.flush()

    inFile = setup()
    data = getData(inFile)
    datasets = splitData(data)

    #writing training set in both formats
    writeOneScorePerRow(datasets[0], "affinity_training")
    writeUserPerRow(datasets[0], "user_training")

    #writing testing set in both formats
    writeOneScorePerRow(datasets[1], "affinity_testing")
    writeUserPerRow(datasets[1], "user_testing")


    print("Done!")
    t = datetime.datetime.now().time()
    print(t)
    sys.stdout.flush()

if __name__ == "__main__":
    main()
