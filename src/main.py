# インストールした discord.py を読み込む
import os
import pytz
import discord
import random
import difflib
import itertools
import pandas as pd
import requests as rq
import datetime
from matplotlib import pyplot as plt
from datetime import datetime as dt
from dateutil.relativedelta import relativedelta
from bs4 import BeautifulSoup


try:
    from local_settings import *
except ImportError:
    import keep_alive

    keep_alive.keep_alive()


# 自分のBotのアクセストークンに置き換えてください
if os.getenv("TOKEN"):
    TOKEN = os.getenv("TOKEN")


# 接続に必要なオブジェクトを生成
client = discord.Client()
prefix = "/"
url = "https://wikiwiki.jp/eft/"
sendTemplatetext = "EFT(Escape from Tarkov) Wiki "
receivedtext = None
maps = [
    "FACTORY",
    "WOODS",
    "CUSTOMS",
    "SHORELINE",
    "INTERCHANGE",
    "LABORATORY",
    "RESERVE",
]
# 新規コマンド追加時は必ずcommandListに追加
commandList = {
    "EFT公式サイト表示": ["TOP"],
    "EFT日本語Wikiトップ表示": ["WIKITOP"],
    "マップ一覧表示": ["MAP"],
    "各マップ情報表示": maps,
    "武器一覧表示": ["WEAPON"],
    "各武器詳細表示": [],
    "弾薬性能表示": ["AMMO"],
    "フリーマーケット情報表示": ["MARKET"],
    "各アイテムのフリーマーケット価格表示": [],
    "タスク一覧表示": ["TASK"],
    "マップ抽選": ["RANDOM"],
    "早見表表示": ["CHART"],
    "更新履歴表示": ["PATCH"],
    "現在時刻表示": ["NOW"],
    "ビットコイン価格表示": ["BTC"],
    "ソースコード表示": ["SOURCE"],
}
# 上に追記していくこと
patchNotes = {
    "2021/03/23": ["内部処理エラーによる 'WEAPON' コマンドの修正"],
    "2021/03/19": [
        "ビットコイン価格表示コマンド 'BTC' を追加しました。",
        "メンテナンス関連のアナウンスがあった場合、テキストチャンネル 'escape-from-tarkov' に通知を送るようにしました。",
    ],
    "2021/03/17": ["現在時刻表示コマンド 'NOW' を追加しました。"],
    "2021/03/15": ["フリーマーケット情報表示コマンド 'MARKET' を追加しました。"],
    "2021/03/14": ["ボイスチャンネル開始、終了時の通知挙動の修正をしました。 ※最終修正"],
    "2021/03/11": ["ボイスチャンネル開始、終了時の通知挙動の修正をしました。"],
    "2021/03/09": ["BOTがボイスチャンネル開始時に通知をしてくれるようになりました。"],
    "2021/03/06": ["BOTが公式アナウンスを自動的に翻訳してくれるようになりました。"],
    "2021/03/04": ["BOTがよりフレンドリーな返答をするようになりました。"],
    "2021/02/25": ["早見表表示コマンドに2件早見表を追加しました。"],
    "2021/02/23": [f"最初の文字が '{prefix}' 以外の文字の場合コマンドとして認識しないように修正。"],
    "2021/02/10": ["タスク一覧表示コマンド 'TASK' を追加しました。", "弾薬性能表示コマンド 'AMMO' を追加しました。"],
    "2021/02/08": ["一部コマンドのレスポンス内容の変更を行いました。"],
    "2021/02/05": ["一部コマンドを除いたレスポンスの向上"],
    "2021/02/04": [
        "入力されたコマンドに近いコマンドを表示するヒント機能を追加しました。",
        "各武器名を入力することで入力された武器の詳細情報のみにアクセスできるようになりました。",
        "BOTのソースコードにアクセスできるコマンド 'SOURCE' を追加しました。",
    ],
    "2021/02/02": [
        "更新履歴表示コマンド 'PATCH' を追加しました。",
        "武器一覧表示コマンドの挙動を大幅に変更しました。",
        "早見表表示コマンドに料金表を追加しました。",
    ],
    "2021/01/30": ["早見表表示コマンド 'CHART' を追加しました。", "早見表コマンドにアイテム早見表を追加しました。"],
}

# 起動時に動作する処理
@client.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    print("ログインしました")
    await client.change_presence(
        activity=discord.Game(name="Escape from Tarkov", type=1)
    )


# メッセージ受信時に動作する処理
@client.event
async def on_voice_state_update(member, before, after):
    # 本番テキストチャンネル
    channel = client.get_channel(818751361511718942)
    # テストテキストチャンネル
    # channel = client.get_channel(808821063387316254)
    user = str(member).split("#")[0]
    if before.channel == None and after.channel:
        await channel.send(
            f"@everyone {user} がボイスチャンネル {after.channel} にてボイスチャットを開始しました。"
        )
    elif (
        before.channel
        and after.channel
        and before.deaf == after.deaf
        and before.mute == after.mute
        and before.self_deaf == after.self_deaf
        and before.self_mute == after.self_mute
        and before.self_stream == after.self_stream
        and before.self_video == after.self_video
    ):
        await channel.send(
            f"@everyone {user} がボイスチャンネル {before.channel} からボイスチャンネル {after.channel} に移動しました。"
        )
    elif before.channel and after.channel == None:
        await channel.send(f"@everyone {user} がボイスチャンネル {before.channel} を退出しました。")


# メッセージ受信時に動作する処理
@client.event
async def on_message(message):
    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        # 本番テキストチャンネル
        specificChannelId = 811566006132408340
        # テストテキストチャンネル
        # specificChannelId = 808821063387316254
        specificUserId = 803770349908131850
        if (
            message.channel.id == specificChannelId
            and message.author.id != specificUserId
        ):
            # 翻訳文書
            text = message.content
            # 翻訳前言語
            source = "en"
            # 翻訳後言語
            Target = "ja"
            gasUrl = f"https://script.google.com/macros/s/AKfycbxvCS-29LVgrm9-cSynGl19QUIB7jTpzuvFqflus_P0BJtXX80ahLazltfm2rbMGVVs/exec?text={text}&source={source}&target={Target}"
            res = rq.get(gasUrl).json()
            if res["code"] == 200:
                text = "多分英語わからんやろ... 翻訳したるわ。感謝しな\n\n"
                text += res["text"]
                await message.channel.send(text)
            else:
                pass
            if "period" in message.content:
                channel = client.get_channel(803425039864561675)
                text = "@everyone 重要なお知らせかもしれないからこっちにも貼っとくで\n"
                text += message.content
                await channel.send(f"{text}{message.content}")

    elif prefix == message.content[0]:
        if message.content.upper() == f"{prefix}TOP":
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
            await message.channel.send(embed=embed)
            return 0

        elif message.content.upper() == f"{prefix}WIKITOP":
            text = "wikiwiki.jp"
            embed = discord.Embed(
                title="Escape from Tarkov 日本語WIKI",
                url=url,
                description=text,
                color=0x2ECC69,
            )
            embed.set_thumbnail(
                url="https://www.escapefromtarkov.com/themes/eft/images/eft_logo_promo.jpg"
            )
            await message.channel.send(embed=embed)
            return 0

        elif message.content.upper() == f"{prefix}MAP":
            text = ""
            for map in maps:
                text += f"[{map}]({url}{map})\n"
            embed = discord.Embed(
                title="マップ", url=f"{url}", description=text, color=0x2ECC69,
            )
            embed.set_footer(text=f"{prefix}マップ名で各マップの詳細情報にアクセスできるよー。 例: /reserve")
            await message.channel.send(embed=embed)
            return 0

        elif message.content.upper().split("/")[1] in maps:
            receivedtext = message.content.upper().split("/")[1]
            text = f"{sendTemplatetext}{receivedtext} INFORMATION\n"
            text += f"{receivedtext}(EFT 日本語 Wiki URL): {url}{receivedtext}\n"

            if message.content.upper() == "/FACTORY":
                text += "https://cdn.wikiwiki.jp/to/w/eft/img/::attach/Factorymap.jpg"

            if message.content.upper() == "/WOODS":
                text += "https://images-ext-1.discordapp.net/external/NyBjPcCWLdnVfdUSAjWs3aGk4Un8qRAZCjnk3eF_8uo/https/cdn.wikiwiki.jp/to/w/eft/WOODS/%3A%3Aattach/Woods_map_v0.12.9b.jpg"

            if message.content.upper() == "/CUSTOMS":
                text += "https://cdn.wikiwiki.jp/to/w/eft/CUSTOMS/::attach/Customs_0.12.7.jpg"

            if message.content.upper() == "/SHORELINE":
                text += "https://cdn.wikiwiki.jp/to/w/eft/SHORELINE/::attach/ShoreLine_Exit_Loot.jpg\n"
                text += "https://cdn.wikiwiki.jp/to/w/eft/SHORELINE/::attach/resort.jpg"

            if message.content.upper() == "/INTERCHANGE":
                text += (
                    "https://cdn.wikiwiki.jp/to/w/eft/img/::ref/Interchange_map.jpg\n"
                )
                text += "https://cdn.wikiwiki.jp/proxy-image?url=https%3A%2F%2Fwww.eftmaps.net%2Fwp-content%2Fuploads%2F2020%2F05%2Finterchange_map.png"

            if message.content.upper() == "/LABORATORY":
                text += "https://cdn.wikiwiki.jp/to/w/eft/LABORATORY/::ref/111000.png\n"
                text += (
                    "https://cdn.wikiwiki.jp/to/w/eft/LABORATORY/::attach/Labmap.jpg"
                )

            if message.content.upper() == "/RESERVE":
                text += "https://cdn.wikiwiki.jp/to/w/eft/RESERVE/::attach/reserve_map_Translated%20fix.jpg\n"
                text += "https://cdn.wikiwiki.jp/to/w/eft/RESERVE/::attach/800px-3D_map_by_loweffortsaltbox.png\n"
                text += "https://cdn.wikiwiki.jp/to/w/eft/RESERVE/::attach/reservekeys.jpg\n"
                text += "https://cdn.wikiwiki.jp/to/w/eft/RESERVE/::attach/reserveUnderground.jpg"

            await message.channel.send(text)
            return 0

        elif message.content.upper() == f"{prefix}RANDOM":
            embed = discord.Embed(
                title="迷ったときのEFTマップ抽選", description="今回のマップは...", color=0x2ECC69,
            )
            embed.add_field(name="MAP", value=random.choice(maps), inline=False)
            await message.channel.send(embed=embed)
            return 0

        elif message.content.upper() == f"{prefix}HELP":
            embed = discord.Embed(
                title="ヘルプ",
                description="EFT(Escape from Tarkov) Wiki Bot使用可能コマンド一覧だよ!",
                color=0x2ECC69,
            )
            for key, values in commandList.items():
                if key == "各武器詳細表示":
                    text = "/武器名"
                elif key == "各アイテムのフリーマーケット価格表示":
                    text = "!p {アイテム名}"
                else:
                    if type(values) == list:
                        text = ""
                        for value in values:
                            text += f"{prefix}{value}\n"
                    else:
                        text = f"{prefix}{values}\n"
                embed.add_field(name=f"{key}コマンド", value=text, inline=False)
            print(len(embed))
            await message.channel.send(embed=embed)
            return 0

        elif message.content.upper() == f"{prefix}CHART":
            text = "https://cdn.discordapp.com/attachments/803425039864561675/804873530335690802/image0.jpg\n"
            text += "https://cdn.discordapp.com/attachments/803425039864561675/804873530637811772/image1.jpg\n"
            text += "https://cdn.discordapp.com/attachments/616231205032951831/805997840140599366/image0.jpg\n"
            text += "https://cdn.discordapp.com/attachments/808820772536582154/814055787479564318/image0.webp\n"
            text += "https://media.discordapp.net/attachments/808820772536582154/814055787898077215/image1.webp"
            await message.channel.send(text)
            return 0

        elif message.content.upper() == f"{prefix}PATCH":
            embed = discord.Embed(title="更新履歴一覧")
            for index, values in patchNotes.items():
                text = ""
                for N, value in enumerate(values):
                    text += f"{N+1}. {value}\n"
                embed.add_field(name=index, value=text, inline=False)
            embed.set_footer(text=f"最終更新: {list(patchNotes.keys())[0]}")
            print(len(embed))
            await message.channel.send(embed=embed)
            return 0

        elif message.content.upper() == f"{prefix}SOURCE":
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
            await message.channel.send(embed=embed)
            return 0

        elif message.content.upper() == f"{prefix}TASK":
            TraderNames = GetTraderNames()
            text = ""
            for TraderName in TraderNames:
                text += f"[{TraderName}]({url}{TraderName.capitalize()}タスク)\n"
            embed = discord.Embed(
                title="タスク", url=f"{url}タスク", description=text, color=0x2ECC69,
            )
            embed.set_footer(text="トレーダー名をクリックすることで各トレーダータスクの詳細情報にアクセスできるよー。")
            await message.channel.send(embed=embed)
            return 0

        elif message.content.upper() == f"{prefix}AMMO":
            text = "eft.monster"
            embed = discord.Embed(
                title="弾薬性能表",
                url="https://eft.monster/",
                description=text,
                color=0x2ECC69,
            )
            embed.set_thumbnail(url="https://eft.monster/ogre_color.png")
            await message.channel.send(embed=embed)
            return 0

        elif message.content.upper() == f"{prefix}MARKET":
            text = "Actual prices, online monitoring, hideout, charts, price history"
            embed = discord.Embed(
                title="Tarkov Market",
                url="https://tarkov-market.com/",
                description=text,
                color=0x2ECC69,
            )
            await message.channel.send(embed=embed)
            return 0

        elif message.content.upper() == f"{prefix}NOW":
            embed = discord.Embed(
                title="現在時刻", description="主要タイムゾーン時刻", color=0x2ECC69,
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
            await message.channel.send(embed=embed)
            return 0

        elif message.content.upper() == f"{prefix}BTC":
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
            embed = discord.Embed(title="1 ビットコイン → 日本円", color=0xFFFF00,)
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
            embed.set_footer(text="Cryptowat Market REST APIを使用しております。")
            await message.channel.send(embed=embed, file=file)

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
            embed = discord.Embed(title="1 ビットコイン → ルーブル", color=0xFFFF00,)
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
            embed.set_footer(text="Cryptowat Market REST APIを使用しております。")
            await message.channel.send(embed=embed, file=file)
            return 0

        elif message.content.upper() == f"{prefix}WEAPON":
            weaponsName, weaponsData, colName = GetweaponData()
            bulletsData = GetBulletData()
            embeds = []
            for n, (index, values) in enumerate(weaponsData.items()):
                embed = discord.Embed(
                    title=f"武器一覧({n+1}/{len(weaponsData)})", url=f"{url}武器一覧"
                )
                embed.add_field(
                    name=f"{index}",
                    value=f"[{index}wikiリンク]({url}武器一覧#h2_content_1_{n})",
                    inline=False,
                )
                infostr = ""
                for value in values:
                    urlencord = value[0].replace(" ", "%20")
                    infostr += f"[{value[0]}]({url}{urlencord})  "
                    for c, v in zip(colName[index][2:], value[2:]):
                        if c == "使用弾薬":
                            fixName = v.replace("×", "x")
                            fixName = fixName.replace(" ", "")
                            infostr += (
                                f"**{c}**: [{v}]({url}弾薬{bulletsData[fixName]})  "
                            )
                        else:
                            infostr += f"**{c}**: {v}  "
                    embed.add_field(
                        name=value[0], value=infostr, inline=False,
                    )
                    infostr = ""
                embed.set_footer(text=f"Escape from Tarkov 日本語 Wiki: {url}")
                embeds.append(embed)
            for embed in embeds:
                await message.channel.send(embed=embed)
            return 0

        weaponsName, weaponsData, colName = GetweaponData()
        commandList["各武器詳細表示"] = weaponsName
        # コマンドの予測変換
        hints = [
            command
            for command in list(itertools.chain.from_iterable(commandList.values()))
            if difflib.SequenceMatcher(
                None, message.content.upper(), prefix + command
            ).ratio()
            >= 0.65
        ]

        if message.content.upper().split("/")[1] in weaponsName:
            bulletsData = GetBulletData()
            infoStr = ""
            fixtext = message.content.upper().replace(" ", "").split("/")[1]
            weaponName = weaponsName[fixtext]
            urlEncord = weaponName[1].replace(" ", "%20")
            # infoStr += f"[{weaponName[1]}]({url}{urlEncord})  "
            for c, v in zip(colName[weaponName[0]][2:], weaponName[3:]):
                if c == "使用弾薬":
                    fixName = v.replace("×", "x")
                    fixName = fixName.replace(" ", "")
                    infoStr += f"**{c}**: [{v}]({url}弾薬{bulletsData[fixName]})  "
                else:
                    infoStr += f"**{c}**: {v}  "
            embed = discord.Embed(
                title=weaponName[1], url=f"{url}{urlEncord}", description=infoStr
            )
            embed.set_image(url=weaponName[2])
            await message.channel.send(embed=embed)
            return 0

        elif len(hints) > 0:
            text = "Hint: もしかして以下のコマンドじゃね?\n"
            for n, hint in enumerate(hints):
                text += f"{n+1}. {prefix}{hint}\n"
            text += "これ以外に使えるコマンドは /help で確認できるよ!"
            await message.channel.send(text)
            return 0

        else:
            text = "入力されたがコマンドが見つからなかった...ごめんなさい。\n"
            text += "これ以外に使えるコマンドは /help で確認できるよ!"
            await message.channel.send(text)
            return 0
    elif "@everyone BOTの更新をしました!" == message.content:
        embed = discord.Embed(title="更新履歴一覧")
        for index, values in patchNotes.items():
            text = ""
            for N, value in enumerate(values):
                text += f"{N+1}. {value}\n"
            embed.add_field(name=index, value=text, inline=False)
        embed.set_footer(text=f"最終更新: {list(patchNotes.keys())[0]}")
        await message.channel.send(embed=embed)


def GetTraderNames():
    res = rq.get(f"{url}タスク")
    soup = BeautifulSoup(res.text, "lxml", from_encoding="utf-8")
    soup = soup.find("div", {"class": "contents"}).find_all("ul", {"class": "list2"})[1]
    return [s.get_text().replace(" ", "") for s in soup.find_all("a")]


def GetBulletData():
    res = rq.get(f"{url}弾薬")
    soup = BeautifulSoup(res.text, "lxml", from_encoding="utf-8").find(
        "div", {"class": "container-wrapper"}
    )
    exclusion = ["概要", "表の見方", "弾薬の選び方", "拳銃弾", "PDW弾", "ライフル弾", "散弾", "グレネード弾", "未実装"]
    bulletsData = {
        s.get_text()
        .replace(" ", "")
        .replace("Gyurza", "")
        .replace("STs-130", ""): s.get("href")
        for s in soup.find("div", {"class": "contents"}).find("ul").find_all("a")
        if s.get_text().replace(" ", "") not in exclusion
    }
    print(bulletsData)
    return bulletsData


def GetweaponData():
    res = rq.get(f"{url}武器一覧")
    soup = BeautifulSoup(res.text, "lxml", from_encoding="utf-8").find(
        "div", {"class": "container-wrapper"}
    )
    exclusion = ["", "開発進行中", "企画中", "コメント", "削除済み"]
    colName = {}
    weaponsData = {
        s.get_text().replace(" ", ""): []
        for s in soup.find("div", {"class": "contents"}).find_all("a")
        if s.get_text().replace(" ", "") not in exclusion
    }
    for index, s in zip(
        weaponsData, soup.find_all("div", {"class": "wikiwiki-tablesorter-wrapper"}),
    ):
        weaponData = []
        newInfoData = []
        oldInfoData = []
        colName_soup = s.find("tr").find_all("strong")
        colName[index] = [str.get_text() for str in colName_soup]
        for i in s.find("tbody").find_all("tr"):
            newInfoData = [
                j.find("img")["src"] if j.find("img") else j.get_text()
                for j in i.find_all("td")
            ]
            if len(i.find_all("td")) == 2:
                newInfoData += oldInfoData[2:]
            oldInfoData = newInfoData
            weaponData.append(newInfoData)
        weaponsData[index] = weaponData
    weaponsName = {
        value[0]: [key] + value
        for key, values in weaponsData.items()
        for value in values
    }
    return weaponsName, weaponsData, colName


# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)
