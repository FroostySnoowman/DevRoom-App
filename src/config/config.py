import discord
import aiosqlite

from discord import app_commands
from discord.ext import commands

class JoinChannelCog(commands.GroupCog, name="config"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        super().__init__() 
    
    joinchannel = app_commands.Group(name="joinchannel", description="Configure your join channel!")

    @joinchannel.command(name="set", description="Set the join channel!")
    @app_commands.describe(channel="What channel do you want to set as the join channel?")
    async def set(self, interaction: discord.Interaction, channel: discord.TextChannel):
        db = await aiosqlite.connect('database.db')
        cursor = await db.execute('SELECT * from joinchannel WHERE guild_id=?', (interaction.guild.id, ))
        a = await cursor.fetchone()
        if a is None:
            if interaction.user.guild_permissions.administrator:
                await db.execute('INSERT INTO joinchannel VALUES (?,?);', (interaction.guild.id, channel.id))
                await interaction.response.send_message(f"I've set the join channel to **{channel}**! To remove this, type `/config joinchannel remove`", ephemeral=True)
            else:
                await interaction.response.send_message(f"You don't have the `Administrator` permission to use this command!", ephemeral=True)
        else:
            await interaction.response.send_message(f"You already have a join channel set!", ephemeral=True)
        await db.commit()
        await db.close()

    @joinchannel.command(name="remove", description="Remove the join channel!")
    async def remove(self, interaction: discord.Interaction):
        db = await aiosqlite.connect('database.db')
        cursor = await db.execute('SELECT * from joinchannel WHERE guild_id=?', (interaction.guild.id, ))
        a = await cursor.fetchone()
        if a is None:
            await interaction.response.send_message(f"You can't remove a join channel if you don't have one!", ephemeral=True)
        else:
            if interaction.user.guild_permissions.administrator:
                await db.execute('DELETE FROM joinnchannel WHERE guild_id=?', (interaction.guild.id, ))
                await interaction.response.send_message(f"Removed the join channel!", ephemeral=True)
            else:
                await interaction.response.send_message(f"You don't have the `Administrator` permission to use this command!", ephemeral=True)
            await db.commit()
            await db.close()

async def setup(bot):
    await bot.add_cog(JoinChannelCog(bot))