from Logs import logevents
# from database.User import User
from discord.ext import commands
from discord.ext.commands import BucketType
# from cogs.controllers.create_embed import create_embed
import discord
import asyncio
import random

class Flip(commands.Cog):
    def _init_(self, bot):
        self.bot = bot


    @commands.hybrid_command(aliases=["f", "Flip", "FLIP", "F"])
    @commands.cooldown(2, 3, BucketType.guild)
    async def flip(self, ctx, bo, target_user: discord.Member = None):
        """
        How it works
        - Check channel
        - Check if any of the two user's are blacklisted
        - Make sure users are doing best of in odd numbers
        - Let the other user choose heads/tails
        - Generate random numbers
        - Decide result based on numbers generated
        - Make a result embed
        - Send result embed
        """

        if {ctx.channel.id} in [1194652099494035558, 1194653134811832451]:
            if ctx.author.get_role(1194577286641492069):
                await ctx.channel.send(f"{ctx.author.mention}Sorry but you are *black Listed* you cant gamble")
            elif target_user.get_role(1194577286641492069):
                await ctx.channel.send(f"{target_user.mention}Sorry but you are *black Listed* you cant gamble")
            elif target_user.id == ctx.author.id:
                await ctx.channel.send("*Sorry but you cant gamble with yourself, Refer to (Exaple)[https://discord.com/channels/1194563432112996362/1194651573297623081/1195671288681873448]*")
            else:
                if int(bo) % 2 == 0:
                    await ctx.channel.send("**NO PLS NO**\nEven numbers are not allowed in best of this will lead to draws")

                elif (int(bo) < 102 and int(bo) > 0):
                    waitMessage = await ctx.channel.send(f"{target_user.mention}\n*{ctx.author.name} wants to Gamble with you\nMake sure you know the rules to be followed\nType `heads` or `tails` If you wish to choose heads or tails respectively\n*This will automatically close in 20 Seconds if no correct reply found")

                    def check(msg):
                        return msg.author == target_user and msg.channel == ctx.channel and msg.content.lower() in ["tails", "heads", "head", "tail", "Heads", "Head", "Tail", "Tails"]

                    try:
                        msg = await self.bot.wait_for('message', timeout=20.0, check=check)
                    except asyncio.TimeoutError:
                        await waitMessage.delete()
                        await ctx.channel.send(f"{ctx.author.mention}\n{target_user.name} doesn't want to flip")
                        return
                    else:
                        await waitMessage.delete()
                        if msg.content.lower() in ["heads", "head"]:
                            user_choice = "tail"
                        elif msg.content.lower() in ["tails", "tail"]:
                            user_choice = "head"

                        OrignalMessage = await ctx.channel.send(f"{ctx.author.mention} and {target_user.mention} \n Flip starts in few seconds")
                        await asyncio.sleep(1.5)
                        
                        for i in range(int(bo)):
                            num = random.randint(-1, 2)
                            if num <= 0:
                                he_ += 1
                                value_head += 1
                            else:
                                ta_ += 1
                                value_tail += 1
                        descriptor = discord.Embed(
                            title=f"RESULT",
                            description=f"H: {he_}\tT: {ta_}\n------------------",color=0x11806A)
                        
                        if user_choice in ["heads", "head", "h"] and he_ > ta_:
                            descriptor.add_field(name=f"Winner is ", value=f"{ctx.author.mention}", inline=False)
                            descriptor.add_field(name=f"----------------\n",value=f"{ctx.author.mention} Heads and {target_user.mention} tails",inline=False)
                            try:
                                await target_user.send(f"You lost flip which took place with {ctx.author.name}")
                            except:
                                print("DMS Error")
                            try:
                                await ctx.author.send(f"You Won flip which took place with {target_user.name}")
                            except:
                                print("DMS Error")

                        elif user_choice in ["tails", "tail", "t"] and ta_ > he_:
                            descriptor.add_field(name=f"Winner is ",value=f"{ctx.author.mention}", inline=False)
                            descriptor.add_field(name=f"----------------\n", value=f"{ctx.author.mention} Tails and {target_user.mention} Heads", inline=False)
                            try:
                                await target_user.send(f"You lost flip which took place with {ctx.author.name}")
                            except:
                                print("DMS Error")
                            try:
                                await ctx.author.send(f"You Won flip which took place with {target_user.name}")
                            except:
                                print("DMS Error")

                        else:
                            descriptor.add_field(name=f"Winner is ",value=f"{target_user.mention}",inline=False)
                            if user_choice in ["tails", "tail", "t"]:
                                descriptor.add_field(name=f"----------------\n",value=f"{ctx.author.mention} Tails and {target_user.mention} Heads",inline=False)
                            if user_choice in ["heads", "head", "h"]:
                                descriptor.add_field(name=f"----------------\n",value=f"{ctx.author.mention} Heads and {target_user.mention} tails",inline=False)
                            try:
                                await target_user.send(f"You Won flip which took place with {ctx.author.name}")
                            except:
                                print("DMS Error")
                            try:
                                await ctx.author.send(f"You Lost flip which took place with {target_user.name}")
                            except:
                                print("DMS Error")
                        await OrignalMessage.delete()
                        await ctx.channel.send(embed=descriptor)
                else:
                    await ctx.channel.send("*Max* best of is 101 and *Min* is 1\n Why do you think its gonna be a zero")
        else:
            await ctx.channel.send("Not the best place to do this")

    @flip.error
    async def info_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f'This command is on cooldown! Try  again in {round(error.retry_after, 3)} seconds')
        elif isinstance(error, commands.MemberNotFound):
            await ctx.send("This is not a valid user in server or You entered the command incorrect\nUse $fliphelp to see Example")

async def setup(bot):
    await bot.add_cog(Flip(bot))