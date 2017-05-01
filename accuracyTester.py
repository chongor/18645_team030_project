
# Test framework to test recommendation engines

import sys

# Input format is follows:
# python accuracyTester [number] [input filename] [output filename]
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

def logicxCode(files):
    return None

def aliCode(files):
    return None

def darrenCode(files):
    return None

def main():
    # files = [infile, outfile]
    # infile => input filename
    # outfile => output filename
    files = setup()

    program = sys.argv[1];

    #run the test on a specific program
    if(program == 0):
        logicxCode(files)
    #run the test on a different program
    elif(program == 1):
        aliCode(files)
    elif(program == 2):
        darrenCode(files)


if __name__ == "__main__":
    main()
