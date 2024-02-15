# responses.py
from datetime import datetime, timedelta
from typing import Optional

from discord import Color, Embed, File

# Keep track of the last time the help message was sent per channel
last_help_message_time: dict[int, datetime] = {}

class EmbedCreator:
    def __init__(self, default_color: Color) -> None:
        self.default_color = default_color

    def create_embed(self, title: str, description: str, color: Optional[Color] = None) -> Embed:
        if color is None:
            color = self.default_color
        return Embed(title=title, description=description, color=color)

    # Help Message
    def rank_help_message(self) -> Embed:
        return self.create_embed(
            title="Rank Command Help",
            description=(
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
            ),
            color=Color.dark_grey()
        )
        
    # Cannot Modify the Server Owner Message
    def mod_server_owner_response(self) -> Embed:
        embed = self.create_embed(
            title="Server Modification Denied",
            description = (
                "A mere program cannot impact a being such as Eru Ilúvatar.\n"
                "I am the one who must be changed."
            ),
            color=Color.dark_red()
        )
        img_path = "assets/bowing_hobbits_320x320.png"
        embed.set_image(url=f"attachment://{img_path}")
        return embed
        
    # An Error Occurred Message
    def error_message(self) -> Embed:
        return self.create_embed(
            title="Not my gumdrop buttons!",
            description="Dark forces have corrupted your request. Please try again later.",
            color=Color.red()
        )
        
    # Successful Rank Change Message
    def successful_rank_change_message(self, rank: str) -> Embed:
        return self.create_embed(
            title="Rank Change",
            description=f"Your rank has been changed to **{rank}**.",
            color=Color.teal()
        )
        
    def wait_message(self) -> Embed:
        return self.create_embed(
            title="Don't Be Hasty!",
            description="Please wait a minute before using the same command again.",
            color=Color.dark_green()
        )
        
    
# Function to determine if the user has recently used the /rank command
def should_send_help_message(channel_id: int) -> bool:
    current_time = datetime.now()

    if channel_id in last_help_message_time:
        if current_time - last_help_message_time[channel_id] < timedelta(minutes=1):
            return False
    last_help_message_time[channel_id] = current_time
    return True