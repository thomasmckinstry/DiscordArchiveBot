class setup:
    """
    Read dates out of a text file and map them to a key/value pair in a dictionary.
    """
    def readDates(self):
        datesDict = {}
        try:
            with open ("backupRecords.csv",  "r") as input_file:
                channelDates = input_file.read().split("\n")
                for channelPair in channelDates:
                    splitPair = channelPair.split(",")
                    datesDict[splitPair[0]] = splitPair[1]
        except:
            print("Error: No Backup File Given")
        return datesDict

    """
    Write the current date to the text file with matching channel id.
    """
    def writeDates(self, datesDict):
        print(datesDict)
        with open ("backupRecords.csv", "w") as write_file:
            for key in datesDict.keys():
                write_file.write(key + ", " + str(datesDict[key]) + "\n")
        return