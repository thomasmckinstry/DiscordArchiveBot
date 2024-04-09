class setup:
    """
    Read dates out of a text file and map them to a key/value pair in a dictionary.
    """
    def readDates():
        datesDict = {}
        with open ("backupRecords.csv",  "r") as input_file:
            channelDates = input_file.split("\n")
            for channelPair in channelDates:
                splitPair = channelPair.split(",")
                datesDict[splitPair[0]] = splitPair[1]
        return datesDict

    """
    Write the current date to the text file with matching channel id.
    """
    def writeDates():
        return