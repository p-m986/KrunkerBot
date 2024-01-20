from Logs import logevents
# from database.User import User
from discord.ext import commands
from discord.ext.commands import BucketType
from cogs.controllers.create_embed import create_embed
from typing import List
import discord


class TicTacToeButton(discord.ui.Button['TicTacToe']):
    def __init__(self, x: int, y: int):
        super().__init__(style=discord.ButtonStyle.secondary, label='\u200b', row=y)
        self.x = x
        self.y = y

    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        view: TicTacToe = self.view
        state = view.board[self.y][self.x]
        if state in (view.X, view.O):
            return

        if view.current_player == view.author:
            self.style = discord.ButtonStyle.danger
            self.label = 'X'
            self.disabled = True
            view.board[self.y][self.x] = view.X
            view.current_player = view.target_user
            content = f"{view.O.mention}'s turn"
        elif view.current_player == view.target_user:
            self.style = discord.ButtonStyle.success
            self.label = 'O'
            self.disabled = True
            view.board[self.y][self.x] = view.O
            view.current_player = view.author
            content = f"{view.X.mention}'s turn"

        winner = view.check_board_winner()
        if winner is not None:
            if winner == view.X:
                content = f'{view.X.mention} WON'
            elif winner == view.O:
                content = f'{view.O.mention} WON'
            else:
                content = "It's a tie!"

            for child in view.children:
                child.disabled = True

            view.stop()

        await interaction.response.edit_message(content=content, view=view)


# This is our actual board View
class TicTacToe(discord.ui.View):
    children: List[TicTacToeButton]
    X = -1
    O = 1
    Tie = 2

    def __init__(self, author, target_user: discord.Member):
        super().__init__()
        self.current_player = author
        self.author = author
        self.target_user = target_user
        self.board = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]

        for x in range(3):
            for y in range(3):
                self.add_item(TicTacToeButton(x, y))

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
        self.create_embeds = create_embed()
        self.selected_class = None
        
    @commands.cooldown(1, 15, BucketType(1))
    @commands.hybrid_command(name="ttt", with_app_command=True,  aliases = ["tictactoe"])
    async def ttt(self, ctx: commands.Context,target_user: discord.Member = None):
        """
        Tic Tac Toe
        """
        if target_user == None:
            await ctx.reply("Gotta metion a user")
        view = TicTacToe(ctx.author, target_user)
        await ctx.send('Tic Tac Toe: X goes first', view=view)
        return
 
async def setup(bot):
    await bot.add_cog(tic_tac_toe(bot))