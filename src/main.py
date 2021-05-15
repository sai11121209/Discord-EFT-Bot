# インストールした discord.py を読み込む
import os
import re
from typing import Text
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

    LOCAL_HOST = True
except ImportError:
    import keep_alive

    keep_alive.keep_alive()


# 自分のBotのアクセストークンに置き換えてください
if os.getenv("TOKEN"):
    TOKEN = os.getenv("TOKEN")
    LOCAL_HOST = False


# 接続に必要なオブジェクトを生成
client = discord.Client()
developMode = False
prefix = "/"
jaWikiUrl = "https://wikiwiki.jp/eft/"
enWikiUrl = "https://escapefromtarkov.fandom.com/wiki/"
sendTemplatetext = "EFT(Escape from Tarkov) Wiki "
voiceChatRole = 839773477095211018
receivedtext = None
mapList = {
    "FACTORY": {
        "overview": "ここ第16科学工場の施設はTerraグループに違法に使用されていた。\n契約戦争の間、プラント施設は、Tarkovの工場地区の支配をめぐりUSECとBEARとの間で多くの戦いの場となった。\n混乱の後、プラント施設は避難民やSCAV、その他の勢力、USECとBEARが残した物資を含む避難所と変わった。",
        "time": {"day": 20, "nigth": 25},
        "difficulty": "BREEZE",
        "number": {"day": "4-5", "nigth": "4-6"},
        "enemies": ["Scavs"],
    },
    "WOODS": {
        "overview": "Prozersk自然保護区は最近、北西連邦の国立野生動物保護区のリストに含まれていた。",
        "time": 50,
        "difficulty": "NORMAL",
        "number": "8-14",
        "enemies": ["Scavs", "Cultists", "Shturman"],
    },
    "CUSTOMS": {
        "overview": "工場に隣接する大規模な工業団地。ターミナル、寮、燃料タンクやその他のオブジェクトが多数存在する。",
        "time": 45,
        "difficulty": "NORMAL",
        "number": "8-12",
        "enemies": ["Scavs", "Cultists", "Reshala"],
    },
    "SHORELINE": {
        "overview": "海岸線(SHORELINE)は、ポートエリアに隣接するタルコフ郊外の主要な部分。\n地域には部分的に放棄された村、近代的な民家と畑、ボート施設付きの長い海岸線、ガソリンスタンド、気象ステーション、携帯電話基地局が存在する。\nその主要なポイントは、独自の水力発電所を備えたいくつかの豪華な建物からなる大規模な「Azure Coast」保養地。\nこのリゾートは、かつてタルコフ港を通じた脱出に備えて、TERRAグループとその関連会社のスタッフの一時的な宿泊施設として使用されていた。",
        "time": 50,
        "difficulty": "HARD",
        "number": "10-13",
        "enemies": ["Scavs", "Cultists", "Sanitar"],
    },
    "INTERCHANGE": {
        "overview": "南インターチェンジは市内での輸送の重要な場所。\nこの戦略的エリアはポートランド港とタルコフの工業郊外を結んでいる。\n大型のウルトラショッピングモールがあり、EMERCOM救出作戦の主要拠点として使用されていた。",
        "time": 45,
        "difficulty": "HARD",
        "number": "10-14",
        "enemies": ["Scavs", "Killa"],
    },
    "LABORATORY": {
        "overview": "タルコフ市中心部の地下に存在するTERRAグループの秘密研究施設。\n非公式な存在であり、化学、物理学、生物学、ハイテク分野での研究開発を秘密裏に行っていた。",
        "time": 40,
        "difficulty": "INSANE",
        "number": "6-10",
        "enemies": ["ScavRaiders"],
    },
    "RESERVE": {
        "overview": "都市伝説となっている連邦準備局の秘密基地。\nそこには核戦争にも耐えうる数年分の備蓄（食料、医薬品、その他物資）が含まれているという。",
        "time": 50,
        "difficulty": "HARD",
        "number": "9-12",
        "enemies": ["Scavs", "ScavRaiders", "Glukhar"],
    },
}
traderList = {
    "Prapor": {
        "stampid": 828552629248327690,
        "fullname": "Pavel Yegorovich Romanenko",
        "location": "Town",
        "origin": "ロシア連邦",
        "wares": ["武器", "弾薬", "手榴弾", "弾倉", "武器MOD",],
        "services": ["保険", "修理",],
        "currencies": ["Roubles (₽)"],
    },
    "Therapist": {
        "stampid": 828552629256192040,
        "fullname": "Elvira Khabibullina",
        "location": "Streets of Tarkov",
        "origin": "ロシア連邦",
        "wares": ["医療品", "地図", "食料品", "コンテナ",],
        "services": ["保険",],
        "currencies": ["Roubles (₽)", "Euros (€)",],
    },
    "Fence": {
        "stampid": 828552627989512204,
        "fullname": "Real name unknown",
        "location": "A network of outlets all over Tarkov and its outskirts",
        "origin": "ロシア連邦",
        "wares": ["売られたもの全て",],
        "services": [],
        "currencies": ["Roubles (₽)",],
    },
    "Skier": {
        "stampid": 828552629436416010,
        "fullname": "Alexander Fyodorovich Kiselyov",
        "location": "Customs",
        "origin": "ロシア連邦",
        "wares": ["武器", "弾薬", "武器MOD", "コンテナ", "ユーロ",],
        "services": ["修理",],
        "currencies": ["Roubles (₽)", "Dollars ($)", "Euros (€)",],
    },
    "Peacekeeper": {
        "stampid": 828552628682096710,
        "fullname": "Tadeusz Pilsudski",
        "location": "Terminal",
        "origin": "ポーランド共和国",
        "wares": ["欧米・NATOの武器", "弾薬", "手榴弾", "弾倉", "武器MOD", "USドル",],
        "services": [],
        "currencies": ["Dollars ($)",],
    },
    "Mechanic": {
        "stampid": 828552628887093328,
        "fullname": "Sergey Arsenyevich Samoylov",
        "location": "Factory",
        "origin": "不明",
        "wares": ["欧米・NATOの武器", "グロック17/18", "弾薬", "弾倉", "武器MOD",],
        "services": ["修理",],
        "currencies": ["Roubles (₽)", "Euros (€)", "Bitcoin (₿)",],
    },
    "Ragman": {
        "stampid": 828552630120349716,
        "fullname": "Abramyan Arshavir Sarkisivich",
        "location": "Interchange",
        "origin": "不明",
        "wares": ["衣類", "アーマー", "バックパック", "タクティカリグ", "ギア",],
        "services": ["戦闘服",],
        "currencies": ["Roubles (₽)",],
    },
    "Jaeger": {
        "stampid": 828552628396621855,
        "fullname": "Kharitonov Ivan Egorovich",
        "location": "Woods",
        "origin": "不明",
        "wares": ["ソビエト連邦の武器", "弾薬", "弾倉", "武器MOD", "隠れ家素材",],
        "services": [],
        "currencies": ["Roubles (₽)",],
    },
}

bossList = {
    "Reshala": {
        "stampid": 834774060029706240,
        "location": ["Customs"],
        "pawnchance": {"Customs": 38},
        "drops": ["TT pistol 7.62x25 TT Gold"],
        "followers": "4",
    },
    "Killa": {
        "stampid": 834774059430313984,
        "location": ["Interchange"],
        "pawnchance": {"Interchange": 38},
        "drops": [
            "RPK-16 5.45x39 light machine gun",
            "Maska 1Sch helmet (Killa)",
            "Maska 1Sch face shield (Killa)",
            "6B13 M assault armor (tan)",
            "Blackhawk! Commando Chest Harness (black)",
        ],
        "followers": "0",
    },
    "Glukhar": {
        "stampid": 834774058724753418,
        "location": ["Reserve"],
        "pawnchance": {"Reserve": 43},
        "drops": ["ASh-12 12.7x55 assault rifle",],
        "followers": "6",
    },
    "Shturman": {
        "stampid": 834774058612555777,
        "location": ["Woods"],
        "pawnchance": {"Woods": 41},
        "drops": [
            "AK-105 5.45x39 assault rifle",
            "SVDS 7.62x54 Sniper rifle",
            "Red Rebel Ice pick",
        ],
        "followers": "2",
    },
    "Sanitar": {
        "stampid": 834774059522588742,
        "location": ["Shoreline"],
        "pawnchance": {"Shoreline": 35},
        "drops": ["Sanitar bag"],
        "followers": "2",
    },
    "CultistPriest": {
        "stampid": 834774056091910195,
        "location": ["Woods", "Shoreline", "Customs"],
        "pawnchance": {"Woods": 28, "Shoreline": 28, "Customs": 20},
        "drops": ["Sanitar bag"],
        "followers": "3-5",
    },
}
# 新規コマンド追加時は必ずcommandListに追加
commandList = {
    "EFT公式サイト表示": ["TOP"],
    "日本EFTWiki表示": ["JAWIKI"],
    "海外EFTWiki表示": ["ENWIKI"],
    "マップ一覧表示": ["MAP"],
    "各マップ情報表示": mapList,
    "武器一覧表示": ["WEAPON"],
    "各武器詳細表示": [],
    "弾薬性能表示": ["AMMO"],
    "フリーマーケット情報表示": ["MARKET"],
    "TarkovTools情報表示": ["TARKOVTOOLS"],
    "各アイテムフリーマーケット価格表示": [],
    "ディーラー一覧表示": ["DEALER"],
    "ボス一覧表示": ["BOSS"],
    "マップ抽選": ["RANDOMMAP"],
    "武器抽選": ["RANDOMWEAPON"],
    "早見表表示": ["CHART"],
    "アーマ早見表表示": ["ARMOR"],
    "更新履歴表示": ["PATCH"],
    "現在時刻表示": ["NOW"],
    "ビットコイン価格表示": ["BTC"],
    "ソースコード表示": ["SOURCE"],
}
# 上に追記していくこと
patchNotes = {
    "2.2:2021/05/15 18:00": ["出会いを目的としたフレンド募集を含む投稿を行った場合警告が送られる様になりました。",],
    "2.1:2021/05/08 17:00": [
        "自動全体メンションに本文を含む様に変更されました。",
        "TarkovTools情報表示コマンド __`TARKOVTOOLS`__ を追加しました。",
        "以前から仕様変更予定にあった早見表表示、アーマ早見表表示コマンド __`CHART`__ __`ARMOR`__ の正式実装を行いました。",
        "早見表表示、アーマ早見表表示コマンド __`CHART`__ __`ARMOR`__ の正式実装、又TarkovTools情報表示コマンド __`TARKOVTOOLS`__ 追加に伴い弾薬性能表示コマンド __`AMMO`__の仕様が一部変更されました。",
    ],
    "2.0.1:2021/05/07 17:00": [
        "notification-general において発言を行うと自動全体メンションをする様になりました。",
        "機能改善会議(メンテナンス)中にbotに話しかけると怒る様になりました。",
    ],
    "2.0:2021/05/06 18:00": [
        "武器一覧表示、各武器詳細表示コマンド __`WEAPON`__ __`武器名`__ の各種データを海外Wikiから取得する様に変更されました。",
        "武器一覧表示、各武器詳細表示、マップ一覧表示、ボス一覧表示コマンドのレスポンス最適化。",
        "ボイスチャンネル使用中のユーザがテキストチャンネルに書き込むとボイスチャンネル参加ユーザを自動メンションする様になりました。",
    ],
    "1.11:2021/04/22 22:10": [
        "武器抽選コマンド __`RANDOMWEAPON`__ 追加に伴いマップ抽選コマンド ~~__`RANDOM`__~~ から __`RANDOMMAP`__ に変更されました。",
        "ボス一覧表示コマンド __`BOSS`__ を追加しました。",
    ],
    "1.10.3:2021/04/20 18:35": [
        "マップ抽選コマンド __`RANDOM`__ で発生していたデータ型キャスト不具合の修正を行いました。",
        "タイムゾーン未指定による更新日時が正常に表示されていなかった問題の修正。",
    ],
    "1.10.2:2021/04/06 19:13": ["弾薬性能表示コマンド　__`AMMO`__ の挙動が変更されました。"],
    "1.10.1:2021/04/06 03:20": [
        "機能改善に伴いタスク一覧表示コマンドが　~~__`TASK`__~~  から ディーラー一覧表示コマンドの __`DEALER`__ に統合されました。"
    ],
    "1.10:2021/04/02 12:00": ["アーマの早見表表示コマンド __`ARMOR`__ が仮実装されました。"],
    "1.9.1:2021/03/30 01:35": [
        "マップ一覧表示コマンド __`MAP`__ の挙動を大幅に改良しました。",
        "類似コマンドが存在し、かつ類似コマンドが1つの場合該当コマンドを実行するようになるようになりました。",
        "使用可能コマンド一覧表示コマンド __`HELP`__ を見やすいように表示方法改善しました。",
    ],
    "1.9:2021/03/23 18:00": [
        "各マップ情報表示コマンドの挙動を大幅に改良しました。",
        "海外公式wiki表示コマンド __`ENWIKI`__ 追加に伴い日本EFTWiki表示コマンドの呼び出しコマンドが 　~~__`WIKITOP`__~~ から __`JAWIKI`__ に変更されました。",
    ],
    "1.8.1:2021/03/22 23:00": ["内部処理エラーによる __`WEAPON`__ コマンドの修正"],
    "1.8:2021/03/19": [
        "ビットコイン価格表示コマンド __`BTC`__ を追加しました。",
        "メンテナンス関連のアナウンスがあった場合、テキストチャンネル __`escape-from-tarkov`__ に通知を送るようにしました。",
    ],
    "1.7:2021/03/17": ["現在時刻表示コマンド __`NOW`__ を追加しました。"],
    "1.6:2021/03/15": ["フリーマーケット情報表示コマンド __`MARKET`__ を追加しました。"],
    "1.5.2:2021/03/14": ["ボイスチャンネル開始、終了時の通知挙動の修正をしました。 ※最終修正"],
    "1.5.1:2021/03/11": ["ボイスチャンネル開始、終了時の通知挙動の修正をしました。"],
    "1.5:2021/03/09": ["BOTがボイスチャンネル開始時に通知をしてくれるようになりました。"],
    "1.4:2021/03/06": ["BOTが公式アナウンスを自動的に翻訳してくれるようになりました。"],
    "1.3.2.1:2021/03/04": ["BOTがよりフレンドリーな返答をするようになりました。"],
    "1.3.2:2021/02/25": ["早見表表示コマンドに2件早見表を追加しました。"],
    "1.3.1:2021/02/23": [f"最初の文字が __`{prefix}`__ 以外の文字の場合コマンドとして認識しないように修正。"],
    "1.3:2021/02/10": [
        "タスク一覧表示コマンド __`TASK`__ を追加しました。",
        "弾薬性能表示コマンド __`AMMO`__ を追加しました。",
    ],
    "1.2.2:2021/02/08": ["一部コマンドのレスポンス内容の変更を行いました。"],
    "1.2.1:2021/02/05": ["一部コマンドを除いたレスポンスの向上"],
    "1.2:2021/02/04": [
        "入力されたコマンドに近いコマンドを表示するヒント機能を追加しました。",
        "各武器名を入力することで入力された武器の詳細情報のみにアクセスできるようになりました。",
        "BOTのソースコードにアクセスできるコマンド __`SOURCE`__ を追加しました。",
    ],
    "1.1:2021/02/02": [
        "更新履歴表示コマンド __`PATCH`__ を追加しました。",
        "武器一覧表示コマンドの挙動を大幅に変更しました。",
        "早見表表示コマンドに料金表を追加しました。",
    ],
    "1.0:2021/01/30": ["早見表表示コマンド __`CHART`__ を追加しました。", "早見表コマンドにアイテム早見表を追加しました。"],
}


async def add_role(member):
    role = member.guild.get_role(voiceChatRole)
    await member.add_roles(role)


async def remove_role(member):
    role = member.guild.get_role(voiceChatRole)
    await member.remove_roles(role)


# 起動時に動作する処理
@client.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    print("読み込み開始")
    if LOCAL_HOST == False:
        await client.change_presence(
            activity=discord.Activity(name="起動中です。しばらくお待ちください", type=5)
        )
    global traderNames, bossNames, weaponsName, weaponsData, updateTimestamp
    traderNames, bossNames, weaponsName, weaponsData, updateTimestamp = Initialize()
    print("ログインしました")
    if LOCAL_HOST == False:
        await client.change_presence(
            activity=discord.Game(name="Escape from Tarkov", type=1)
        )


# ボイスチャット参加時に動作する処理
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
        await add_role(member)
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
        await remove_role(member)


# メッセージ受信時に動作する処理
@client.event
async def on_message(message):
    global developMode, enrageCounter
    notificationGneralChannelId = 839769626585333761
    # メッセージ送信者がBotだった場合は無視する
    if not len(message.content):
        return 0
    try:
        if (
            message.guild.get_role(voiceChatRole) in message.author.roles
            and message.channel.id != notificationGneralChannelId
        ):
            await message.channel.send(f"<@&{voiceChatRole}> ")
    except:
        pass
    if not message.author.bot:
        if message.channel.id == notificationGneralChannelId:
            await message.channel.send(
                f"<@&820310764652462130> {message.content} by {message.author.name}"
            )
            return 0

    if message.author.bot and LOCAL_HOST == False:
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
                text = "<@&820310764652462130> 多分英語わからんやろ... 翻訳したるわ。感謝しな\n\n"
                text += res["text"]
                await message.channel.send(text)
            else:
                pass
            if "period" in message.content:
                channel = client.get_channel(803425039864561675)
                text = "<@&820310764652462130> 重要なお知らせかもしれないからこっちにも貼っとくで\n"
                text += message.content
                await channel.send(f"{text}{message.content}")

    if message.author.bot == False and LOCAL_HOST == False:
        if re.search(r"出会い|繋がりたい|美女|美男|可愛い|募集|フレンド|", message.content):
            text = f"本discordサーバでは**出会い**を目的とした**フレンド募集**を含む投稿を全面的に禁止しています。\n\n 以下の文章が違反している可能性があります。\n\n **以下違反文** \n ```{message.content}```"
            embed = discord.Embed(title="警告!!", description=text, color=0xFF0000,)

            await message.channel.send(f"{message.author.mention}")
            await message.channel.send(embed=embed)

    if prefix == message.content[0] and LOCAL_HOST == False:
        if message.content.upper() == f"{prefix}DEVELOP":
            developMode = not developMode
            text = f"開発モード: {developMode}"
            if developMode:
                await client.change_presence(
                    activity=discord.Activity(name="機能改善会議(メンテナンス中)", type=5)
                )
                enrageCounter = 0
            else:
                await client.change_presence(
                    activity=discord.Game(name="Escape from Tarkov", type=1)
                )
            await message.channel.send(text)
            return 0
    if (
        developMode
        and message.author.id != 279995095124803595
        and not message.author.bot
        and prefix == message.content[0]
    ):
        if enrageCounter < 5:
            await message.channel.send("機能改善会議しとるねん。話しかけんといて。")
        elif enrageCounter < 10:
            await message.channel.send("やめて。キレそうです。")
        else:
            await message.channel.send("やめて。呼ばないで。")
        enrageCounter += 1
        return 0

    if prefix == message.content[0] and not developMode:
        if LOCAL_HOST:
            embed = discord.Embed(
                title="現在開発環境での処理内容が表示されており、実装の際に採用されない可能性がある機能、表示等が含まれている可能性があります。",
                color=0xFF0000,
            )
            await message.channel.send(embed=embed)
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

        elif message.content.upper() == f"{prefix}JAWIKI":
            text = "wikiwiki.jp"
            embed = discord.Embed(
                title="日本Escape from Tarkov WIKI",
                url=jaWikiUrl,
                description=text,
                color=0x2ECC69,
            )
            embed.set_thumbnail(
                url="https://www.escapefromtarkov.com/themes/eft/images/eft_logo_promo.jpg"
            )
            await message.channel.send(embed=embed)
            return 0

        elif message.content.upper() == f"{prefix}ENWIKI":
            text = "The Official Escape from Tarkov Wiki"
            embed = discord.Embed(
                title="海外Escape from Tarkov WIKI",
                url=enWikiUrl + "Escape_from_Tarkov_Wiki",
                description=text,
                color=0x2ECC69,
            )
            embed.set_thumbnail(
                url="https://static.wikia.nocookie.net/escapefromtarkov_gamepedia/images/b/bc/Wiki.png/revision/latest/scale-to-width-down/200?cb=20200612143203"
            )
            await message.channel.send(embed=embed)
            return 0

        elif message.content.upper() == f"{prefix}MAP":
            embed = discord.Embed(title="マップ", url=f"{enWikiUrl}Map", color=0x2ECC69,)
            for map, values in mapList.items():
                text = ""
                if map == "LABORATORY":
                    receivedtext = "The_Lab"
                else:
                    receivedtext = map.capitalize()
                for key, value in values.items():
                    if key == "time":
                        text += f"**時間制限**: "
                        try:
                            day = value["day"]
                            nigth = value["nigth"]
                            text += f"__昼間:{day}分__ __夜間:{nigth}分__"
                        except:
                            text += f"__{value}分__"
                    elif key == "difficulty":
                        text += f"**難易度**: __{value}__"
                    elif key == "number":
                        text += f"**人数**: "
                        try:
                            day = value["day"]
                            nigth = value["nigth"]
                            text += f"__昼間:{day}人__ __夜間:{nigth}人__"
                        except:
                            text += f"__{value}人__"
                    elif key == "enemies":
                        text += f"**出現敵兵**: "
                        for v in value:
                            if v == "ScavRaiders":
                                text += f"__[{v}]({enWikiUrl}Scav_Raiders)__ "
                            else:
                                text += f"__[{v}]({enWikiUrl}{v})__ "
                    text += "\n"
                text += f"**詳細情報**: __[JA]({jaWikiUrl}{map})__ / __[EN]({enWikiUrl}{receivedtext})__\n"
                embed.add_field(name=map, value=text)
            embed.set_thumbnail(
                url="https://static.wikia.nocookie.net/escapefromtarkov_gamepedia/images/4/43/Map.png/revision/latest?cb=20200619104902&format=original"
            )
            embed.set_footer(text=f"{prefix}マップ名で各マップの地形情報を表示できるよー。 例: /reserve")
            await message.channel.send(embed=embed)
            return 0

        elif message.content.upper().split("/")[1] in mapList:
            receivedtext = message.content.upper().split("/")[1]
            text = f"{receivedtext} MAP INFORMATION\n"
            # LABORATORYのみ海外公式wikiのURLがThe_Labとなるため例外
            if receivedtext == "LABORATORY":
                receivedtext = "The_Lab"
                mapImages = GetMapImage(receivedtext)
            else:
                mapImages = GetMapImage(receivedtext.capitalize())
            n = 1
            for key, value in mapImages.items():
                embed = discord.Embed(
                    title=f"({n}/{len(mapImages)}){text}",
                    description=f"[{key}]({value})",
                )
                embed.set_image(url=value)
                embed.set_footer(text=f"Source: The Official Escape from Tarkov Wiki")
                await message.channel.send(embed=embed)
                n += 1
            return 0

        elif message.content.upper() == f"{prefix}RANDOMMAP":
            embed = discord.Embed(
                title="迷ったときのEFTマップ抽選",
                description=f"{str(message.author).split('#')[0]}が赴くマップは...",
                color=0x2ECC69,
            )
            embed.add_field(
                name="MAP", value=random.choice(list(mapList)), inline=False
            )
            await message.channel.send(embed=embed)
            return 0

        elif message.content.upper() == f"{prefix}HELP":
            embed = discord.Embed(
                title="EFT(Escape from Tarkov) Wiki Bot使用可能コマンド一覧だよ!",
                description=f"```Prefix:{prefix}```",
                color=0x2ECC69,
                timestamp=datetime.datetime.utcfromtimestamp(
                    dt.strptime(
                        list(patchNotes.keys())[0].split(":", 1)[1] + "+09:00",
                        "%Y/%m/%d %H:%M%z",
                    ).timestamp()
                ),
            )
            for key, values in commandList.items():
                if key == "各武器詳細表示":
                    text = "```/{武器名}```"
                elif key == "各アイテムフリーマーケット価格表示":
                    text = "```!p {アイテム名}```"
                elif key == "各マップ情報表示":
                    text = "```/{マップ名}```"
                else:
                    text = "```"
                    for value in values:
                        text += f"{prefix}{value}\n"
                    text += "```"
                embed.add_field(name=f"{key}コマンド", value=text)
            # embed.set_thumbnail(url=client.get_user(803770349908131850).avatar_url)
            embed.set_author(
                name="EFT(Escape from Tarkov) Wiki Bot",
                url="https://github.com/sai11121209",
                # icon_url=client.get_user(279995095124803595).avatar_url,
            )
            embed.set_footer(text="最終更新")
            await message.channel.send(embed=embed)
            return 0

        elif message.content.upper() == f"{prefix}CHART":
            text = "その他早見表"
            chartImages = [
                "https://cdn.discordapp.com/attachments/803425039864561675/804873530335690802/image0.jpg",
                "https://cdn.discordapp.com/attachments/803425039864561675/804873530637811772/image1.jpg",
                "https://cdn.discordapp.com/attachments/616231205032951831/805997840140599366/image0.jpg",
                "https://cdn.discordapp.com/attachments/808820772536582154/814055787479564318/image0.webp",
                "https://media.discordapp.net/attachments/808820772536582154/814055787898077215/image1.webp",
            ]
            authorList = [
                {
                    "author": {
                        "name": "Twitter: Rushy_ve_",
                        "url": "https://twitter.com/Rushy_ve_",
                    },
                    "link": "https://twitter.com/Rushy_ve_/status/1231153891808440321?s=20",
                },
                {
                    "author": {
                        "name": "Twitter: Rushy_ve_",
                        "url": "https://twitter.com/Rushy_ve_",
                    },
                    "link": "https://twitter.com/Rushy_ve_/status/1231153891808440321?s=20",
                },
                {
                    "author": {
                        "name": "Reddit: CALLSIGN-ASTRO",
                        "url": "https://www.reddit.com/user/CALLSIGN-ASTRO/",
                    },
                    "link": "https://www.reddit.com/r/EscapefromTarkov/comments/eu0pmi/i_tried_to_make_quick_barter_items_price_list_but/?utm_source=share&utm_medium=web2x",
                },
                {
                    "author": {
                        "name": "Reddit: MarcoQuarko",
                        "url": "https://www.reddit.com/user/MarcoQuarko/",
                    },
                    "link": "https://www.reddit.com/r/EscapefromTarkov/comments/8een3x/all_quest_items_on_one_page_not_my_work_credits/",
                },
                {
                    "author": {
                        "name": "Tarkov Tools",
                        "url": "https://tarkov-tools.com/",
                    },
                    "link": "https://tarkov-tools.com/loot-tier/",
                },
            ]
            for n, (url, author) in enumerate(zip(chartImages, authorList)):
                embed = discord.Embed(
                    title=f"({n+1}/{len(chartImages)}){text}",
                    color=0x808080,
                    url=author["link"],
                )
                embed.set_image(url=url)
                embed.set_author(
                    name=author["author"]["name"], url=author["author"]["url"],
                )
                embed.set_footer(text=f"提供元: {author['link']}")
                await message.channel.send(embed=embed)
            return 0

        elif message.content.upper() == f"{prefix}ARMOR":
            text = "アーマー早見表"
            armorImages = [
                "https://cdn.discordapp.com/attachments/806055934211653632/826790299619426354/image3.jpg",
                "https://cdn.discordapp.com/attachments/806055934211653632/826790298649624586/image0.jpg",
                "https://cdn.discordapp.com/attachments/806055934211653632/826790298918453268/image1.jpg",
                "https://cdn.discordapp.com/attachments/806055934211653632/826790299299872798/image2.jpg",
            ]
            for n, url in enumerate(armorImages):
                embed = discord.Embed(
                    title=f"({n+1}/{len(armorImages)}){text}",
                    color=0x808080,
                    url=f"{enWikiUrl}Armor_vests",
                )
                embed.set_image(url=url)
                embed.set_author(
                    name="Twitter: @N7th_WF", url="https://twitter.com/N7th_WF",
                )
                embed.set_footer(
                    text="提供元: https://twitter.com/N7th_WF/status/1376825476598013957?s=20"
                )
                await message.channel.send(embed=embed)
            return 0

        elif message.content.upper() == f"{prefix}PATCH":
            embed = discord.Embed(
                title="更新履歴一覧",
                timestamp=datetime.datetime.utcfromtimestamp(
                    dt.strptime(
                        list(patchNotes.keys())[0].split(":", 1)[1] + "+09:00",
                        "%Y/%m/%d %H:%M%z",
                    ).timestamp()
                ),
            )
            for index, values in patchNotes.items():
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

        elif message.content.upper() == f"{prefix}DEALER":
            embed = discord.Embed(
                title="ディーラー",
                url=f"{enWikiUrl}Characters#Dealers",
                color=0x808080,
                timestamp=updateTimestamp,
            )
            for TraderName in traderNames:
                trader = traderList[TraderName]
                text = f"**本名**: __{trader['fullname']}__\n"
                if (
                    "A network of outlets all over Tarkov and its outskirts"
                    != trader["location"]
                ):
                    text += f"**場所**: __[{trader['location']}]({enWikiUrl}{trader['location'].replace(' ', '_')})__\n"
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
                text += f"**タスク情報**: [JA]({jaWikiUrl}{TraderName}タスク) / [EN]({enWikiUrl}Quests)\n"
                text += f"**詳細情報**: [EN]({enWikiUrl}{TraderName})"
                embed.add_field(
                    name=f"<:{TraderName}:{trader['stampid']}> {TraderName}",
                    value=text,
                )
            embed.set_author(
                name="EFT(Escape from Tarkov) Wiki Bot",
                url="https://github.com/sai11121209",
                # icon_url=client.get_user(279995095124803595).avatar_url,
            )
            embed.set_footer(text="トレーダー名をクリックすることで各トレーダータスクの詳細情報にアクセスできるよー。",)
            await message.channel.send(embed=embed)
            return 0

        elif message.content.upper() == f"{prefix}BOSS":
            embed = discord.Embed(
                title="ボス",
                url=f"{enWikiUrl}Characters#Bosses",
                color=0x808080,
                timestamp=updateTimestamp,
            )
            for bossName in bossNames:
                boss = bossList[bossName]
                text = ""
                text += "**場所**:"
                if len(boss["location"]) == 1:
                    text += f"__[{boss['location'][0]}]({enWikiUrl}{boss['location'][0]})__\n"
                    text += (
                        f"**出現確率**: __{boss['pawnchance'][boss['location'][0]]}%__\n"
                    )
                else:
                    text += "\n"
                    for location in boss["location"]:
                        text += f"・__[{location}]({enWikiUrl}{location})__\n"
                    text += f"**出現確率**:\n"
                    for location in boss["location"]:
                        text += (
                            f"・__{location}__: __{boss['pawnchance'][location]}%__\n"
                        )
                text += "**レアドロップ**:\n"
                for drop in boss["drops"]:
                    text += f"・__[{drop}]({enWikiUrl}{drop.replace(' ', '_')})__\n"
                text += f"**護衛**: {boss['followers']}人\n"
                if bossName != "CultistPriest":
                    text += f"**詳細情報**: [EN]({enWikiUrl}{bossName})"
                else:
                    text += f"**詳細情報**: [EN]({enWikiUrl}Cultists)"
                embed.add_field(
                    name=f"<:{bossName}:{boss['stampid']}> {bossName}", value=text,
                )
            embed.set_author(
                name="EFT(Escape from Tarkov) Wiki Bot",
                url="https://github.com/sai11121209",
                # icon_url=client.get_user(279995095124803595).avatar_url,
            )
            embed.set_footer(text="トレーダー名をクリックすることで各トレーダータスクの詳細情報にアクセスできるよー。",)
            await message.channel.send(embed=embed)
            return 0

        elif message.content.upper() == f"{prefix}AMMO":
            text = "弾薬早見表"
            ammoImages = [
                "https://cdn.discordapp.com/attachments/806055934211653632/828931828101546024/image0.jpg",
                "https://cdn.discordapp.com/attachments/806055934211653632/828931828353073172/image1.jpg",
            ]
            for n, url in enumerate(ammoImages):
                embed = discord.Embed(
                    title=f"({n+1}/{len(ammoImages)}){text}",
                    color=0x808080,
                    url=f"https://eft.monster/",
                )
                embed.set_image(url=url)
                embed.set_author(
                    name="Twitter: bojotaro_tarkov",
                    url="https://twitter.com/bojotaro_tarkov",
                )
                embed.set_footer(
                    text="提供元: https://twitter.com/bojotaro_tarkov/status/1368569066928046080?s=20"
                )
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

        elif message.content.upper() == f"{prefix}TARKOVTOOLS":
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
            await message.channel.send(embed=embed, file=file)
            return 0

        elif message.content.upper() == f"{prefix}WEAPON":
            embeds = []
            for n, (index, values) in enumerate(weaponsData.items()):
                embed = discord.Embed(
                    title=f"武器一覧({n+1}/{len(weaponsData)})",
                    url=f"{enWikiUrl}Weapons",
                    timestamp=updateTimestamp,
                )
                embed.add_field(
                    name=f"{index}",
                    value=f"[{index} Wikiリンク]({enWikiUrl}Weapons#{index.replace(' ', '_')})",
                    inline=False,
                )
                for value in values:
                    embed.add_field(
                        name=value["名前"],
                        value=f"[海外Wikiリンク]({enWikiUrl}{value['weaponUrl']})",
                        inline=False,
                    )
                embed.set_footer(
                    text=f"Source: The Official Escape from Tarkov Wiki 最終更新"
                )
                embeds.append(embed)
            for embed in embeds:
                print(len(embed))
                await message.channel.send(embed=embed)
            return 0

        # 日本語wiki版 武器取得廃止
        """
        elif message.content.upper() == f"{prefix}WEAPON":
            weaponsName, weaponsData, colName = GetweaponData()
            bulletsData = GetBulletData()
            embeds = []
            for n, (index, values) in enumerate(weaponsData.items()):
                embed = discord.Embed(
                    title=f"武器一覧({n+1}/{len(weaponsData)})", url=f"{jaWikiUrl}武器一覧"
                )
                embed.add_field(
                    name=f"{index}",
                    value=f"[{index}wikiリンク]({jaWikiUrl}武器一覧#h2_content_1_{n})",
                    inline=False,
                )
                infostr = ""
                for value in values:
                    urlencord = value[0].replace(" ", "%20")
                    infostr += f"[{value[0]}]({jaWikiUrl}{urlencord})  "
                    for c, v in zip(colName[index][2:], value[2:]):
                        if c == "使用弾薬":
                            fixName = v.replace("×", "x")
                            fixName = fixName.replace(" ", "")
                            infostr += (
                                f"**{c}**: [{v}]({jaWikiUrl}弾薬{bulletsData[fixName]})  "
                            )
                        else:
                            infostr += f"**{c}**: {v}  "
                    embed.add_field(
                        name=value[0], value=infostr, inline=False,
                    )
                    infostr = ""
                embed.set_footer(text=f"Escape from Tarkov 日本語 Wiki: {jaWikiUrl}")
                embeds.append(embed)
            for embed in embeds:
                await message.channel.send(embed=embed)
            return 0
        """

        commandList["各武器詳細表示"] = [weaponName.upper() for weaponName in weaponsName]
        # コマンドの予測変換
        hints = {
            command
            for command in list(itertools.chain.from_iterable(commandList.values()))
            if difflib.SequenceMatcher(
                None, message.content.upper(), prefix + command
            ).ratio()
            >= 0.65
        }

        if message.content.upper().split("/")[1] in [
            weaponName.upper() for weaponName in weaponsName
        ]:
            infoStr = ""
            fixtext = message.content.upper().replace(" ", "").split("/")[1]
            weaponData = [
                value
                for values in weaponsData.values()
                for value in values
                if value["名前"].upper().replace(" ", "") == fixtext
            ][0]
            for colName, value in weaponData.items():
                if colName in [
                    "名前",
                    "weaponUrl",
                    "typeUrl",
                    "imageUrl",
                    "cartridgeUrl",
                    "soldByUrl",
                ]:
                    pass
                elif weaponData[colName] == "":
                    pass
                elif colName == "種類":
                    infoStr += f"\n**{colName.capitalize()}**: __[{weaponData[colName]}]({enWikiUrl}{weaponData['typeUrl']})__"
                elif colName == "口径":
                    infoStr += f"\n**{colName.capitalize()}**: __[{weaponData[colName]}]({enWikiUrl}{weaponData['cartridgeUrl']})__"
                elif colName == "発射機構":
                    infoStr += f"\n**{colName.capitalize()}**:"
                    for firingMode in weaponData[colName]:
                        infoStr += f"\n・__{firingMode}__"
                elif colName == "販売元":
                    infoStr += f"\n**{colName.capitalize()}**: __[{weaponData[colName]}]({enWikiUrl}{weaponData['soldByUrl']})__"
                elif colName == "詳細":
                    text = weaponData[colName]
                    # 翻訳前言語
                    source = "en"
                    # 翻訳後言語
                    Target = "ja"
                    gasUrl = f"https://script.google.com/macros/s/AKfycbxvCS-29LVgrm9-cSynGl19QUIB7jTpzuvFqflus_P0BJtXX80ahLazltfm2rbMGVVs/exec?text={text}&source={source}&target={Target}"
                    res = rq.get(gasUrl).json()
                    if res["code"] == 200:
                        text = res["text"]
                    infoStr += f"\n**{colName}**:"
                    infoStr += f"\n> {weaponData[colName]}"
                    infoStr += f"\n> {text}"
                    infoStr += "> Google翻訳"
                elif colName == "使用可能弾薬":
                    infoStr += f"\n**{colName.capitalize()}**:"
                    for ammunition in weaponData[colName]:
                        infoStr += f"\n・__{ammunition}__"
                elif colName == "リコイル":
                    infoStr += f"\n**{colName.capitalize()}**:"
                    for key, value in weaponData[colName].items():
                        infoStr += f"\n・**{key}**: __{value}__"
                else:
                    infoStr += (
                        f"\n**{colName.capitalize()}**: __{weaponData[colName]}__"
                    )
            embed = discord.Embed(
                title=weaponData["名前"],
                url=f"{enWikiUrl}{weaponData['weaponUrl']}",
                description=infoStr,
                timestamp=updateTimestamp,
            )
            embed.set_footer(text=f"Source: The Official Escape from Tarkov Wiki 最終更新")
            embed.set_image(url=weaponData["imageUrl"])
            await message.channel.send(embed=embed)
            return 0

        elif message.content.upper() == f"{prefix}RANDOMWEAPON":
            embed = discord.Embed(
                title="迷ったときのEFT武器抽選",
                description=f"{str(message.author).split('#')[0]}が使用する武器は...",
                color=0x2ECC69,
            )
            weapon = random.choice(weaponsName)
            await message.channel.send(embed=embed)
            await message.channel.send(f"/{weapon}")
            return 0

        elif len(hints) > 0:
            text = ""
            embed = discord.Embed(
                title="Hint", description="もしかして以下のコマンドじゃね?", color=0xFF0000
            )
            n = 0
            comand = None
            for n, hint in enumerate(hints):
                comand = hint
                embed.add_field(name=f"{n+1}", value=f"__`{prefix}{hint}`__")
            if n == 0:
                text = f"{prefix}{comand}"
                await message.channel.send(text)
            else:
                embed.set_footer(text="これ以外に使えるコマンドは /help で確認できるよ!")
                await message.channel.send(embed=embed)
            return 0

        else:
            text = "入力されたがコマンドが見つからなかった...ごめんなさい。\n"
            text += "これ以外に使えるコマンドは /help で確認できるよ!"
            await message.channel.send(text)
            return 0
    elif "@everyone BOTの更新をしました!" == message.content:
        embed = discord.Embed(
            title="更新履歴一覧",
            timestamp=datetime.datetime.utcfromtimestamp(
                dt.strptime(
                    list(patchNotes.keys())[0].split(":", 1)[1] + "+09:00",
                    "%Y/%m/%d %H:%M%z",
                ).timestamp()
            ),
        )
        for index, values in patchNotes.items():
            text = ""
            for N, value in enumerate(values):
                text += f"{N+1}. {value}\n"
            embed.add_field(
                name=f"version: {index.split(':', 1)[0]}", value=text, inline=False
            )
        embed.set_footer(text=f"EFT Wiki Bot 最終更新")
        await message.channel.send(embed=embed)


def Initialize():
    traderNames = GetTraderName()
    bossNames = GetBossName()
    weaponsName, weaponsData = GetWeaponsData()
    updateTimestamp = datetime.datetime.utcfromtimestamp(
        dt.now(pytz.timezone("Asia/Tokyo")).timestamp()
    )
    return traderNames, bossNames, weaponsName, weaponsData, updateTimestamp


def GetTraderName():
    res = rq.get(f"{enWikiUrl}Trading")
    soup = BeautifulSoup(res.text, "lxml")
    soup = soup.find(class_="wikitable sortable")
    return [
        s.find_all("a")[0].get_text().replace(" ", "")
        for s in soup.find_all("tr")
        if s.find_all("a")
    ]


def GetBossName():
    res = rq.get(f"{enWikiUrl}Characters")
    soup = BeautifulSoup(res.text, "lxml")
    soup = soup.find_all(class_="wikitable sortable")
    return [
        s.find_all("a")[0].get_text().replace(" ", "")
        for s in soup[1].find_all("tr")
        if s.find_all("a")
    ]


def GetBulletData():
    res = rq.get(f"{jaWikiUrl}弾薬")
    soup = BeautifulSoup(res.text, "lxml").find("div", {"class": "container-wrapper"})
    exclusion = ["概要", "表の見方", "弾薬の選び方", "拳銃弾", "PDW弾", "ライフル弾", "散弾", "グレネード弾", "未実装"]
    bulletsData = {
        s.get_text()
        .replace(" ", "")
        .replace("Gyurza", "")
        .replace("STs-130", ""): s.get("href")
        for s in soup.find("div", {"class": "contents"}).find("ul").find_all("a")
        if s.get_text().replace(" ", "") not in exclusion
    }
    return bulletsData


def GetWeaponsData():
    res = rq.get(f"{enWikiUrl}Weapons")
    soup = BeautifulSoup(res.text, "lxml")
    exclusion = [
        "Primaryweapons",
        "Secondaryweapons",
        "Stationaryweapons",
        "Throwableweapons",
        "Upcomingweapons",
        "Primaryweapons",
        "Secondaryweapons",
        "Launchers",
        "Throwableweapons",
        "Mines",
        "Stationaryweapons",
        "Mortar",
        "AntitankGun",
        "Unconfirmedweapons",
        "PrimaryWeapons",
        "SecondaryWeapons",
        "Launchers",
    ]
    primaryCategory = [
        "Assault rifles",
        "Assault carbines",
        "Light machine guns",
        "Submachine guns",
        "Shotguns",
        "Designated marksman rifles",
        "Sniper rifles",
        "Grenade launchers",
    ]
    secondaryCategory = ["Pistols"]
    stationaryCategory = [
        "Heavy machine guns",
        "Automatic Grenade launchers",
    ]
    meleeCategory = ["Melee weapons"]
    throwableCategoryOne = [
        "Fragmentation grenades",
    ]
    throwableCategoryTwo = [
        "Smoke grenades",
        "Stun grenades",
    ]
    weaponCategoryList = [
        category.get_text()
        for category in soup.find_all("span", {"class": "toctext"})
        if category.get_text().replace(" ", "") not in exclusion
    ]
    weaponsData = {}
    for weapons, category in zip(
        soup.find_all(class_="wikitable sortable")[: len(weaponCategoryList) - 1],
        weaponCategoryList,
    ):
        weaponsData[category] = []
        if category in primaryCategory or category in secondaryCategory:
            for weapon in weapons.find("tbody").find_all("tr")[1:]:
                weaponInformations = GetWeaponInformations(weapon)
                weaponsData[category].append(
                    {
                        "名前": weapon.find_all("td")[0].find("a")["title"],
                        "種類": weaponInformations["Type"].get_text(),
                        "typeUrl": weaponInformations["Type"]
                        .find("a")["href"]
                        .replace("/wiki/", "", 1),
                        "weaponUrl": weapon.find_all("td")[0]
                        .find("a")["href"]
                        .replace("/wiki/", "", 1),
                        "imageUrl": re.sub(
                            "scale-to-width-down/[0-9]*\?cb=[0-9]*",
                            "",
                            weapon.find("img")["src"],
                        )
                        + "?format=original",
                        "重量": [
                            ""
                            if weaponInformations["Weight"] == ""
                            else weaponInformations["Weight"].get_text()
                        ][0],
                        "サイズ": [
                            ""
                            if weaponInformations["Grid size"] == ""
                            else weaponInformations["Grid size"].get_text()
                        ][0],
                        "販売元": [
                            ""
                            if weaponInformations["Sold by"] == ""
                            else weaponInformations["Sold by"].get_text()
                        ][0],
                        "soldByUrl": [
                            ""
                            if weaponInformations["Sold by"] == ""
                            else weaponInformations["Sold by"]
                            .find("a")["href"]
                            .replace("/wiki/", "", 1)
                        ][0],
                        "リコイル": {
                            "垂直反動": str(
                                weaponInformations["Recoil %"]
                                .contents[0]
                                .replace(" ", "")
                                .split(":")[1]
                            ),
                            "水平反動": str(
                                weaponInformations["Recoil %"]
                                .contents[2]
                                .replace(" ", "")
                                .split(":")[1]
                            ),
                        },
                        "有効射程": weaponInformations["Effective distance"].get_text(),
                        "口径": weapon.find_all("td")[1].find("a")["title"],
                        "cartridgeUrl": weapon.find_all("td")[1]
                        .find("a")["href"]
                        .replace("/wiki/", "", 1),
                        "発射機構": [
                            firingmode.replace("\n", "").replace("\xa0", " ")
                            for firingmode in weapon.find_all("td")[2].contents
                            if firingmode != soup.hr and firingmode != soup.br
                        ],
                        "連射速度": weapon.find_all("td")[3].get_text().replace("\n", ""),
                        "使用可能弾薬": [
                            acceptedAmmunition
                            for acceptedAmmunition in weaponInformations[
                                "Accepted ammunition"
                            ]
                            .get_text()
                            .split("\n")
                            if acceptedAmmunition != ""
                        ],
                        "詳細": weapon.find_all("td")[4].get_text(),
                    }
                )
        elif category in stationaryCategory:
            for weapon in weapons.find("tbody").find_all("tr")[1:]:
                weaponInformations = GetWeaponInformations(weapon)
                weaponsData[category].append(
                    {
                        "名前": weapon.find_all("td")[0].find("a")["title"],
                        "weaponUrl": weapon.find_all("td")[0]
                        .find("a")["href"]
                        .replace("/wiki/", "", 1),
                        "imageUrl": re.sub(
                            "scale-to-width-down/[0-9]*\?cb=[0-9]*",
                            "",
                            weapon.find("img")["src"],
                        )
                        + "?format=original",
                        "重量": [
                            ""
                            if weaponInformations["Weight"] == ""
                            else weaponInformations["Weight"].get_text()
                        ][0],
                        "サイズ": [
                            ""
                            if weaponInformations["Grid size"] == ""
                            else weaponInformations["Grid size"].get_text()
                        ][0],
                        "販売元": [
                            ""
                            if weaponInformations["Sold by"] == ""
                            else weaponInformations["Sold by"].get_text()
                        ][0],
                        "soldByUrl": [
                            ""
                            if weaponInformations["Sold by"] == ""
                            else weaponInformations["Sold by"]
                            .find("a")["href"]
                            .replace("/wiki/", "", 1)
                        ][0],
                        "口径": weapon.find_all("td")[1].find("a")["title"],
                        "cartridgeUrl": weapon.find_all("td")[1]
                        .find("a")["href"]
                        .replace("/wiki/", "", 1),
                        "発射機構": [
                            firingmode.replace("\n", "").replace("\xa0", " ")
                            for firingmode in weapon.find_all("td")[2].contents
                            if firingmode != soup.hr and firingmode != soup.br
                        ],
                        "使用可能弾薬": [
                            acceptedAmmunition
                            for acceptedAmmunition in weaponInformations[
                                "Accepted ammunition"
                            ]
                            .get_text()
                            .split("\n")
                            if acceptedAmmunition != ""
                        ],
                    }
                )
        elif category in meleeCategory:
            for weapon in weapons.find("tbody").find_all("tr")[1:]:
                weaponInformations = GetWeaponInformations(weapon)
                weaponsData[category].append(
                    {
                        "名前": weapon.find_all("td")[0].find("a")["title"],
                        "weaponUrl": weapon.find_all("td")[0]
                        .find("a")["href"]
                        .replace("/wiki/", "", 1),
                        "imageUrl": re.sub(
                            "scale-to-width-down/[0-9]*\?cb=[0-9]*",
                            "",
                            weapon.find("img")["src"],
                        )
                        + "?format=original",
                        "重量": [
                            ""
                            if weaponInformations["Weight"] == ""
                            else weaponInformations["Weight"].get_text()
                        ][0],
                        "サイズ": [
                            ""
                            if weaponInformations["Grid size"] == ""
                            else weaponInformations["Grid size"].get_text()
                        ][0],
                        "販売元": [
                            ""
                            if weaponInformations["Sold by"] == ""
                            else weaponInformations["Sold by"].get_text()
                        ][0],
                        "soldByUrl": [
                            ""
                            if weaponInformations["Sold by"] == ""
                            else weaponInformations["Sold by"]
                            .find("a")["href"]
                            .replace("/wiki/", "", 1)
                        ][0],
                        "斬撃ダメージ": weapon.find_all("td")[1]
                        .get_text()
                        .replace("\n", "",),
                        "斬撃距離": weapon.find_all("td")[2].get_text().replace("\n", "",),
                        "刺突ダメージ": weapon.find_all("td")[3]
                        .get_text()
                        .replace("\n", "",),
                        "刺突距離": weapon.find_all("td")[4].get_text().replace("\n", "",),
                        "詳細": weapon.find_all("td")[5].get_text().replace("\n", "",),
                    }
                )

        elif category in throwableCategoryOne:
            for weapon in weapons.find("tbody").find_all("tr")[1:]:
                weaponInformations = GetWeaponInformations(weapon)
                weaponsData[category].append(
                    {
                        "名前": weapon.find_all("td")[0].find("a")["title"],
                        "weaponUrl": weapon.find_all("td")[0]
                        .find("a")["href"]
                        .replace("/wiki/", "", 1),
                        "imageUrl": re.sub(
                            "scale-to-width-down/[0-9]*\?cb=[0-9]*",
                            "",
                            weapon.find("img")["src"],
                        )
                        + "?format=original",
                        "重量": [
                            ""
                            if weaponInformations["Weight"] == ""
                            else weaponInformations["Weight"].get_text()
                        ][0],
                        "サイズ": [
                            ""
                            if weaponInformations["Grid size"] == ""
                            else weaponInformations["Grid size"].get_text()
                        ][0],
                        "販売元": [
                            ""
                            if weaponInformations["Sold by"] == ""
                            else weaponInformations["Sold by"].get_text()
                        ][0],
                        "soldByUrl": [
                            ""
                            if weaponInformations["Sold by"] == ""
                            else weaponInformations["Sold by"]
                            .find("a")["href"]
                            .replace("/wiki/", "", 1)
                        ][0],
                        "信管作動時間(s)": weapon.find_all("td")[1].get_text(),
                        "加害範囲": weapon.find_all("td")[2].get_text(),
                        "1破片当たりの最大ダメージ": weapon.find_all("td")[3].get_text(),
                        "破片数": weapon.find_all("td")[4].get_text(),
                        "詳細": weapon.find_all("td")[5].get_text(),
                    }
                )

        elif category in throwableCategoryTwo:
            for weapon in weapons.find("tbody").find_all("tr")[1:]:
                weaponInformations = GetWeaponInformations(weapon)
                weaponsData[category].append(
                    {
                        "名前": weapon.find_all("td")[0].find("a")["title"],
                        "weaponUrl": weapon.find_all("td")[0]
                        .find("a")["href"]
                        .replace("/wiki/", "", 1),
                        "imageUrl": re.sub(
                            "scale-to-width-down/[0-9]*\?cb=[0-9]*",
                            "",
                            weapon.find("img")["src"],
                        )
                        + "?format=original",
                        "重量": [
                            ""
                            if weaponInformations["Weight"] == ""
                            else weaponInformations["Weight"].get_text()
                        ][0],
                        "サイズ": [
                            ""
                            if weaponInformations["Grid size"] == ""
                            else weaponInformations["Grid size"].get_text()
                        ][0],
                        "販売元": [
                            ""
                            if weaponInformations["Sold by"] == ""
                            else weaponInformations["Sold by"].get_text()
                        ][0],
                        "soldByUrl": [
                            ""
                            if weaponInformations["Sold by"] == ""
                            else weaponInformations["Sold by"]
                            .find("a")["href"]
                            .replace("/wiki/", "", 1)
                        ][0],
                        "信管作動時間(s)": weapon.find_all("td")[1].get_text(),
                        "詳細": weapon.find_all("td")[2].get_text(),
                    }
                )

    weaponsName = [
        weapon["名前"] for weaponData in weaponsData.values() for weapon in weaponData
    ]
    return weaponsName, weaponsData


def GetWeaponInformations(weapon):
    res = rq.get(
        f"{enWikiUrl}{weapon.find_all('td')[0].find('a')['href'].replace('/wiki/', '', 1)}"
    )
    soup = BeautifulSoup(res.text, "lxml")
    weaponInformations = {}
    weaponInformations = {
        label.get_text().replace("\xa0", " "): contents
        for weaponInformation in soup.find_all("table", {"class": "va-infobox-group"})
        for label, contents in zip(
            weaponInformation.find_all("td", {"class": "va-infobox-label"}),
            weaponInformation.find_all("td", {"class": "va-infobox-content"}),
        )
    }
    if "Weight" not in weaponInformations:
        weaponInformations["Weight"] = ""
    if "Sold by" not in weaponInformations:
        weaponInformations["Sold by"] = ""
    if "Grid size" not in weaponInformations:
        weaponInformations["Grid size"] = ""
    return weaponInformations


"""
def GetweaponData():
    res = rq.get(f"{jaWikiUrl}武器一覧")
    soup = BeautifulSoup(res.text, "lxml").find(
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
"""

# マップ画像取得
def GetMapImage(mapName):
    url = "https://escapefromtarkov.fandom.com/wiki/"
    mapImages = {}
    res = rq.get(f"{url}{mapName}")
    soup = BeautifulSoup(res.text, "lxml").find("div", {"class": "mw-parser-output"})
    # Map情報以外のimgタグを除去
    for s in soup.find_all("table"):
        s.decompose()
    soup.find("center").decompose()
    try:
        soup.find("div", {"class": "thumb"}).decompose()
    except:
        pass
    # Map情報の全imgタグを取得
    images = soup.find_all("img")
    for image in images:
        if (
            # customs: "FullScreenMapIcon.png"
            image["alt"] != "FullScreenMapIcon.png"
            # interchange: "The Power Switch"
            and image["alt"] != "The Power Switch"
            # laboratory: "TheLab-Insurance-Messages-01.PNG"
            and image["alt"] != "TheLab-Insurance-Messages-01.PNG"
            and image["alt"] != ""
        ):
            # 参照画像サイズを800px -> オリジナル画像サイズに変換
            mapImages[image["alt"]] = (
                image["src"].replace("/scale-to-width-down/800", "")
                + "&format=original"
            )
    return mapImages


# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)
