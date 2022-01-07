import config
import random as r
import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext


class Random(commands.Cog):
    guild_ids = [config.guild_ids]
    # TestCogクラスのコンストラクタ。Botを受取り、インスタンス変数として保持。
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(
        name="randommap",
        description="マップ抽選",
        guild_ids=guild_ids,
    )
    async def randommap(self, ctx: SlashContext):
        async with ctx.typing():
            embed = discord.Embed(
                title="迷ったときのEFTマップ抽選",
                description=f"{ctx.author.mention}が赴くマップは...",
                color=0x2ECC69,
            )
            map = r.choice(
                [key for key, val in self.bot.mapData.items() if val["Duration"] != ""]
            ).lower()
            embed.add_field(name="MAP", value=map, inline=False)
            sendMessage = await ctx.send(embed=embed)
            await sendMessage.add_reaction("❌")
            await self.bot.all_commands["map"](ctx, [map])

    @cog_ext.cog_slash(
        name="randomweapon",
        description="武器抽選",
        guild_ids=guild_ids,
    )
    async def randomweapon(self, ctx: SlashContext):
        async with ctx.typing():
            embed = discord.Embed(
                title="迷ったときのEFT武器抽選",
                description=f"{ctx.author.mention}が使用する武器は...",
                color=0x2ECC69,
            )
            weapon = r.choice(self.bot.weaponsName)
            embed.add_field(name="WEAPON", value=weapon, inline=False)
            sendMessage = await ctx.send(embed=embed)
            await sendMessage.add_reaction("❌")
            await self.bot.all_commands["weapon"](ctx, [weapon])


# Bot本体側からコグを読み込む際に呼び出される関数。
def setup(bot):
    bot.add_cog(Random(bot))  # TestCogにBotを渡してインスタンス化し、Botにコグとして登録する。
