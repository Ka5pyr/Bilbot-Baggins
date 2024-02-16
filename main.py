import logging
import os
import re
import sys
from datetime import datetime, timedelta
from typing import Final

from daemonize import Daemonize
from discord import Color, Intents
from discord.ext import commands
from dotenv import load_dotenv

import responses

# Load Discord Token
load_dotenv()
DISCORD_TOKEN: Final[str] = os.environ['DISCORD_TOKEN']

# Logging Setup
logging.basicConfig(filename='bilbot.log',
                    level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')

# Dictionary to keep track of the last time the help message was sent
last_rank_command_time: dict[int, datetime] = {}

# Load Embed Class
embed_creator = responses.EmbedCreator(Color.green())

# BOT Intents - https://discordpy.readthedocs.io/en/stable/intents.html
intents: Intents = Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="/", intents=intents)


# Function that specifies a specific help menu for the /rank command
async def send_help_message(ctx):
    channel_id = ctx.channel.id
    current_time = datetime.now()

    if last_rank_command_time.get(channel_id):
        last_sent = last_rank_command_time[channel_id]
        if (current_time - last_sent) < timedelta(minutes=1):
            await ctx.send(embed=embed_creator.wait_message())
            return

    last_rank_command_time[channel_id] = current_time
    embed = embed_creator.rank_help_message()
    await ctx.send(embed=embed)


# Funtion to check if a rank has already been added to the username
def current_name_check(current_name: str) -> str:

    # Check if a patter is in the current name
    pattern = re.compile(r"\s*\[\d{1,2}[a-z]{1,3}\]$", re.IGNORECASE)

    # If the ranking is found replace it with an empty string
    # Return the username with the rank removed
    return re.sub(pattern, '', current_name).strip()


# Funtion to verify the user input of the rank command
def rank_check(rank: str) -> str:

    # Modify the rank variable for easy checking
    lower_rank = rank.lower()
    pattern = re.compile(r'^(\d{1,2})([a-z]+)$')
    match = pattern.match(lower_rank)

    # Initial check to see if the rank matches the basic RegEx format
    if match:
        # Split the rank input into the number and the letter
        num_group, str_group = match.groups()
        if str_group == 'k':
            rank = lower_rank.replace('k', 'kyu')
        elif str_group == 'd':
            rank = lower_rank.replace('d', 'dan')
        elif str_group == 'p':
            rank = lower_rank.replace('p', 'pro')

        # Match the input to the possible Go ranks
        if (rank.endswith('kyu') and 1<= int(num_group) <= 30)\
            or (rank.endswith('dan') and 1<= int(num_group) <= 10)\
            or (rank.endswith('pro') and 1<= int(num_group) <= 10):
            return rank
    return ""
    
    
# Message when the bot is ready
@bot.event
async def on_ready():
    print(f"{bot.user} has connected to Discord.")
    logging.info(f"{bot.user} has connected to the Discord.")
    # Log the names of the servers the bot is connects to
    for guild in bot.guilds:
        logging.info(f"{bot.user} connected to guild: {guild.name} (id: {guild.id})")


# Command to Add/Change the rank of the user
@bot.command(name="rank")
async def change_nickname(ctx, *, rank: str=""):
    member = ctx.message.author
    current_time = datetime.now()
    logging.info(f"Received rank command from user {member.name} with input: '{rank}'")

    # Check if the user already has a rank and remove it if so
    tmp_uname = current_name_check(member.display_name)
    logging.debug(f"Current name: {tmp_uname}")

    valid_rank = rank_check(rank)
    if rank.lower().strip() in ["","-h", "help"] or not valid_rank:
        await send_help_message(ctx)
        return

    # Check if the user is the Server Owner
    elif member.id == ctx.guild.owner_id:
        embed = embed_creator.mod_server_owner_response()
        await ctx.send(embed=embed)
        logging.info(f"Server Owner {member} attempted the rank command")
        
    # Verify the user hasn't recently updated their rank
    elif member.id in last_rank_command_time:
        time_since_last_command = current_time - last_rank_command_time[member.id]
        if time_since_last_command < timedelta(minutes=1):
            # Inform the user about the cooldown
            logging.warning(f"User {member} attempted to update their rank too frequently")
            embed = embed_creator.wait_message()
            await ctx.send(embed=embed)
            return  # Exit the command without changing the rank
    else:
        try:
            # Change the user's nickname
            await member.edit(nick=f"{tmp_uname} [{valid_rank}]")
            embed = embed_creator.successful_rank_change_message(valid_rank) 
            await ctx.send(embed=embed)
            logging.info(f"Changed nickname for user {member} to rank: {valid_rank}")
        # Grab any errors that occur
        except Exception as e:
            logging.error(f"Failed to change nickname for user {member}: {e}")
            embed = embed_creator.error_message() 
            await ctx.send(embed=embed)
            
    # Update the last time the /rank command was used by the user
    last_rank_command_time[member.id] = current_time
 
def main() -> None:
    bot.run(token=DISCORD_TOKEN)


if __name__ == '__main__':
    if len(sys.argv) == 2 and (sys.argv[1] in ['-d', '--daemon']):
        app_name = "bilbot_baggins"
        pid_file = f"/run/{app_name}/{app_name}.pid"
        daemon = Daemonize(app=app_name, pid=pid_file, action=main)
        daemon.start()
    else:
        main()