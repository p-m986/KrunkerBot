from Logs import logevents
# from database.User import User
from discord.ext import commands
from discord.ext.commands import BucketType
from cogs.controllers.create_embed import create_embed
from typing import List
import discord

blacklist_role_id=1194577286641492069
allowed_channel_ids=[1194652099494035558, 1194653134811832451]

class TicTacToeButton(discord.ui.Button['TicTacToe']):
    def __init__(self, x: int, y: int):
        super().__init__(style=discord.ButtonStyle.secondary, label='\u200b', row=y)
        self.x = x
        self.y = y

    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        view: TicTacToe = self.view
        state = view.board[self.y][self.x]
        embed = None

        # Check if it's the current player's turn
        if interaction.user != view.current_player:
            return

        if state in (view.X, view.O):
            return

        if view.current_player == view.author and interaction.user == view.author:
            self.style = discord.ButtonStyle.danger
            self.label = 'X'
            self.disabled = True
            view.board[self.y][self.x] = view.X
            view.current_player = view.target_user
            content = f"{view.target_user.mention}'s turn"
        elif view.current_player == view.target_user and interaction.user == view.target_user:
            self.style = discord.ButtonStyle.success
            self.label = 'O'
            self.disabled = True
            view.board[self.y][self.x] = view.O
            view.current_player = view.author
            content = f"{view.author.mention}'s turn"

        winner = view.check_board_winner()
        if winner is not None:
            if winner == view.X:
                content = None
                embed = await view.create_embed.createTictactoeresult(view.author, view.target_user, view.author)
            elif winner == view.O:
                content = None
                embed = await view.create_embed.createTictactoeresult(view.author, view.target_user, view.target_user)
            else:
                content = None
                embed = await view.create_embed.createTictactoeresult(view.author, view.target_user, "tie")

            for child in view.children:
                child.disabled = True

            view.stop()

        await interaction.response.edit_message(content=content, view=view, embed = embed)



# This is our actual board View
class TicTacToe(discord.ui.View):
    children: List[TicTacToeButton]
    X = -1
    O = 1
    Tie = 2

    def __init__(self, author, target_user: discord.Member, timeout=15):
        super().__init__(timeout=timeout)
        self.current_player = author
        self.author = author
        self.target_user = target_user
        self.create_embed = create_embed()
        self.board = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]

        for x in range(3):
            for y in range(3):
                self.add_item(TicTacToeButton(x, y))
    
    async def on_timeout(self) -> None:
        for item in self.children:
            item.disabled = True
        ttt_timeout_embed = await self.create_embed.createTictactoeTimeout(self.auther, self.target_user, self.current_player)
        await self.message.edit(content="", view = self, embed = ttt_timeout_embed)

    def check_board_winner(self):
        for across in self.board:
            value = sum(across)
            if value == 3:
                return self.O
            elif value == -3:
                return self.X

        # Check vertical
        for line in range(3):
            value = self.board[0][line] + self.board[1][line] + self.board[2][line]
            if value == 3:
                return self.O
            elif value == -3:
                return self.X

        # Check diagonals
        diag = self.board[0][2] + self.board[1][1] + self.board[2][0]
        if diag == 3:
            return self.O
        elif diag == -3:
            return self.X

        diag = self.board[0][0] + self.board[1][1] + self.board[2][2]
        if diag == 3:
            return self.O
        elif diag == -3:
            return self.X

        if all(i != 0 for row in self.board for i in row):
            return self.Tie

        return None

# Commands
class tic_tac_toe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = logevents()
        self.selected_class = None
        self.create_embed = create_embed()
        
    @commands.cooldown(1, 10, BucketType(1))
    @commands.hybrid_command(name="ttt", with_app_command=True,  aliases = ["tictactoe"])
    async def ttt(self, ctx: commands.Context,target_user: discord.Member = None):
        """
        Tic Tac Toe
        """
        if ctx.channel.id in allowed_channel_ids: # Channel check
            print("Channel correct")
            if target_user == None:
                embed = await self.create_embed.createFlipErrorEmbed(title = "Missing 2nd player", messge = f"{ctx.author.mention} Please mention the 2nd player")
                await ctx.reply(embed = embed)
                return
            elif target_user == ctx.author:
                embed = await self.create_embed.createFlipErrorEmbed(title = "Self Gamble", messge = f"{ctx.author.mention}Sorry but you cant gamble with yourself")
                await ctx.reply(embed = embed)
                return
            if ctx.author.get_role(blacklist_role_id):
                embed = await self.create_embed.createFlipErrorEmbed(title = "BLACKLISTED", messge = f"{ctx.author.mention}Sorry but you are *black Listed* you cant gamble")
                await ctx.reply(embed = embed)  # Check if author is blacklisted

            elif target_user.get_role(blacklist_role_id):
                embed = await self.create_embed.createFlipErrorEmbed(title = "BLACKLISTED", message = f"{target_user.mention}Sorry but you are *black Listed* you cant gamble")
                await ctx.reply(embed = embed) # Check if target user is blacklisted
                view = TicTacToe(ctx.author, target_user)
                await ctx.send(f'Tic Tac Toe:{ctx.author.mention} goes first', view=view)
                await view.wait()

        return
    
    @ttt.error
    async def info_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            cooldown_embed = await self.create_embed.createFlipErrorEmbed(title = "Command on Cooldown", message = f'This command is on cooldown! Try  again in {round(error.retry_after, 5)} seconds')
            await ctx.reply(embed = cooldown_embed)
        elif isinstance(error, commands.MemberNotFound):
            membererror_embed = await self.create_embed.createFlipErrorEmbed(title = "Not a member", message = "This is not a valid user in server or You entered the command incorrect\n[REFER HERE FOR EXAPLE](https://discord.com/channels/1194563432112996362/1194651573297623081/1195671288681873448)")
            await ctx.reply(embed = membererror_embed)
 
async def setup(bot):
    await bot.add_cog(tic_tac_toe(bot))