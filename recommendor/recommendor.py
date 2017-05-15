
# Subreddit Recommendor
# Works based off

# our own libraries
# if using accuracy tester comment out line 7 and uncomment line 8
from . import util
#import util

# python libraries
import pymongo
import operator
import sys
import decimal


# Program input: program_name username k n
# k and n is optional and only applicable to program "two"
# program "one"  utilizes Distributed Cache Strategy
# program "two" utilizes All Pairs Strategy


# Get a user
def getUser(username, client):
    collection = client.reddit.users
    user = collection.find_one({"username": username})

    # Exit if user doesn't exist
    if user is None:
        sys.exit("User doesn't exist in database.")

    print("Found user: " + user["username"])
    return user

# Get a list of users
def getListOfUsers(username_list, client):
    collection = client.reddit.users
    users = collection.find({"username": {"$in": username_list}})
    return list(users)


# Get pairs with distance where either user of the pair
# is the given username, in sorted order (smallest to largest)
def getSortedPairs(username, k, client):
    collection = client.reddit.pairs
    pairs = collection.find({ "$or":[ {"username1": username}, {"username2": username} ]}).sort("distance", pymongo.ASCENDING).limit(k)
    return list(pairs)


# get the precomputed knn of given user
def getKNN_one(username, client):
    collection = client.reddit.kneighbors
    neighbors = collection.find_one({"username": username})
    print(neighbors)

    return neighbors


# get the k nearest neighbors
def getKNN_two(username, k, client):
    #get the nearest k pairs
    pairs = getSortedPairs(username, k, client)
    print("Found pairs: " + pairs[0]["username1"] + "\t" + pairs[0]["username2"])

    return pairs


# recommend sub based on neighbors given
# recommend n top subreddit recommendations
def weightedSum(userObj, user_list, client):
    other_subs = dict()

    # calculated weighted sums
    for neighbor in user_list:
        name = neighbor["username"]
        for i in range(len(neighbor["subreddits"])):
            sub = neighbor["subreddits"][i]
            if sub not in userObj["subreddits"]:
                if sub in other_subs:
                    other_subs[sub] += decimal.Decimal(neighbor["ascores"][i])
                else:
                    other_subs[sub] = decimal.Decimal(neighbor["ascores"][i])

    # sort other_subs in descending order
    other_subs = sorted(other_subs.items(), key=operator.itemgetter(1), reverse=True)

    # recommend top n subs
    return other_subs


# recommend sub based on the neighbors given
# recommend n top subreddit recommendations, n is default = 1
def recommend(userObj, neighbors, n, client):
    # based on the neighbors
    # get the weighted ascore sum of each subreddit
    # that is not in the list of subs that user has
    # and recommend the heaviest

    nearest_users = dict()
    other_subs = dict()
    neighbor_set = set()

    # get just a list of unique
    for neighbor in neighbors:
        if neighbor["username1"] == userObj["username"]:
            neighbor_set.add(neighbor["username2"])
        else:
            neighbor_set.add(neighbor["username1"])

    user_list = getListOfUsers(list(neighbor_set), client)
    print(len(user_list))

    # calculated weighted sums
    for neighbor in user_list:
        name = neighbor["username"]
        for i in range(len(neighbor["subreddits"])):
            sub = neighbor["subreddits"][i]
            if sub not in userObj["subreddits"]:
                if sub in other_subs:
                    other_subs[sub] += decimal.Decimal(neighbor["ascores"][i])
                else:
                    other_subs[sub] = decimal.Decimal(neighbor["ascores"][i])

    # sort other_subs in descending order
    other_subs = sorted(other_subs.items(), key=operator.itemgetter(1), reverse=True)

    # recommend top n subs
    return weightedSum(userObj, user_list, client)[:n]


# recommendation based on precomputed k nearest neighbors
def recommendorOne(client):

    print("Running Recommendor One")

    n = 1

    if len(sys.argv) < 3:
        sys.exit("No user given.")
    elif len(sys.argv) == 3:
        print("Using default n value, 1")
    elif len(sys.argv) == 4:
        n = int(sys.argv[3])
    else:
        print("Extra options given and will be ignored.")

    username = sys.argv[2]

    userObj = getUser(username, client)
    knn = getKNN_one(username, client)
    neighbors = getListOfUsers(knn["neighbors"], client)
    recommendations = weightedSum(userObj, neighbors, client)[:n]

    #print(recommendations)
    for sub in recommendations:
        print(sub[0])


# recommendation where all distances have been computed
# i.e. entire reddit neighborhood has been calculated
def recommendorTwo(client):

    print("Running Recommendor Two")

    k = 70
    n = 1

    if len(sys.argv) < 3:
        sys.exit("No user given.")
    elif len(sys.argv) == 3:
        print("Using default K value, 70")
        print("Using default n value, 1")
    elif len(sys.argv) == 4:
        k = sys.argv[3]
        print("Using default n value, 1")
    elif  len(sys.argv) == 5:
        k = sys.argv[3]
        n = sys.argv[4]
    else:
        print("Extra options given and will be ignored.")

    username = sys.argv[2]
    k = int(k)
    n = int(n)

    userObj = getUser(username, client)
    pairs = getKNN_two(username, k, client)
    recommendations = recommend(userObj, pairs, n, client)

    #print(recommendations)
    for sub in recommendations:
        print(sub[0])



def main():
    program_name = "Recommending..."
    util.start_time(program_name);

    if len(sys.argv) < 2:
        sys.exit("No program given")

    program = sys.argv[1]
    client = pymongo.MongoClient()

    if program == "one":
        recommendorOne(client)
    elif program == "two":
        recommendorTwo(client)

    util.end_time(program_name)

if __name__ == "__main__":
    main()
