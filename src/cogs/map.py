import json
import config
import discord
import requests as rq
from bs4 import BeautifulSoup
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice


class Map(commands.Cog):
    try:
        guild_ids = [config.guild_ids]
        choices = []
        json_open = open("./main_data.json", "r")
        main_data = json.load(json_open)
        for name in main_data["mapData"]:
            choices.append(create_choice(name=name, value=name))
        map_options = [
            create_option(
                name="name",
                description="マップ名を指定します。",
                option_type=3,  # str
                required=False,
                choices=choices,
            ),
        ]
    except:
        map_options = None
    # TestCogクラスのコンストラクタ。Botを受取り、インスタンス変数として保持。
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(
        name="map",
        description="マップ一覧表示",
        options=map_options,
        guild_ids=guild_ids,
    )
    async def map(self, ctx: SlashContext, name: str = None):
        releaseText = ""
        releasedColor = 0x2ECC69
        unreleasedColor = 0xFF0000
        if name:
            text = f"{name} MAP INFORMATION\n"
            # LABORATORYのみ海外公式wikiのURLがThe_Labとなるため例外
            desText = ""
            name = name.upper()
            for key, value in self.bot.mapData[name.upper()].items():
                if key == "Banner":
                    pass
                elif key == "Name":
                    pass
                elif key == "MapUrl":
                    pass
                elif key == "Features":
                    featuresText = value
                    # 翻訳前言語
                    source = "en"
                    # 翻訳後言語
                    Target = "ja"
                    gasUrl = f"https://script.google.com/macros/s/AKfycbxvCS-29LVgrm9-cSynGl19QUIB7jTpzuvFqflus_P0BJtXX80ahLazltfm2rbMGVVs/exec?text={featuresText}&source={source}&target={Target}"
                    res = rq.get(gasUrl).json()
                    if res["code"] == 200:
                        tranceText = res["text"]
                        featuresText = f"\n**特徴**:"
                        featuresText += f"\n> {value}"
                        featuresText += f"\n\n> {tranceText}"
                        featuresText += "\n> Google翻訳"
                elif key == "Duration":
                    desText += f"**時間制限**: "
                    try:
                        desText += f"__昼間:{value['Day']}分__ __夜間:{value['Night']}分__"
                    except:
                        desText += f"__{value}分__"
                    desText += "\n"
                elif key == "Players":
                    desText += f"**人数**: "
                    try:
                        desText += f"__昼間:{value['Day']}人__ __夜間:{value['Night']}人__"
                    except:
                        desText += f"__{value}人__"
                    desText += "\n"
                elif key == "Enemies":
                    desText += f"**出現敵兵**: "
                    for v in value:
                        if v == "ScavRaiders":
                            desText += f"__[{v}]({self.bot.enWikiUrl}Scav_Raiders)__ "
                        else:
                            desText += f"__[{v}]({self.bot.enWikiUrl}{v})__ "
                    desText += "\n"
                elif key == "Release State":
                    if value == "Released":
                        color = releasedColor
                    else:
                        releaseText = "**未実装マップ**\n\n"
                        color = unreleasedColor
            embed = discord.Embed(
                title=text,
                description=releaseText + desText + featuresText,
                color=color,
                url=f"{self.bot.enWikiUrl}{self.bot.mapData[name]['MapUrl']}",
                timestamp=self.bot.updateTimestamp,
            )
            embed.set_image(url=self.bot.mapData[name]["Banner"])
            embed.set_footer(text=f"Source: The Official Escape from Tarkov Wiki 最終更新")
            sendMessage = await ctx.send(embed=embed)
            await sendMessage.add_reaction("❌")
            mapData = self.bot.mapData[name]["Images"]
            n = 1
            for key, value in mapData.items():
                embed = discord.Embed(
                    title=f"({n}/{len(mapData)}){text}",
                    description=f"[{key}]({value})",
                    color=color,
                    url=f"{self.bot.enWikiUrl}{self.bot.mapData[name]['MapUrl']}",
                    timestamp=self.bot.updateTimestamp,
                )
                embed.set_image(url=value)
                embed.set_footer(
                    text=f"Source: The Official Escape from Tarkov Wiki 最終更新"
                )
                sendMessage = await ctx.send(embed=embed)
                await sendMessage.add_reaction("❌")
                n += 1
            if name == "RESERVE":
                file = discord.File(f"../imgs/map/reserve/1.jpg")
                embed = discord.Embed(
                    title=f"({n}/{len(mapData)}){text}",
                    color=0x808080,
                    color=color,
                    url=f"{self.bot.enWikiUrl}{self.bot.mapData[name]['MapUrl']}",
                    timestamp=self.bot.updateTimestamp,
                )
                embed.set_image(url=f"attachment://1.jpg")
                embed.set_footer(
                    text=f"Source: The Official Escape from Tarkov Wiki 最終更新"
                )
                sendMessage = await ctx.send(embed=embed, file=file)
                await sendMessage.add_reaction("❌")
        else:
            embed = discord.Embed(
                title="マップ",
                url=f"{self.bot.enWikiUrl}Map",
                color=0x2ECC69,
                timestamp=self.bot.updateTimestamp,
            )
            for map, values in self.bot.mapData.items():
                text = ""
                if map == "The_Lab":
                    receivedtext = "LABORATORY"
                else:
                    receivedtext = map.capitalize()
                for key, value in values.items():
                    if key == "Duration":
                        text += f"**時間制限**: "
                        try:
                            text += f"__昼間:{value['Day']}分__ __夜間:{value['Night']}分__"
                        except:
                            text += f"__{value}分__"
                        text += "\n"
                    elif key == "difficulty":
                        text += f"**難易度**: __{value}__"
                        text += "\n"
                    elif key == "Players":
                        text += f"**人数**: "
                        try:
                            text += f"__昼間:{value['Day']}人__ __夜間:{value['Night']}人__"
                        except:
                            text += f"__{value}人__"
                        text += "\n"
                    elif key == "Enemies":
                        text += f"**出現敵兵**: "
                        for v in value:
                            if v == "ScavRaiders":
                                text += f"__[{v}]({self.bot.enWikiUrl}Scav_Raiders)__ "
                            else:
                                text += f"__[{v}]({self.bot.enWikiUrl}{v})__ "
                        text += "\n"
                text += f"**詳細情報**: __[JA]({self.bot.jaWikiUrl}{map})__ / __[EN]({self.bot.enWikiUrl}{self.bot.mapData[map]['MapUrl']})__\n"
                if values["Release State"] == "Released":
                    embed.add_field(name=values["Name"].upper(), value=text)
                else:
                    embed.add_field(name=map, value=f"~~{text}~~")
            embed.set_thumbnail(
                url="https://static.wikia.nocookie.net/escapefromtarkov_gamepedia/images/4/43/Map.png/revision/latest?cb=20200619104902&format=original"
            )
            embed.set_footer(
                text=f"{self.bot.command_prefix}マップ名で各マップの地形情報を表示できるよー。 例: {self.bot.command_prefix}reserve \n Source: The Official Escape from Tarkov Wiki 最終更新"
            )
            sendMessage = await ctx.send(embed=embed)
            await sendMessage.add_reaction("❌")


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


# Bot本体側からコグを読み込む際に呼び出される関数。
def setup(bot):
    bot.add_cog(Map(bot))  # TestCogにBotを渡してインスタンス化し、Botにコグとして登録する。
