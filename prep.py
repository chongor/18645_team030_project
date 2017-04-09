
# Preprocess reddit comment data
# take in reddit comment jsons
# output a txt file with data

import sys
import json

def main():
    inFile = sys.argv[1]

    print(sys.argv)
    #check if output file has been entered
    if(len(sys.argv) == 3):
        outFile = sys.argv[2]
    else:
        outFile = "reddit_comments.txt"

    d = dict()

    #read data
    with open(inFile, 'r') as fin:
        for line in fin:
            print("...")
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
                    d[author][subreddit][0] += c["ups"]
                    d[author][subreddit][1] += c["downs"]
                    d[author][subreddit][2] += c["score"]
                    d[author][subreddit][3] += 1
                #else create new subreddit subscription
                else:
                    d[author][subreddit] = [c["ups"], c["downs"], c["score"], 1]
            #author doesn't exist, create new author in dict
            #with subreddit subscription
            else:
                d[author] = {subreddit: [c["ups"], c["downs"], c["score"], 1]}

    with open(outFile, 'w') as fout:
        for author in d:
            record = author + "," + "["

            for subreddit in d[author]:
                ups = d[author][subreddit][0]
                downs = d[author][subreddit][1]
                score = d[author][subreddit][2]
                count = d[author][subreddit][3]

                record += "(" + subreddit + "," + str(ups) + "," + str(downs) + "," + str(score) + "," + str(count) + "),"

            record = record[:-1] + "]\n"

            fout.write(record)


if __name__ == "__main__":
    main()
