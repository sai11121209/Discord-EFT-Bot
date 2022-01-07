import config
import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext


class Link(commands.Cog):
    guild_ids = [config.guild_ids]
    # TestCogクラスのコンストラクタ。Botを受取り、インスタンス変数として保持。
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(
        name="top",
        description="EFT公式サイト表示",
        guild_ids=guild_ids,
    )
    async def top(self, ctx: SlashContext):
        text = "www.escapefromtarkov.com"
        embed = discord.Embed(
            title="Escape from Tarkov official page",
            url="https://www.escapefromtarkov.com/",
            description=text,
            color=0x2ECC69,
        )
        embed.set_thumbnail(
            url="https://www.escapefromtarkov.com/themes/eft/images/eft_logo_promo.jpg"
        )
        sendMessage = await ctx.send(embed=embed)
        await sendMessage.add_reaction("❌")

    @cog_ext.cog_slash(
        name="jawiki",
        description="日本EFTWikiサイト表示",
        guild_ids=guild_ids,
    )
    async def jawiki(self, ctx: SlashContext):
        text = "wikiwiki.jp"
        embed = discord.Embed(
            title="日本Escape from Tarkov WIKI",
            url=self.bot.jaWikiUrl,
            description=text,
            color=0x2ECC69,
        )
        embed.set_thumbnail(
            url="https://www.escapefromtarkov.com/themes/eft/images/eft_logo_promo.jpg"
        )
        sendMessage = await ctx.send(embed=embed)
        await sendMessage.add_reaction("❌")

    @cog_ext.cog_slash(
        name="enwiki",
        description="海外EFTWikiサイト表示",
        guild_ids=guild_ids,
    )
    async def enwiki(self, ctx: SlashContext):
        text = "The Official Escape from Tarkov Wiki"
        embed = discord.Embed(
            title="海外Escape from Tarkov WIKI",
            url=self.bot.enWikiUrl + "Escape_from_Tarkov_Wiki",
            description=text,
            color=0x2ECC69,
        )
        embed.set_thumbnail(
            url="https://static.wikia.nocookie.net/escapefromtarkov_gamepedia/images/b/bc/Wiki.png/revision/latest/scale-to-width-down/200?cb=20200612143203"
        )
        sendMessage = await ctx.send(embed=embed)
        await sendMessage.add_reaction("❌")

    @cog_ext.cog_slash(
        name="market",
        description="フリーマーケット情報表示",
        guild_ids=guild_ids,
    )
    async def market(self, ctx: SlashContext):
        text = "Actual prices, online monitoring, hideout, charts, price history"
        embed = discord.Embed(
            title="Tarkov Market フリーマーケット情報",
            url="https://tarkov-market.com/",
            description=text,
            color=0x2ECC69,
        )
        sendMessage = await ctx.send(embed=embed)
        await sendMessage.add_reaction("❌")

    @cog_ext.cog_slash(
        name="loadouts",
        description="ロードアウト作成",
        guild_ids=guild_ids,
    )
    async def loadouts(self, ctx: SlashContext):
        text = "Actual prices, online monitoring, hideout, charts, price history"
        embed = discord.Embed(
            title="Tarkov Market ロードアウト作成",
            url="https://tarkov-market.com/loadouts/weapon",
            description=text,
            color=0x2ECC69,
        )
        sendMessage = await ctx.send(embed=embed)
        await sendMessage.add_reaction("❌")

    @cog_ext.cog_slash(
        name="tarkovtools",
        description="TarkovTools情報表示",
        guild_ids=guild_ids,
    )
    async def tarkovtools(self, ctx: SlashContext):
        text = "Visualization of all ammo types in Escape from Tarkov, along with maps and other great tools"
        embed = discord.Embed(
            title="Tarkov Tools",
            url="https://tarkov-tools.com/",
            description=text,
            color=0x2ECC69,
        )
        embed.add_field(
            name="Tarkov-Tools",
            value="> [Tarkov-Tools携帯リモート操作リンク](https://tarkov-tools.com/control/)",
        )
        sendMessage = await ctx.send(embed=embed)
        await sendMessage.add_reaction("❌")

    @cog_ext.cog_slash(
        name="source",
        description="ソースコード表示",
        guild_ids=guild_ids,
    )
    async def source(self, ctx: SlashContext):
        text = "Contribute to sai11121209/Discord-EFT-Bot development by creating an account on GitHub."
        embed = discord.Embed(
            title="GitHub",
            url="https://github.com/sai11121209/Discord-EFT-Bot",
            description=text,
            color=0x2ECC69,
        )
        embed.set_thumbnail(
            url="https://avatars.githubusercontent.com/u/55883274?s=400&v=4"
        )
        sendMessage = await ctx.send(embed=embed)
        await sendMessage.add_reaction("❌")


# Bot本体側からコグを読み込む際に呼び出される関数。
def setup(bot):
    bot.add_cog(Link(bot))  # TestCogにBotを渡してインスタンス化し、Botにコグとして登録する。
