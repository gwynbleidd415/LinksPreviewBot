import discord
import os
import re
import requests
from lxml import html
from dotenv import load_dotenv

# import nest_asyncio

# nest_asyncio.apply()

load_dotenv(".env")
token = os.getenv("BOT_TOKEN")
pattern = re.compile(r"^https?://\S*\.\S*$")

client = discord.Client()


def getTagValue(tree, tag):
    metaList = tree.xpath(
        f'//meta[@*="{tag}" or @*="og:{tag}" or @*="twitter:{tag}"]/@content'
    )
    if metaList:
        return metaList[-1]
    return None


@client.event
async def on_start():
    print(f"We have logged in as {client.user}")


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if pattern.search(message.content):
        res = requests.get(message.content)
        tree = html.fromstring(res.content).find("head")
        title, description = (
            getTagValue(tree, "title"),
            getTagValue(tree, "description"),
        )
        siteName = getTagValue(tree, "site")
        thumbnail = getTagValue(tree, "image")
        if not thumbnail:
            thumbnail = getTagValue(tree, "image:src")
        if not siteName:
            siteName = getTagValue(tree, "site_name")
        if description:
            description = description[:119]
        embed = discord.Embed(title=title, url=message.content, description=description)
        if thumbnail:
            embed.set_thumbnail(url=thumbnail)
        if siteName:
            embed.set_footer(text=siteName)
        # embed.set_author(name = getTagValue(tree, 'author'))
        if title or description:
            await message.channel.send(embed=embed)
            await message.delete()


client.run(token)
