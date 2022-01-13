import config
import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext


class Character(commands.Cog):
    guild_ids = [config.guild_ids]
    # TestCogクラスのコンストラクタ。Botを受取り、インスタンス変数として保持。
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(
        name="dealers",
        description="ディーラー一覧表示",
        guild_ids=guild_ids,
    )
    async def dealers(self, ctx: SlashContext):
        embed = discord.Embed(
            title="ディーラー",
            url=f"{self.bot.enWikiUrl}Characters#Dealers",
            color=0x808080,
            timestamp=self.bot.updateTimestamp,
        )
        for TraderName in self.bot.traderNames:
            trader = self.bot.traderList[TraderName]
            text = f"**本名**: __{trader['fullname']}__\n"
            if (
                "A network of outlets all over Tarkov and its outskirts"
                != trader["location"]
            ):
                text += f"**場所**: __[{trader['location']}]({self.bot.enWikiUrl}{trader['location'].replace(' ', '_')})__\n"
            else:
                text += f"**場所**: __{trader['location']}__\n"
            text += f"**出身地**: __{trader['origin']}__\n"
            text += "**取り扱い品**:\n"
            for ware in trader["wares"]:
                text += f"・__{ware}__\n"
            if trader["services"]:
                text += "**サービス**:\n"
                for service in trader["services"]:
                    text += f"・__{service}__\n"
            else:
                text += "**サービス**: 無し\n"
            text += f"**通貨**:\n"
            for currencie in trader["currencies"]:
                text += f"・__{currencie}__\n"
                # TraderName.capitalize()
            text += f"**タスク情報**: [JA]({self.bot.jaWikiUrl}{TraderName}タスク) / [EN]({self.bot.enWikiUrl}Quests)\n"
            text += f"**詳細情報**: [EN]({self.bot.enWikiUrl}{TraderName})"
            embed.add_field(
                name=f"<:{TraderName}:{trader['stampid']}> {TraderName}",
                value=text,
            )
        embed.set_author(
            name="EFT(Escape from Tarkov) Wiki Bot",
            url="https://github.com/sai11121209",
            # icon_url=client.get_user(279995095124803595).avatar_url,
        )
        embed.set_footer(
            text="トレーダー名をクリックすることで各トレーダータスクの詳細情報にアクセスできるよー。",
        )
        sendMessage = await ctx.send(embed=embed)
        await sendMessage.add_reaction("❌")

    @cog_ext.cog_slash(
        name="boss",
        description="ボス一覧表示",
        guild_ids=guild_ids,
    )
    async def boss(self, ctx):
        embed = discord.Embed(
            title="ボス",
            url=f"{self.bot.enWikiUrl}Characters#Bosses",
            color=0x808080,
            timestamp=self.bot.updateTimestamp,
        )
        for bossName in self.bot.bossNames:
            try:
                boss = self.bot.bossList[bossName]
                text = ""
                text += "**場所**:"
                if len(boss["location"]) == 1:
                    text += f"__[{boss['location'][0]}]({self.bot.enWikiUrl}{boss['location'][0]})__\n"
                    text += (
                        f"**出現確率**: __{boss['pawnchance'][boss['location'][0]]}%__\n"
                    )
                else:
                    text += "\n"
                    for location in boss["location"]:
                        text += f"・__[{location}]({self.bot.enWikiUrl}{location})__\n"
                    text += f"**出現確率**:\n"
                    for location in boss["location"]:
                        text += (
                            f"・__{location}__: __{boss['pawnchance'][location]}%__\n"
                        )
                text += "**レアドロップ**:\n"
                for drop in boss["drops"]:
                    text += (
                        f"・__[{drop}]({self.bot.enWikiUrl}{drop.replace(' ', '_')})__\n"
                    )
                text += f"**護衛**: {boss['followers']}人\n"
                if bossName != "CultistPriest":
                    text += f"**詳細情報**: [EN]({self.bot.enWikiUrl}{bossName})"
                else:
                    text += f"**詳細情報**: [EN]({self.bot.enWikiUrl}Cultists)"
                embed.add_field(
                    name=f"<:{bossName}:{boss['stampid']}> {bossName}",
                    value=text,
                )
            except:
                pass
        embed.set_author(
            name="EFT(Escape from Tarkov) Wiki Bot",
            url="https://github.com/sai11121209",
            # icon_url=client.get_user(279995095124803595).avatar_url,
        )
        embed.set_footer(
            text="ボス名をクリックすることで各ボスの詳細情報にアクセスできるよー。",
        )
        sendMessage = await ctx.send(embed=embed)
        await sendMessage.add_reaction("❌")


# Bot本体側からコグを読み込む際に呼び出される関数。
def setup(bot):
    bot.add_cog(Character(bot))  # TestCogにBotを渡してインスタンス化し、Botにコグとして登録する。
