from tkinter import *

attrArr = ['date_posted', 'date_edited', 'author', 'contents', 'images', 'videos', 'reactions', 'jump_url', 'replies', 'id', 'thread_id']

"""
Maintains an array of all messages from a channel, gets returned by pullRecords()
"""
class Channel:
    head = None
    tail = None
    messageArr = []

    def __init__(self, messageArr):
        self.messageArr = messageArr

    def toString(self):
        printMessageArr = []

        for message in self.messageArr:
            printMessageArr.append(message.toString())

        return "\n".join(printMessageArr)

"""
Takes all elements of a message, see attrArr at top of code.
"""
class Message:
    global attrArr
    prev = None
    next = None
    reply = None
    thread = None

    def __init__(self, attrs):
        for attr, val in zip(attrArr, attrs):
            setattr(self, attr, val)

    def toString(self):
        propertyArr = []
        for attr in attrArr:
            propertyArr.append(getattr(self, attr))
        return ",".join(propertyArr)

"""
Reads messages out of the .csv file for the correct channel, makes an array 
of Message objects and returns a Channel object out of the array.
"""
def pullRecords(channel):
    head = None
    tail = None
    messageArr = []

    with open(channel + "/" + channel + "_messages.csv", 'r', encoding="utf-8") as f:
        messageStr = f.read()
        lpointer = 0
        rpointer = 0

        while len(messageStr) > 5:
            currentMessageArr = []
            for i in range(11):
                lpointer = 0
                rpointer = messageStr.find("\\null")
                currentMessageArr.append(messageStr[lpointer:rpointer])
                lpointer = rpointer + 6
                messageStr = messageStr[lpointer:len(messageStr)]
            currentMessage = Message(currentMessageArr)
            messageArr.append(currentMessage)
            if not head:
                head = currentMessage

        tail = currentMessage
        
        currChannel = Channel(messageArr)
        currChannel.head = head
        currChannel.tail = tail

        return currChannel

"""
Currently non-functional
"""
def displayArchive():
    master = Tk()
    Label(master, text='Channel').grid(row=0)
    c1 = Entry(master)
    c1.grid(row=0, column=1)
    mainloop()

#Demo
testmessages = pullRecords("testmessages")  
print(testmessages.toString())