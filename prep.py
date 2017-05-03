
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
    program_name = "prepData";
    start_time(program_name);

    #read data
    with open(inFile, 'r') as fin, open(outFile, 'w') as fout:
        for line in fin:
            #load json as a dictionary
            c = json.loads(line)
            author = c["author"]
            sub = c["subreddit"]

            #ignore '[deleted]' users
            if(author == "[deleted]"):
                continue

            fout.write(author + "," + sub)

    end_time(program_name)


# preprocess the data into a format for algorithm
def get_raw_data(inFile, outFile):

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


# number of comments in a sub
def get_sub_counts(inFile, outFile):
    program_name = "getSubCounts";
    start_time(program_name);

    #key: sub, value: set(users)
    #sub_users = dict();
    #key: sub, value: comment count
    sub_stats = dict();

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
            #if subreddit exists as key in sub_comments
            if(sub in sub_stats):
                #increment the comment count
                sub_stats[sub] += 1
            #else initialize subreddit comment count
            else:
                sub_stats[sub] = 1

            ### SUB_USER_BASE ###
            # # if sub exists
            # if sub in sub_stats:
            #     # if unique author hasn't been subscribed
            #     # subscribed the author
            #     if author not in sub_stats[sub]:
            #         sub_stats[sub].add(author)
            # #create new sub if it doesn't exist with the author
            # else:
            #     sub_stats[sub] = set(author)

    #get dict key = sub, value = # of total comments
    # for sub in sub_stats:
    #     if len(sub_stats[sub]) > 100:
    #         sub_users[sub] = len(sub_stats[sub])

    #sort the subs
    # sorted_subs = sorted(sub_stats.items(), key=operator.itemgetter(1))
    # sorted_subs = sorted_subs[::-1]

    with open(outFile, 'w') as fout:
        #sub and total comments in sub
        for sub in sub_stats:
            record = sub + "," + str(sub_stats[sub]) +"\n"
            fout.write(record)

    end_time(program_name)


def get_affinity_scores(inFile, outFile, subFile):

    program_name = "getAffinityScores";
    start_time(program_name);

    subs = dict();
    d = dict();

    #load sub data
    with open(subFile, 'r') as dat:
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
                if subreddit in subs:
                    d[author] = {subreddit: 1}

    with open(outFile, 'w') as fout:
        for author in d:
            record = author + ";"
            for subreddit in d[author]:
                record = author + ","

                count = d[author][subreddit]
                total_comments = subs[subreddit]

                ascore = count / total_comments

                record += subreddit + "," + str(ascore) + "\n"

            fout.write(record)

    end_time(program_name);

def start_time(name):
    t = datetime.datetime.now().time()
    print(name + " started: " + t.isoformat())

def end_time(name):
    print(name + " done")
    t = datetime.datetime.now().time()
    print(name + " took: " + t.isoformat())

def main():
    start_time("prep.py")
    sys.stdout.flush()

    files = setup()

    get_sub_counts(files[0], "sub_counts");
    sys.stdout.flush()
    
    get_affinity_scores(files[0], files[1], "sub_counts");
    sys.stdout.flush()

    end_time("prep.py")

if __name__ == "__main__":
    main()
