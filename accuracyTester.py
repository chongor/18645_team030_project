
# Test framework to test recommendation engines

import sys

# load our own code and logix's
from src import *
from recommendor import *

# Input format is follows:
# python accuracyTester [number] [input filename]
# output filename is optional

# Take in a test file to run on a recommendation engine
def setup():
    # check if input file was entered
    if len(sys.argv) < 3:
        sys.exit("No input data file given.")

    inFile = sys.argv[2]

    # check if output file was specified
    if(len(sys.argv) == 4):
        outFile = sys.argv[3]
    else:
        outFile = "accuracyReport.txt"

    return [inFile, outFile]


def logixCode(inputFile):
    program_name = "logix"
    util.start_time(program_name)

    total = 0
    success = 0

    with open(inFile, 'r') as fin:
        for line in fin:



    util.end_time(program_name)


def aliCode(inputFile):
    program_name = "ali's implementation"
    util.start_time(program_name)



    util.end_time(program_name)


def darrenCode(inputFile):
    program_name = "darren's implementation"
    util.start_time(program_name)



    util.end_time(program_name)


def main():
    # files = [infile, outfile]
    # infile => input filename
    # outfile => output filename
    inputFile = setup()

    program = sys.argv[1];

    #run the test on a specific program
    if(program == 0):
        logixCode(files)
    elif(program == 1):
        aliCode(files)
    elif(program == 2):
        darrenCode(files)
    #or run on all
    elif(program == 4):
        logixCode("user_testing_1k")
        aliCode("user_testing_1k")
        darrenCode("affinity_testing_1m")
    else:
        print("No program specified")


if __name__ == "__main__":
    main()
