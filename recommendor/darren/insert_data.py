
# Takes hadoop output of reddit neighborhood
# i.e. distance between all users
# and inserts it into a mongodb instance

import sys
import util
from pymongo import*

# insert a new user into the db
# with a list of subreddits and list of ascores for each subreddit
def insertUser(username, subreddits, ascores, client):
    user = {
        "username": username,
        "subreddits": subreddits
        "ascores": ascores
    }
    db = client.reddit
    collection = db.users
    user_id = collection.insert_one(user).inserted_id
    return user_id


# insert a new user pair with distance into the db
def insertPairs(username1, username2, distance, client):
    pair = {
        "username1": username1,
        "username2": username2,
        "distance": distance
    }
    db = client.reddit
    collection = db.pairs
    pair_id = collection.insert_one(pair).inserted_id
    return pair_id


# Get a user
def getUser(username, client):
    collection = client.reddit.users
    user = collection.find_one({"username": username})
    return user


# Get pairs with distance where either user of the pair
# is the given username, in sorted order (smallest to largest)
def getSortedPairs(username, k, client):
    collection = client.reddit.pairs
    pairs = collection.find_one({ "$or":[ {"username1": username}, {"username2": username} ]}).sort("distance", pymongo.ASCENDING).limit(k)
    return pairs


# Load the reddit users into mongoDb
def loadUsers(inFile, client):
    subs = dict()
    ascores = dict()
    # read data
    with open(inFile, 'r') as fin:
        for line in fin:
            data = line.split(",")
            user = data[0]
            sub = data[1]
            ascore = data[2]

            if(user in d):
                subs[author].append(sub)
                ascores[author].append(ascore)
            else:
                subs[author] = list(sub)
                ascores[author] = list(ascore)

    # Now that we have a list of subreddits per user
    for user in d:
        insertUser(user, subs[user], ascores[user], client)


# Load the reddit neighborhood data into mongoDb
def loadPairs(inFile, client):
    # read data
    with open(inFile, 'r') as fin:
        for line in fin:
            key_dist = line.split("\t")
            key = key_dist[0].split(" ")
            dist = key_dist[1]

            insertPair(key[0], key[1], dist, client)


# load files
def setup():
    if len(sys.argv) < 2:
        sys.exit("No input file given.")
    elif len(sys.argv) < 3:
        sys.exit("No mode number given. 0 or 1")

    return sys.argv[1]


def main():
    program = "Inserting data into mongo"
    util.start_time(program);

    inFile = setup()
    mode = argv[2]

    client = MongoClient()

    if(mode == 0):
        loadUsers(inFile, client)
        print("loaded users")
    elif(mode == 1):
        loadPairs(inFile, client)
        print("loaded user pairs")

    util.end_time(program)

if __name__ == "__main__":
    main()
