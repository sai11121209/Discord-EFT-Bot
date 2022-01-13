import config
import discord
import datetime
from discord.ext import commands
from datetime import datetime as dt
from discord_slash import cog_ext, SlashContext


class Help(commands.Cog):
    guild_ids = [config.guild_ids]
    # TestCogクラスのコンストラクタ。Botを受取り、インスタンス変数として保持。
    def __init__(self, bot):
        self.bot = bot

    # コマンドの作成。コマンドはcommandデコレータで必ず修飾する。
    @cog_ext.cog_slash(
        name="help",
        description="使用可能コマンド表示",
        guild_ids=guild_ids,
    )
    async def help(self, ctx: SlashContext):
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
        for command in self.bot.slash.commands:
            try:
                if command == "weapon":
                    text = f"```{self.bot.command_prefix}{command}```"
                    text += "```/weapon {武器名}```"
                elif command == "market":
                    text = f"```{self.bot.command_prefix}{command}```"
                    text += "```!p {アイテム名}```"
                elif command == "map":
                    text = f"```{self.bot.command_prefix}{command}```"
                    text += "```/map {マップ名}```"
                elif command == "task":
                    text = f"```{self.bot.command_prefix}{command}```"
                    text += "```/task {タスク名}```"
                else:
                    text = f"```{self.bot.command_prefix}{command}```"
                if command != "help":
                    embed.add_field(
                        name=f"{self.bot.slash.commands[command].description}コマンド",
                        value=text,
                    )
            except:
                pass
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
