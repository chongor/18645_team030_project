#! /usr/bin/env python

import math
from .loadData import subDict, listUsers, allSubreddits
# import dataset
import datetime
import operator
import sys
import numpy as np

listAllSubreddits = list(allSubreddits)

def createUserVector(username):
	# client = MongoClient()
	# user = queryUser(username, client)
	client = username
	#unique_subs = list(subreddits(client))
	unique_subs = listAllSubreddits
	vector = [0]*len(unique_subs)
	for i in range(len(unique_subs)):
		if unique_subs[i] in subDict[username]:
			vector[i] = 10
	return vector

def vectorDistance(user1, user2):
	vector1 = createUserVector(user1)
	vector2 = createUserVector(user2)
	# dist = 0
	# for i in range(len(vector1)):
	# 	dist += pow(vector1[i] - vector2[i], 2)
	# return math.sqrt(dist)
	return np.linalg.norm(np.array(vector1) - np.array(vector2))

def getNeighbors(username, k):
	#client = MongoClient()
	distances = []
	for user in listUsers:
		dist = vectorDistance(username, user)
		distances.append((user, dist))
		#dist = vectorDistance(username, user['username'])
		#distances.append((user['username'], dist))
	distances.sort(key=operator.itemgetter(1))
	return distances[:k]

def getRecommendedSubreddit(username):
	#client = MongoClient()
	neighbors = getNeighbors(username, 70)
	#users = allUsersInArray([neighbor[0] for neighbor in neighbors], client)
	users = []
	for neighbor in neighbors:
		users.append(neighbor[0])
	#banned = queryUser(username, client)['subreddits']
	banned = subDict[username]
	subredditFrequency = {}
	#totalsubs = [sub for user in users for sub in user['subreddits']]
	totalsubs = [sub for user in users for sub in subDict[user]]
	subredditFrequency = {word : totalsubs.count(word) for word in set(totalsubs) if word not in banned}

	#return max(subredditFrequency, key=subredditFrequency.get)
	return sorted(subredditFrequency, key=subredditFrequency.get)


def main(username, n):
	# dataset.getComments(username)
	#return getRecommendedSubreddit(username)
	subreddit = getRecommendedSubreddit(username)
	return subreddit[:n]


if __name__ == "__main__":
	username = sys.argv[1]
	n = sys.argv[2]

	t = datetime.datetime.now().time()
	print("Start: " + t.isoformat())
	sys.stdout.flush()

	print(main(username, n))

	t = datetime.datetime.now().time()
	print("Finished: " + t.isoformat())
