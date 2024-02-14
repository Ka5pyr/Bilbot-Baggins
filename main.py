import os
import re
from datetime import datetime, timedelta
from typing import Final

from discord import File, Intents
from discord.ext import commands
from dotenv import load_dotenv

# Load Discord Token
load_dotenv()
DISCORD_TOKEN: Final[str] = os.environ['DISCORD_TOKEN']

# Dictionary to keep track of the last time the help message was sent
last_help_message_time: dict[str, datetime] = {}

# BOT Intents - https://discordpy.readthedocs.io/en/stable/intents.html
intents: Intents = Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="/", intents=intents)

# Function that specifies a specific help menu for the /rank command
async def send_help_message(ctx):
    global last_help_message_time
    current_time = datetime.now()
    channel_id = ctx.channel.id

    # Check if the help message has been sent within the last 5 minutes
    if channel_id in last_help_message_time and current_time - \
        last_help_message_time[channel_id] < timedelta(minutes=1):     
        
        # Don't Return andything if the time is too recent
        await ctx.send('Please reference the above help menu on' + 
                        'how to use the /rank command.')
        return
    
    help_message = (
        "**Command Format:** `/rank [rank]`\n"
        "**Valid rank formats include:**\n"
        "\t + For kyu ranks: `<number>k` or `<number>kyu` (e.g., `8k` or `12kyu`)\n"
        "\t + For dan ranks: `<number>d` or `<number>dan` (e.g., `1d` or `4dan`)\n"
        "\t + For pro ranks: `<number>p` or `<number>pro` (e.g., `1p` or `2pro`)\n"
        "**Examples:**\n"
        "\t + `/rank 8k`\n"
        "\t + `/rank 1dan`\n"
        "_Use the command with your rank to set or update your rank._"
    )
    last_help_message_time[channel_id] = current_time
    await ctx.send(help_message)
    

# Funtion to check if a rank has already been added to the username
def current_name_check(current_name: str) -> str:

    # Check if a patter is in the current name
    pattern = re.compile(r"\d{1,2}[a-z]{1,3}$")

    # If the ranking is found replace it with an empty string
    # Return the username with the rank removed
    return re.sub(pattern, '', current_name)


# Funtion to verify the user input of the rank command
def rank_check(rank: str) -> bool:

    # Modify the rank variable for easy checking
    lower_rank = rank.lower()
    pattern = re.compile(r'^(\d{1,2})([a-z]+)$')
    match = pattern.match(lower_rank)

    # Initial check to see if the rank matches the basic RegEx format
    if match:
        # Split the rank input into the number and the letter
        num_group, str_group = match.groups()

        # Match the input to the possible Go ranks
        return (str_group in ['k', 'kyu'] and 1<= int(num_group) <= 30) \
           or (str_group in ['d', 'dan','p','pro'] and 1<= int(num_group) <= 10)
    else:
        return False
        
"""    
@bot.event
async def on_message(message: Message):
    if message.author == bot.user:
        return
        
    await bot.process_commands(message)
"""
    
# Message when the bot is ready
@bot.event
async def on_ready():
    print(f"{bot.user} has connected to the Discord Channel.")

# Command to Add/Change the rank of the user
@bot.command(name="rank")
async def change_nickname(ctx, *, rank: str=""):
    member = ctx.message.author

    # Check if the user already has a rank and remove it if so
    tmp_uname = current_name_check(member.display_name)

    if rank == "" or rank == "-h":
        await send_help_message(ctx)
        return

    # Validate the input was formatted correctly
    if not rank_check(rank):
        return await send_help_message(ctx)
        
    # Check if the user is the Server Owner
    elif member.id == ctx.guild.owner_id:
        with open("./assets/bowing_hobbit_320x320.png", "rb") as f:
            pic = File(f)
        await ctx.send("A mere program cannot impact a being such as Eru Ilúvatar." +
                       "\nI am the one who must be changed.", file=pic)
    else:
        try:
            # Change the user's nickname
            await member.edit(nick=f"{tmp_uname} [{rank}]")
            await ctx.send(f"Your rank has been changed to [{rank}].")
        # Grab any errors that occur
        except Exception as e:
            print(e)

 
def main() -> None:
    bot.run(token=DISCORD_TOKEN)


if __name__ == '__main__':
    main()