import discord
import re
import os
import requests
from lxml import html
from dotenv import load_dotenv
# import nest_asyncio


# nest_asyncio.apply()

load_dotenv('.env')
token = os.getenv('BOT_TOKEN')
pattern = re.compile(r'^https?://\S*\.\S*$')

client = discord.Client()


def getTagValue(tree, tag):
    metaList = tree.xpath(
        f'//meta[@*="{tag}" or @*="og:{tag}" or @*="twitter:{tag}"]/@content')
    if(metaList):
        return metaList[-1]
    return None


@client.event
async def on_start():
    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if(pattern.search(message.content)):
        res = requests.get(message.content)
        tree = html.fromstring(res.content).find('head')
        thumbnail = getTagValue(tree, 'image')
        if(not thumbnail):
            thumbnail = getTagValue(tree, 'image:src')
        embed = discord.Embed(title=getTagValue(tree, 'title'), url=message.content, description=getTagValue(
            tree, 'description'), provider=getTagValue(tree, 'site_name'))
        if(thumbnail):
            embed.set_thumbnail(url=thumbnail)
        embed.set_footer(text=getTagValue(tree, 'site_name'))
        # embed.set_author(name = getTagValue(tree, 'author'))
        await message.channel.send(embed=embed)
        await message.delete()


client.run(token)
