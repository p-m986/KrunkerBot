from Logs import logevents
# from database.User import User
from discord.ext import commands
from discord.ext.commands import BucketType
from cogs.controllers.create_embed import create_embed
import discord
import asyncio
import random


def generate_flip_result(bo):
    """
    Returns lists which contain either a 1 or 0 in all its indexes
    """
    print("Generating result")
    head_count = []
    for _ in range(int(bo)):
        num = random.randint(-9, 10)
        if num <= 0:
            head_count += 1
        else:
            head_count += 0
    return head_count, bo - head_count

class Buttons(discord.ui.View):
    def __init__(self, author, target_user, heads_count, tails_count, *, timeout=20):
        super().__init__(timeout=timeout)
        self.target_choice = None
        self.author = author
        self.target_user = target_user
        self.heads_count = heads_count
        self.tails_count = tails_count
    
    @discord.ui.button(label = "Heads", style = discord.ButtonStyle.blurple)
    async def gray_button(self,interaction:discord.Interaction, button:discord.ui.Button):
        if interaction.user == self.target_user:
            interaction.defer()
            button.style = discord.ButtonStyle.green
            self.target_choice = "heads"
            button.disabled = True
            resultEmbed = create_embed.createFlipresult(heads_count = self.heads_count, tails_count = self.tails_count, author = self.author, target = self.target_user, target_choice = self.target_choice)
            await interaction.response.edit_message(content = f"Chose Heads", view = self, embed = resultEmbed)
            self.stop()
    
    @discord.ui.button(label = "Tails", style = discord.ButtonStyle.blurple)
    async def tails_button(self, interaction:discord.Interaction, button:discord.ui.Button):
        if interaction.user == self.target_user:
            interaction.defer()
            button.style = discord.ButtonStyle.green
            self.target_choice = "tails"
            button.disabled = True
            resultEmbed = create_embed.createFlipresult(heads_count = self.heads_count, tails_count = self.tails_count, author = self.author, target = self.target_user, target_choice = self.target_choice)
            await interaction.response.edit_message(content = "Chose Tails", view = self, embed = resultEmbed)
            self.stop()

class Flip(commands.Cog):
    def _init_(self, bot):
        self.bot = bot

    @commands.cooldown(2, 3, BucketType(2))
    @commands.hybrid_command(name="flip", with_app_command=True)
    async def flip(self, ctx: commands.context, bo, target_user: discord.Member = None):
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
        print("Command Recieved") # to be removed
        if ctx.channel.id in [1194652099494035558, 1194653134811832451]: # Channel check
            if ctx.author.get_role(1194577286641492069):
                await ctx.send(f"{ctx.author.mention}Sorry but you are *black Listed* you cant gamble")  # Check if author is blacklisted
            elif target_user.get_role(1194577286641492069):
                await ctx.send(f"{target_user.mention}Sorry but you are *black Listed* you cant gamble") # Check if target user is blacklisted
            elif target_user.id == ctx.author.id:
                await ctx.send("*Sorry but you cant gamble with yourself, Refer to (Exaple)[https://discord.com/channels/1194563432112996362/1194651573297623081/1195671288681873448]*")
            else:
                if int(bo) % 2 == 0:
                    await ctx.send("**NO PLS NO**\nEven numbers are not allowed in best of this will lead to draws")

                elif (int(bo) < 102 and int(bo) > 0):
                    heads_count, tails_count = generate_flip_result(bo = bo)
                    view = Buttons(author = ctx.author, target_user = target_user, heads_count = heads_count, tails_count = tails_count)
                    await ctx.send(content = f"{target_user.mention}\n**{ctx.author.mention} wants to bet on coinflip with you**\nMake sure you know the rules to be followed\nBest of: {bo}\nChoose `heads` or `tails`\n*This will automatically close in 20 Seconds if no response found*", view = view)
                    await view.wait()

                else:
                    await ctx.send("*Max* best of is 101 and *Min* is 1\n Why do you think its gonna be a zero")
        else:
            await ctx.send("Not the best place to do this")

    @flip.error
    async def info_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f'This command is on cooldown! Try  again in {round(error.retry_after, 3)} seconds')
        elif isinstance(error, commands.MemberNotFound):
            await ctx.send("This is not a valid user in server or You entered the command incorrect\nUse $fliphelp to see Example")

async def setup(bot):
    await bot.add_cog(Flip(bot))




# waitMessage = await ctx.reply(f"{target_user.mention}\n**{ctx.author.name} wants to Gamble with you**\nMake sure you know the rules to be followed\nType `heads` or `tails` If you wish to choose heads or tails respectively\n*This will automatically close in 20 Seconds if no correct reply found*")
#                     print("Waiting...")
#                     msg = ''
#                     def check():
#                         return msg.author == target_user and msg.channel == ctx.channel and msg.content.lower() in ["tails", "heads", "head", "tail", "Heads", "Head", "Tail", "Tails"]

#                     try:
#                         print("Reached here...")
#                         msg = await self.bot.wait_for('message', timeout=20.0, check=check)
#                         print(msg.author)
#                     except asyncio.TimeoutError:
#                         await waitMessage.delete()
#                         await ctx.send(f"{ctx.author.mention}\n{target_user.name} doesn't want to flip")
#                         return
#                     else:
#                         await waitMessage.delete()
#                         if msg.content.lower() in ["heads", "head"]:
#                             user_choice = "tail"
#                         elif msg.content.lower() in ["tails", "tail"]:
#                             user_choice = "head"

#                         OrignalMessage = await ctx.send(f"{ctx.author.mention} and {target_user.mention} \n Flip starts in few seconds")
#                         await asyncio.sleep(1.5)
                        
#                         for i in range(int(bo)):
#                             num = random.randint(-1, 2)
#                             if num <= 0:
#                                 he_ += 1
#                                 value_head += 1
#                             else:
#                                 ta_ += 1
#                                 value_tail += 1
#                         descriptor = discord.Embed(
#                             title=f"RESULT",
#                             description=f"H: {he_}\tT: {ta_}\n------------------",color=0x11806A)
                        
#                         if user_choice in ["heads", "head", "h"] and he_ > ta_:
#                             descriptor.add_field(name=f"Winner is ", value=f"{ctx.author.mention}", inline=False)
#                             descriptor.add_field(name=f"----------------\n",value=f"{ctx.author.mention} Heads and {target_user.mention} tails",inline=False)
#                             try:
#                                 await target_user.send(f"You lost flip which took place with {ctx.author.name}")
#                             except:
#                                 print("DMS Error")
#                             try:
#                                 await ctx.author.send(f"You Won flip which took place with {target_user.name}")
#                             except:
#                                 print("DMS Error")

#                         elif user_choice in ["tails", "tail", "t"] and ta_ > he_:
#                             descriptor.add_field(name=f"Winner is ",value=f"{ctx.author.mention}", inline=False)
#                             descriptor.add_field(name=f"----------------\n", value=f"{ctx.author.mention} Tails and {target_user.mention} Heads", inline=False)
#                             try:
#                                 await target_user.send(f"You lost flip which took place with {ctx.author.name}")
#                             except:
#                                 print("DMS Error")
#                             try:
#                                 await ctx.author.send(f"You Won flip which took place with {target_user.name}")
#                             except:
#                                 print("DMS Error")

#                         else:
#                             descriptor.add_field(name=f"Winner is ",value=f"{target_user.mention}",inline=False)
#                             if user_choice in ["tails", "tail", "t"]:
#                                 descriptor.add_field(name=f"----------------\n",value=f"{ctx.author.mention} Tails and {target_user.mention} Heads",inline=False)
#                             if user_choice in ["heads", "head", "h"]:
#                                 descriptor.add_field(name=f"----------------\n",value=f"{ctx.author.mention} Heads and {target_user.mention} tails",inline=False)
#                             try:
#                                 await target_user.send(f"You Won flip which took place with {ctx.author.name}")
#                             except:
#                                 print("DMS Error")
#                             try:
#                                 await ctx.author.send(f"You Lost flip which took place with {target_user.name}")
#                             except:
#                                 print("DMS Error")
#                         await OrignalMessage.delete()
#                         await ctx.send(embed=descriptor)