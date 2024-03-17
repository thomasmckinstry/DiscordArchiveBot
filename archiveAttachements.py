from ast import arg
import discord
import requests
import urllib.request
import datetime
import os

from discord.ext import commands

#Setup
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
imageArr = [".jpg", ".jpeg", ".png"]
#soundArr = [".wav", ".mp3", ".ogg"]
videoArr = [".webm", ".mp4"]

#Creates starter directories and confirms bot launch
@bot.event
async def on_ready():
    print("bot is online")

#Archive files out of the channel the command was sent in.
@bot.command()
async def archiveDocs(ctx, *args):
    parsedArgs = parseArgs(args)
    print(parsedArgs)
    channel = ctx.channel.name
    set_directories(channel, channel + "/Images", channel + "/Videos")

    image = 0
    video = 0
    sound = 0

    count = 0
    failedImage = 0
    failedVideo = 0

    failedImages = ""
    failedVideos = ""

    #Loops through each message sent in the channel
    async for message in ctx.channel.history(limit=None, before=parsedArgs["E"], after=parsedArgs["S"], around=None, oldest_first=True):

        count += 1

        #Loop through and save attachments
        if len(message.attachments) > 0:
            for i in message.attachments:

                fileType = getFileType(i.filename)

                if fileType in imageArr:
                    try:
                        dirPath = channel + "/Images/"
                        filename = str(image) + " " + message.created_at.strftime('%d %b %y') + fileType
                        await i.save(f'' + dirPath + filename)
                        image += 1
                    except:
                        failedImage += 1
                        failedImages += filename + " " + message.jump_url + "\n"
                        continue

                if fileType in videoArr:
                    try:
                        dirPath = channel + "/Videos/"
                        filename = str(video) + " " + message.created_at.strftime('%d %b %y') + fileType
                        await i.save(f'' + dirPath + filename)
                        video += 1
                    except:
                        failedVideo += 1
                        failedVideos += filename + " " + message.jump_url + "\n"
                        continue
        
        #Loop through and save embeds (Some older embeds do not work)
        if message.embeds: 
            for i in message.embeds:

                extensionStr = getFileType(i.url)

                url = i.url

                if (extensionStr in imageArr):
                    filename = str(image) + " " + message.created_at.strftime('%d %b %y') + extensionStr
                    dirPath = channel + "/Images/"

                    try:
                        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                        response = urllib.request.urlopen(req)

                        imageFile = response.read()

                        with open(dirPath + filename, 'wb') as f:
                            f.write(imageFile)

                        image += 1

                    except:
                        failedImage += 1
                        failedImages += filename + " " + message.jump_url + "\n"
                        continue

                if (extensionStr in videoArr):
                    filename = str(video) + " " + message.created_at.strftime('%d %b %y') + extensionStr
                    dirPath = channel + "/Videos/"

                    try:
                        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                        response = urllib.request.urlopen(req)

                        videoFile = response.read()

                        with open(dirPath + filename, 'wb') as f:
                            f.write(videoFile)

                        video += 1

                    except:
                        failedVideo += 1
                        failedVideos += filename + " " + message.jump_url + "\n"
                        continue
        
    #Give specs on saved files                    
    await message.channel.send("Saved " + str(video) + " videos", delete_after=20.0)
    await message.channel.send("Saved " + str(image) + " images", delete_after=20.0)
    await message.channel.send(str(count) + " Messages were scanned", delete_after=20.0)  

    await message.channel.send(str(failedImage) + " Images Failed", delete_after=20.0) 
    await message.channel.send(str(failedVideo) + " Videos failed", delete_after=20.0)   

    with open(channel + "/Videos/failedVideos.txt", 'w') as f:
        f.write(failedVideos)  

    with open(channel + "/Images/failedImages.txt", 'w') as f:
        f.write(failedImages)     

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
    for j in range(len(filename) - 4, 0, -1):
                    
        if filename[j : j+4] in imageArr or filename[j : j+4] in videoArr:
            extensionStr = filename[j : j+4]
            #print(extensionStr)
            return extensionStr

        if j <= len(filename)-5:
            if filename[j : j+6] in imageArr or filename[j : j+6] in videoArr:
                extensionStr = filename[j : j+6]
                #print(extensionStr)
                return extensionStr

"""
Gives a dictionary containing arguments mapped to keys
Parameter: Array of arguments
Returns: Dictionary
"""         
def parseArgs(args):
    dict = {"I" : None, "V" : None, "S" : None, "E" : None}
    for par in args:
        print(par.strip("-S").split("-"))
        if par[1] == "I":
            dict["I"] = True
        elif par[1] == "V":
            dict["V"] = True
        elif par[1] == "S":
            startArr = par.strip("-S").split("-")
            startDate = datetime.datetime(int(startArr[0]), int(startArr[1]), int(startArr[2]))
            dict["S"] = startDate
        elif par[1] == "E":
            endArr = par.strip("-E").split("-")
            endDate = datetime.datetime(endArr[0], endArr[1], endArr[2])
            dict["E"] = endDate
        return dict



bot.run("MTA5NDY5ODQ0NzkwMDI1NDI0MA.GJF1pn.sjfXhY0ZKluDXXatO6WVx-y364hT5SjlD_1mK4")

