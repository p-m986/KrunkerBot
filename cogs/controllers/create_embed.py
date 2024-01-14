import discord

class create_embed():
    def __init__(self):
        self.startembed = 0x00FFFF
        self.resultembed = 0x75ff85
    
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
            author_choice = "tails"
            file = discord.File("../../Images/heads-removebg.png", filename="image.png")
        else:
            winner = target if target_choice == "tails" else author
            author_choice = "heads"
            file = discord.File("../../Images/tails-removebg.png", filename="image.png")
        
        res = discord.Embed(
            title=f"COIN FLIP RESULT",
            description=f"Coin flip between\n{author.mention}: {author_choice}\n{target.mention}: {target_choice}",
            color = self.resultembed,
            timestamp = discord.utils.utcnow(),
        )
        res.add_field(
            name = "Coin Flips",
            value = f"Heads Occoured: {heads_count}\nTails Occoured: {tails_count}",
        )
        
        res.add_field(
            name = f"Winner is",
            value = f"{winner.mention}"
        )

        res.set_thumbnail(url="attachment://image.png")

        res.set_footer(text=f"{discord.utils.utcnow()}")

        return res