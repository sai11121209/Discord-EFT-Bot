# インストールした discord.py を読み込む
import os
import discord
import random
import difflib
import itertools
import requests as rq
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
    "タスク一覧表示": ["TASK"],
    "マップ抽選": ["RANDOM"],
    "早見表表示": ["CHART"],
    "更新履歴表示": ["PATCH"],
    "ソースコード表示": ["SOURCE"],
}
# 上に追記していくこと
PatchNotes = {
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
async def on_message(message):
    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return

    if Prefix == message.content[0]:
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
            Embed.set_footer(text=f"{Prefix}マップ名で各マップの詳細情報にアクセスできます。 例: /reserve")
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
                description="EFT(Escape from Tarkov) Wiki Bot使用可能コマンド一覧",
                color=0x2ECC69,
            )
            for Key, Values in CommandList.items():
                if Key != "各武器詳細表示":
                    if type(Values) == list:
                        Text = ""
                        for Value in Values:
                            Text += f"{Prefix}{Value}\n"
                    else:
                        Text = f"{Prefix}{Values}\n"
                else:
                    Text = "/武器名"
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
            Embed.set_footer(text="トレーダー名をクリックすることで各トレーダータスクの詳細情報にアクセスできます。")
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
            Text = "Hint: もしかして以下のコマンドですか?\n"
            for n, hint in enumerate(hints):
                Text += f"{n+1}. {Prefix}{hint}\n"
            Text += "その他使用可能コマンド表示は /help で確認できます。"
            await message.channel.send(Text)
            return 0

        else:
            Text = "そのようなコマンドは存在しません。\n"
            Text += "使用可能コマンド表示は /help で確認できます。"
            await message.channel.send(Text)
            return 0


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
