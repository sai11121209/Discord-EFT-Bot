import config
import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.model import SlashCommandPermissionType
from discord_slash.utils.manage_commands import create_permission


class Develop(commands.Cog):
    guild_ids = [config.guild_ids]
    # TestCogクラスのコンストラクタ。Botを受取り、インスタンス変数として保持。
    def __init__(self, bot):
        self.bot = bot

    # コマンドの作成。コマンドはcommandデコレータで必ず修飾する。
    @cog_ext.cog_slash(
        name="develop",
        description="開発用(実行権限制限あり)",
        permissions={
            616231205032951825: [
                create_permission(
                    848998133882159174, SlashCommandPermissionType.ROLE, True
                ),
            ]
        },
        guild_ids=guild_ids,
    )
    async def develop(self, ctx: SlashContext):
        if self.bot.LOCAL_HOST == False:
            self.bot.developMode = not self.bot.developMode
            text = f"開発モード: {self.bot.developMode}"
            if self.bot.developMode:
                await self.bot.change_presence(
                    status=discord.Status.dnd,
                    activity=discord.Activity(name="機能改善会議(メンテナンス中)", type=5),
                )
                self.bot.enrageCounter = 0
            else:
                await self.bot.change_presence(
                    status=discord.Status.online,
                    activity=discord.Game(name="Escape from Tarkov", type=1),
                )
            sendMessage = await ctx.send(text)
            await sendMessage.add_reaction("❌")


# Bot本体側からコグを読み込む際に呼び出される関数。
def setup(bot):
    bot.add_cog(Develop(bot))  # TestCogにBotを渡してインスタンス化し、Botにコグとして登録する。
