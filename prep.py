
# Preprocess reddit comment data
# take in reddit comment jsons
# output a txt file with data

import sys
import json
import datetime
import operator

#INFO ABOUT rc_2015_01 (and all reddit comment data available):
# downs are all 0
# upvotes == scores
# upvotes/scores can be negative
# just aggregate score

#setup filenames by arguments
def setup():

    if len(sys.argv) < 2:
        sys.exit("No input data file given.")

    inFile = sys.argv[1]

    #check if output file has been entered
    if(len(sys.argv) == 3):
        outFile = sys.argv[2]
    else:
        outFile = "processsed_rc_data.txt"

    return [inFile, outFile];

#shorten data
def prep_data(inFile, outFile):

    #read data
    with open(inFile, 'r') as fin, open(outFile, 'w') as fout:
        for line in fin:
            #load json as a dictionary
            c = json.loads(line)
            author = c["author"]
            sub = c["subreddit"]
            score = c["score"]

            #ignore '[deleted]' users
            if(author == "[deleted]"):
                continue

            fout.write(author + "," + sub + "," + str(score))

# preprocess the data into a format for algorithm
def process_data(inFile, outFile):

    d = dict();

    #read data
    with open(inFile, 'r') as fin:
        for line in fin:
            #load json as a dictionary
            c = json.loads(line)
            author = c["author"]
            subreddit = c["subreddit"]

            #ignore '[deleted]' users
            if(author == "[deleted]"):
                continue

            #if author is in dictionary
            if(author in d):
                #if author already subscribed to this subreddit
                if(subreddit in d[author]):
                    #increase total number of ups, downs, score, and count
                    d[author][subreddit][0] += c["score"]
                    d[author][subreddit][1] += 1
                #else create new subreddit subscription
                else:
                    d[author][subreddit] = [c["score"], 1]
            #author doesn't exist, create new author in dict
            #with subreddit subscription
            else:
                d[author] = {subreddit: [c["score"], 1]}

    with open(outFile, 'w') as fout:
        for author in d:
            record = author + ";"

            for subreddit in d[author]:
                record += subreddit + ","

            record = record[:-1] + "\n"

            fout.write(record)

# STATS (doesn't calculate all of these)
# unique users
# unique subs
# number of users in a sub
# number of comments in a sub
def stats(inFile, outFile):
    #key: sub, value: set(users)
    #sub_users = dict();
    #key: sub, value: [comment count, score count]
    sub_stats = dict();

    print("begin stats")

    #read data
    with open(inFile, 'r') as fin:
        for line in fin:
            #load json as a dictionary
            c = json.loads(line)
            author = c["author"]
            sub = c["subreddit"]

            #ignore '[deleted]' users
            if author == "[deleted]":
                continue

            # ### SUB_STATS ###
            # #if subreddit exists as key in sub_comments
            # if(sub in sub_stats):
            #     #increment the comment count
            #     sub_stats[sub][0] += 1
            #     #increment the score count
            #     sub_stats[sub][1] += c["score"]
            # #else initialize subreddit comment count
            # else:
            #     sub_stats[sub] = [1, c["score"]]

            ### SUB_USER_BASE ###
            # if sub exists
            if sub in sub_stats:
                # if unique author hasn't been subscribed
                # subccribed the author
                if author not in sub_stats[sub]:
                    sub_stats[sub].add(author)
            #create new sub if it doesn't exist with the author
            else:
                sub_stats[sub] = set(author)

    #get dict key = sub, value = # of unique users
    sub_users = dict()
    for sub in sub_stats:
        if len(sub_stats[sub]) > 100:
            sub_users[sub] = len(sub_stats[sub])

    print("writing top subreddits")
    print(len(sub_users))
    sorted_subs = sorted(sub_users.items(), key=operator.itemgetter(1))
    sorted_subs = sorted_subs[::-1]
    print(len(sorted_subs))
    sys.stdout.flush()
    with open(outFile, 'w') as fout:
        #number of unique users per subreddit
        for sub in sorted_subs:
            record = sub[0] + "," + str(sub[1]) +"\n"
            fout.write(record)


def affinity_output(inFile, outFile):

        subs = dict();
        d = dict();

        #load sub data
        with open("1k_popular_subs.txt", 'r') as dat:
            for line in dat:
                l = line.split(',')
                sub = l[0]
                total_comments = l[1]

                #total comments for each sub
                subs[sub] = int(total_comments)

        #read raw
        with open(inFile, 'r') as fin:
            for line in fin:
                #load json as a dictionary
                c = json.loads(line)
                author = c["author"]
                subreddit = c["subreddit"]

                #ignore '[deleted]' users
                if(author == "[deleted]"):
                    continue

                #if author is in dictionary
                if(author in d):
                    #ignore subreddit if it's not in the top 1000
                    if subreddit in subs:
                        #if author already subscribed to this subreddit
                        if(subreddit in d[author]):
                            #increment number of comments in that sub
                            d[author][subreddit] += 1
                        #else create new subreddit subscription
                        else:
                            d[author][subreddit] = 1
                #author doesn't exist, create new author in dict
                #with subreddit subscription with count of 1
                else:
                    #only if the subreddit exists in top 1000
                    if subreddit in subs:
                        d[author] = {subreddit: 1}

        with open(outFile, 'w') as fout:
            for author in d:
                record = author + ";"
                for subreddit in d[author]:
                    # record = author + ","
                    #
                    # count = d[author][subreddit]
                    # total_comments = subs[subreddit]
                    #
                    # ascore = count / total_comments
                    #
                    # record += subreddit + "," + str(ascore) + "\n"
                    record += subreddit + ","
                record = record[:-1] + "\n"
                fout.write(record)


def start_time():
    t = datetime.datetime.now().time()
    print("job started: " + t.isoformat())

def end_time():
    print("job done")
    t = datetime.datetime.now().time()
    print("job took: " + t.isoformat())

def main():
    start_time()
    files = setup()
    #process_data(files[0], files[1])
    affinity_output(files[0], files[1])
    #stats(files[0], files[1])
    #prep_data(files[0], files[1])
    end_time()

if __name__ == "__main__":
    main()
