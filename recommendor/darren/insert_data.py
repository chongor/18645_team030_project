
# Takes hadoop output of reddit neighborhood
# i.e. distance between all users
# and inserts it into a mongodb instance

import sys
import util
from pymongo import*

# insert a new user into the db
def insertUser(username, subreddits, client):
    user = {
        "username": username,
        "subreddits": subreddits
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
# is the given username
def getPairs(username, client):
    collection = client.reddit.pairs
    pairs = collection.find_one({ "$or":[ {"username1": username}, {"username2": username} ]})
    return pairs


# Load the reddit users into mongoDb
def loadUsers(inFile):
    d = dict()
    # read data
    with open(inFile, 'r') as fin:
        for line in fin:
            data = line.split(",")
            user = data[0]
            sub = data[1]

            if(user in d):
                d[author].append(sub)
            else:
                d[author] = list(sub)

    # Now that we have a list of subreddits per user
    for user in d:
        insertUser(user, d[user])


# Load the reddit neighborhood data into mongoDb
def loadPairs(inFile):
    # read data
    with open(inFile, 'r') as fin:
        for line in fin:
            key_dist = line.split("\t")
            key = key_dist[0].split(" ")
            dist = key_dist[1]

            insertPair(key[0], key[1], dist)


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

    if(mode == 0):
        loadUsers()
        print("loaded users")
    elif(mode == 1):
        loadPairs()
        print("loaded user pairs")

    util.end_time(program)

if __name__ == "__main__":
    main()
