import discord
import discord.app_commands as ac
from discord.ext import commands

class Example(commands.Cog):
    def __init__(self, bot: commands.AutoShardedBot):
        self.bot = bot

    @ac.command(
        name="example",
        description="Example command"
    )
    async def example(self,interaction: discord.Interaction):
        await interaction.response.defer(thinking=True)
        await interaction.followup.send("example")