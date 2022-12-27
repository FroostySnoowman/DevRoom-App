import discord
import random
from discord import app_commands
from discord.ext import commands
from typing import Literal

class FunCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="rps", description="Play RPS against the bot!")
    @app_commands.describe(choice="What is your RPS choice?")
    async def rps(self, interaction: discord.Interaction, choice: Literal["Rock", "Paper", "Scissors"]) -> None:
        botchoice = random.randint(1,3)
        if botchoice == 1:
            botchoice = "Rock"
        if botchoice == 2:
            botchoice = "Paper"
        if botchoice == 3:
            botchoice = "Scissors"
        if choice == botchoice:
            message = f"You chose {choice} and the bot chose {botchoice}! It was a **TIE**!"
        if choice == "Rock":
            if botchoice == "Paper":
                message = f"You chose {choice} and the bot chose {botchoice}! You **LOST**!"
            if botchoice == "Scissors":
                message = f"You chose {choice} and the bot chose {botchoice}! You **WON**!"
        if choice == "Paper":
            if botchoice == "Rock":
                message = f"You chose {choice} and the bot chose {botchoice}! You **WON**!"
            if botchoice == "Scissors":
                message = f"You chose {choice} and the bot chose {botchoice}! You **LOST**!"
        if choice == "Scissors":
            if botchoice == "Rock":
                message = f"You chose {choice} and the bot chose {botchoice}! You **LOST**!"
            if botchoice == "Paper":
                message = f"You chose {choice} and the bot chose {botchoice}! You **WON**!"
        await interaction.response.send_message(message, ephemeral=True)

async def setup(bot):
    await bot.add_cog(FunCog(bot))