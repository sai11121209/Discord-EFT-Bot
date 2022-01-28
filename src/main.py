# インストールした discord.py を読み込む
import os
import re
import time
import pytz
import json
import config
import random
import discord
import difflib
import datetime
import traceback
import random as r
import requests as rq
from bs4 import BeautifulSoup
from datetime import datetime as dt
from discord_slash import SlashCommand
from discord.ext import commands, tasks


os.chdir(os.path.dirname(os.path.abspath(__file__)))  # カレントディレクトリ変更

start = time.time()

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

INITIAL_EXTENSIONS = [
    "cogs.help",
    "cogs.link",
    "cogs.map",
    "cogs.character",
    "cogs.task",
    "cogs.weapon",
    "cogs.chart",
    "cogs.other",
    "cogs.random",
    "cogs.status",
    "cogs.rate",
    "cogs.develop",
]

# BOT起動時にデータ読み込みしない場合True
SAFE_MODE = False
start_state = True
# 接続に必要なオブジェクトを生成
intents = discord.Intents.all()
intents.members = True
intents.reactions = True
client = discord.Client(intents=intents)
developMode = False
prefix = "/"
jaWikiUrl = "https://wikiwiki.jp/eft/"
enWikiUrl = "https://escapefromtarkov.fandom.com/wiki/"
marketUrl = "https://tarkov-market.com/item/"
sendTemplatetext = "EFT(Escape from Tarkov) Wiki "
voiceChatRole = 839773477095211018
receivedtext = None
mapData = None
slash = None
emojiList = [
    "1️⃣",
    "2️⃣",
    "3️⃣",
    "4️⃣",
    "5️⃣",
    "6️⃣",
    "7️⃣",
    "8️⃣",
    "9️⃣",
    "🔟",
]
traderList = {
    "Prapor": {
        "stampid": 828552629248327690,
        "fullname": "Pavel Yegorovich Romanenko",
        "location": "Town",
        "origin": "ロシア連邦",
        "wares": [
            "武器",
            "弾薬",
            "手榴弾",
            "弾倉",
            "武器MOD",
        ],
        "services": [
            "保険",
            "修理",
        ],
        "currencies": ["Roubles (₽)"],
    },
    "Therapist": {
        "stampid": 828552629256192040,
        "fullname": "Elvira Khabibullina",
        "location": "Streets of Tarkov",
        "origin": "ロシア連邦",
        "wares": [
            "医療品",
            "地図",
            "食料品",
            "コンテナ",
        ],
        "services": [
            "保険",
        ],
        "currencies": [
            "Roubles (₽)",
            "Euros (€)",
        ],
    },
    "Fence": {
        "stampid": 828552627989512204,
        "fullname": "Real name unknown",
        "location": "A network of outlets all over Tarkov and its outskirts",
        "origin": "ロシア連邦",
        "wares": [
            "売られたもの全て",
        ],
        "services": [],
        "currencies": [
            "Roubles (₽)",
        ],
    },
    "Skier": {
        "stampid": 828552629436416010,
        "fullname": "Alexander Fyodorovich Kiselyov",
        "location": "Customs",
        "origin": "ロシア連邦",
        "wares": [
            "武器",
            "弾薬",
            "武器MOD",
            "コンテナ",
            "ユーロ",
        ],
        "services": [
            "修理",
        ],
        "currencies": [
            "Roubles (₽)",
            "Dollars ($)",
            "Euros (€)",
        ],
    },
    "Peacekeeper": {
        "stampid": 828552628682096710,
        "fullname": "Tadeusz Pilsudski",
        "location": "Terminal",
        "origin": "ポーランド共和国",
        "wares": [
            "欧米・NATOの武器",
            "弾薬",
            "手榴弾",
            "弾倉",
            "武器MOD",
            "USドル",
        ],
        "services": [],
        "currencies": [
            "Dollars ($)",
        ],
    },
    "Mechanic": {
        "stampid": 828552628887093328,
        "fullname": "Sergey Arsenyevich Samoylov",
        "location": "Factory",
        "origin": "不明",
        "wares": [
            "欧米・NATOの武器",
            "グロック17/18",
            "弾薬",
            "弾倉",
            "武器MOD",
        ],
        "services": [
            "修理",
        ],
        "currencies": [
            "Roubles (₽)",
            "Euros (€)",
            "Bitcoin (₿)",
        ],
    },
    "Ragman": {
        "stampid": 828552630120349716,
        "fullname": "Abramyan Arshavir Sarkisivich",
        "location": "Interchange",
        "origin": "不明",
        "wares": [
            "衣類",
            "アーマー",
            "バックパック",
            "タクティカリグ",
            "ギア",
        ],
        "services": [
            "戦闘服",
        ],
        "currencies": [
            "Roubles (₽)",
        ],
    },
    "Jaeger": {
        "stampid": 828552628396621855,
        "fullname": "Kharitonov Ivan Egorovich",
        "location": "Woods",
        "origin": "不明",
        "wares": [
            "ソビエト連邦の武器",
            "弾薬",
            "弾倉",
            "武器MOD",
            "隠れ家素材",
        ],
        "services": [],
        "currencies": [
            "Roubles (₽)",
        ],
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
        "drops": [
            "ASh-12 12.7x55 assault rifle",
        ],
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
    # "各マップ情報表示": mapList,
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
    "ヘッドセット早見表": ["HEADSET"],
    "更新履歴表示": ["PATCH"],
    "現在時刻表示": ["NOW"],
    "ビットコイン価格表示": ["BTC"],
    "ソースコード表示": ["SOURCE"],
}
notificationInformation = {}
# 上に追記していくこと
patchNotes = {
    "4.2:2022/01/28 16:00": [
        "マップ情報表示コマンド __`MAP`__ のReserveにおいて日本語翻訳マップを追加しました。",
    ],
    "4.1:2022/01/20 16:00": [
        "現在のユーロ、ドルのEFT為替レート表示コマンド _`RATE`_ を追加しました。",
        "ユーロからルーブルの値段を計算するコマンド _`RATE EURO`_ を追加しました。",
        "ドルからルーブルの値段を計算するコマンド _`RATE DOLLAR`_ を追加しました。",
        "弾薬性能表示コマンド __`AMMO`__ を呼び出した際に表示される弾薬の性能比較画像を12.12版に更新しました。",
    ],
    "4.0:2022/01/14 02:00": [
        "Discord SlashCommand の実装に伴う大幅仕様変更",
        "各武器詳細表示コマンド __`WEAPON 武器名`__ において表示されるEmbedの表示方式を変更しました。",
        "__`ARMOR`__ __`HEADSET`__ __`ITEMVALUE`__ __`RECOVERY`__ __`TASKITEM`__ __`TASKTREE`__ __`LIGHTHOUSETASK`__ の7コマンドが早見表表示コマンド __`CHART`__ のサブコマンドとして組み込まれました。以降は __`CHART ARMOR`__ のように呼び出せるようになります。",
        "サーバステータス確認コマンド __`STATUS`__ の動作を安定化しました。",
        "武器抽選コマンド __`RANDOMWEAPON`__ マップ抽選コマンド __`RANDOMMAP`__ において発生していたバグの修正。",
        "一部処理の並列化による起動時間、応答時間の短縮。",
        "その他細かい修正",
    ],
    "3.7:2022/01/02 06:00": [
        "サーバステータス確認コマンドを __`STATUS`__ を実装しました。",
        "本BOTが5分置きににEscape from Tarkovサーバの状態を監視し、異常があった場合に通知してくれる機能を実装しました。",
        "その他細かい修正",
    ],
    "3.6:2021/11/25 20:00": [
        "弾薬性能表示コマンドにおいて __`AMMO 口径名`__ __`AMMO 弾薬名`__ を入力することで特定口径の弾薬や、弾薬の性能を見ることできるようになりました。",
        "その他細かい修正",
    ],
    "3.5:2021/11/09 13:00": [
        "海外Wikiのサイト仕様変更に伴う内部処理の修正",
        "各武器詳細表示コマンド __`WEAPON 武器名`__ において表示されるAmmoChartのUIを変更しました。",
        "その他細かい修正",
    ],
    "3.4:2021/10/25 18:00": [
        "コマンド実行時呼び出しに使用したメッセージを消去するようになりました",
        "海外Wikiのサイト仕様変更に伴う内部処理の修正",
        "その他細かい修正",
    ],
    "3.3:2021/09/30 00:00": [
        "Among Us Botとの連携アップデート",
        "その他細かい修正",
    ],
    "3.2.1:2021/09/14 00:00": [
        "武器抽選コマンド __`RANDOMWEAPON`__ においてすべての処理が正常に実行されず複数回同様のコマンドが実行されてしまう問題の修正。WOLTERFEN#6329ありがとうございます。",
        "マップ抽選コマンド __`RANDOMMAP`__ においてすべての処理が正常に実行されず複数回同様のコマンドが実行されてしまう問題に加え、未実装マップも結果として出力されてしまっていた問題を修正。",
    ],
    "3.2:2021/08/19 13:00": [
        "ヘッドセット早見表コマンド __`HEADSET`__ を追加しました。",
        "各武器詳細表示コマンド __`WEAPON 武器名`__ において投擲武器名を入力した際正常にレスポンスが行われなかった問題の修正。",
        "各武器詳細表示コマンド __`WEAPON 武器名`__ にArmorクラス7が表示されてしまっていた問題の修正。",
    ],
    "3.1:2021/08/07 16:00": [
        "各武器詳細表示コマンド __`WEAPON 武器名`__ を入力した際に弾薬表も同時に表示されるようになりました。",
    ],
    "3.0.1:2021/07/24 01:00": [
        "各武器詳細表示コマンド __`WEAPON 武器名`__ を入力した際に発生していたエラー20210654072607を修正しました。WOLTERFEN#6329ありがとうございます。",
        "海外公式wikiのサイト更新に伴う仕様変更によりマップ、タスク、武器情報にアクセスできなかった問題を修正しました。",
        "各武器詳細表示コマンド __`WEAPON 武器名`__  、タスク詳細表示コマンド __`TASK {タスク名}`__ コマンドの補完処理における不具合を修正しました。",
        "ボイスチャット参加中(ボイスチャンネル参加者ロール付与中)に特定メッセージに対して返信を行なった際に返信先のユーザを自動的にメンションする様になりました。",
        "各種細かい不具合、動作改善。",
    ],
    "3.0:2021/07/12 23:30": [
        "コマンド呼び出し時の不具合を修正しました。",
        "タスク詳細表示コマンド __`TASK {タスク名}`__ の動作を一部変更しました。",
        "タスクツリー早見表コマンド __`TASKTREE`__ を追加しました。",
        "武器のロードアウトを組むことができるURLを呼び出すロードアウト作成コマンド __`LOADOUTS`__ を追加しました。",
        "タスク詳細表示コマンド __`TASK {タスク名}`__ を正式実装しました。",
        "タスク一覧コマンド __`TASK`__ とタスク詳細表示コマンド __`TASK {タスク名}`__ の2コマンドが仮追加されました。",
        "本サーバに送信されたメッセージに対して __`❌`__ リアクションが付与すると誰でもメッセージを消去できてしまう脆弱性の修正を行いました。",
        "__`notification-general`__ において発言した際の全体メンションの処理が変更されました。",
        "ボイスチャンネル使用中のユーザがテキストを書き込んだ際の処理が変更されました。",
        "各マップ情報表示コマンド __`MAP マップ名`__ 各武器詳細表示コマンド __`WEAPON 武器名`__ を入力した際に発生していたエラー20210617212538を修正しました。",
        "Discord Botフレームワーク環境への移行準に伴い各マップ情報表示コマンド ~~__`マップ名`__~~ から __`MAP マップ名`__ に変更されました。",
        "Discord Botフレームワーク環境への移行準に伴い各武器詳細表示コマンド ~~__`武器名`__~~ から __`WEAPON 武器名`__ に変更されました。",
        "ヘルプコマンド __`HELP`__ が呼び出された際にヘルプコマンドが消去されてしまう不具合を修正しました。",
        "全コマンドにおいて __`❌`__ リアクションが付与されクリックすることで表示されている実行結果が消去できるようになりました。",
    ],
    "3.0:2021/06/08 20:35": [
        "タスク使用アイテム早見表コマンド __`TASKITEM`__ で表示される画像が0.12.9.10532時点のものに更新されました。",
        "ヘルプコマンド __`HELP`__ を呼び出した後コマンドを入力し正常に呼び出された場合HELPコマンドの出力が消去されるようになりました。",
        "ボイスチャット入退室通知が入室時のみ通知されるように変更されました。",
        "マップ関連情報をBot起動時に動的取得するようになりました。",
        "未実装マップもマップ一覧表示コマンド __`MAP`__ で表示されるようになりました",
        "Discord Botフレームワーク環境への移行準備完了。現在試験的に新環境でプログラムを実行中です。",
        "例外処理発生時エラーログを出力するようになりました。",
        "コマンド補完性能向上。",
        "各種不具合の修正。",
    ],
    "2.3:2021/05/20 19:00": ["コマンド不一致時に表示されるヒントコマンドをリアクション選択から実行できるようになりました。"],
    "2.2.1:2021/05/20 14:00": ["各武器詳細表示コマンド __`武器名`__ の仕様を変更しました。"],
    "2.2:2021/05/15 18:00": [
        "出会いを目的としたフレンド募集を含む投稿を行った場合警告が送られる様になりました。",
    ],
    "2.1:2021/05/08 17:00": [
        "自動全体メンションに本文を含む様に変更されました。",
        "TarkovTools情報表示コマンド __`TARKOVTOOLS`__ を追加しました。",
        "以前から仕様変更予定にあった早見表表示、アーマ早見表表示コマンド __`CHART`__ __`ARMOR`__ の正式実装を行いました。",
        "早見表表示、アーマ早見表表示コマンド __`CHART`__ __`ARMOR`__ の正式実装、又TarkovTools情報表示コマンド __`TARKOVTOOLS`__ 追加に伴い弾薬性能表示コマンド __`AMMO`__の仕様が一部変更されました。",
    ],
    "2.0.1:2021/05/07 17:00": [
        "__`notification-general`__ において発言を行うと自動全体メンションをする様になりました。",
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
    "1.10.2:2021/04/06 19:13": ["弾薬性能表示コマンド __`AMMO`__ の挙動が変更されました。"],
    "1.10.1:2021/04/06 03:20": [
        "機能改善に伴いタスク一覧表示コマンドが ~~__`TASK`__~~  から ディーラー一覧表示コマンドの __`DEALER`__ に統合されました。"
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


class EFTBot(commands.Bot):
    def __init__(
        self,
        command_prefix,
        intents,
        case_insensitive,
        LOCAL_HOST,
        developMode,
        jaWikiUrl,
        enWikiUrl,
        marketUrl,
        emojiList,
        mapData,
        traderList,
        bossList,
        notificationInformation,
        patchNotes,
        traderNames,
        bossNames,
        weaponsName,
        weaponsData,
        taskName,
        taskData,
        ammoData,
        updateTimestamp,
        safeMode,
    ):
        super().__init__(
            command_prefix, intents=intents, case_insensitive=case_insensitive
        )
        global slash
        slash = SlashCommand(self, sync_commands=True, override_type=True)
        self.LOCAL_HOST = LOCAL_HOST
        self.developMode = developMode
        self.jaWikiUrl = jaWikiUrl
        self.enWikiUrl = enWikiUrl
        self.marketUrl = marketUrl
        self.emojiList = emojiList
        self.mapData = mapData
        self.traderList = traderList
        self.bossList = bossList
        self.notificationInformation = notificationInformation
        self.patchNotes = patchNotes
        self.traderNames = traderNames
        self.bossNames = bossNames
        self.weaponsName = weaponsName
        self.weaponsData = weaponsData
        self.taskName = taskName
        self.taskData = taskData
        self.ammoData = ammoData
        self.updateTimestamp = updateTimestamp
        self.safeMode = safeMode
        self.hits = {}
        self.enrageCounter = 0
        self.bot_id = config.bot_id
        self.guild_ids = config.guild_ids
        self.saiId = config.saiId
        self.remove_command("help")
        self.helpEmbed = None
        self.server_status = None
        self.server_status_count = 0
        try:
            for cog in INITIAL_EXTENSIONS:
                try:
                    self.load_extension(cog)
                except Exception:
                    traceback.print_exc()
        except:
            pass

    # 起動時発火
    @client.event
    async def on_ready(self):
        # exception-log チャンネル
        channel = self.get_channel(848999028658405406)
        # 起動したらターミナルにログイン通知が表示される
        print("ログインしました")
        if LOCAL_HOST == False:
            await self.change_presence(
                activity=discord.Game(name="Escape from Tarkov", type=1)
            )
            elapsed_time = time.time() - start
            startTime = dt.now(pytz.timezone("Asia/Tokyo"))
            embed = discord.Embed(
                title=f" StartingLog ({startTime.strftime('%Y%m%d%H%M%S')})",
                color=0xFF0000,
                timestamp=datetime.datetime.utcfromtimestamp(
                    dt.now(pytz.timezone("Asia/Tokyo")).timestamp()
                ),
            )
            embed.add_field(
                name="StartupTime",
                value=f"```{startTime.strftime('%Y/%m/%d %H:%M:%S')}```",
                inline=False,
            )
            embed.add_field(
                name="TimeRequired", value=f"```{elapsed_time}```", inline=False
            )
            embed.set_footer(text=f"{self.user.name}")
            self.change_status.start()
            self.server_status_checker.start()
            await channel.send(embed=embed)

    @tasks.loop(minutes=10)
    async def change_status(self):
        rand_int = random.randint(0, 5)
        if LOCAL_HOST == False:
            if not developMode:
                if self.server_status == 0:
                    if rand_int == 0:
                        await self.change_presence(
                            activity=discord.Game(name="Escape from Tarkov", type=1)
                        )
                    else:
                        map = r.choice(
                            [
                                key
                                for key, val in self.mapData.items()
                                if val["Duration"] != ""
                            ]
                        ).upper()
                        await self.change_presence(
                            activity=discord.Game(name=f"マップ{map}", type=1)
                        )

    @tasks.loop(minutes=1)
    async def server_status_checker(self):
        res = rq.get("https://status.escapefromtarkov.com/api/global/status")
        res = json.loads(res.text)["status"]
        channel = self.get_channel(811566006132408340)
        if self.server_status_count == 0:
            self.server_status = res
            self.server_status_count += 1
            if res == 0:
                pass
            elif res == 1:
                await self.change_presence(
                    activity=discord.Game(
                        name="EFTサーバアップデートにより停止中",
                        start=dt.now(pytz.timezone("Asia/Tokyo")),
                        type=5,
                    )
                )
            elif res == 2:
                await self.change_presence(
                    activity=discord.Game(
                        name="EFTサーバ接続不安定",
                        start=dt.now(pytz.timezone("Asia/Tokyo")),
                        type=5,
                    )
                )
            else:
                await self.change_presence(
                    activity=discord.Game(
                        name="EFTサーバ障害発生中",
                        start=dt.now(pytz.timezone("Asia/Tokyo")),
                        type=5,
                    )
                )
        else:
            if self.server_status == 0 and res != 0:
                # 鯖落ち発生
                if res == 1:
                    embed = discord.Embed(
                        title=f"EscapeTarkovServerStatus",
                        description="現在アップデートのためEscapeTarkovServerは停止しています。",
                        color=0xD42929,
                        url="https://status.escapefromtarkov.com/",
                        timestamp=datetime.datetime.utcfromtimestamp(
                            dt.now(pytz.timezone("Asia/Tokyo")).timestamp()
                        ),
                    )
                    await self.change_presence(
                        activity=discord.Game(
                            name="EFTサーバアップデートにより停止中",
                            start=dt.now(pytz.timezone("Asia/Tokyo")),
                            type=5,
                        )
                    )
                elif res == 2:
                    embed = discord.Embed(
                        title=f"EscapeTarkovServerStatus",
                        description="現在EscapeTarkovServerへの接続が不安定な状態になっています。",
                        color=0xD42929,
                        url="https://status.escapefromtarkov.com/",
                        timestamp=datetime.datetime.utcfromtimestamp(
                            dt.now(pytz.timezone("Asia/Tokyo")).timestamp()
                        ),
                    )
                    await self.change_presence(
                        activity=discord.Game(
                            name="EFTサーバ接続不安定",
                            start=dt.now(pytz.timezone("Asia/Tokyo")),
                            type=5,
                        )
                    )
                else:
                    embed = discord.Embed(
                        title=f"EscapeTarkovServerStatus",
                        description="現在EscapeTarkovServerにおいて障害が発生しています。",
                        color=0xD42929,
                        url="https://status.escapefromtarkov.com/",
                        timestamp=datetime.datetime.utcfromtimestamp(
                            dt.now(pytz.timezone("Asia/Tokyo")).timestamp()
                        ),
                    )
                    await self.change_presence(
                        activity=discord.Game(
                            name="EFTサーバ障害発生中",
                            start=dt.now(pytz.timezone("Asia/Tokyo")),
                            type=5,
                        )
                    )
                await channel.send("@everyone", embed=embed)
                await self.slash.commands["status"].invoke(channel)
            elif self.server_status == 2 and res == 3:
                # 鯖状況悪化
                embed = discord.Embed(
                    title=f"EscapeTarkovServerStatus",
                    description="現在EscapeTarkovServerにおいて障害が発生しています。",
                    color=0x70B035,
                    url="https://status.escapefromtarkov.com/",
                    timestamp=datetime.datetime.utcfromtimestamp(
                        dt.now(pytz.timezone("Asia/Tokyo")).timestamp()
                    ),
                )
                await self.change_presence(
                    activity=discord.Game(
                        name="EFTサーバ障害発生中",
                        start=dt.now(pytz.timezone("Asia/Tokyo")),
                        type=5,
                    )
                )
                await channel.send("@everyone", embed=embed)
                await self.slash.commands["status"].invoke(channel)
            elif self.server_status != 0 and res == 0:
                # 鯖復活
                if self.server_status == 1:
                    embed = discord.Embed(
                        title=f"EscapeTarkovServerStatus",
                        description="EscapeTarkovServerのアップデートが終了しサービスが再開しました。",
                        color=0x70B035,
                        url="https://status.escapefromtarkov.com/",
                        timestamp=datetime.datetime.utcfromtimestamp(
                            dt.now(pytz.timezone("Asia/Tokyo")).timestamp()
                        ),
                    )
                else:
                    embed = discord.Embed(
                        title=f"EscapeTarkovServerStatus",
                        description="EscapeTarkovServerにおいて発生していた障害は現在解消されました。",
                        color=0x70B035,
                        url="https://status.escapefromtarkov.com/",
                        timestamp=datetime.datetime.utcfromtimestamp(
                            dt.now(pytz.timezone("Asia/Tokyo")).timestamp()
                        ),
                    )
                await channel.send("@everyone", embed=embed)
                await self.slash.commands["status"].invoke(channel)
                await self.change_presence(
                    activity=discord.Game(name="Escape from Tarkov", type=1)
                )
            self.server_status = res
            self.server_status_count += 1

    # 役職追加時発火
    @client.event
    async def add_role(self, member):
        role = member.guild.get_role(voiceChatRole)
        await member.add_roles(role)

    # 役職剥奪時発火
    @client.event
    async def remove_role(self, member):
        role = member.guild.get_role(voiceChatRole)
        await member.remove_roles(role)

    # ボイスチャンネル参加・退出時発火
    @client.event
    async def on_voice_state_update(self, member, before, after):
        # 本番テキストチャンネル
        channel = self.get_channel(818751361511718942)
        # テストテキストチャンネル
        # channel = client.get_channel(808821063387316254)
        user = str(member).split("#")[0]
        if before.channel == None and after.channel:
            await channel.send(
                f"@everyone {user} がボイスチャンネル {after.channel} にてボイスチャットを開始しました。"
            )
            await self.add_role(member)
        elif (
            before.channel
            and after.channel
            and before.deaf == after.deaf
            and before.mute == after.mute
            and before.self_deaf == after.self_deaf
            and before.self_mute == after.self_mute
            and before.self_stream == after.self_stream
            and before.self_video == after.self_video
            and before.channel.id != after.channel.id
        ):
            await channel.send(
                f"@everyone {user} がボイスチャンネル {before.channel} からボイスチャンネル {after.channel} に移動しました。"
            )
        elif before.channel and after.channel == None:
            # await channel.send(f"@everyone {user} がボイスチャンネル {before.channel} を退出しました。")
            await self.remove_role(member)

    # リアクション反応時発火
    @client.event
    async def on_reaction_add(self, reaction, user):
        if (
            not user.bot
            and not self.developMode
            and reaction.message.channel.id != 890461420330819586
        ):
            try:
                if len(self.hints[reaction.emoji].split(" ")) == 1:
                    await self.slash.commands[self.hints[reaction.emoji]](
                        reaction.message.channel
                    )
                else:
                    if self.hintsEmbed:
                        await self.hintsEmbed.delete()
                        self.hintsEmbed = None
                    await self.slash.commands[
                        self.hints[reaction.emoji].split(" ")[0]
                    ].invoke(
                        reaction.message.channel,
                        self.hints[reaction.emoji].split(" ")[1:],
                    )
            except:
                pass

    @client.event
    async def on_raw_reaction_add(self, payload):
        user = await self.fetch_user(payload.user_id)
        if not user.bot:
            try:
                channel = await self.fetch_channel(payload.channel_id)
                message = await channel.fetch_message(payload.message_id)
                if not self.developMode:
                    if (
                        payload.emoji.name == "❌"
                        and message.author.bot
                        and message.channel.id != 890618625508122624
                    ):
                        await message.delete()
            except:
                pass

    @client.event
    async def on_slash_command_error(self, ctx, ex):
        if isinstance(ex, commands.CommandNotFound):
            fixText = ""
            hitCommands = []
            if ctx.command == "map":
                hitCommands += [map.lower() for map in self.mapData]
            elif ctx.command == "weapon":
                hitCommands += [weaponName.lower() for weaponName in self.weaponsName]
            elif ctx.command == "ammo":
                hitCommands += [ammoData for ammoData in self.ammoData.keys()]
                hitCommands += [
                    ammo["Name"]
                    for ammoData in self.ammoData.values()
                    for ammo in ammoData
                ]
            elif ctx.command == "task":
                hitCommands += [taskName.lower() for taskName in self.taskName]
            # コマンドの予測変換
            self.hints = {
                self.emojiList[n]: hint
                for n, hint in enumerate(
                    [
                        command
                        for command in hitCommands
                        if difflib.SequenceMatcher(
                            None,
                            ctx.args[0].lower(),
                            self.command_prefix + command,
                        ).ratio()
                        >= 0.59
                    ][:10]
                )
            }
            if ctx.args[0].lower() in self.hints.values():
                self.hints = {"1️⃣": ctx.args[0].lower()}
            if len(self.hints) > 0:
                text = ""
                embed = discord.Embed(
                    title="Hint", description="もしかして以下のコマンドじゃね?", color=0xFF0000
                )
                fixHints = self.hints
                for emoji, hint in self.hints.items():
                    if hint in [map.lower() for map in self.mapData]:
                        fixHints[emoji] = f"map {hint}"
                    elif hint in [
                        weaponName.lower() for weaponName in self.weaponsName
                    ]:
                        fixHints[emoji] = f"weapon {hint}"
                    elif hint in [ammoData for ammoData in self.ammoData.keys()]:
                        fixHints[emoji] = f"ammo {hint}"
                    elif hint in [
                        ammo["Name"]
                        for ammoData in self.ammoData.values()
                        for ammo in ammoData
                    ]:
                        fixHints[emoji] = f"ammo {hint}"
                    elif hint in [task.lower() for task in self.taskName]:
                        fixHints[emoji] = f"task {hint}"
                    embed.add_field(
                        name=emoji, value=f"__`{prefix}{fixHints[emoji]}`__"
                    )
                self.hints = fixHints
                if len(self.hints) == 1:
                    if len(self.hints["1️⃣"].split(" ")) != 1:
                        await self.slash.commands[
                            self.hints["1️⃣"].split(" ")[0]
                        ].invoke(
                            ctx,
                            self.hints["1️⃣"].split(" ")[1:],
                        )
                    else:
                        await self.slash.commands[self.hints["1️⃣"]].invoke(
                            ctx,
                        )
                else:
                    embed.set_footer(text="これ以外に使えるコマンドは /help で確認できるよ!")
                    self.hintsEmbed = await ctx.send(embed=embed)
                    try:
                        for emoji in self.hints.keys():
                            await self.hintsEmbed.add_reaction(emoji)
                        await self.hintsEmbed.add_reaction("❌")
                    except:
                        pass
            else:
                text = f"入力されたコマンド {ctx.command} {ctx.args[0]} は見つからなかったよ...ごめんね。\n"
                text += f"これ以外に使えるコマンドは {self.command_prefix}help で確認できるよ!"
                await ctx.send(text)
        elif isinstance(ex, commands.ExtensionError):
            pass
        elif isinstance(ex, commands.MissingRole):
            pass
        else:
            # exception-log チャンネル
            channel = self.get_channel(846977129211101206)
            errorTime = dt.now(pytz.timezone("Asia/Tokyo"))
            embed = discord.Embed(
                title=f"ErrorLog ({errorTime.strftime('%Y%m%d%H%M%S')})",
                description=f"ご迷惑をおかけしております。コマンド実行中において例外処理が発生しました。\nこのエラーログは sai11121209 に送信されています。 {ctx.author.mention} バグを発見してくれてありがとう!",
                color=0xFF0000,
                timestamp=datetime.datetime.utcfromtimestamp(
                    dt.now(pytz.timezone("Asia/Tokyo")).timestamp()
                ),
            )
            embed.add_field(
                name="Time",
                value=f"```{errorTime.strftime('%Y/%m/%d %H:%M:%S')}```",
                inline=False,
            )
            embed.add_field(
                name="ServerId", value=f"```{ctx.guild.id}```", inline=False
            )
            embed.add_field(
                name="ServerName", value=f"```{ctx.guild.name}```", inline=False
            )
            embed.add_field(
                name="ChannelId", value=f"```{ctx.channel.id}```", inline=False
            )
            embed.add_field(
                name="ChannelName", value=f"```{ctx.channel.name}```", inline=False
            )
            embed.add_field(name="UserId", value=f"```{ctx.author.id}```", inline=False)
            embed.add_field(
                name="UserName", value=f"```{ctx.author.name}```", inline=False
            )
            embed.add_field(
                name="ErrorCommand", value=f"```{ctx.command}```", inline=False
            )
            embed.add_field(name="ErrorDetails", value=f"```{ex}```", inline=False)
            embed.set_footer(text=f"{ctx.me.name}")
            await channel.send(embed=embed)
            if self.LOCAL_HOST == False:
                sendMessage = await ctx.send(embed=embed)
                await sendMessage.add_reaction("❌")

    @client.event
    async def on_slash_command(self, ctx):
        if self.developMode:
            await self.on_slash_command_error(
                ctx, commands.ExtensionError("develop_mode")
            )

    @client.event
    async def on_command_completion(self, ctx):
        if ctx.message.content != f"{self.command_prefix}help" and self.helpEmbed:
            await self.helpEmbed.delete()
            self.helpEmbed = None

    @client.event
    async def on_message(self, message):
        notificationGneralChannelId = 839769626585333761
        attachmentData = None
        attachmentsData = []
        # メッセージ送信者がBotだった場合は無視する
        if not len(message.content):
            return 0
        if not message.author.bot:
            if message.channel.id == notificationGneralChannelId:
                await message.delete()
                if message.reference:
                    user = [
                        member
                        for member in message.guild.members
                        if message.reference.resolved.content.split(" by ")[1]
                        == member.name
                    ][0]
                    await message.channel.send(f"{user.mention} {message.content}")
                else:
                    await message.channel.send(
                        f"@everyone {message.content} by {message.author.name}"
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
                    text = "@everyone 多分英語わからんやろ... 翻訳したるわ。感謝しな\n\n"
                    text += res["text"]
                    await message.channel.send(text)
                else:
                    pass
                if "MSK" in message.content:
                    channel = self.get_channel(839769626585333761)
                    text = "@everyone 重要なお知らせかもしれないからこっちにも貼っとくで\n"
                    text += f"{message.content}\n\n"
                    text += f"多分英語わからんやろ... 翻訳したるわ。感謝しな\n\n{res['text']}"
                    await channel.send(f"{text}{message.content}")

        if message.author.bot == False and self.LOCAL_HOST == False:
            if re.search(r"出会い|繋がりたい|美女|美男|可愛い|募集|フレンド", message.content):
                text = f"本discordサーバでは**出会い**を目的とした**フレンド募集**を含む投稿を全面的に禁止しています。\n\n 以下の文章が違反している可能性があります。\n\n **以下違反文** \n ```{message.content}```"
                embed = discord.Embed(
                    title="警告!!",
                    description=text,
                    color=0xFF0000,
                )

                await message.channel.send(f"{message.author.mention}")
                await message.channel.send(embed=embed)

        if (
            self.developMode
            and message.author.id != 279995095124803595
            and not message.author.bot
            and self.command_prefix == message.content[0]
        ):
            if self.enrageCounter < 5:
                await message.channel.send("機能改善会議しとるねん。話しかけんといて。")
            elif self.enrageCounter < 10:
                await message.channel.send("やめて。キレそうです。")
            else:
                await message.channel.send("やめて。呼ばないで。")
            self.enrageCounter += 1

        elif "@everyone BOTの更新をしました!" == message.content:
            await self.slash.commands["patch"].invoke(message.channel)
        if message.content[0] == self.command_prefix:
            if self.safeMode:
                await message.delete()
                embed = discord.Embed(
                    title="現在セーフモードで動作しているためコマンドを呼び出すことはできません。",
                    color=0xFF0000,
                )
                await message.channel.send(embed=embed)
            else:
                if not self.developMode:
                    await message.delete()
                    # await bot.process_commands(message)
                elif message.content == f"{self.command_prefix}develop":
                    await message.delete()
                    # await bot.process_commands(message)
        else:
            try:
                if (
                    message.guild.get_role(voiceChatRole) in message.author.roles
                    and message.channel.id != notificationGneralChannelId
                    and message.channel.id != 890618625508122624
                ):
                    await message.delete()
                    if message.mentions:
                        await message.channel.send(
                            f"<@&{voiceChatRole}> {message.mentions[0].mention} {message.content} by {message.author.name}"
                        )
                    else:
                        await message.channel.send(
                            f"<@&{voiceChatRole}> {message.content} by {message.author.name}"
                        )
            except:
                pass


def Initialize():
    mapLists = GetMapList()
    mapData = GetMapData(mapLists)
    traderNames = GetTraderName()
    bossNames = GetBossName()
    weaponsName, weaponsData = GetWeaponsData()
    taskName, taskData = GetTaskData()
    ammoData = GetAmmoData()
    updateTimestamp = datetime.datetime.utcfromtimestamp(
        dt.now(pytz.timezone("Asia/Tokyo")).timestamp()
    )
    return (
        mapData,
        traderNames,
        bossNames,
        weaponsName,
        weaponsData,
        taskName,
        taskData,
        ammoData,
        updateTimestamp,
    )


def GetMapList():
    res = rq.get(f"{enWikiUrl}Map_of_Tarkov")
    soup = BeautifulSoup(res.text, "lxml")
    mapList = {}
    columnData = []
    for i, mapDatas in enumerate(soup.find("tbody").find_all("tr")):
        if i != 0:
            mapName = (
                mapDatas.find_all("th")[1].find("a")["title"].upper().replace(" ", "")
            )
            mapList[mapName] = {}
        for j, mapData in enumerate(mapDatas.find_all(["th", "td"])):
            if i == 0:
                # 列名取得
                columnData.append(mapData.get_text().replace("\n", ""))
            else:
                if columnData[j] == "Banner":
                    try:
                        mapList[mapName].update(
                            {
                                columnData[j]: re.sub(
                                    "scale-to-width-down/[0-9]*\?cb=[0-9]*",
                                    "",
                                    mapData.find("img")["data-src"],
                                )
                                + "?format=original"
                            }
                        )
                    except:
                        mapList[mapName].update(
                            {
                                columnData[j]: re.sub(
                                    "scale-to-width-down/[0-9]*\?cb=[0-9]*",
                                    "",
                                    mapData.find("img")["src"],
                                )
                                + "?format=original"
                            }
                        )

                elif columnData[j] == "Name":
                    mapList[mapName].update(
                        {
                            columnData[j]: mapData.get_text().replace("\n", ""),
                            "MapUrl": mapData.find("a")["href"].replace(
                                "/wiki/", "", 1
                            ),
                        }
                    )
                else:
                    if mapData.find("hr"):
                        mapData.contents = [
                            map
                            for map in mapData
                            if map != mapData.find("hr") and map != "\n"
                        ]
                        if columnData[j] == "Duration" or columnData[j] == "Players":
                            tempData = {}
                            for map in mapData.contents:
                                key, value = (
                                    map.replace(" ", "")
                                    .replace("minutes", "")
                                    .split(":")
                                )
                                tempData.update({key: value.replace("\n", "")})
                            mapList[mapName].update({columnData[j]: tempData})

                        elif columnData[j] == "Enemies":
                            tempData = []
                            for map in mapData.contents:
                                try:
                                    tempData.append(map.get_text().replace(" ", ""))
                                except:
                                    pass
                            mapList[mapName].update(
                                {columnData[j]: list(set(tempData))}
                            )
                    else:
                        if columnData[j] == "Enemies":
                            mapList[mapName].update(
                                {
                                    columnData[j]: [
                                        mapData.get_text()
                                        .replace(" ", "")
                                        .replace("\n", "")
                                    ]
                                }
                            )
                        else:
                            mapList[mapName].update(
                                {
                                    columnData[j]: mapData.get_text()
                                    .replace("\n", "")
                                    .replace("minutes", "")
                                }
                            )

    return mapList


def GetMapData(mapLists):
    mapData = {}
    for key, value in mapLists.items():
        mapData[key] = value
        res = rq.get(f"{enWikiUrl}{value['MapUrl']}")
        soup = BeautifulSoup(res.text, "lxml").find(
            "div", {"class": "mw-parser-output"}
        )
        for s in soup.find_all("table"):
            s.decompose()

        try:
            soup.find("center").decompose()
            soup.find("div", {"class": "thumb"}).decompose()
        except:
            pass
        # Map情報の全imgタグを取得
        images = soup.find_all("img")
        mapData[key]["Images"] = {}
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
                mapData[key]["Images"].update(
                    {
                        image["alt"]: re.sub(
                            "scale-to-width-down/[0-9]*\?cb=[0-9]*",
                            "",
                            image["data-src"],
                        )
                        + "?format=original"
                    }
                )
    return mapData


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
    res = rq.get(f"{enWikiUrl}Scav_Bosses")
    soup = BeautifulSoup(res.text, "lxml")
    soup = soup.find(class_="wikitable sortable")
    return [
        s.find_all("a")[0].get_text().replace(" ", "")
        for s in soup.find_all("tr")
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
                try:
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
                                weapon.find("img")["data-src"],
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
                            "連射速度": weapon.find_all("td")[3]
                            .get_text()
                            .replace("\n", ""),
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
                except:
                    pass
        elif category in stationaryCategory:
            for weapon in weapons.find("tbody").find_all("tr")[1:]:
                try:
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
                                weapon.find("img")["data-src"],
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
                except:
                    pass
        elif category in meleeCategory:
            for weapon in weapons.find("tbody").find_all("tr")[1:]:
                try:
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
                                weapon.find("img")["data-src"],
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
                            .replace(
                                "\n",
                                "",
                            ),
                            "斬撃距離": weapon.find_all("td")[2]
                            .get_text()
                            .replace(
                                "\n",
                                "",
                            ),
                            "刺突ダメージ": weapon.find_all("td")[3]
                            .get_text()
                            .replace(
                                "\n",
                                "",
                            ),
                            "刺突距離": weapon.find_all("td")[4]
                            .get_text()
                            .replace(
                                "\n",
                                "",
                            ),
                            "詳細": weapon.find_all("td")[5]
                            .get_text()
                            .replace(
                                "\n",
                                "",
                            ),
                        }
                    )
                except:
                    pass
        elif category in throwableCategoryOne:
            for weapon in weapons.find("tbody").find_all("tr")[1:]:
                try:
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
                                weapon.find("img")["data-src"],
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
                except:
                    pass

        elif category in throwableCategoryTwo:
            for weapon in weapons.find("tbody").find_all("tr")[1:]:
                try:
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
                                weapon.find("img")["data-src"],
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
                except:
                    pass

    weaponsName = [
        weapon["名前"].upper()
        for weaponData in weaponsData.values()
        for weapon in weaponData
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


def GetTaskData():
    res = rq.get(f"{enWikiUrl}Quests")
    soup = BeautifulSoup(res.text, "lxml")
    taskData = {}
    for tasks in soup.find_all("table", {"class": "wikitable"}):
        dealerName = tasks.find_all("a")[0].text.replace("\n", "")
        try:
            taskData[dealerName] = {
                "dealerName": tasks.find_all("a")[0].text.replace("\n", ""),
                "dealerUrl": tasks.find_all("th")[0]
                .find("a")["href"]
                .replace("/wiki/", "", 1),
                "tasks": [],
            }
            res = rq.get(f"{enWikiUrl}{taskData[dealerName]['dealerUrl']}")
            soup = BeautifulSoup(res.text, "lxml").find(
                "div", {"class": "mw-parser-output"}
            )
        except:
            pass
        try:
            dealerThumbnail = (
                re.sub(
                    "scale-to-width-down/[0-9]*\?cb=[0-9]*",
                    "",
                    soup.find("td", {"class": "va-infobox-mainimage-image"}).find(
                        "img"
                    )["data-src"],
                )
                + "?format=original"
            )
        except:
            dealerThumbnail = (
                re.sub(
                    "scale-to-width-down/[0-9]*\?cb=[0-9]*",
                    "",
                    soup.find("td", {"class": "va-infobox-mainimage-image"}).find(
                        "img"
                    )["src"],
                )
                + "?format=original"
            )
        for task in tasks.find_all("tr")[2:]:
            try:
                taskDict = {
                    "questName": task.find_all("th")[0].text.replace("\n", ""),
                    "questUrl": task.find_all("th")[0]
                    .find("a")["href"]
                    .replace("/wiki/", "", 1),
                    "dealerName": dealerName,
                    "dealerUrl": tasks.find_all("th")[0]
                    .find("a")["href"]
                    .replace("/wiki/", "", 1),
                    "dealerThumbnail": dealerThumbnail,
                    "type": task.find_all("th")[1].text.replace("\n", ""),
                    "objectives": [
                        {
                            "text": objective.text.replace("\n", ""),
                            "linkText": {
                                linkText.text.replace("\n", ""): linkText[
                                    "href"
                                ].replace("/wiki/", "", 1)
                                for linkText in objective.find_all("a")
                            },
                        }
                        for objective in task.find_all("td")[0].find_all("li")
                    ],
                    "rewards": [
                        {
                            "text": reward.text.replace("\n", ""),
                            "linkText": {
                                linkText.text.replace("\n", ""): linkText[
                                    "href"
                                ].replace("/wiki/", "", 1)
                                for linkText in reward.find_all("a")
                            },
                        }
                        for reward in task.find_all("td")[1].find_all("li")
                    ],
                }
                res = rq.get(f"{enWikiUrl}{taskDict['questUrl']}")
                soup = BeautifulSoup(res.text, "lxml").find(
                    "div", {"class": "mw-parser-output"}
                )
                taskImages = {}
                for n, image in enumerate(soup.find_all("li", {"class": "gallerybox"})):
                    try:
                        taskImages.update(
                            {
                                image.find(
                                    "div", {"class": "gallerytext"}
                                ).p.text.replace("\n", ""): re.sub(
                                    "scale-to-width-down/[0-9]*\?cb=[0-9]*",
                                    "",
                                    image.find("img")["data-src"],
                                )
                                + "?format=original"
                            }
                        )
                    except:
                        try:
                            taskImages.update(
                                {
                                    f"No Name Image {n}": re.sub(
                                        "scale-to-width-down/[0-9]*\?cb=[0-9]*",
                                        "",
                                        image.find("img")["data-src"],
                                    )
                                    + "?format=original"
                                }
                            )
                        except:
                            taskImages.update(
                                {
                                    f"None{n}": re.sub(
                                        "scale-to-width-down/[0-9]*\?cb=[0-9]*",
                                        "",
                                        image.find("img")["src"],
                                    )
                                    + "?format=original"
                                }
                            )
                try:
                    taskDict.update(
                        {
                            "taskThumbnail": re.sub(
                                "scale-to-width-down/[0-9]*\?cb=[0-9]*",
                                "",
                                soup.find(
                                    "td", {"class": "va-infobox-mainimage-image"}
                                ).find("img")["data-src"],
                            )
                            + "?format=original",
                        }
                    )
                except:
                    taskDict.update(
                        {
                            "taskThumbnail": re.sub(
                                "scale-to-width-down/[0-9]*\?cb=[0-9]*",
                                "",
                                soup.find(
                                    "td", {"class": "va-infobox-mainimage-image"}
                                ).find("img")["src"],
                            )
                            + "?format=original",
                        }
                    )
                taskDict.update(
                    {
                        "taskImage": taskImages,
                        "location": [
                            {
                                "text": location.text,
                                "linkText": location["href"].replace("/wiki/", "", 1),
                            }
                            for location in soup.find_all(
                                "td", {"class": "va-infobox-content"}
                            )[1].find_all("a")
                        ],
                        "reqKappa": soup.find_all(
                            "table", {"class": "va-infobox-group"}
                        )[1]
                        .find_all("td", {"class": "va-infobox-content"})[-1]
                        .text,
                    }
                )
                try:
                    taskDict.update(
                        {
                            "previousQuest": [
                                {
                                    "text": PreviousQuest.text,
                                    "linkText": PreviousQuest["href"].replace(
                                        "/wiki/", "", 1
                                    ),
                                }
                                for PreviousQuest in soup.find_all(
                                    "table", {"class": "va-infobox-group"}
                                )[2]
                                .find_all("td", {"class": "va-infobox-content"})[0]
                                .find_all("a")
                            ],
                            "nextQuest": [
                                {
                                    "text": nextQuest.text,
                                    "linkText": nextQuest["href"].replace(
                                        "/wiki/", "", 1
                                    ),
                                }
                                for nextQuest in soup.find_all(
                                    "table", {"class": "va-infobox-group"}
                                )[2]
                                .find_all("td", {"class": "va-infobox-content"})[1]
                                .find_all("a")
                            ],
                        }
                    )
                except:
                    taskDict.update(
                        {
                            "previousQuest": [],
                            "nextQuest": [],
                        }
                    )
                taskData[dealerName]["tasks"].append(taskDict)
            except:
                pass
        taskName = [
            task["questName"].replace(" ", "").upper()
            for tasks in taskData.values()
            for task in tasks["tasks"]
        ]
    return taskName, taskData


def GetAmmoData():
    ammoCaliberUrlList = []
    ammoHeader = []
    ammoDatas = {}
    res = rq.get(f"{enWikiUrl}Ammunition")
    soup = BeautifulSoup(res.text, "lxml").find("div", {"class": "mw-parser-output"})
    soup.find("div", {"class": "toc"}).decompose()
    for table in soup.find_all("table", {"class": "wikitable"}):
        for ammoCaliber in table.find("tbody").find_all("tr")[1:]:
            ammoCaliberUrlList.append(
                ammoCaliber.find("a").get("href").replace("/wiki/", "")
            )
    for ammoCaliberUrl in ammoCaliberUrlList:
        res = rq.get(f"{enWikiUrl}{ammoCaliberUrl}")
        soup = BeautifulSoup(res.text, "lxml").find(
            "div", {"class": "mw-parser-output"}
        )
        ammoDatas[ammoCaliberUrl.replace("_", " ")] = []
        for table in soup.find_all("table", {"class": "wikitable"}):
            for n, ammoCaliber in enumerate(table.find("tbody").find_all("tr")):
                if n == 0:
                    for theader in ammoCaliber.find_all("th")[1:]:
                        ammoHeader.append(
                            theader.get_text(strip=True).replace("\xa0%", "")
                        )
                else:
                    ammoData = {}
                    ammoData["Caliber"] = ammoCaliberUrl.replace("_", " ")
                    try:
                        ammoData["Icon"] = (
                            re.sub(
                                "scale-to-width-down/[0-9]*\?cb=[0-9]*",
                                "",
                                ammoCaliber.find(["th", "td"]).find("img")["data-src"],
                            )
                            + "?format=original"
                        )
                    except:
                        ammoData["Icon"] = (
                            re.sub(
                                "scale-to-width-down/[0-9]*\?cb=[0-9]*",
                                "",
                                ammoCaliber.find(["th", "td"]).find("img")["src"],
                            )
                            + "?format=original"
                        )
                    for theader, ammo in zip(
                        ammoHeader, ammoCaliber.find_all(["th", "td"])[1:]
                    ):
                        ammoData[theader] = ammo.get_text(strip=True)
                    ammoDatas[ammoCaliberUrl.replace("_", " ")].append(ammoData)
    return ammoDatas


if __name__ == "__main__":
    if SAFE_MODE:
        mapData = None
        traderNames = None
        bossNames = None
        weaponsName = None
        weaponsData = None
        taskName = None
        taskData = None
        ammoData = None
        updateTimestamp = None
        bot = EFTBot(
            command_prefix="/",
            intents=intents,
            case_insensitive=True,
            LOCAL_HOST=LOCAL_HOST,
            developMode=developMode,
            jaWikiUrl=jaWikiUrl,
            enWikiUrl=enWikiUrl,
            emojiList=emojiList,
            mapData=mapData,
            traderList=traderList,
            bossList=bossList,
            notificationInformation=notificationInformation,
            patchNotes=patchNotes,
            traderNames=traderNames,
            bossNames=bossNames,
            weaponsName=weaponsName,
            weaponsData=weaponsData,
            taskName=taskName,
            taskData=taskData,
            ammoData=ammoData,
            updateTimestamp=updateTimestamp,
            safeMode=SAFE_MODE,
        )  # command_prefixはコマンドの最初の文字として使うもの。 e.g. !ping
        bot.run(TOKEN)  # Botのトークン
    else:
        (
            mapData,
            traderNames,
            bossNames,
            weaponsName,
            weaponsData,
            taskName,
            taskData,
            ammoData,
            updateTimestamp,
        ) = Initialize()
        MAINDATA = {
            "mapData": mapData,
            "ammoData": ammoData,
        }
        with open("main_data.json", "w") as f:
            json.dump(MAINDATA, f, indent=4)
        bot = EFTBot(
            command_prefix="/",
            intents=intents,
            case_insensitive=True,
            LOCAL_HOST=LOCAL_HOST,
            developMode=developMode,
            jaWikiUrl=jaWikiUrl,
            enWikiUrl=enWikiUrl,
            marketUrl=marketUrl,
            emojiList=emojiList,
            mapData=mapData,
            traderList=traderList,
            bossList=bossList,
            notificationInformation=notificationInformation,
            patchNotes=patchNotes,
            traderNames=traderNames,
            bossNames=bossNames,
            weaponsName=weaponsName,
            weaponsData=weaponsData,
            taskName=taskName,
            taskData=taskData,
            ammoData=ammoData,
            updateTimestamp=updateTimestamp,
            safeMode=SAFE_MODE,
        )  # command_prefixはコマンドの最初の文字として使うもの。 e.g. !ping
        bot.run(TOKEN)  # Botのトークン
