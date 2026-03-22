import random
import discord
from discord.ext import commands
import db


class Betting(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="coinflip", aliases=["cf"])
    async def coinflip(self, ctx, amount: int, pick: str):
        """Flip a coin. Pick heads or tails and bet an amount."""
        user_id = str(ctx.author.id)

        pick = pick.lower()
        if pick not in ("heads", "tails", "h", "t"):
            await ctx.send("Pick must be `heads` or `tails`. Usage: `pbot coinflip <amount> <heads|tails>`")
            return

        # normalise shorthand h/t → heads/tails
        if pick == "h":
            pick = "heads"
        elif pick == "t":
            pick = "tails"

        if amount <= 0:
            await ctx.send("Bet amount must be greater than 0.")
            return

        balance = db.get_balance(user_id)
        if amount > balance:
            await ctx.send(
                f"Not enough coins. Your balance: **{balance}** coins."
            )
            return

        msg = await ctx.send(
            f"🪙 {ctx.author.display_name} picked **{pick}** — waiting for the result..."
        )

        result = random.choice(["heads", "tails"])
        win = result == pick

        if win:
            db.update_balance(user_id, amount)
            await msg.edit(content=
                f"🪙 {ctx.author.display_name} picked **{pick}** — it landed on **{result.upper()}** — You **won** {amount} coins!"
            )
        else:
            db.update_balance(user_id, -amount)
            await msg.edit(content=
                f"🪙 {ctx.author.display_name} picked **{pick}** — it landed on **{result.upper()}** — You **lost** {amount} coins."
            )

    @coinflip.error
    async def coinflip_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Usage: `pbot coinflip <amount> <heads|tails>`")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Amount must be a whole number. Usage: `pbot coinflip <amount> <heads|tails>`")

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
            await ctx.send("Usage: `pbot give <@user> <amount>`")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Usage: `pbot give <@user> <amount>`")


async def setup(bot):
    await bot.add_cog(Betting(bot))
