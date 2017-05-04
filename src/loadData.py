from collections import defaultdict

file = open('../../rc_by_users.txt', 'r')
lines = file.readlines()
last = lines[-1];
subDict = defaultdict(list)
listUsers = [];
allSubreddits = set();


for rawLine in lines:
	line = rawLine.split(';')
	username = line[0]
	listUsers.append(username)
	subredditsIndex = rawLine.find(';')
	#remove new line \r\n
	if(rawLine is not last):
		lastIndex = len(rawLine)-2		
	else:
		lastIndex = len(rawLine)
	
	listSubredditsRaw = rawLine[subredditsIndex+1:lastIndex]
	listSubreddits = listSubredditsRaw.split(',')

	for subreddit in listSubreddits:
		subDict[username].append(subreddit)
		allSubreddits.add(subreddit)