# Fast Import

To reduce boilerplate imports, DeeSyn provides a convenience module that re-exports the most commonly used classes and objects from **discord.py**.

Instead of importing everything individually:

```python
import discord
from discord import app_commands
from discord.ext import commands
```

you can simply write:

```python
from deesyn.api.dsc import *
```

This automatically imports commonly used objects such as:

- `commands`
- `app_commands`
- `Interaction`
- `Embed`
- `Member`
- `User`
- `Message`
- and other frequently used Discord.py classes.

## Example

```python
from deesyn.api.dsc import *

class Example(commands.Cog):
    def __init__(self, bot: commands.AutoShardedBot):
        self.bot = bot

    @app_commands.command(
        name="test",
        description="Example slash command"
    )
    async def test(self, interaction: Interaction):
        await interaction.response.send_message("Hello, DeeSyn!")
```

## Why use Fast Import?

- Less boilerplate code.
- Cleaner and more readable modules.
- No need to remember multiple Discord.py import paths.
- Makes module development faster and more consistent.

> **Note**
>
> `from deesyn.api.dsc import *` is completely optional. You can still import directly from `discord.py` if you prefer.
