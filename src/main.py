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
Prefix = "/"
Url = "https://wikiwiki.jp/eft/"
SendTemplateText = "EFT(Escape from Tarkov) Wiki "
ReceivedText = None
Maps = [
    "FACTORY",
    "WOODS",
    "CUSTOMS",
    "SHORELINE",
    "INTERCHANGE",
    "LABORATORY",
    "RESERVE",
]
# 新規コマンド追加時は必ずCommandListに追加
CommandList = {
    "EFT公式サイト表示": ["TOP"],
    "EFT日本語Wikiトップ表示": ["WIKITOP"],
    "マップ一覧表示": ["MAP"],
    "各マップ情報表示": Maps,
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
PatchNotes = {
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
    "2021/02/23": [f"最初の文字が '{Prefix}' 以外の文字の場合コマンドとして認識しないように修正。"],
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
    print("before")
    print(before)
    print("after")
    print(after)
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
        SpecificChannelId = 811566006132408340
        # テストテキストチャンネル
        # SpecificChannelId = 808821063387316254
        SpecificUserId = 803770349908131850
        if (
            message.channel.id == SpecificChannelId
            and message.author.id != SpecificUserId
        ):
            # 翻訳文書
            Text = message.content
            # 翻訳前言語
            Source = "en"
            # 翻訳後言語
            Target = "ja"
            url = f"https://script.google.com/macros/s/AKfycbxvCS-29LVgrm9-cSynGl19QUIB7jTpzuvFqflus_P0BJtXX80ahLazltfm2rbMGVVs/exec?text={Text}&source={Source}&target={Target}"
            Res = rq.get(url).json()
            if Res["code"] == 200:
                Text = "多分英語わからんやろ... 翻訳したるわ。感謝しな\n\n"
                Text += Res["text"]
                await message.channel.send(Text)
            else:
                pass
            if "period" in message.content:
                channel = client.get_channel(803425039864561675)
                Text = "@everyone 重要なお知らせかもしれないからこっちにも貼っとくで\n"
                Text += message.content
                await channel.send(f"{Text}{message.content}")

    elif Prefix == message.content[0]:
        if message.content.upper() == f"{Prefix}TOP":
            Text = "www.escapefromtarkov.com"
            Embed = discord.Embed(
                title="Escape from Tarkov official page",
                url="https://www.escapefromtarkov.com/",
                description=Text,
                color=0x2ECC69,
            )
            Embed.set_thumbnail(
                url="https://www.escapefromtarkov.com/themes/eft/images/eft_logo_promo.jpg"
            )
            await message.channel.send(embed=Embed)
            return 0

        elif message.content.upper() == f"{Prefix}WIKITOP":
            Text = "wikiwiki.jp"
            Embed = discord.Embed(
                title="Escape from Tarkov 日本語WIKI",
                url=Url,
                description=Text,
                color=0x2ECC69,
            )
            Embed.set_thumbnail(
                url="https://www.escapefromtarkov.com/themes/eft/images/eft_logo_promo.jpg"
            )
            await message.channel.send(embed=Embed)
            return 0

        elif message.content.upper() == f"{Prefix}MAP":
            Text = ""
            for Map in Maps:
                Text += f"[{Map}]({Url}{Map})\n"
            Embed = discord.Embed(
                title="マップ", url=f"{Url}", description=Text, color=0x2ECC69,
            )
            Embed.set_footer(text=f"{Prefix}マップ名で各マップの詳細情報にアクセスできるよー。 例: /reserve")
            await message.channel.send(embed=Embed)
            return 0

        elif message.content.upper().split("/")[1] in Maps:
            ReceivedText = message.content.upper().split("/")[1]
            Text = f"{SendTemplateText}{ReceivedText} INFORMATION\n"
            Text += f"{ReceivedText}(EFT 日本語 Wiki URL): {Url}{ReceivedText}\n"

            if message.content.upper() == "/FACTORY":
                Text += "https://cdn.wikiwiki.jp/to/w/eft/img/::attach/FactoryMap.jpg"

            if message.content.upper() == "/WOODS":
                Text += "https://images-ext-1.discordapp.net/external/NyBjPcCWLdnVfdUSAjWs3aGk4Un8qRAZCjnk3eF_8uo/https/cdn.wikiwiki.jp/to/w/eft/WOODS/%3A%3Aattach/Woods_map_v0.12.9b.jpg"

            if message.content.upper() == "/CUSTOMS":
                Text += "https://cdn.wikiwiki.jp/to/w/eft/CUSTOMS/::attach/Customs_0.12.7.jpg"

            if message.content.upper() == "/SHORELINE":
                Text += "https://cdn.wikiwiki.jp/to/w/eft/SHORELINE/::attach/ShoreLine_Exit_Loot.jpg\n"
                Text += "https://cdn.wikiwiki.jp/to/w/eft/SHORELINE/::attach/resort.jpg"

            if message.content.upper() == "/INTERCHANGE":
                Text += (
                    "https://cdn.wikiwiki.jp/to/w/eft/img/::ref/Interchange_Map.jpg\n"
                )
                Text += "https://cdn.wikiwiki.jp/proxy-image?url=https%3A%2F%2Fwww.eftmaps.net%2Fwp-content%2Fuploads%2F2020%2F05%2Finterchange_map.png"

            if message.content.upper() == "/LABORATORY":
                Text += "https://cdn.wikiwiki.jp/to/w/eft/LABORATORY/::ref/111000.png\n"
                Text += (
                    "https://cdn.wikiwiki.jp/to/w/eft/LABORATORY/::attach/LabMap.jpg"
                )

            if message.content.upper() == "/RESERVE":
                Text += "https://cdn.wikiwiki.jp/to/w/eft/RESERVE/::attach/Reserve_Map_Translated%20fix.jpg\n"
                Text += "https://cdn.wikiwiki.jp/to/w/eft/RESERVE/::attach/800px-3D_Map_by_loweffortsaltbox.png\n"
                Text += "https://cdn.wikiwiki.jp/to/w/eft/RESERVE/::attach/ReserveKeys.jpg\n"
                Text += "https://cdn.wikiwiki.jp/to/w/eft/RESERVE/::attach/ReserveUnderground.jpg"

            await message.channel.send(Text)
            return 0

        elif message.content.upper() == f"{Prefix}RANDOM":
            embed = discord.Embed(
                title="迷ったときのEFTマップ抽選", description="今回のマップは...", color=0x2ECC69,
            )
            embed.add_field(name="MAP", value=random.choice(Maps), inline=False)
            await message.channel.send(embed=embed)
            return 0

        elif message.content.upper() == f"{Prefix}HELP":
            embed = discord.Embed(
                title="ヘルプ",
                description="EFT(Escape from Tarkov) Wiki Bot使用可能コマンド一覧だよ!",
                color=0x2ECC69,
            )
            for Key, Values in CommandList.items():
                if Key == "各武器詳細表示":
                    Text = "/武器名"
                elif Key == "各アイテムのフリーマーケット価格表示":
                    Text = "!p {アイテム名}"
                else:
                    if type(Values) == list:
                        Text = ""
                        for Value in Values:
                            Text += f"{Prefix}{Value}\n"
                    else:
                        Text = f"{Prefix}{Values}\n"
                embed.add_field(name=f"{Key}コマンド", value=Text, inline=False)
            await message.channel.send(embed=embed)
            return 0

        elif message.content.upper() == f"{Prefix}CHART":
            Text = "https://cdn.discordapp.com/attachments/803425039864561675/804873530335690802/image0.jpg\n"
            Text += "https://cdn.discordapp.com/attachments/803425039864561675/804873530637811772/image1.jpg\n"
            Text += "https://cdn.discordapp.com/attachments/616231205032951831/805997840140599366/image0.jpg\n"
            Text += "https://cdn.discordapp.com/attachments/808820772536582154/814055787479564318/image0.webp\n"
            Text += "https://media.discordapp.net/attachments/808820772536582154/814055787898077215/image1.webp"
            await message.channel.send(Text)
            return 0

        elif message.content.upper() == f"{Prefix}PATCH":
            Embed = discord.Embed(title="更新履歴一覧")
            for Index, Values in PatchNotes.items():
                Text = ""
                for N, Value in enumerate(Values):
                    Text += f"{N+1}. {Value}\n"
                Embed.add_field(name=Index, value=Text, inline=False)
            Embed.set_footer(text=f"最終更新: {list(PatchNotes.keys())[0]}")
            await message.channel.send(embed=Embed)
            return 0

        elif message.content.upper() == f"{Prefix}SOURCE":
            Text = "Contribute to sai11121209/Discord-EFT-Bot development by creating an account on GitHub."
            Embed = discord.Embed(
                title="GitHub",
                url="https://github.com/sai11121209/Discord-EFT-Bot",
                description=Text,
                color=0x2ECC69,
            )
            Embed.set_thumbnail(
                url="https://avatars.githubusercontent.com/u/55883274?s=400&v=4"
            )
            await message.channel.send(embed=Embed)
            return 0

        elif message.content.upper() == f"{Prefix}TASK":
            TraderNames = GetTraderNames()
            Text = ""
            for TraderName in TraderNames:
                Text += f"[{TraderName}]({Url}{TraderName.capitalize()}タスク)\n"
            Embed = discord.Embed(
                title="タスク", url=f"{Url}タスク", description=Text, color=0x2ECC69,
            )
            Embed.set_footer(text="トレーダー名をクリックすることで各トレーダータスクの詳細情報にアクセスできるよー。")
            await message.channel.send(embed=Embed)
            return 0

        elif message.content.upper() == f"{Prefix}AMMO":
            Text = "eft.monster"
            Embed = discord.Embed(
                title="弾薬性能表",
                url="https://eft.monster/",
                description=Text,
                color=0x2ECC69,
            )
            Embed.set_thumbnail(url="https://eft.monster/ogre_color.png")
            await message.channel.send(embed=Embed)
            return 0

        elif message.content.upper() == f"{Prefix}MARKET":
            Text = "Actual prices, online monitoring, hideout, charts, price history"
            Embed = discord.Embed(
                title="Tarkov Market",
                url="https://tarkov-market.com/",
                description=Text,
                color=0x2ECC69,
            )
            await message.channel.send(embed=Embed)
            return 0

        elif message.content.upper() == f"{Prefix}NOW":
            Embed = discord.Embed(
                title="現在時刻", description="主要タイムゾーン時刻", color=0x2ECC69,
            )
            Embed.add_field(
                name="日本時間(JST)",
                value=dt.now().strftime("%Y/%m/%d %H:%M:%S"),
                inline=False,
            )
            Embed.add_field(
                name="モスクワ時間(EAT)",
                value=dt.now(
                    datetime.timezone(datetime.timedelta(hours=3), name="EAT")
                ).strftime("%Y/%m/%d %H:%M:%S"),
                inline=False,
            )
            Embed.add_field(
                name="太平洋標準時刻(PST)",
                value=dt.now(
                    datetime.timezone(datetime.timedelta(hours=-8), name="PST")
                ).strftime("%Y/%m/%d %H:%M:%S"),
                inline=False,
            )
            Embed.add_field(
                name="太平洋夏時刻(PDT)",
                value=dt.now(
                    datetime.timezone(datetime.timedelta(hours=-7), name="PDT")
                ).strftime("%Y/%m/%d %H:%M:%S"),
                inline=False,
            )
            Embed.set_footer(text="夏時間は3月の第2日曜日午前2時から11月の第1日曜日午前2時まで。")
            await message.channel.send(embed=Embed)
            return 0

        elif message.content.upper() == f"{Prefix}BTC":
            Timestamp = (
                dt.now(pytz.timezone("Asia/Tokyo")) - relativedelta(months=1)
            ).timestamp()
            SummaryJpy = rq.get(
                "https://api.cryptowat.ch/markets/bitflyer/btcjpy/summary"
            ).json()["result"]
            BtcJpyData = rq.get(
                f"https://api.cryptowat.ch/markets/bitflyer/btcjpy/ohlc?periods=1800&after={int(Timestamp)}"
            ).json()["result"]
            PD_BtcData = pd.DataFrame(BtcJpyData["1800"])
            PD_BtcData[0] = pd.to_datetime(PD_BtcData[0].astype(int), unit="s")
            plt.figure(figsize=(15, 10), dpi=100)
            plt.plot(PD_BtcData[0], PD_BtcData[1], label="OpenPrice")
            plt.plot(PD_BtcData[0], PD_BtcData[2], label="HighPrice")
            plt.plot(PD_BtcData[0], PD_BtcData[3], label="LowPrice")
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
            Embed = discord.Embed(title="1 ビットコイン → 日本円", color=0xFFFF00,)
            Embed.set_image(url="attachment://btc_jpy.png")
            Embed.add_field(name="現在の金額", value="{:,}".format(BtcJpyPrice) + " 円")
            Embed.add_field(
                name="0.2BTCあたりの金額",
                value="約 " + "{:,}".format(int(BtcJpyPrice * 0.2)) + " 円",
            )
            Embed.add_field(
                name="最高値", value="{:,}".format(SummaryJpy["price"]["high"]) + " 円"
            )
            Embed.add_field(
                name="最安値", value="{:,}".format(SummaryJpy["price"]["low"]) + " 円"
            )
            await message.channel.send(embed=Embed, file=file)

            BtcRubData = rq.get(
                f"https://api.cryptowat.ch/markets/cexio/btcrub/ohlc?periods=1800&after={int(Timestamp)}"
            ).json()["result"]
            PD_BtcData = pd.DataFrame(BtcRubData["1800"])
            PD_BtcData[0] = pd.to_datetime(PD_BtcData[0].astype(int), unit="s")
            plt.figure(figsize=(15, 10), dpi=100)
            plt.plot(PD_BtcData[0], PD_BtcData[1], label="OpenPrice")
            plt.plot(PD_BtcData[0], PD_BtcData[2], label="HighPrice")
            plt.plot(PD_BtcData[0], PD_BtcData[3], label="LowPrice")
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
            Embed = discord.Embed(title="1 ビットコイン → ルーブル", color=0xFFFF00,)
            Embed.set_image(url="attachment://btc_rub.png")
            Embed.add_field(name="現在の金額", value="{:,}".format(BtcRubPrice) + " RUB")
            Embed.add_field(
                name="0.2BTCあたりの金額",
                value="約 " + "{:,}".format(int(BtcRubPrice * 0.2)) + " RUB",
            )
            Embed.add_field(
                name="最高値", value="{:,}".format(SummaryJpy["price"]["high"]) + " RUB"
            )
            Embed.add_field(
                name="最安値", value="{:,}".format(SummaryJpy["price"]["low"]) + " RUB"
            )
            await message.channel.send(embed=Embed, file=file)
            return 0

        elif message.content.upper() == f"{Prefix}WEAPON":
            WeaponsName, WeaponsData, ColName = GetWeaponData()
            BulletsData = GetBulletData()
            Embeds = []
            for N, (Index, Values) in enumerate(WeaponsData.items()):
                Embed = discord.Embed(
                    title=f"武器一覧({N+1}/{len(WeaponsData)})", url=f"{Url}武器一覧"
                )
                Embed.add_field(
                    name=f"{Index}",
                    value=f"[{Index}wikiリンク]({Url}武器一覧#h2_content_1_{N})",
                    inline=False,
                )
                Infostr = ""
                for Value in Values:
                    Urlencord = Value[0].replace(" ", "%20")
                    Infostr += f"[{Value[0]}]({Url}{Urlencord})  "
                    for c, v in zip(ColName[Index][2:], Value[2:]):
                        if c == "使用弾薬":
                            FixName = v.replace("×", "x")
                            FixName = FixName.replace(" ", "")
                            Infostr += (
                                f"**{c}**: [{v}]({Url}弾薬{BulletsData[FixName]})  "
                            )
                        else:
                            Infostr += f"**{c}**: {v}  "
                    Embed.add_field(
                        name=Value[0], value=Infostr, inline=False,
                    )
                    Infostr = ""
                Embed.set_footer(text=f"Escape from Tarkov 日本語 Wiki: {Url}")
                Embeds.append(Embed)
            for Embed in Embeds:
                await message.channel.send(embed=Embed)
            return 0

        WeaponsName, WeaponsData, ColName = GetWeaponData()
        CommandList["各武器詳細表示"] = WeaponsName
        # コマンドの予測変換
        hints = [
            Command
            for Command in list(itertools.chain.from_iterable(CommandList.values()))
            if difflib.SequenceMatcher(
                None, message.content.upper(), Prefix + Command
            ).ratio()
            >= 0.65
        ]

        if message.content.upper().split("/")[1] in WeaponsName:
            BulletsData = GetBulletData()
            InfoStr = ""
            FixText = message.content.upper().replace(" ", "").split("/")[1]
            WeaponName = WeaponsName[FixText]
            UrlEncord = WeaponName[1].replace(" ", "%20")
            # InfoStr += f"[{WeaponName[1]}]({Url}{UrlEncord})  "
            for c, v in zip(ColName[WeaponName[0]][2:], WeaponName[3:]):
                if c == "使用弾薬":
                    FixName = v.replace("×", "x")
                    FixName = FixName.replace(" ", "")
                    InfoStr += f"**{c}**: [{v}]({Url}弾薬{BulletsData[FixName]})  "
                else:
                    InfoStr += f"**{c}**: {v}  "
            Embed = discord.Embed(
                title=WeaponName[1], url=f"{Url}{UrlEncord}", description=InfoStr
            )
            Embed.set_image(url=WeaponName[2])
            await message.channel.send(embed=Embed)
            return 0

        elif len(hints) > 0:
            Text = "Hint: もしかして以下のコマンドじゃね?\n"
            for n, hint in enumerate(hints):
                Text += f"{n+1}. {Prefix}{hint}\n"
            Text += "これ以外に使えるコマンドは /help で確認できるよ!"
            await message.channel.send(Text)
            return 0

        else:
            Text = "入力されたがコマンドが見つからなかった...ごめんなさい。\n"
            Text += "これ以外に使えるコマンドは /help で確認できるよ!"
            await message.channel.send(Text)
            return 0
    elif "@everyone BOTの更新をしました!" == message.content:
        Embed = discord.Embed(title="更新履歴一覧")
        for Index, Values in PatchNotes.items():
            Text = ""
            for N, Value in enumerate(Values):
                Text += f"{N+1}. {Value}\n"
            Embed.add_field(name=Index, value=Text, inline=False)
        Embed.set_footer(text=f"最終更新: {list(PatchNotes.keys())[0]}")
        await message.channel.send(embed=Embed)


def GetTraderNames():
    Res = rq.get(f"{Url}タスク")
    Soup = BeautifulSoup(Res.text, "lxml", from_encoding="utf-8")
    Soup = Soup.find("div", {"class": "contents"}).find_all("ul", {"class": "list2"})[1]
    return [s.get_text().replace(" ", "") for s in Soup.find_all("a")]


def GetBulletData():
    Res = rq.get(f"{Url}弾薬")
    Soup = BeautifulSoup(Res.text, "lxml", from_encoding="utf-8").find(
        "div", {"class": "container-wrapper"}
    )
    Exclusion = ["概要", "表の見方", "弾薬の選び方", "拳銃弾", "PDW弾", "ライフル弾", "散弾", "グレネード弾", "未実装"]
    BulletsData = {
        s.get_text().replace(" ", ""): s.get("href")
        for s in Soup.find("div", {"class": "contents"}).find("ul").find_all("a")
        if s.get_text().replace(" ", "") not in Exclusion
    }
    return BulletsData


def GetWeaponData():
    Res = rq.get(f"{Url}武器一覧")
    Soup = BeautifulSoup(Res.text, "lxml", from_encoding="utf-8").find(
        "div", {"class": "container-wrapper"}
    )
    Exclusion = ["", "開発進行中", "企画中", "コメント", "削除済み"]
    ColName = {}
    WeaponsData = {
        s.get_text().replace(" ", ""): []
        for s in Soup.find("div", {"class": "contents"}).find_all("a")
        if s.get_text().replace(" ", "") not in Exclusion
    }
    for index, s in zip(
        WeaponsData, Soup.find_all("div", {"class": "wikiwiki-tablesorter-wrapper"}),
    ):
        WeaponData = []
        NewInfoData = []
        OldInfoData = []
        ColName_soup = s.find("tr").find_all("strong")
        ColName[index] = [str.get_text() for str in ColName_soup]
        for i in s.find("tbody").find_all("tr"):
            NewInfoData = [
                j.find("img")["src"] if j.find("img") else j.get_text()
                for j in i.find_all("td")
            ]
            if len(i.find_all("td")) == 2:
                NewInfoData += OldInfoData[2:]
            OldInfoData = NewInfoData
            WeaponData.append(NewInfoData)
        WeaponsData[index] = WeaponData
    WeaponsName = {
        Value[0]: [Key] + Value
        for Key, Values in WeaponsData.items()
        for Value in Values
    }
    return WeaponsName, WeaponsData, ColName


# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)
