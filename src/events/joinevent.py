import discord
import aiosqlite
from discord.ext import commands
from datetime import datetime


class MemberEventsCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.bot:
            return
        db = await aiosqlite.connect('database.db')
        try:
            cursor = await db.execute('SELECT * from joinchannel WHERE guild_id=?', (member.guild.id, ))
            a = await cursor.fetchone()
            created = member.created_at.timestamp()
            member_created = int(created)
            embed = discord.Embed(
                description=
                f"""
{member.mention} {member}

**Account Created**
<t:{member_created}:R>
""",
                color=discord.Color.random())
            embed.set_author(name=f"Member Joined", icon_url = member.display_avatar.url)
            embed.timestamp=datetime.now()
            embed.set_footer(text=f"Member: {member.id}")
            channel = self.bot.get_channel(a[1])
            await channel.send(embed=embed)
        except:
            pass
        await db.close()

async def setup(bot):
    await bot.add_cog(MemberEventsCog(bot))