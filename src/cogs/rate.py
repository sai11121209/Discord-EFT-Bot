import json
import time
import pytz
import config
import discord
import datetime
import requests as rq
from pytz import timezone
from bs4 import BeautifulSoup
from discord.ext import commands
from datetime import datetime as dt
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option


class Rate(commands.Cog):
    guild_ids = [config.guild_ids]
    rate_euro_options = [
        create_option(
            name="price",
            description="ユーロの値段を入力。",
            option_type=4,  # int
            required=True,
        ),
    ]
    rate_dollar_options = [
        create_option(
            name="price",
            description="ドルの値段を入力。",
            option_type=4,  # int
            required=True,
        ),
    ]
    # TestCogクラスのコンストラクタ。Botを受取り、インスタンス変数として保持。
    def __init__(self, bot):
        self.bot = bot

    def GetRate(self, name):
        res = rq.get(f"{self.bot.marketUrl}{name}")
        soup = BeautifulSoup(res.text, "lxml")
        return soup.find("div", {"class": "bold alt"}).get_text().replace("₽", "")

    @cog_ext.cog_slash(
        name="rate",
        description="EFT為替レートを表示",
        guild_ids=guild_ids,
    )
    async def rate(self, ctx: SlashContext):
        embed = discord.Embed(
            title=f"為替レート取得中",
            timestamp=datetime.datetime.utcfromtimestamp(
                dt.now(pytz.timezone("Asia/Tokyo")).timestamp()
            ),
            description="為替レート情報取得中です。しばらくお待ちください。",
        )
        load_embed = await ctx.send(embed=embed)
        await load_embed.add_reaction("❌")
        euro = self.GetRate("euros")
        dollar = self.GetRate("dollars")
        embed = discord.Embed(
            title=f"EFT為替レート",
            color=0x808080,
        )
        embed.add_field(
            name="ユーロ値段",
            value=f"{euro}₽",
        )
        embed.add_field(
            name="ドル値段",
            value=f"{dollar}₽",
        )
        embed.set_footer(text=f"提供元: {self.bot.marketUrl}")
        await load_embed.edit(embed=embed)

    @cog_ext.cog_subcommand(
        base="rate",
        name="euro",
        description="EUR → RUB 為替レート計算",
        options=rate_euro_options,
        guild_ids=guild_ids,
    )
    async def rate_euro(self, ctx: SlashContext, price: int):
        embed = discord.Embed(
            title=f"為替レート取得中",
            timestamp=datetime.datetime.utcfromtimestamp(
                dt.now(pytz.timezone("Asia/Tokyo")).timestamp()
            ),
            description="為替レート情報取得中です。しばらくお待ちください。",
        )
        load_embed = await ctx.send(embed=embed)
        await load_embed.add_reaction("❌")
        euro = self.GetRate("euros")
        embed = discord.Embed(
            title=f"RUB → EUR 為替レート計算",
            color=0x808080,
        )
        embed.add_field(
            name="ユーロ値段",
            value=f"{price}€",
        )
        embed.add_field(
            name="換算ルーブル値段",
            value=f"{int(euro)*price}₽",
        )
        embed.set_footer(text=f"提供元: {self.bot.marketUrl}")
        await load_embed.edit(embed=embed)

    @cog_ext.cog_subcommand(
        base="rate",
        name="dollar",
        description="USD → RUB 為替レート計算",
        options=rate_dollar_options,
        guild_ids=guild_ids,
    )
    async def rate_dollar(self, ctx: SlashContext, price: int):
        embed = discord.Embed(
            title=f"為替レート取得中",
            timestamp=datetime.datetime.utcfromtimestamp(
                dt.now(pytz.timezone("Asia/Tokyo")).timestamp()
            ),
            description="為替レート情報取得中です。しばらくお待ちください。",
        )
        load_embed = await ctx.send(embed=embed)
        await load_embed.add_reaction("❌")
        dollar = self.GetRate("dollars")
        embed = discord.Embed(
            title=f"EFT為替レート",
            color=0x808080,
        )
        embed.add_field(
            name="ドル値段",
            value=f"{price}$",
        )
        embed.add_field(
            name="換算ルーブル値段",
            value=f"{int(dollar)*price}₽",
        )
        embed.set_footer(text=f"提供元: {self.bot.marketUrl}")
        await load_embed.edit(embed=embed)


# Bot本体側からコグを読み込む際に呼び出される関数。
def setup(bot):
    bot.add_cog(Rate(bot))  # TestCogにBotを渡してインスタンス化し、Botにコグとして登録する。
