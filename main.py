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
        response = requests.get('https://charlottelatin.instructure.com/api/v1/announcements?context_codes[]=course_281&context_codes[]=course_313', headers=headers)
        data = response.json()
        #print(data)
        for i in data:
            id = i["id"]

            if str(id) not in ids:
                ids.append(str(id))
                file = open("ids.txt", "a")
                file.write(str(id) + "\n")
                file.close()

                title = i['title']
                name = i['author']['display_name']
                author_url = i['author']['html_url']
                posted = i['posted_at']
                url = i['url']

                posted = datetime.datetime.strptime(posted, '%Y-%m-%dT%H:%M:%SZ')
                delta = datetime.timedelta(hours=4)
                posted = posted - delta
                postedstr = posted.strftime("%I:%M %p")
                if postedstr[0] == "0":
                    postedstr = postedstr[1:]

                
                message = html.unescape(i['message'])
                message = markdownify.markdownify(message)

                embed = discord.Embed(title=title, timestamp=posted, url=url, description=message)
                embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/998642902920069210/1009143571653328967/2019_CanvasLogoStacked_Color.png")
                embed.set_author(name=name, url=author_url)
                embed.set_footer(text=postedstr)
                msg = await client.get_channel(1008868944733544468).send(content="<@&1008888570536280116>", embed=embed)
                await msg.publish()
                print("SENT NEW MESSAGE")

            else:
                print("SKIPPED")
                break

        await asyncio.sleep(60)


client.run(os.getenv("CANVAS_DISCORD_TOKEN"))