import discord
from discord.ext import commands


class Develop(commands.Cog):

    # TestCogクラスのコンストラクタ。Botを受取り、インスタンス変数として保持。
    def __init__(self, bot):
        self.bot = bot

    # コマンドの作成。コマンドはcommandデコレータで必ず修飾する。
    @commands.command(description="開発用(実行権限制限あり)")
    @commands.has_role(848998133882159174)
    async def develop(self, ctx):
        async with ctx.typing():
            # if self.bot.LOCAL_HOST == False:
            self.bot.developMode = not self.bot.developMode
            text = f"開発モード: {self.bot.developMode}"
            if self.bot.developMode:
                await self.bot.change_presence(
                    activity=discord.Activity(name="機能改善会議(メンテナンス中)", type=5)
                )
                self.bot.enrageCounter = 0
            else:
                await self.bot.change_presence(
                    activity=discord.Game(name="Escape from Tarkov", type=1)
                )
            await ctx.send(text)


# Bot本体側からコグを読み込む際に呼び出される関数。
def setup(bot):
    bot.add_cog(Develop(bot))  # TestCogにBotを渡してインスタンス化し、Botにコグとして登録する。
