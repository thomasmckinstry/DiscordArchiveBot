from ast import arg
import records
import discord
import requests
import urllib.request
import datetime
import os

from discord.ext import commands

#Setup
setup = records.setup()

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
imageArr = [".jpg", ".jpeg", ".png", ".webp"]
#soundArr = [".wav", ".mp3", ".ogg"]
videoArr = [".webm", ".mp4", ".mov"]

image = 0
video = 0
sound = 0

count = 0
failedImage = 0
failedVideo = 0

failedImages = ""
failedVideos = ""

imageList = []
videoList = []

datesDict = setup.readDates()

#Creates starter directories and confirms bot launch
@bot.event
async def on_ready():
    print("bot is online")

#Archive files out of the channel the command was sent in.
@bot.command()
async def archiveDocs(ctx, *args):
    channel = ctx.channel.name
    parsedArgs = parseArgs(args, datesDict, channel)
    #print(parsedArgs)
    datesDict[channel] = parsedArgs["E"]
    set_directories(channel, channel + "/Images", channel + "/Videos")
    with open(channel + "messages.csv", 'a') as f:
        f.write("")  
    

    global image
    global video
    global count
    global failedImage
    global failedVideo

    global imageList
    global videoList

    failedImages = ""
    failedVideos = ""

    #Loops through each message sent in the channel
    #print(parsedArgs)
    async for message in ctx.channel.history(limit=None, before=parsedArgs["E"], after=parsedArgs["S"], around=None, oldest_first=True):
        imageList = []
        videoList = []
        #print(message.attachments, message.embeds)
        count += 1

        #Loop through and save attachments
        if len(message.attachments) > 0:
            #print("Found attachments")
            await getAttachments(message, channel, parsedArgs)

        if len(message.embeds) > 0:
            await getEmbeds(message, channel, parsedArgs)

        await getText(message, channel, imageList, videoList, parsedArgs, False)
        
    #Give specs on saved files                    
    await message.channel.send("Saved " + str(video) + " videos", delete_after=5.0)
    await message.channel.send("Saved " + str(image) + " images", delete_after=5.0)
    await message.channel.send(str(count) + " Messages were scanned", delete_after=5.0)  

    #await message.channel.send(str(failedImage) + " Images Failed", delete_after=20.0) 
    #await message.channel.send(str(failedVideo) + " Videos failed", delete_after=20.0)   

    setup.writeDates(datesDict)

    # with open(channel + "/Videos/failedVideos.txt", 'w') as f:
    #     f.write(failedVideos)  

    # with open(channel + "/Images/failedImages.txt", 'w') as f:
    #     f.write(failedImages)     

async def getAttachments(msg, channel, dict):
    #print("getting attachments")

    global image
    global video
    global count
    global failedImage
    global failedVideo

    global imageList
    global videoList

    for i in msg.attachments:
            fileType = getFileType(i.filename)

            if fileType in imageArr and dict["I"] == True:
                filename = str(image) + " " + msg.created_at.strftime('%d %b %y') + fileType
                try:
                    dirPath = channel + "/Images/"
                    await i.save(f'' + dirPath + filename)
                    imageList.append(filename)
                    image += 1
                except:
                    with open(channel + "/Images/failedImages.txt", 'a') as f:
                        f.write(filename + " - " + msg.jump_url + "\n") 
                    failedImage += 1
                    continue

            if fileType in videoArr and dict["V"] == True:
                filename = str(video) + " " + msg.created_at.strftime('%d %b %y') + fileType
                try:
                    dirPath = channel + "/Videos/"
                    await i.save(f'' + dirPath + filename)
                    videoList.append(filename)
                    video += 1
                except:
                    with open(channel + "/Videos/failedVideos.txt", 'a') as f:
                        f.write(filename + " - " + msg.jump_url + "\n")  
                    failedVideo += 1
                    continue

async def getEmbeds(msg, channel, dict):

    global image
    global video
    global count
    global failedImage
    global failedVideo

    global imageList
    global videoList

    for i in msg.embeds:
                    
                extensionStr = getFileType(i.url)

                if (extensionStr in imageArr) and dict["I"] == True:
                    url = i.image.url
                    #print("recognized embedded image")
                    filename = str(image) + " " + msg.created_at.strftime('%d %b %y') + extensionStr
                    dirPath = channel + "/Images/"

                    try:
                        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                        response = urllib.request.urlopen(req)

                        imageFile = response.read()

                        with open(dirPath + filename, 'wb') as f:
                            f.write(imageFile)

                        imageList.append(filename)
                        image += 1

                    except Exception as error:
                        with open(channel + "/Images/failedImages.txt", 'a') as f:
                            f.write(filename + " - " + msg.jump_url + "\n") 
                        failedImage += 1
                        continue

                if (extensionStr in videoArr) and dict["V"] == True:
                    url = i.video.url
                    filename = str(video) + " " + msg.created_at.strftime('%d %b %y') + extensionStr
                    dirPath = channel + "/Videos/"

                    try:
                        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                        response = urllib.request.urlopen(req)

                        videoFile = response.read()

                        with open(dirPath + filename, 'wb') as f:
                            f.write(videoFile)

                        videoList.append(filename)
                        video += 1

                    except:
                        with open(channel + "/Videos/failedVideos.txt", 'a') as f:
                            f.write(filename + " - " + msg.jump_url + "\n")  
                        failedVideo += 1
                        continue

"""
Write text messages to messages.csv in the following form.
datetime, author, contents, reference.id, 
"""
async def getText(msg, channel, currImageList, currVideoList, parsedArgs, thread):

    global imageList
    global videoList

    created_at = msg.created_at
    edited_at = msg.edited_at
    author = msg.author
    clean_content = msg.clean_content
    reactions = msg.reactions
    reactionsArr = []
    for react in reactions:
        reactionsArr.append([react.emoji,  react.count])
    jump_url = msg.jump_url
    reference = msg.reference
    replies = None
    if (reference):
        replies = reference.message_id
    id = msg.id
    thread_id = None
    #print(clean_content, thread)
    if (not thread and msg.channel.get_thread(id)):
        #print("Thread found")
        async for message in msg.channel.get_thread(id).history(oldest_first = True):
            imageList = []
            videoList = []
            await getAttachments(message, channel, parsedArgs)
            await getEmbeds(message, channel, parsedArgs)
            await getText(message, channel, imageList, videoList, parsedArgs, True)
    elif thread:
        thread_id = msg.channel.id
    
    messageArr = [created_at, edited_at, author, clean_content, currImageList, currVideoList, reactionsArr, jump_url, replies, id, thread_id]

    stringArr = map(lambda x : str(x) + "\\null", messageArr)

    with open (channel + "/" + channel + "_messages.csv", 'a', encoding="utf-8") as f:
        f.write(', '.join(stringArr) + "\n")
    return

"""
Checks for and creates directories with given Strings.
Parameter: Any Strings
Returns: Null
"""
def set_directories(*args):
    files = os.listdir()
    if (not files.count(args[0])):
        for dir in args:
            os.mkdir(dir)
    
"""
Returns a substring of a filename to decide if a file is a video or image.
Parameter: Filename String
Returns: File Extension String
"""
def getFileType(filename):
    extensionStr = ""
    for ext in (imageArr + videoArr):
        if ext in filename:
            return ext

"""
Gives a dictionary containing arguments mapped to keys
Parameter: Array of arguments (Dates of form '-EYYYY-MM-DD)
Returns: Dictionary
"""         
def parseArgs(args, datesDict, channel):
    #print("parsingArgs")
    try:
        startArr = datesDict[channel].strip("0:").split("-")
        startDatetime = datetime.datetime(int(startArr[0]), int(startArr[1]), int(startArr[2]))
    except:
        startDatetime = None
    dict = {"I" : True, "V" : True, "S" : startDatetime, "E" : datetime.datetime.today(), "T" : True}
    for par in args:
        #print(par)
        if par[1] == "I":
            dict["I"] = True
        elif par[1] == "V":
            dict["V"] = True
        elif par[1] == "T":
            dict["T"] = True
        elif par[1] == "S":
            startArr = par.strip("-S").split("-")
            startDate = datetime.datetime(int(startArr[0]), int(startArr[1]), int(startArr[2]))
            dict["S"] = startDate
        elif par[1] == "E":
            endArr = par.strip("-E").split("-")
            #print(endArr)
            endDate = datetime.datetime(int(endArr[0]), int(endArr[1]), int(endArr[2]))
            #print(endDate)
            dict["E"] = endDate
    return dict

bot.run("MTA5NDY5ODQ0NzkwMDI1NDI0MA.GJF1pn.sjfXhY0ZKluDXXatO6WVx-y364hT5SjlD_1mK4")

