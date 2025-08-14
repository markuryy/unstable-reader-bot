import os
import io
import logging
import discord
from discord.ext import commands
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from unstable_reader.extractor import ImageMetadataExtractor
import uvicorn
import threading
from dotenv import load_dotenv

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.DEBUG)

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.reactions = True
intents.guilds = True
intents.dm_messages = True

ADD_STARS = True

bot = commands.Bot(command_prefix='!', intents=intents)
excluded_channels = set()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/extract-metadata/")
async def extract_metadata(file: UploadFile = File(...)):
    logging.debug(f"Received file: {file.filename}")
    try:
        file_data = await file.read()
        logging.debug(f"File size: {len(file_data)} bytes")
        with open('temp_file', 'wb') as f:
            f.write(file_data)
        extractor = ImageMetadataExtractor('temp_file')
        extractor.extract_metadata()
        if os.path.exists('temp_file'):
            os.remove('temp_file')
        return JSONResponse(content={"metadata": extractor.raw}, status_code=200)
    except Exception as e:
        logging.error(f"Error: {e}")
        if os.path.exists('temp_file'):
            os.remove('temp_file')
        return JSONResponse(content={"error": str(e)}, status_code=500)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} (ID: {bot.user.id})')
    print('Bot is ready. Press Ctrl+C to stop.')

@bot.command(name='exclude')
@commands.has_permissions(administrator=True)
async def exclude_channel(ctx):
    channel = ctx.channel
    excluded_channels.add(channel.id)
    await ctx.send(f'Channel {channel.mention} is now excluded from image analysis.')

@bot.command(name='include')
@commands.has_permissions(administrator=True)
async def include_channel(ctx):
    channel = ctx.channel
    if channel.id in excluded_channels:
        excluded_channels.remove(channel.id)
        await ctx.send(f'Channel {channel.mention} is no longer excluded from image analysis.')
    else:
        await ctx.send(f'This channel is not currently excluded.')

@bot.event
async def on_message(message):
    if message.channel.id not in excluded_channels:
        await process_message(message)
    await bot.process_commands(message)

async def process_message(message):
    for attachment in message.attachments:
        if attachment.content_type.startswith('image/') or attachment.content_type.startswith('video/') or attachment.filename.lower().endswith('.gif'):
            has_metadata = False
            try:
                file_data = await attachment.read()
                with open('temp_file', 'wb') as f:
                    f.write(file_data)
                extractor = ImageMetadataExtractor('temp_file')
                extractor.extract_metadata()
                if extractor.raw:
                    has_metadata = True
            except Exception as e:
                print(f"Error processing file: {e}")
            finally:
                if os.path.exists('temp_file'):
                    os.remove('temp_file')
            if message.guild:
                if has_metadata:
                    await message.add_reaction('🔍')
                    if ADD_STARS:
                        await message.add_reaction('⭐')
                else:
                    await message.add_reaction('✉️')
                    if ADD_STARS:
                        await message.add_reaction('⭐')

@bot.event
async def on_raw_reaction_add(payload):
    if payload.user_id == bot.user.id:
        return

    channel = bot.get_channel(payload.channel_id)
    if channel is None or isinstance(channel, discord.DMChannel):
        await handle_dm_reaction_add(payload)
    else:
        message = await channel.fetch_message(payload.message_id)
        user = bot.get_user(payload.user_id) or await bot.fetch_user(payload.user_id)
        await handle_guild_reaction_add(message, payload.emoji, user)

async def handle_dm_reaction_add(payload):
    if str(payload.emoji) == '❌':
        channel = bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        await message.delete()

async def handle_guild_reaction_add(message, emoji, user):
    if message.channel.id in excluded_channels or user.id == bot.user.id:
        return

    if str(emoji) == '🔍' or str(emoji) == '✉️':
        try:
            await get_metadata(message, user, emoji)
        except Exception as e:
            print(f"Error handling metadata request: {str(e)}")

async def get_metadata(message, user, emoji):
    for attachment in message.attachments:
        if attachment.content_type.startswith('image/') or attachment.content_type.startswith('video/') or attachment.filename.lower().endswith('.gif'):
            try:
                file_data = await attachment.read()
                with open('temp_file', 'wb') as f:
                    f.write(file_data)

                extractor = None
                if attachment.content_type.startswith('image/'):
                    extractor = ImageMetadataExtractor('temp_file')
                    extractor.extract_metadata()

                embed = discord.Embed(title=f"Image by {message.author.name}", color=0xf4acb7)
                embed.add_field(name="Tool", value=extractor.tool if extractor else "N/A", inline=True)
                embed.add_field(name="Original Message", value=f"[Jump to Message]({message.jump_url})", inline=True)

                file_extension = attachment.filename.split('.')[-1]
                file_obj = discord.File(fp=io.BytesIO(file_data), filename=f"media.{file_extension}")

                if str(emoji) == '🔍' and extractor:
                    metadata_file = discord.File(fp=io.StringIO(extractor.raw), filename=f"metadata.txt")
                    await user.send(embed=embed, files=[file_obj, metadata_file])
                elif str(emoji) == '✉️':
                    await user.send(embed=embed, file=file_obj)

            except Exception as e:
                print(f"Error processing file: {e}")
            finally:
                if os.path.exists('temp_file'):
                    os.remove('temp_file')

@bot.event
async def on_reaction_remove(reaction, user):
    if user != bot.user and isinstance(reaction.message.channel, discord.DMChannel):
        if str(reaction.emoji) == '❌':
            await reaction.message.delete()

def start_discord_bot():
    bot_token = os.getenv('DISCORD_BOT_TOKEN')
    if not bot_token:
        raise ValueError("DISCORD_BOT_TOKEN not found in environment variables")
    bot.run(bot_token)

def start_fastapi_server():
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    discord_thread = threading.Thread(target=start_discord_bot)
    discord_thread.start()
    start_fastapi_server()
