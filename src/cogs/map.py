import discord
import requests as rq
from bs4 import BeautifulSoup
from discord.ext import commands


class Map(commands.Cog):

    # TestCogクラスのコンストラクタ。Botを受取り、インスタンス変数として保持。
    def __init__(self, bot):
        self.bot = bot

    # コマンドの作成。コマンドはcommandデコレータで必ず修飾する。
    @commands.command(description="マップ一覧表示")
    async def map(self, ctx, *arg):
        async with ctx.typing():
            if len(arg) == 1:
                if arg[0].upper() in self.bot.mapList:
                    receivedtext = arg[0].upper()
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
                        embed.set_footer(
                            text=f"Source: The Official Escape from Tarkov Wiki"
                        )
                        await ctx.send(embed=embed)
                        n += 1
                else:
                    await self.on_command_error(self, ctx, commands.CommandNotFound)
            else:
                embed = discord.Embed(
                    title="マップ",
                    url=f"{self.bot.enWikiUrl}Map",
                    color=0x2ECC69,
                )
                for map, values in self.bot.mapList.items():
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
                                    text += (
                                        f"__[{v}]({self.bot.enWikiUrl}Scav_Raiders)__ "
                                    )
                                else:
                                    text += f"__[{v}]({self.bot.enWikiUrl}{v})__ "
                        text += "\n"
                    text += f"**詳細情報**: __[JA]({self.bot.jaWikiUrl}{map})__ / __[EN]({self.bot.enWikiUrl}{receivedtext})__\n"
                    embed.add_field(name=map, value=text)
                embed.set_thumbnail(
                    url="https://static.wikia.nocookie.net/escapefromtarkov_gamepedia/images/4/43/Map.png/revision/latest?cb=20200619104902&format=original"
                )
                embed.set_footer(
                    text=f"{self.bot.command_prefix}マップ名で各マップの地形情報を表示できるよー。 例: {self.bot.command_prefix}reserve"
                )
                await ctx.send(embed=embed)


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
