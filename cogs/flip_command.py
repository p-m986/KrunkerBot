from Logs import logevents
# from database.User import User
from discord.ext import commands
from discord.ext.commands import BucketType
from cogs.controllers.create_embed import create_embed
import discord
import asyncio
import random
# from configuration import blacklist_role_id, allowed_channel_ids
blacklist_role_id=1204265320857083965
allowed_channel_ids=[1202920194843090965]


def generate_flip_result(bo):
    """
    Returns heads and tails count integers
    """
    print("Generating...")
    head_count = 0
    for i in range(int(bo)):
        num = random.randint(-1, 2)
        if num <= 0:
            head_count += 1
        else:
            head_count += 0
    print("Returning")
    return head_count, int(bo) - head_count

class Buttons(discord.ui.View):
    def __init__(self, author, target_user, heads_count, tails_count, *, timeout=20):
        super().__init__(timeout=timeout)
        self.create_embed = create_embed()
        self.target_choice = None
        self.author = author
        self.target_user = target_user
        self.heads_count = heads_count
        self.tails_count = tails_count
    
    async def on_timeout(self) -> None:
        for item in self.children:
            item.disabled = True

        await self.message.edit(content = "Coin Flip timed out", view = self)
    
    @discord.ui.button(label = "Heads", style = discord.ButtonStyle.blurple)
    async def gray_button(self,interaction:discord.Interaction, button:discord.ui.Button):
        if interaction.user == self.target_user:
            await self.message.delete()
            await interaction.response.defer()
            button.style = discord.ButtonStyle.green
            self.target_choice = "heads"
            button.disabled = True
            resultEmbed = await self.create_embed.createFlipresult(heads_count = self.heads_count, tails_count = self.tails_count, author = self.author, target = self.target_user, target_choice = self.target_choice)
            await interaction.followup.send(content = f"Chose Heads", embed = resultEmbed)
            self.stop()
    
    @discord.ui.button(label = "Tails", style = discord.ButtonStyle.blurple)
    async def tails_button(self, interaction:discord.Interaction, button:discord.ui.Button):
        if interaction.user == self.target_user:
            await self.message.delete()
            await interaction.response.defer()
            button.style = discord.ButtonStyle.green
            self.target_choice = "tails"
            button.disabled = True
            resultEmbed = await self.create_embed.createFlipresult(heads_count = self.heads_count, tails_count = self.tails_count, author = self.author, target = self.target_user, target_choice = self.target_choice)
            await interaction.followup.send(content = "Chose Tails", embed = resultEmbed)
            self.stop()
    
    @discord.ui.button(label = "Cancel", style = discord.ButtonStyle.danger)
    async def calcel_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        for item in self.children:
            item.disabled = True
            item.style = discord.ButtonStyle.danger
        await self.message.edit(content = "Canceled..", view = self)
        self.stop()

class Flip(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.create_embed = create_embed()

    @commands.cooldown(1, 3, BucketType(2))
    @commands.hybrid_command(name="htf", with_app_command = True, aliases = ["how to flip"])
    async def htf(self, ctx: commands.context):
        print("here")
        referEmbed = await self.create_embed.createReferEmbed(title = "How to coinflip?", message = "To Be added soon.. Please contact staff for help for now")
        print("Got embed")
        await ctx.reply(embed = referEmbed)


    @commands.cooldown(2, 5, BucketType(2))
    @commands.hybrid_command(name="flip", with_app_command=True, aliases = ["coinflip"])
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
        if ctx.channel.id in allowed_channel_ids: # Channel check
            print("Channel correct")
            if ctx.author.get_role(blacklist_role_id):
                embed = await self.create_embed.createFlipErrorEmbed(title = "BLACKLISTED", messge = f"{ctx.author.mention}Sorry but you are *black Listed* you cant gamble")
                await ctx.reply(embed = embed)  # Check if author is blacklisted

            elif target_user.get_role(blacklist_role_id):
                embed = await self.create_embed.createFlipErrorEmbed(title = "BLACKLISTED", message = f"{target_user.mention}Sorry but you are *black Listed* you cant gamble")
                await ctx.reply(embed = embed) # Check if target user is blacklisted

            elif bo == None or target_user == None:
                embed = await self.create_embed.createFlipErrorEmbed(title = "INCOMPLETE COMMAND", message = "*Sorry but your command is incomplete, To be added soon.. Please contact staff for help*")
                await ctx.reply(embed = embed)

            elif target_user.id == ctx.author.id:
                embed = await self.create_embed.createFlipErrorEmbed(title = "ERROR", message = "*Sorry but you cant gamble with yourself, To be added soon.. Please contact staff for help*")
                await ctx.reply(embed = embed)
            
            else:
                print("Checking bo")
                if int(bo) % 2 == 0:
                    print("Even bo")
                    embed = await self.create_embed.createFlipErrorEmbed(title = "ERROR", message = "**NO PLS NO**\nEven numbers are not allowed in best of this will lead to draws")
                    await ctx.reply(embed = embed)

                elif (int(bo) < 102 and int(bo) > 0):
                    heads_count, tails_count = generate_flip_result(bo = bo)
                    print("Returning....")
                    view = Buttons(author = ctx.author, target_user = target_user, heads_count = heads_count, tails_count = tails_count)
                    view.message = await ctx.reply(content = f"{target_user.mention}\n**{ctx.author.mention} wants to bet on coinflip with you**\nMake sure you know the rules to be followed\nBest of: {bo}\nChoose `heads` or `tails`\n*This will automatically close in 20 Seconds if no response found*", view = view)
                    await view.wait()

                else:
                    print("Max number error")
                    embed = await self.create_embed.createFlipErrorEmbed(title = "ERROR", message = "*Max* best of is 101 and *Min* is 1\n Why do you think its gonna be a zero")
                    await ctx.reply(embed = embed)
        else:
            print("Channel Error..")
            embed = await self.create_embed.createFlipErrorEmbed(title = "Wrong Channel", message = "Not the best place to do this, Use #ps99-casino")
            await ctx.reply(embed = embed)

    @flip.error
    async def info_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            create_embed = create_embed()
            cooldown_embed = await create_embed.createFlipErrorEmbed(title = "Command on Cooldown", message = f'This command is on cooldown! Try  again in {round(error.retry_after, 5)} seconds')
            await ctx.reply(embed = cooldown_embed)
        elif isinstance(error, commands.MemberNotFound):
            create_embed = create_embed()
            membererror_embed = await create_embed.createFlipErrorEmbed(title = "Not a member", message = "This is not a valid user in server or You entered the command incorrect\nTo be added soon.. Please contact staff for help")
            await ctx.reply(embed = membererror_embed)

    @htf.error
    async def cooldown_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            create_embed = create_embed()
            cooldown_embed = await create_embed.createFlipErrorEmbed(title = "Command on Cooldown", message = f'This command is on cooldown! Try  again in {round(error.retry_after, 3)} seconds')
            await ctx.reply(embed = cooldown_embed)
        

async def setup(bot):
    await bot.add_cog(Flip(bot))