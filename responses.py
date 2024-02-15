# responses.py
from datetime import datetime, timedelta

from discord import File

# Keep track of the last time the help message was sent per channel
last_help_message_time: dict[int, datetime] = {}

# Help Message
def get_help_message() -> str:
    return (
        "**Command Format:** `/rank [rank]`\n"
        "**Valid rank formats include:**\n"
        "\t + For kyu ranks: `<number>k` or `<number>kyu` (e.g., `8k` or `12kyu`)\n"
        "\t + For dan ranks: `<number>d` or `<number>dan` (e.g., `1d` or `4dan`)\n"
        "\t + For pro ranks: `<number>p` or `<number>pro` (e.g., `1p` or `2pro`)\n"
        "**Examples:**\n"
        "\t + `/rank 8k`\n"
        "\t + `/rank 1dan`\n"
        "_Use the command with your rank to set or update your rank._"
        "_Make sure there isn't a space between your <number> and <rank> (i.e. 1 Dan)._"
    )

# Function to determine if the user has recently used the /rank command
def should_send_help_message(channel_id: int) -> bool:
    current_time = datetime.now()

    if channel_id in last_help_message_time:
        if current_time - last_help_message_time[channel_id] < timedelta(minutes=1):
            return False
    last_help_message_time[channel_id] = current_time
    return True

# An Error Occurred Message
def error_message() -> str:
    return ("Dark forces have corrupted your request. Please try again later.")

# Cannot Modify the Server Owner Message
def mod_server_owner_response() -> tuple[str, File]:
    resp_msg = "A mere program cannot impact a being such as Eru Ilúvatar.\n" +\
                "I am the one who must be changed." 
    pic_file = "/home/sgamgee/bots/Bilbot-Baggins/assets/bowing_hobbit_320x320.png"

    with open(pic_file, "rb") as f:
        pic = File(f)
        return (resp_msg, pic)
        
# Successful Rank Change Message
def successful_rank_change_message(rank: str) -> str:
    return f"Your rank has been changed to **{rank}**."

def wait_message() -> str:
    return "Please wait a minute before using the same command again."