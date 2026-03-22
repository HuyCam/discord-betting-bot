from discord.ext import commands


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="cam")
    async def cam(self, ctx):
        await ctx.send("Huy Cam the King of 5 realms")

    @commands.command(name="tin")
    async def tin(self, ctx):
        await ctx.send("Tin Trong, aka Viego the King of shadow isles")


async def setup(bot):
    await bot.add_cog(Fun(bot))
