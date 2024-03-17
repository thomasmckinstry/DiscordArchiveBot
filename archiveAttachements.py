from ast import arg
import discord
import requests
import urllib.request

from discord.ext import commands

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
imageArr = [".jpg", ".jpeg", ".png"]
#soundArr = [".wav", ".mp3", ".ogg"]
videoArr = [".webm", ".mp4"]

@bot.event
async def on_ready():
    print("bot is online")

@bot.command()
async def archiveDocs(ctx):
    print()
    image = 0
    video = 0
    sound = 0

    count = 0
    failedImage = 0
    failedVideo = 0

    async for message in ctx.channel.history(limit=None, before=None, after=None, around=None, oldest_first=True):

        count += 1
        #print(count)

        if len(message.attachments) > 0:
            for i in message.attachments:

                fileType = getFileType(i.filename)
                #print(fileType)

                if fileType in imageArr:
                    #print("In image if")
                    filename = str(image) + message.created_at.strftime('%d %b %y') + fileType
                    image += 1
                    await i.save(f'Image/' + ctx.channel.name  +"/" + filename)
                    #print("saved Image" + str(image))

                if fileType in videoArr:
                    #print("hit video")
                    filename = str(video) + message.created_at.strftime('%d %b %y') + fileType
                    video += 1
                    await i.save(f'Video/' + ctx.channel.name + "/" + filename)
                    #print("saved Video" + str(video))
                    
        if message.embeds: 
            #print("hit embeds")  
            for i in message.embeds:
                #print("hit embeds loop 1")
                extensionStr = getFileType(i.url)
                
                #print(i.url + " url")
                #print(extensionStr + " extension")

                url = i.url

                #print(url)

                if (extensionStr in imageArr):
                    filename = str(image) + message.channel.name + message.created_at.strftime('%d %b %y') + extensionStr

                    try:
                        #print("Image try")
                        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                        response = urllib.request.urlopen(req)

                        imageFile = response.read()

                        with open('Image/' + filename, 'wb') as f:
                            f.write(imageFile)
                            #print("saved embedded Image" + str(image))

                        image += 1

                    except:
                        #print("Image " + filename + " failed to save")
                        failedImage += 1
                        continue

                if (extensionStr in videoArr):
                    #print("hit video if")
                    #print(url)

                    filename = str(video) + message.channel.name + message.created_at.strftime('%d %b %y') + extensionStr
                    try:
                        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                        response = urllib.request.urlopen(req)

                        videoFile = response.read()

                        with open('Video/' + filename, 'wb') as f:
                            f.write(videoFile)

                            video += 1

                    except:
                        #print("Video " + filename + " failed to save")
                        failedVideo += 1
                        continue

                    #urllib.request.urlopen("https://www.youtube.com/")

    await message.channel.send("Saved " + str(video) + " videos", delete_after=20.0)
    await message.channel.send("Saved " + str(image) + " images", delete_after=20.0)
    await message.channel.send(str(count) + " Messages were scanned", delete_after=20.0)  

    await message.channel.send(str(failedImage) + " Images Failed", delete_after=20.0) 
    await message.channel.send(str(failedVideo) + " Videos failed", delete_after=20.0)          

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

bot.run("MTA5NDY5ODQ0NzkwMDI1NDI0MA.GJF1pn.sjfXhY0ZKluDXXatO6WVx-y364hT5SjlD_1mK4")

