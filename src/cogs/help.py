import time
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
            embed = discord.Embed(
                title="EFT(Escape from Tarkov) Wiki Bot使用可能コマンド一覧だよ!",
                description=f"```Prefix:{self.bot.command_prefix}```",
                color=0x2ECC69,
                timestamp=datetime.datetime.utcfromtimestamp(
                    dt.strptime(
                        list(self.bot.patchNotes.keys())[0].split(":", 1)[1] + "+09:00",
                        "%Y/%m/%d %H:%M%z",
                    ).timestamp()
                ),
            )
            for command in self.bot.all_commands:
                if self.bot.all_commands[command].name == "weapon":
                    text = f"```{self.bot.command_prefix}{self.bot.all_commands[command].name}```"
                    text += "```/weapon {武器名}```"
                elif self.bot.all_commands[command].name == "market":
                    text = f"```{self.bot.command_prefix}{self.bot.all_commands[command].name}```"
                    text += "```!p {アイテム名}```"
                elif self.bot.all_commands[command].name == "map":
                    text = f"```{self.bot.command_prefix}{self.bot.all_commands[command].name}```"
                    text += "```/map {マップ名}```"
                elif self.bot.all_commands[command].name == "task":
                    text = f"```{self.bot.command_prefix}{self.bot.all_commands[command].name}```"
                    text += "```/task {タスク名}```"
                else:
                    text = f"```{self.bot.command_prefix}{self.bot.all_commands[command].name}```"
                if self.bot.all_commands[command].name != "help":
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
            embed.set_footer(text="EFT Wiki Bot最終更新")
            self.bot.helpEmbed = await ctx.send(embed=embed)
            await self.bot.helpEmbed.add_reaction("❌")


# Bot本体側からコグを読み込む際に呼び出される関数。
def setup(bot):
    bot.add_cog(Help(bot))  # TestCogにBotを渡してインスタンス化し、Botにコグとして登録する。
