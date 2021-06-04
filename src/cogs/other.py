import pytz
import discord
import datetime
import pandas as pd
import requests as rq
from discord.ext import commands
from datetime import datetime as dt
from matplotlib import pyplot as plt
from dateutil.relativedelta import relativedelta


class Other(commands.Cog):

    # TestCogクラスのコンストラクタ。Botを受取り、インスタンス変数として保持。
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="パッチノート表示")
    async def patch(self, ctx):
        async with ctx.typing():
            if self.bot.notificationInformation:
                embed = discord.Embed(
                    title="近日大規模なアップデートが行われる予定です。",
                    description="近日行われるアップデートでは以下の機能が変更又は追加される予定です。\n※アップデートに伴い現在テストバージョンでの処理となっているため**一部又は全体の動作が不安定**になる恐れがあります。",
                    color=0xFF0000,
                    timestamp=datetime.datetime.utcfromtimestamp(
                        dt.strptime(
                            list(self.bot.patchNotes.keys())[0].split(":", 1)[1]
                            + "+09:00",
                            "%Y/%m/%d %H:%M%z",
                        ).timestamp()
                    ),
                )
                text = ""
                for index, values in self.bot.notificationInformation.items():
                    for N, value in enumerate(values):
                        text += f"{N+1}. {value}\n"
                embed.add_field(
                    name=f"version: {index.split(':', 1)[0]}", value=text, inline=False
                )
                embed.set_author(
                    name="EFT(Escape from Tarkov) Wiki Bot",
                    url="https://github.com/sai11121209",
                    # icon_url=client.get_user(279995095124803595).avatar_url,
                )
                embed.set_footer(text=f"EFT Wiki Bot最終更新")
                await ctx.send(embed=embed)
            embed = discord.Embed(
                title="更新履歴一覧",
                timestamp=datetime.datetime.utcfromtimestamp(
                    dt.strptime(
                        list(self.bot.patchNotes.keys())[0].split(":", 1)[1] + "+09:00",
                        "%Y/%m/%d %H:%M%z",
                    ).timestamp()
                ),
            )
            for index, values in self.bot.patchNotes.items():
                text = ""
                for N, value in enumerate(values):
                    text += f"{N+1}. {value}\n"
                embed.add_field(
                    name=f"version: {index.split(':', 1)[0]}", value=text, inline=False
                )
            # embed.set_thumbnail(url=client.get_user(803770349908131850).avatar_url)
            embed.set_author(
                name="EFT(Escape from Tarkov) Wiki Bot",
                url="https://github.com/sai11121209",
                # icon_url=client.get_user(279995095124803595).avatar_url,
            )
            embed.set_footer(text=f"EFT Wiki Bot最終更新")
            await ctx.send(embed=embed)

    @commands.command(description="現在時刻表示")
    async def now(self, ctx):
        async with ctx.typing():
            embed = discord.Embed(
                title="現在時刻",
                description="主要タイムゾーン時刻",
                color=0x2ECC69,
            )
            embed.add_field(
                name="日本時間(JST)",
                value=dt.now().strftime("%Y/%m/%d %H:%M:%S"),
                inline=False,
            )
            embed.add_field(
                name="モスクワ時間(EAT)",
                value=dt.now(
                    datetime.timezone(datetime.timedelta(hours=3), name="EAT")
                ).strftime("%Y/%m/%d %H:%M:%S"),
                inline=False,
            )
            embed.add_field(
                name="太平洋標準時刻(PST)",
                value=dt.now(
                    datetime.timezone(datetime.timedelta(hours=-8), name="PST")
                ).strftime("%Y/%m/%d %H:%M:%S"),
                inline=False,
            )
            embed.add_field(
                name="太平洋夏時刻(PDT)",
                value=dt.now(
                    datetime.timezone(datetime.timedelta(hours=-7), name="PDT")
                ).strftime("%Y/%m/%d %H:%M:%S"),
                inline=False,
            )
            embed.set_footer(text="夏時間は3月の第2日曜日午前2時から11月の第1日曜日午前2時まで。")
            await ctx.send(embed=embed)

    @commands.command(description="ビットコイン価格表示")
    async def btc(self, ctx):
        async with ctx.typing():
            timestamp = (
                dt.now(pytz.timezone("Asia/Tokyo")) - relativedelta(months=1)
            ).timestamp()
            summaryJpy = rq.get(
                "https://api.cryptowat.ch/markets/bitflyer/btcjpy/summary"
            ).json()["result"]
            btcJpyData = rq.get(
                f"https://api.cryptowat.ch/markets/bitflyer/btcjpy/ohlc?periods=1800&after={int(timestamp)}"
            ).json()["result"]
            btcData = pd.DataFrame(btcJpyData["1800"])
            btcData[0] = pd.to_datetime(btcData[0].astype(int), unit="s")
            plt.figure(figsize=(15, 10), dpi=100)
            plt.plot(btcData[0], btcData[1], label="OpenPrice")
            plt.plot(btcData[0], btcData[2], label="HighPrice")
            plt.plot(btcData[0], btcData[3], label="LowPrice")
            plt.title("BTC_JPY Rate")
            plt.grid(axis="y", linestyle="dotted", color="b")
            plt.tight_layout()
            plt.legend()
            plt.savefig("btc_jpy.png")
            plt.close()
            BtcJpyPrice = rq.get(
                "https://api.cryptowat.ch/markets/bitflyer/btcjpy/price"
            ).json()["result"]["price"]
            file = discord.File("btc_jpy.png")
            embed = discord.Embed(
                title="1 ビットコイン → 日本円",
                color=0xFFFF00,
                timestamp=datetime.datetime.utcfromtimestamp(
                    dt.now(pytz.timezone("Asia/Tokyo")).timestamp()
                ),
            )
            embed.set_image(url="attachment://btc_jpy.png")
            embed.add_field(name="現在の金額", value="{:,}".format(BtcJpyPrice) + " 円")
            embed.add_field(
                name="0.2BTCあたりの金額",
                value="約 " + "{:,}".format(int(BtcJpyPrice * 0.2)) + " 円",
            )
            embed.add_field(
                name="最高値", value="{:,}".format(summaryJpy["price"]["high"]) + " 円"
            )
            embed.add_field(
                name="最安値", value="{:,}".format(summaryJpy["price"]["low"]) + " 円"
            )
            embed.set_footer(text="Cryptowat Market REST APIを使用しております。取得日時")
            await ctx.send(embed=embed, file=file)

            BtcRubData = rq.get(
                f"https://api.cryptowat.ch/markets/cexio/btcrub/ohlc?periods=1800&after={int(timestamp)}"
            ).json()["result"]
            btcData = pd.DataFrame(BtcRubData["1800"])
            btcData[0] = pd.to_datetime(btcData[0].astype(int), unit="s")
            plt.figure(figsize=(15, 10), dpi=100)
            plt.plot(btcData[0], btcData[1], label="OpenPrice")
            plt.plot(btcData[0], btcData[2], label="HighPrice")
            plt.plot(btcData[0], btcData[3], label="LowPrice")
            plt.title("BTC_RUB Rate")
            plt.grid(axis="y", linestyle="dotted", color="b")
            plt.tight_layout()
            plt.legend()
            plt.savefig("btc_rub.png")
            plt.close()
            BtcRubPrice = rq.get(
                "https://api.cryptowat.ch/markets/cexio/btcrub/price"
            ).json()["result"]["price"]
            file = discord.File("btc_rub.png")
            embed = discord.Embed(
                title="1 ビットコイン → ルーブル",
                color=0xFFFF00,
                timestamp=datetime.datetime.utcfromtimestamp(
                    dt.now(pytz.timezone("Asia/Tokyo")).timestamp()
                ),
            )
            embed.set_image(url="attachment://btc_rub.png")
            embed.add_field(name="現在の金額", value="{:,}".format(BtcRubPrice) + " RUB")
            embed.add_field(
                name="0.2BTCあたりの金額",
                value="約 " + "{:,}".format(int(BtcRubPrice * 0.2)) + " RUB",
            )
            embed.add_field(
                name="最高値", value="{:,}".format(summaryJpy["price"]["high"]) + " RUB"
            )
            embed.add_field(
                name="最安値", value="{:,}".format(summaryJpy["price"]["low"]) + " RUB"
            )
            embed.set_footer(text="Cryptowat Market REST APIを使用しております。取得日時")
            await ctx.send(embed=embed, file=file)


# Bot本体側からコグを読み込む際に呼び出される関数。
def setup(bot):
    bot.add_cog(Other(bot))  # TestCogにBotを渡してインスタンス化し、Botにコグとして登録する。