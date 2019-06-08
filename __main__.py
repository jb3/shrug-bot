from PIL import Image, ImageDraw, ImageOps
from discord.ext import commands
import discord
import logging
from io import BytesIO
import aiohttp
import os

logging.basicConfig(level=logging.INFO)

log = logging.getLogger("shrug bot")

bot = commands.Bot(command_prefix="!", pm_help=False, description="¯\_(ツ)_/¯")

if os.environ.get("TOKEN") is None:
    print("Woah! You forgot to set a TOKEN environment variable.")
    exit(1)

@bot.event
async def on_ready():
    log.info(f"Logged in on {len(bot.guilds)} guilds")

@bot.command()
async def shrug(ctx, user : discord.Member = None):
    if user is None:
        user = ctx.author
    img1 = Image.open(fp=open("shrug.png", "rb"))
    async with aiohttp.ClientSession() as session:
        avatar = await session.get(str(user.avatar_url_as(format="png")))
        data = await avatar.read()
        av_bytes = BytesIO(data)
        avatar = Image.open(av_bytes)

    dest = (155, 70)
    size = avatar.size
    mask = Image.new('L', size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + size, fill=255)
    av = ImageOps.fit(avatar, mask.size, centering=(0.5, 0.5))
    av.putalpha(mask)

    face_1 = av.resize((78, 78), Image.LANCZOS)
    face_1 = face_1.rotate(15, expand=True)

    img1.paste(face_1, dest, face_1)

    dest = (351, 43)
    size = avatar.size
    mask = Image.new('L', size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + size, fill=255)
    av = ImageOps.fit(avatar, mask.size, centering=(0.5, 0.5))
    av.putalpha(mask)

    face_2 = av.resize((36, 36), Image.LANCZOS)
    face_2 = face_2.rotate(-4, expand=True)

    img1.paste(face_2, dest, face_2)

    dest = (350, 225)
    size = avatar.size
    mask = Image.new('L', size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + size, fill=255)
    av = ImageOps.fit(avatar, mask.size, centering=(0.5, 0.5))
    av.putalpha(mask)

    face_3 = av.resize((40, 40), Image.LANCZOS)
    face_3 = face_3.rotate(5, expand=True)

    img1.paste(face_3, dest, face_3)

    processed = BytesIO()
    img1.save(processed, format="PNG")
    processed.seek(0)
    await ctx.send(file=discord.File(fp=processed, filename="shrugged.png"))

bot.run(os.environ.get("TOKEN"))
