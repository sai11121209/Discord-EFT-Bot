import discord
from discord.ext import commands


class Link(commands.Cog):

    # TestCogクラスのコンストラクタ。Botを受取り、インスタンス変数として保持。
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="EFT公式サイト表示")
    async def top(self, ctx):
        async with ctx.typing():
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
            await ctx.send(embed=embed)

    @commands.command(description="日本EFTWikiサイト表示")
    async def jawiki(self, ctx):
        async with ctx.typing():
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
            await ctx.send(embed=embed)

    @commands.command(description="海外EFTWikiサイト表示")
    async def enwiki(self, ctx):
        async with ctx.typing():
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
            await ctx.send(embed=embed)

    @commands.command(description="フリーマーケット情報表示")
    async def market(self, ctx):
        async with ctx.typing():
            text = "Actual prices, online monitoring, hideout, charts, price history"
            embed = discord.Embed(
                title="Tarkov Market",
                url="https://tarkov-market.com/",
                description=text,
                color=0x2ECC69,
            )
            await ctx.send(embed=embed)

    @commands.command(description="TarkovTools情報表示")
    async def tarkovtools(self, ctx):
        async with ctx.typing():
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
            await ctx.send(embed=embed)

    @commands.command(description="ソースコード表示")
    async def source(self, ctx):
        async with ctx.typing():
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
            await ctx.send(embed=embed)


# Bot本体側からコグを読み込む際に呼び出される関数。
def setup(bot):
    bot.add_cog(Link(bot))  # TestCogにBotを渡してインスタンス化し、Botにコグとして登録する。