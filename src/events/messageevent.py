import discord
import aiosqlite
from discord.ext import commands


class MessageEventsCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener('on_message')
    async def on_message(self, message: discord.Message):
        if message.author == self.bot.user:
            return
        db = await aiosqlite.connect('database.db')
        try:
            cursor = await db.execute('SELECT * from messages WHERE guild_id=? AND user_id=?', (message.guild.id, message.author.id))
            a = await cursor.fetchone()
            if a is None:
                await db.execute('INSERT INTO messages VALUES (?,?,?);', (message.guild.id, message.author.id, 1))
            else:
                await db.execute('UPDATE messages SET count=count+? WHERE user_id=? AND guild_id=?', (1, message.author.id, message.guild.id))
        except:
            pass
        await db.commit()
        await db.close()
            

async def setup(bot):
    await bot.add_cog(MessageEventsCog(bot))