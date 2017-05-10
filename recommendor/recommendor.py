
# Subreddit Recommendor
# Works based off

# our own libraries
import util

# python libraries
import pymongo
import operator
import sys
import decimal


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
    elif  len(sys.argv) == 4:
        k = sys.argv[2]
        n = sys.argv[3]
    else:
        print("Extra options given and will be ignored.")

    return [sys.argv[1], int(k), int(n)]


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


# get the k nearest neighbors
def getKNN(username, k, client):
    #get the nearest k pairs
    pairs = getSortedPairs(username, k, client)
    print("Found pairs: " + pairs[0]["username1"] + "\t" + pairs[0]["username2"])

    return pairs


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
    return other_subs[:n]


def main():
    program = "Recommending..."
    util.start_time(program);

    inputs = setup()
    username = inputs[0]
    k = inputs[1]
    n = inputs[2]

    client = pymongo.MongoClient()

    user = getUser(username, client)
    neighbors = getKNN(username, k, client)
    recommendations = recommend(user, neighbors, n, client)

    for sub in recommendations:
        print(sub[0])

    util.end_time(program)

if __name__ == "__main__":
    main()
