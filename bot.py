import os
import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv
import db

load_dotenv()

_REQUIRED_ENV = ["DISCORD_TOKEN", "DATABASE_URL"]
_missing = [v for v in _REQUIRED_ENV if not os.environ.get(v)]
if _missing:
    raise EnvironmentError(
        f"Missing required environment variables: {', '.join(_missing)}\n"
        "Copy .env.example to .env and fill in your credentials."
    )

intents = discord.Intents.default()
intents.message_content = True  # required for prefix commands

bot = commands.Bot(command_prefix="cbot ", intents=intents)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")


async def main():
    db.init_db()
    async with bot:
        await bot.load_extension("cogs.betting")
        await bot.start(os.environ["DISCORD_TOKEN"])


asyncio.run(main())
