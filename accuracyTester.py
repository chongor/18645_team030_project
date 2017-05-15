
# Test framework to test recommendation engines

# python libraries
import sys
import decimal

# load our own code and logix's sequential
from src import kNN, loadData
from recommendor import insert_data, recommendor, util

# Input format is follows:
# python accuracyTester [input filename] [program number]

# Take in a test file to run on a recommendation engine
def setup():
    # check if input file was entered
    if len(sys.argv) < 2:
        sys.exit("No input data file given.")

    inFile = sys.argv[1]

    # check if a mode was specified
    if(len(sys.argv) < 3):
        sys.exit("No mode specified.")

    return inFile


def sequential(inFile):
    program_name = "sequential"
    util.start_time(program_name)
    sys.stdout.flush()

    total = 0
    success = 0

    # open file
    with open(inFile, 'r') as fin:
        # read in a test user
        for line in fin:
            data = line.split("\t")

            subs = set()

            # get the test subs for this user
            for pair in data[1].strip().split(";"):
                subs.add(pair.split(",")[0])

            # get an extra 5 subs to recommend
            recommendations = kNN.main(data[0],len(subs)+5)

            # check and see if test sub is in the list of recommended subs
            for sub in subs:
                total += 1
                if sub in recommendations:
                    success += 1

    accuracy = decimal.Decimal(success/total)
    print("Sequential accuracy: " + str(accuracy))
    print("Sequential total: " + str(total))

    util.end_time(program_name)


def DC(inFile):
    program_name = "Distributed Cache implementation"
    util.start_time(program_name)
    sys.stdout.flush()

    total = 0
    success = 0

    # open file
    with open(inFile, 'r') as fin:
        # read in a test user
        for line in fin:
            data = line.split(",")

            subs = set()

            # get the test subs for this user
            for pair in data[1].strip().split(";"):
                subs.add(pair.split(",")[0])

            # get an extra 5 subs to recommend
            recommendations = kNN.main(data[0],len(subs)+5)

            # check and see if test sub is in the list of recommended subs
            for sub in subs:
                total += 1
                if sub in recommendations:
                    success += 1

    accuracy = decimal.Decimal(success/total)
    print("Distributed Cache accuracy: " + str(accuracy))
    print("Distributed Cache total: " + str(total))

    util.end_time(program_name)


def allPairs(inFile):
    program_name = "All Pairs implementation"
    util.start_time(program_name)
    sys.stdout.flush()

    total = 0
    success = 0

    # open file
    with open(inFile, 'r') as fin:
        for line in fin:
            data = line.strip().slit(",")

            #need to rewrite
            recommendations = recommendor.main()

            if data[1] in recommendations:
                success += 1
            total += 1

    accuracy = decimal.Decimal(success/total)
    print("All Pairs accuracy: " + str(accuracy))
    print("All Pairs total: " + str(total))

    util.end_time(program_name)


def main():
    # infile => input filename
    inFile = setup()

    program = int(sys.argv[2]);

    #run the test on a specific program
    if(program == 0):
        sequential(inFile)
    elif(program == 1):
        DC(inFile)
    elif(program == 2):
        allPairs(inFile)
    #or run on all
    elif(program == 4):
        sequential("user_testing_1k")
        DC("user_testing_1k")
        allPairs("affinity_testing_1k")
    else:
        print("No program specified")


if __name__ == "__main__":
    main()
