import discord

class create_embed():
    def __init__(self):
        self.startembed = 0x00FFFF
        self.resultembed = 0x75ff85
        self.fliperror = 0xff7575
        self.referEmbed = 0xefff5c
    
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
    
    async def createFlipresult(self, heads_count, tails_count, author, target, target_choice):
        print("Creating Embed") # To be removed
        if heads_count > tails_count:
            winner = target if target_choice == "heads" else author
            author_choice = "tails" if target_choice == "heads" else "heads"
            uri = "https://media.discordapp.net/attachments/1194656963821305997/1196051552385892362/heads-removebg.png?ex=65b638cf&is=65a3c3cf&hm=455c2cb8e1ed8aaba031d95d98735daac7f42a2aa14cbe38f09c342ecc3ad147&=&format=webp&quality=lossless&width=450&height=450"
        else:
            winner = target if target_choice == "tails" else author
            author_choice = "heads" if target_choice == "tails" else "tails"
            uri = "https://media.discordapp.net/attachments/1194656963821305997/1196051552612401172/tails-removebg.png?ex=65b638cf&is=65a3c3cf&hm=4321bbcaafc0872726692d1eae676042f113357fedd4a19ded623faa5085ff0a&=&format=webp&quality=lossless&width=1100&height=908"
        
        res = discord.Embed(
            title=f"COIN FLIP RESULT",
            description=f"Coin flip between\n{author.mention}: {author_choice}\n{target.mention}: {target_choice}",
            color = self.resultembed,
            timestamp = discord.utils.utcnow(),
        )
        res.add_field(
            name = "Coin Flips",
            value = f"Heads Occoured: {heads_count}\nTails Occoured: {tails_count}",
            inline=False
        )
        
        res.add_field(
            name = f"Winner is",
            value = f"{winner.mention}",
            inline = False
        )

        res.set_thumbnail(url=uri)

        res.set_footer(text=f"{discord.utils.utcnow()}")

        return res
    
    async def createFlipErrorEmbed(self, title, message):
        res = discord.Embed(
            title = f"{title}",
            description = f"{message}",
            color = self.fliperror,
            timestamp = discord.utils.utcnow()
        )
        return res

    async def createReferEmbed(self, title, message):
        res = discord.Embed(
            title = f"{title}",
            description = f"{message}",
            color = self.referEmbed,
            timestamp = discord.utils.utcnow()
        )
