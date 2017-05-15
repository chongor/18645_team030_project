
# Takes hadoop output of reddit neighborhood
# i.e. distance between all users
# and inserts it into a mongodb instance

# our own library
# if using accuracy tester comment out line 8 and uncomment line 9
from . import util
#import util

#python libraries
from pymongo import *
import sys

# insert a new user into the db
# with a list of subreddits and list of ascores for each subreddit
def insertUser(username, subreddits, ascores, client):
    user = {
        "username": username,
        "subreddits": subreddits,
        "ascores": ascores
    }
    db = client.reddit
    collection = db.users
    user_id = collection.insert_one(user).inserted_id
    return user_id


# insert a new user pair with distance into the db
def insertPair(username1, username2, distance, client):
    pair = {
        "username1": username1,
        "username2": username2,
        "distance": distance
    }
    db = client.reddit
    collection = db.pairs
    pair_id = collection.insert_one(pair).inserted_id
    return pair_id


# insert a new username with k nearest neighbors
def insert_knn(username, neighbors, client):
    knn = {
        "username": username,
        "neighbors": neighbors
    }
    db = client.reddit
    collection = db.kneighbors
    knn_id = collection.insert_one(knn).inserted_id
    return knn_id


# Load the reddit users with affinity scores into mongoDb
def loadUsers(inFile, client):
    subs = dict()
    ascores = dict()
    # read data
    with open(inFile, 'r') as fin:
        for line in fin:
            data = line.strip().split(",")
            user = data[0]
            sub = data[1]
            ascore = data[2]

            if user in subs:
                subs[user].append(sub)
                ascores[user].append(ascore)
            else:
                subs[user] = [sub]
                ascores[user] = [ascore]

    # Now that we have a list of subreddits per user
    for user in subs:
        insertUser(user, subs[user], ascores[user], client)


# Load the reddit neighborhood data into mongoDb
def loadPairs(inFile, client):
    # read data
    with open(inFile, 'r') as fin:
        for line in fin:
            key_dist = line.strip().split("\t")
            key = key_dist[0].split(" ")
            dist = key_dist[1]

            insertPair(key[0], key[1], dist, client)


# load the knn data into mongoDB
def loadKnn(inFile, client):
    # read data
    with open(inFile, 'r') as fin:
        for line in fin:
            splitOne = line.split("\t")
            username = splitOne[0]
            neighbors = []

            splitTwo = splitOne[1].strip().split(";")
            for user in splitTwo[:-1]:
                neighbors.append(user.split(":")[0])

            insert_knn(username, neighbors, client)

# load files
def setup():
    if len(sys.argv) < 2:
        sys.exit("No input file given.")
    elif len(sys.argv) < 3:
        sys.exit("No mode number given. 0 or 1")

    return sys.argv[1]


def main():
    program = "Inserting data into mongo"
    util.start_time(program)
    sys.stdout.flush()

    inFile = setup()
    mode = sys.argv[2]

    client = MongoClient()

    if(mode == "user"):
        loadUsers(inFile, client)
        print("loaded users")
    elif(mode == "neighborhood"):
        loadPairs(inFile, client)
        print("loaded user pairs")
    elif(mode == "knn"):
        loadKnn(inFile, client)
        print("loaded k neighbors")
    else:
        print("no known mode specified")

    util.end_time()

if __name__ == "__main__":
    main()
