import ast
file = open('subsetData.txt', 'r')
 
for rawLine in file:
	line = rawLine.split(',')
	username = line[0]
	openingIndex = rawLine.find('[');
	closingIndex = rawLine.find(']');

	listTuplesRaw = rawLine[openingIndex+1:closingIndex]	
	listTuples = listTuplesRaw.split(',')
	print listTuplesRaw
