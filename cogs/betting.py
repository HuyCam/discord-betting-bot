import random
import discord
from discord.ext import commands
import db


class Betting(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="coinflip", aliases=["cf"])
    async def coinflip(self, ctx, amount: int):
        """Flip a coin. Win or lose the bet amount."""
        user_id = str(ctx.author.id)
        balance = db.get_balance(user_id)

        if amount <= 0:
            await ctx.send("Bet amount must be greater than 0.")
            return

        if amount > balance:
            await ctx.send(
                f"Not enough coins. Your balance: **{balance}** coins."
            )
            return

        result = random.choice(["heads", "tails"])
        win = random.random() < 0.5

        if win:
            new_balance = db.update_balance(user_id, amount)
            await ctx.send(
                f"🪙 **{result.upper()}** — You **won** {amount} coins! "
                f"Balance: **{new_balance}** coins."
            )
        else:
            new_balance = db.update_balance(user_id, -amount)
            await ctx.send(
                f"🪙 **{result.upper()}** — You **lost** {amount} coins. "
                f"Balance: **{new_balance}** coins."
            )

    @coinflip.error
    async def coinflip_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Usage: `cbot coinflip <amount>`")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Amount must be a whole number. Usage: `cbot coinflip <amount>`")

    @commands.command(name="balance", aliases=["bal"])
    async def balance(self, ctx):
        """Check your coin balance."""
        user_id = str(ctx.author.id)
        balance = db.get_balance(user_id)
        await ctx.send(
            f"{ctx.author.display_name}'s balance: **{balance}** coins."
        )

    @commands.command(name="give")
    async def give(self, ctx, target: discord.Member, amount: int):
        """Transfer coins to another user."""
        sender_id = str(ctx.author.id)
        receiver_id = str(target.id)

        if sender_id == receiver_id:
            await ctx.send("You can't give coins to yourself.")
            return

        if amount <= 0:
            await ctx.send("Amount must be greater than 0.")
            return

        sender_balance = db.get_balance(sender_id)
        if amount > sender_balance:
            await ctx.send(
                f"Not enough coins. Your balance: **{sender_balance}** coins."
            )
            return

        db.update_balance(sender_id, -amount)
        new_receiver_balance = db.update_balance(receiver_id, amount)
        new_sender_balance = db.get_balance(sender_id)

        await ctx.send(
            f"✅ {ctx.author.display_name} gave **{amount}** coins to "
            f"{target.display_name}. "
            f"({ctx.author.display_name}: **{new_sender_balance}** | "
            f"{target.display_name}: **{new_receiver_balance}**)"
        )

    @give.error
    async def give_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Usage: `cbot give <@user> <amount>`")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Usage: `cbot give <@user> <amount>`")

    @commands.command(name="cam")
    async def talk(self, ctx):
        await ctx.send("Huy Cam the King of 5 realms")

    @commands.command(name="tin")
    async def talk(self, ctx):
        await ctx.send("Tin Trong, aka Viego the King of shadow isles")


async def setup(bot):
    await bot.add_cog(Betting(bot))
