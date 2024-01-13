import discord

class create_embed():
    def __init__(self):
        self.startembed = 0x00FFFF
    
    async def createStartEmbed(self, ctx):
        res = discord.Embed(
            title=f"Hello {ctx.author.mention} 👋,  Welcome to Pet Sim 99 on Discord,",
            description=f"To get started please select a class to be a part of,",
            color=self.startembed,
            timestamp=discord.utils.utcnow(),
        )

        res.set_author(
            name="PS99Discord",
            icon_url="https://cdn.discordapp.com/avatars/1184075738496913419/5f2a38f9c2cd28b0696d9716e8e904a1.webp?size=1024"
        )

        res.add_field(
            name="WE HAVE",
            value="Treasure Hunter <:VoidChest:1188656696600580227>: 2x Treasure finding luck\nLucky class <:LuckyEgg:1188752325653823518>: 2x Egg hatch luck\nDamage class <:Damage:1188838450187747400>: 2x Pet damage"
        )
        res.set_thumbnail(url="https://cdn.discordapp.com/avatars/1184075738496913419/5f2a38f9c2cd28b0696d9716e8e904a1.webp?size=320")

        res.set_footer(
            text="PS99Discord", icon_url="https://cdn.discordapp.com/avatars/1184075738496913419/5f2a38f9c2cd28b0696d9716e8e904a1.webp?size=1024")
        return res