import discord
import aiosqlite
from discord import app_commands
from discord.ext import commands

class LeaderboardCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="leaderboard", description="Shows you the message leaderboard!")
    async def leaderboard(self, interaction: discord.Interaction) -> None:
        db = await aiosqlite.connect('database.db')
        try:
            cursor = await db.execute('SELECT * from messages WHERE guild_id=?', (interaction.guild.id, ))
            a = await cursor.fetchall()
            x = sorted(a, key=lambda x: x[2])[-5:]
            y = (list(reversed(x)))
            board = "\n".join([str(lead[2])for lead in y])
            embed = discord.Embed(title="Top 5 Leaderboard", description=f"{board}", color=discord.Color.random())
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except:
            await interaction.response.send_message("An error occured. Please assure that you have set up the message database!", ephemeral=True)
        await db.close()

async def setup(bot):
    await bot.add_cog(LeaderboardCog(bot))