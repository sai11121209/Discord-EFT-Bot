import discord
import datetime
from discord.ext import commands
from datetime import datetime as dt
import traceback  # エラー表示のためにインポート


class Help(commands.Cog):

    # TestCogクラスのコンストラクタ。Botを受取り、インスタンス変数として保持。
    def __init__(self, bot):
        self.bot = bot

    # コマンドの作成。コマンドはcommandデコレータで必ず修飾する。
    @commands.command(description="使用可能コマンド表示")
    async def help(self, ctx):
        async with ctx.typing():
            try:
                embed = discord.Embed(
                    title="EFT(Escape from Tarkov) Wiki Bot使用可能コマンド一覧だよ!",
                    description=f"```Prefix:{self.bot.command_prefix}```",
                    color=0x2ECC69,
                    timestamp=datetime.datetime.utcfromtimestamp(
                        dt.strptime(
                            list(self.bot.patchNotes.keys())[0].split(":", 1)[1]
                            + "+09:00",
                            "%Y/%m/%d %H:%M%z",
                        ).timestamp()
                    ),
                )
                for command in self.bot.all_commands:
                    if self.bot.all_commands[command].name == "weapon":
                        text = f"```{self.bot.command_prefix}{self.bot.all_commands[command].name}```"
                        text += "```/{武器名}```"
                    elif self.bot.all_commands[command].name == "market":
                        text = f"```{self.bot.command_prefix}{self.bot.all_commands[command].name}```"
                        text += "```!p {アイテム名}```"
                    elif self.bot.all_commands[command].name == "map":
                        text = f"```{self.bot.command_prefix}{self.bot.all_commands[command].name}```"
                        text += "```/{マップ名}```"
                    else:
                        text = f"```{self.bot.command_prefix}{self.bot.all_commands[command].name}```"
                    embed.add_field(
                        name=f"{self.bot.all_commands[command].description}コマンド",
                        value=text,
                    )
                # embed.set_thumbnail(url=client.get_user(803770349908131850).avatar_url)
                embed.set_author(
                    name="EFT(Escape from Tarkov) Wiki Bot",
                    url="https://github.com/sai11121209",
                    # icon_url=client.get_user(279995095124803595).avatar_url,
                )
                embed.set_footer(text="最終更新")
                await ctx.send(embed=embed)
            except:
                traceback.print_exc()

    @commands.command()
    async def hello(self, ctx):
        await ctx.send("どうしました?")
        ans = await self.bot.wait_for("message")
        print(ans)

    @commands.command()
    async def report(self, ctx):
        await ctx.send("game_idを教えてください")
        game_id = await self.bot.wait_for("message")
        await ctx.send("勝利チームのチームIDととったラウンド数を教えてください")
        win_data = await self.bot.wait_for("message")
        win_id, win_round = win_data.content.split(" ")
        await ctx.send("敗北チームのチームIDととったラウンド数を教えてください")
        lose_data = await self.bot.wait_for("message")
        lose_id, lose_round = lose_data.content.split(" ")

        print(win_id, win_round, lose_id, lose_round)


# Bot本体側からコグを読み込む際に呼び出される関数。
def setup(bot):
    bot.add_cog(Help(bot))  # TestCogにBotを渡してインスタンス化し、Botにコグとして登録する。
