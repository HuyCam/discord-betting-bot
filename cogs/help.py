import discord
from discord.ext import commands


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help")
    async def help(self, ctx):
        """Show all available commands."""
        embed = discord.Embed(
            title="🎰 CBot — Command List",
            description="Prefix: `cbot `",
            color=discord.Color.gold()
        )

        embed.add_field(
            name="💰 Betting",
            value=(
                "`cbot coinflip <amount> <heads|tails>` — Flip a coin and bet on the result\n"
                "`cbot balance` — Check your current coin balance\n"
                "`cbot give <@user> <amount>` — Transfer coins to another player"
            ),
            inline=False
        )

        embed.add_field(
            name="🎭 Fun",
            value=(
                "`cbot cam` — Who is Cam?\n"
                "`cbot tin` — Who is Tin?"
            ),
            inline=False
        )

        embed.set_footer(text="Aliases: coinflip → cf | balance → bal")

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Help(bot))
