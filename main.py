# インストールした discord.py を読み込む
import os
import discord
import random
import keep_alive

try:
    from .local_settings import *
except ImportError:
    pass

keep_alive.keep_alive()

# 自分のBotのアクセストークンに置き換えてください
if os.getenv("TOKEN"):
    TOKEN = os.getenv("TOKEN")


# 接続に必要なオブジェクトを生成
client = discord.Client()

# 起動時に動作する処理
@client.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    print("ログインしました")


# メッセージ受信時に動作する処理
@client.event
async def on_message(message):
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
        "EFT公式サイト": "TOP",
        "EFT日本語Wikiトップ": "WIKITOP",
        "マップ一覧": "MAP",
        "各マップ情報取得": Maps,
        "武器一覧": "WEAPON",
        "マップ抽選": "RANDOM",
    }
    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return

    if Prefix in message.content:
        if message.content.upper() == f"{Prefix}TOP":
            Text = f"{Prefix}EFT公式サイト\n"
            Text += "https://www.escapefromtarkov.com/"
            await message.channel.send(Text)

        if message.content.upper() == f"{Prefix}WIKITOP":
            Text = f"{Prefix}EFT日本語Wikiトップ\n"
            Text += Url
            await message.channel.send(Text)
        elif message.content.upper() == f"{Prefix}MAP":
            Text = "マップ一覧\n"
            for Map in Maps:
                Text += f"{Map}: {Url}{Map}\n"
            Text += f"{Prefix}マップ名で各マップの詳細情報にアクセスできます。 例: /reserve"
            await message.channel.send(Text)
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
        elif message.content.upper() == f"{Prefix}RANDOM":
            embed = discord.Embed(
                title="迷ったときのEFTマップ抽選", description="今回のマップは...", color=0x2ECC69,
            )
            # embed.set_thumbnail(url=message.author.avatar_url)
            embed.add_field(name="MAP", value=random.choice(Maps), inline=False)
            await message.channel.send(embed=embed)

        elif message.content.upper() == f"{Prefix}WEAPON":
            Text = f"{Prefix}武器一覧\n"
            Text += f"{Url}武器一覧"
            await message.channel.send(Text)

        elif message.content.upper() == f"{Prefix}HELP":
            embed = discord.Embed(
                title="ヘルプ",
                description="EFT(Escape from Tarkov) Wiki Bot使用可能コマンド一覧",
                color=0x2ECC69,
            )
            for Key, Values in CommandList.items():
                if type(Values) == list:
                    Text = ""
                    for Value in Values:
                        Text += f"{Prefix}{Value}\n"
                else:
                    Text = f"{Prefix}{Values}\n"
                embed.add_field(name=f"{Key}コマンド", value=Text, inline=False)
            await message.channel.send(embed=embed)


# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)
