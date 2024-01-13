from Logs import logevents
# from database.User import User
from discord.ext import commands
from discord.ext.commands import BucketType
from cogs.controllers.create_embed import create_embed
import discord

# class Select_class(discord.ui.Select):
#     def __init__(self):
#         options=[
#             discord.SelectOption(label="Treasure Hunter",emoji='<:VoidChest:1188656696600580227>',description="2x Treasure finding luck"),
#             discord.SelectOption(label="Lucky class",emoji="<:LuckyEgg:1188752325653823518>",description="2x Egg hatch luck"),
#             discord.SelectOption(label="Damage class",emoji="<:Damage:1188838450187747400>",description="2x Pet damage")
#             ]
#         super().__init__(placeholder="Select a class",max_values=1,min_values=1,options=options)
    
#     async def callback(self, interaction: discord.Interaction):
#         await interaction.response.defer(ephemeral=False)

#         guild = interaction.guild
#         user = interaction.user

#         treasure_hunter = guild.get_role(1188492588169297940)
#         egg_luck = guild.get_role(1188492792213807134)
#         strong_pets = guild.get_role(1188492901790003200)
        
#         user_obj = User()
        
#         await user_obj.set_client()

#         profile_id, intentory_id = await user_obj.add_user(discord_userid = user.id, user_class = self.values[0])

#         if not profile_id:
#             await interaction.followup.send("❗🚨You are already registered🚨❗ \nIf you wish to change your class contact staff", ephemeral=True)
#             await interaction.delete_original_response()
#             return

#         if self.values[0] == "Treasure Hunter":
#             await user.add_roles(treasure_hunter)
#             await interaction.followup.send(content="🎁CONGRATULATIONS🎁!! You are now a member of Treasure Hunter class <:VoidChest:1188656696600580227>", ephemeral = False)
        
#         elif self.values[0] == "Lucky class":
#             await user.add_roles(egg_luck)
#             await interaction.followup.send(content = "🍀CONGRATULATIONS🍀!! You are now a member of the Lucky Egg class <:LuckyEgg:1188752325653823518>", ephemeral=False)
        
#         elif self.values[0] == "Damage class":
#             await user.add_roles(strong_pets)
#             await interaction.followup.send(content = "💪CONGRATULATIONS💪!! You are now a member of the Strong Pets class <:Damage:1188838450187747400>", ephemeral=False)
        
#         await interaction.delete_original_response()

        
# class SelectView(discord.ui.View):
#     def __init__(self, *, timeout = 40):
#         super().__init__(timeout=timeout)
#         self.add_item(Select_class())


# Commands
class testing(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = logevents()
        self.create_embeds = create_embed()
        self.selected_class = None
        
    @commands.cooldown(1, 10, BucketType(1))
    @commands.hybrid_command(name="start", with_app_command=True)
    async def start(self, ctx: commands.Context):
        """
        To be changed
        """
        await ctx.send("This command is not in use")
        return
        # await ctx.defer(ephemeral=False)

        # start_embed = await self.create_embeds.createStartEmbed(ctx)
        
        # await ctx.reply(view=SelectView(), embed=start_embed, delete_after=50.00)
 
async def setup(bot):
    await bot.add_cog(testing(bot))