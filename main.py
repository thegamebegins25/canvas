import requests
import os
import html
import markdownify
import datetime
import math
import discord
import asyncio

token = os.getenv("CANVAS_TOKEN")
headers = {"Authorization": "Bearer " + token}
ids = []

file = open("ids.txt", "r")
ids = file.read().splitlines()
file.close()


client = discord.Client()


@client.event
async def on_ready():
    while True:
        response = requests.get('https://charlottelatin.instructure.com/api/v1/announcements?context_codes[]=course_281', headers=headers)
        data = response.json()

        for i in data:
            id = i["id"]

            if str(id) not in ids:
                ids.append(str(id))
                file = open("ids.txt", "a")
                file.write(str(id) + "\n")
                file.close()

                title = i['title']
                name = i['user_name']
                posted = i['posted_at']

                posted = datetime.datetime.strptime(posted, '%Y-%m-%dT%H:%M:%SZ')
                flt = math.trunc(datetime.datetime.timestamp(posted))
                posted = "<t:" + str(flt) + ">"
                
                message = html.unescape(i['message'])
                message = markdownify.markdownify(message)

                message = "<@&1008888570536280116>\nNEW CANVAS ANNOUNCEMENT!\nby: " + name + "\nPosted at: " + posted + "\n-------------------------------\n" + title + "\n-------------------------------\n" + message

                msg = await client.get_channel(1008868944733544468).send(message)
                await msg.publish()
                print("SENT NEW MESSAGE")

            else:
                print("SKIPPED")
                break

        await asyncio.sleep(60)


client.run("MTAwODg2OTUyNjY5MzIyNDUxOA.G_VRQA.BhEZUkx_hBUAngEZl8DDvUvVV0D1bOi-ZVaEiI")