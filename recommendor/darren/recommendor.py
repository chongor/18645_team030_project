
# Subreddit Recommendor
# Works based off

import insert_data as mongo
import util
import sys


# get user to recommend subreddit for
def setup():
    k = 70
    n = 1

    if len(sys.argv) < 2:
        sys.exit("No user given.")
    elif len(sys.argv) == 2:
        print("Using default K value, 70")
        print("Using default n value, 1")
    elif len(sys.argv) == 3:
        k = sys.argv[2]
        print("Using default n value, 1")
    elif  len(sys.argv) == 3:
        k = sys.argv[2]
        n = sys.argv[3]
    else:
        print("Extra options given and will be ignored.")

    return [sys.argv[1], k, n]


# check if the user exists
def getUser(username, client):
    user = mongo.getUser(username, client)
    print("Found user: " user)

    if user is None:
        sys.exit("User doesn't exist in database.")

    return user


# get the k nearest neighbors
def getKNN(username, k, client):
    #get the nearest k pairs
    pairs = mongo.getSortedPairs(username, k, client)
    print("Found pairs: " pairs)

    return pairs


# recommend sub based on the
# recommend n top subreddit recommendations, n is default = 1
def recommend(subs, neighbors, n):
    # based on the neighbors
    # get the weighted ascore sum of each subreddit
    # that is not in the list of subs that user has
    # and recommend the heaviest

    # ===== PSUEDO CODE ======
    # get nearest user data
    # weighted_sums = dict()
    # for each user data
    #   for each subreddit in their data
    #       if subreddit not in subs
    #           if subreddit in weighted_sums:
    #               weighted_sums[subreddit] += user's ascore
    #           else:
    #               weighted_sums[subreddit] = user's ascore
    #
    # sort weighted sums and return top n subreddits with greatest weighted sum



def main():
    program = "Inserting data into mongo"
    util.start_time(program);

    inputs = setup()
    username = inputs[0]
    k = inputs[1]
    n = inputs[2]

    client = MongoClient()

    user = getUser(username)
    neighbors = getKNN(username, k)
    recommend(user.subreddits, neighbors, n)

    util.end_time(program)

if __name__ == "__main__":
    main()
