from __future__ import annotations

import os
import discord
from discord.ext import commands

from dotenv import load_dotenv
from deesyn.loader.loader import Loader

load_dotenv()

class App(commands.AutoShardedBot):
    def __init__(self):
        super().__init__(
            command_prefix='!',
            intents=discord.Intents.all()
        )

    async def on_ready(self):
        print("Bot ready")
        print("load modules")

        loader = Loader(self)
        total_cog = await loader.start_loader(sync=True)
        print(f"Loaded {len(total_cog)} cogs")
    def _start(self):
        self.run(os.getenv("TOKEN"))
