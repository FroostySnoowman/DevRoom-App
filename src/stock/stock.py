import discord
import yfinance as yf
from discord import app_commands
from discord.ext import commands

class StockCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="msft", description="Shows you the MSFT stock price!")
    async def msft(self, interaction: discord.Interaction) -> None:
        await interaction.response.defer(thinking=True, ephemeral=True)
        msft = yf.Ticker("MSFT")
        price = msft.info['currentPrice']
        embed = discord.Embed(title="MSFT Stock Price", description=f"MSFT's Stock Price is currently at **${price}**!", color=discord.Color.random())
        await interaction.followup.send(embed=embed)

async def setup(bot):
    await bot.add_cog(StockCog(bot))