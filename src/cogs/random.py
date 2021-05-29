import random as r
import discord
from discord.ext import commands


class Random(commands.Cog):

    # TestCogクラスのコンストラクタ。Botを受取り、インスタンス変数として保持。
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="マップ抽選")
    async def randommap(self, ctx):
        async with ctx.typing():
            embed = discord.Embed(
                title="迷ったときのEFTマップ抽選",
                description=f"{ctx.author.name}が赴くマップは...",
                color=0x2ECC69,
            )
            map = r.choice(list(self.bot.mapList)).lower()
            embed.add_field(name="MAP", value=map, inline=False)
            await ctx.send(embed=embed)
            await self.bot.all_commands["map"](ctx, map)

    @commands.command(description="武器抽選")
    async def randomweapon(self, ctx):
        async with ctx.typing():
            embed = discord.Embed(
                title="迷ったときのEFT武器抽選",
                description=f"{ctx.author.name}が使用する武器は...",
                color=0x2ECC69,
            )
            weapon = r.choice(self.bot.weaponsName)
            embed.add_field(name="WEAPON", value=weapon, inline=False)
            await ctx.send(embed=embed)
            await self.bot.all_commands["weapon"](ctx, weapon)


# Bot本体側からコグを読み込む際に呼び出される関数。
def setup(bot):
    bot.add_cog(Random(bot))  # TestCogにBotを渡してインスタンス化し、Botにコグとして登録する。