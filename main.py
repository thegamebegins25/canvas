from dis import disco
import requests
import os
import html
import markdownify
import datetime
import discord
from discord import app_commands
import asyncio

token = os.getenv("CANVAS_TOKEN")
headers = {"Authorization": "Bearer " + token}
ids = []

file = open("ids.txt", "r")
ids = file.read().splitlines()
file.close()

intents = discord.Intents.default()
client = discord.Client(intents=intents)

tree = discord.app_commands.CommandTree(client=client)
client.tree = tree

guild = discord.Object(1008864344597074050)  # Guild ID here

@tree.command(name="role", description="Use this command to get the CanvasPing role.")
@app_commands.guilds(guild)
async def role(interaction: discord.Interaction):
    ping_role = client.get_guild(guild.id).get_role(1008888570536280116)
    member = await interaction.guild.fetch_member(interaction.user.id)
    

    if ping_role in member.roles:
        await member.remove_roles(ping_role)
        await interaction.response.send_message('Removed CanvasPing role.', ephemeral=True)
    else:
        await member.add_roles(ping_role)
        await interaction.response.send_message('Added CanvasPing role.', ephemeral=True)


@client.event
async def on_message(message):
    if message.content == "!sync":
        print("Syncing...")
        await client.tree.sync(guild=guild)


@client.event
async def on_ready():
    while True:
        try:
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
                    author_icon = i["author"]["avatar_image_url"]
                    posted = i['posted_at']
                    url = i['url']
                    color = discord.Colour.from_str("#ff0000")

                    posted = datetime.datetime.strptime(posted, '%Y-%m-%dT%H:%M:%SZ')
                    delta = datetime.timedelta(hours=4)
                    posted = posted - delta
                    postedstr = posted.strftime("%I:%M %p")
                    if postedstr[0] == "0":
                        postedstr = postedstr[1:]

                    
                    message = html.unescape(i['message'])
                    message = markdownify.markdownify(message)

                    embed = discord.Embed(title=title, timestamp=posted, url=url, description=message, color=color)
                    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/998642902920069210/1009143571653328967/2019_CanvasLogoStacked_Color.png")
                    embed.set_author(name=name, url=author_url, icon_url=author_icon)
                    embed.set_footer(text=postedstr)
                    msg = await client.get_channel(1008868944733544468).send(content="<@&1008888570536280116>", embed=embed)
                    await msg.publish()
                    print("SENT NEW MESSAGE")

                else:
                    print("SKIPPED")
                    break

            await asyncio.sleep(60)
        except Exception as e:
            print("Error: " + str(e))






client.run(os.getenv("CANVAS_DISCORD_TOKEN"))