from discord.ext import commands
from Logs import logevents
from dotenv import load_dotenv
from typing import Literal, Optional
import discord
import os
import asyncio

load_dotenv()
bot = commands.Bot(command_prefix=commands.when_mentioned_or('$'),case_insensitive=True, help_command=None, owner_id=820611084938510337, strip_after_prefix=True, intents=discord.Intents.all())

# Connecting to the Discord API


@bot.event
async def on_connect():
    print(f"{bot.user.name} connected to the api successfully")

@bot.event
async def on_ready():
    obj = logevents()
    await obj.log_restart()
    print("Ready for code execution")  

@bot.event
async def on_resumed():
    print("Graceful disconnect happened, resumed connnection now")

@bot.hybrid_command()
async def ping(ctx):
    await ctx.send("Pong!")

@bot.command()
@commands.guild_only()
@commands.is_owner()
async def sync(ctx: commands.Context, guilds: commands.Greedy[discord.Object], spec: Optional[Literal["~", "*", "^"]] = None) -> None:
    if not guilds:
        if spec == "~":
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        elif spec == "*":
            ctx.bot.tree.copy_global_to(guild=ctx.guild)
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        elif spec == "^":
            ctx.bot.tree.clear_commands(guild=ctx.guild)
            await ctx.bot.tree.sync(guild=ctx.guild)
            synced = []
        else:
            synced = await ctx.bot.tree.sync()

        await ctx.send(
            f"Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild.'}"
        )
        return

    ret = 0
    for guild in guilds:
        try:
            await ctx.bot.tree.sync(guild=guild)
        except discord.HTTPException:
            pass
        else:
            ret += 1

    await ctx.send(f"Synced the tree to {ret}/{len(guilds)}.")


# Fetching the modules sotred in the cogs folder and loading them onto the bot using the load_extension function


@bot.hybrid_command()
async def reload(ctx, cog: str):
    if ctx.author.id == 820611084938510337:
        try:
            await bot.reload_extension(f"cogs.{cog}")
            await ctx.reply(f"{cog} has been reloaded successfully", ephemeral=True)
        except Exception as e:
            obj = logevents()
            errorid = await obj.log_error(class_name="Main", function_name="ReloadCommand", message=str(e))
            print(f'An error occoured in the Main class wtihin the {cog} cog, check error logs with id {errorid} for more details')
            raise e


async def loadcog():
    for cog in os.listdir("./cogs"):
        if cog.endswith(".py"):
            # try:
            cog = f"cogs.{cog.replace('.py', '')}"
            print(cog)
            await bot.load_extension(cog, package='ps99bot')
            print("Loaded:\t", cog)
            # except Exception as e:
                # print(e)
                # obj = logevents()
                # errorid = await obj.log_error(class_name="Main", function_name="loadcog", message=str(e))
                # print(f'An error occoured in the main file, {cog} cog, check error logs with id {errorid} for more details')


# try:
asyncio.run(loadcog())
# except Exception as e:
#     print(e)


try:
    bot.run(os.getenv('TOKEN'))
except Exception as e:
    print(e)
    obj = logevents()
    asyncio.run(obj.log_error(class_name="Main", function_name="loadcog", message=str(e)))