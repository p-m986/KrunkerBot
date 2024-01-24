from Logs import logevents
# from database.User import User
from discord.ext import commands
from discord.ext.commands import BucketType
from cogs.controllers.create_embed import create_embed
import discord
import random
# from configuration import blacklist_role_id, allowed_channel_ids
blacklist_role_id=1194577286641492069
allowed_channel_ids=[1194652099494035558, 1194653134811832451]

def generate_diceroll_result():
    print("Generating")
    res1 = random.randint(1, 6)
    res2 = random.randint(1, 6)
    print("returning")
    return res1, res2

class Buttons(discord.ui.View):
    def __init__(self, author, target_user:discord.Member, res1, res2, *, timeout=20):
        super().__init__(timeout=timeout)
        self.create_embed = create_embed()
        self.author = author
        self.target_user = target_user
        self.res1 = res1
        self.res2 = res2

    async def on_timeout(self) -> None:
        for item in self.children:
            item.disabled = True
        await self.message.edit(content = "Dice roll timed out", view = self)
    
    @discord.ui.button(label = "Start", style = discord.ButtonStyle.blurple)
    async def gray_button(self,interaction:discord.Interaction, button:discord.ui.Button):
        if interaction.user == self.target_user:
            await self.message.delete()
            await interaction.response.defer()

            for item in self.children:
                item.disabled = True

            button.style = discord.ButtonStyle.green

            resultEmbed = await self.create_embed.createDicerollresult(author = self.author, target_user = self.target_user, res1 = self.res1, res2 = self.res2)
            await interaction.followup.send(embed = resultEmbed, view = self)
            self.stop()
    
    
    @discord.ui.button(label = "Cancel", style = discord.ButtonStyle.danger)
    async def calcel_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        for item in self.children:
            item.disabled = True
            item.style = discord.ButtonStyle.danger
        await self.message.edit(content = "Canceled..", view = self)
        self.stop()


class Diceroll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.create_embed = create_embed()

    @commands.cooldown(1, 3, BucketType(2))
    @commands.hybrid_command(name="htr", with_app_command = True, aliases = ["how to roll", "htdr"])
    async def htr(self, ctx: commands.context):
        referEmbed = await self.create_embed.createReferEmbed(title = "How to diceroll works?", message = "Refer to [How it works](https://discord.com/channels/1194563432112996362/1194651573297623081/1195661941998358599)\n[How Dice roll command works](https://discord.com/channels/1194563432112996362/1194651573297623081/1195671288681873448)")
        await ctx.reply(embed = referEmbed)


    @commands.cooldown(2, 5, BucketType(2))
    @commands.hybrid_command(name="roll", with_app_command=True, aliases = ["diceroll"])
    async def roll(self, ctx: commands.context, target_user: discord.Member = None):
        """
        How it works
        - Check channel
        - Check if any of the two user's are blacklisted
        - Let the other user choose start/cancel
        - Generate random numbers
        - Decide result based on numbers generated
        - Make a result embed
        - Send result embed
        """
        print("Command Recieved") # to be removed
        if ctx.channel.id in allowed_channel_ids: # Channel check

            if ctx.author.get_role(blacklist_role_id):
                embed = await self.create_embed.createFlipErrorEmbed(title = "BLACKLISTED", messge = f"{ctx.author.mention}Sorry but you are *black Listed* you cant gamble")
                await ctx.reply(embed = embed)  # Check if author is blacklisted

            elif target_user.get_role(blacklist_role_id):
                embed = await self.create_embed.createFlipErrorEmbed(title = "BLACKLISTED", message = f"{target_user.mention}Sorry but you are *black Listed* you cant gamble")
                await ctx.reply(embed = embed) # Check if target user is blacklisted

            elif target_user == None:
                embed = await self.create_embed.createFlipErrorEmbed(title = "INCOMPLETE COMMAND", message = "*Sorry but your command is incomplete, Refer to [Exaple](https://discord.com/channels/1194563432112996362/1194651573297623081/1195671288681873448)*")
                await ctx.reply(embed = embed)

            elif target_user.id == ctx.author.id:
                embed = await self.create_embed.createFlipErrorEmbed(title = "ERROR", message = "*Sorry but you cant gamble with yourself, Refer to [Exaple](https://discord.com/channels/1194563432112996362/1194651573297623081/1195671288681873448)*")
                await ctx.reply(embed = embed)
            
            else:
                print("Starting")
                res1, res2 = generate_diceroll_result()
                print("Returned", res1, res2)
                view = Buttons(author = ctx.author, target_user = target_user, res1 = res1, res2 = res2)
                print("Sending")
                view.message = await ctx.reply(content = f"{target_user.mention}\n**{ctx.author.mention} wants to bet on diceroll with you**\nMake sure you know the rules to be followed\n*This will automatically close in 20 Seconds if no response found*", view = view)
                await view.wait()

        else:
            print("Channel Error..")
            embed = await self.create_embed.createFlipErrorEmbed(title = "Wrong Channel", message = "Not the best place to do this, Use #ps99-casino")
            await ctx.reply(embed = embed)

    @roll.error
    async def info_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            create_embed = create_embed()
            cooldown_embed = await create_embed.createFlipErrorEmbed(title = "Command on Cooldown", message = f'This command is on cooldown! Try  again in {round(error.retry_after, 5)} seconds')
            await ctx.reply(embed = cooldown_embed)
        elif isinstance(error, commands.MemberNotFound):
            create_embed = create_embed()
            membererror_embed = await create_embed.createFlipErrorEmbed(title = "Not a member", message = "This is not a valid user in server or You entered the command incorrect\n[REFER HERE FOR EXAPLE](https://discord.com/channels/1194563432112996362/1194651573297623081/1195671288681873448)")
            await ctx.reply(embed = membererror_embed)

    @htr.error
    async def cooldown_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            create_embed = create_embed()
            cooldown_embed = await create_embed.createFlipErrorEmbed(title = "Command on Cooldown", message = f'This command is on cooldown! Try  again in {round(error.retry_after, 3)} seconds')
            await ctx.reply(embed = cooldown_embed)
        

async def setup(bot):
    await bot.add_cog(Diceroll(bot))