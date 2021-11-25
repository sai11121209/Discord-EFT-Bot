from typing import Tuple
import discord
import requests as rq
import itertools
from discord.ext import commands
import numpy as np
import matplotlib.pyplot as plt
import os


class Weapon(commands.Cog):

    # TestCogクラスのコンストラクタ。Botを受取り、インスタンス変数として保持。
    def __init__(self, bot):
        self.bot = bot
        self.ammoChartCheck = None
        self.file = None

    def ammunition_figure_generation(self, ammoData, Caliber):
        try:
            X, Y, Name = [], [], []
            for ammunition in ammoData[Caliber]:
                Name.append(ammunition["Name"])
                X.append(int(ammunition["Damage"]))
                Y.append(int(ammunition["Penetration Power"]))
            xmin, xmax = 0, max(X) + 10
            hlinesList = np.arange(10, 61, 10)
            for x, y, name in zip(X, Y, Name):
                plt.plot(x, y, "o")
                plt.annotate(name.split(" ", 1)[1], xy=(x, y), color="white")
            plt.hlines(hlinesList, xmin, xmax, linestyle="dashed")
            for n, hline in enumerate(hlinesList):
                if hline < max(Y) + 10:
                    plt.text(
                        max(X) + 10,
                        hline + 0.5,
                        f"ARMOR CLASS {n+1}",
                        size=10,
                        horizontalalignment="right",
                        color="green",
                    )
            plt.xlim(min(X) - 10, max(X) + 10)
            plt.ylim(0, max(Y) + 10)
            plt.xlabel("DAMAGE")
            plt.ylabel("PENETRATION")
            plt.title(f"{Caliber} Ammo Chart")
            plt.grid()
            ax = plt.gca()
            ax.set_facecolor("black")
            plt.savefig("ammo.png", bbox_inches="tight", pad_inches=0.05)
            plt.close()
            self.ammoChartCheck = True
            self.file = discord.File("ammo.png")
        except:
            pass

    @commands.command(description="弾薬性能表示")
    async def ammo(self, ctx, *arg):
        async with ctx.typing():
            self.ammoChartCheck = False
            arg = list(itertools.chain.from_iterable(arg))
            if len(arg) != 0:
                if len(arg) == 1:
                    argText = arg[0]
                else:
                    argText = " ".join(arg)
                if argText in self.bot.ammoData.keys():
                    infoStr = ""
                    infoStr += f"\n**弾薬一覧**:"
                    for ammunition in self.bot.ammoData[argText]:
                        infoStr += f"\n・__[{ammunition['Name']}]({self.bot.enWikiUrl}{ammunition['Name'].replace(' ','_')})__"
                    embed = discord.Embed(
                        title=argText,
                        url=f"{self.bot.enWikiUrl}{argText.replace(' ', '_')}",
                        description=infoStr,
                        timestamp=self.bot.updateTimestamp,
                    )
                    embed.set_footer(
                        text=f"Source: The Official Escape from Tarkov Wiki 最終更新"
                    )
                    self.ammunition_figure_generation(self.bot.ammoData, argText)
                    embed.set_image(url="attachment://ammo.png")
                    sendMessage = await ctx.send(embed=embed, file=self.file)
                    await sendMessage.add_reaction("❌")
                    os.remove("ammo.png")
                elif argText in [
                    ammo["Name"]
                    for ammoData in self.bot.ammoData.values()
                    for ammo in ammoData
                ]:
                    ammunition = [
                        ammo
                        for ammoData in self.bot.ammoData.values()
                        for ammo in ammoData
                        if argText == ammo["Name"]
                    ][0]
                    infoStr = ""
                    for key, value in ammunition.items():
                        if value != "":
                            if key == "Caliber":
                                infoStr += f"\n**口径**: __[{value}]({self.bot.enWikiUrl}{value.replace('_', ' ')})__"
                            elif key == "Damage":
                                infoStr += f"\n**ダメージ**: {value}"
                            elif key == "Penetration Power":
                                infoStr += f"\n**貫通力**: {value}"
                            elif key == "Armor Damage":
                                infoStr += f"\n**アーマーダメージ**: {value}"
                            elif key == "Accuracy":
                                infoStr += f"\n**精度**: {value}"
                            elif key == "Recoil":
                                infoStr += f"\n**リコイル**: {value}"
                            elif key == "Fragmentationchance":
                                infoStr += f"\n**破裂確率**: {value}"
                            elif key == "Projectile Speed (m/s)":
                                infoStr += f"\n**跳弾確率**: {value}"
                            elif key == "Light bleedingchance":
                                infoStr += f"\n**軽度出血確率**: {value}%"
                            elif key == "Heavy bleedingchance":
                                infoStr += f"\n**重度出血確率**: {value}%"
                            elif key == "Ricochetchance":
                                infoStr += f"\n**弾速**: {value}"
                            elif key == "Special effects":
                                infoStr += f"\n**特殊効果**: {value}"
                            elif key == "Sold by":
                                infoStr += f"\n**販売元**: {value}"

                    embed = discord.Embed(
                        title=argText,
                        url=f"{self.bot.enWikiUrl}{argText.replace(' ', '_')}",
                        description=infoStr,
                        timestamp=self.bot.updateTimestamp,
                    )
                    embed.set_thumbnail(url=ammunition["Icon"])
                    embed.set_footer(
                        text=f"Source: The Official Escape from Tarkov Wiki 最終更新"
                    )
                    try:
                        sendMessage = await ctx.send(embed=embed)
                        await sendMessage.add_reaction("❌")
                    except:
                        import traceback

                        traceback.print_exc()
                else:
                    await self.bot.on_command_error(
                        ctx, commands.CommandNotFound("weapon")
                    )
            else:
                text = "弾薬性能表示"
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
                    sendMessage = await ctx.send(embed=embed)
                    await sendMessage.add_reaction("❌")

    @commands.command(description="武器一覧表示")
    async def weapon(self, ctx, *arg):
        async with ctx.typing():
            self.ammoChartCheck = False
            arg = list(itertools.chain.from_iterable(arg))
            if len(arg) != 0:
                if len(arg) == 1:
                    argText = arg[0].upper()
                else:
                    argText = " ".join(arg).upper()
                if argText in self.bot.weaponsName:
                    infoStr = ""
                    fixtext = argText.upper().replace(" ", "")
                    weaponData = [
                        value
                        for values in self.bot.weaponsData.values()
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
                            infoStr += f"\n**{colName.capitalize()}**: __[{weaponData[colName]}]({self.bot.enWikiUrl}{weaponData['typeUrl']})__"
                        elif colName == "口径":
                            infoStr += f"\n**{colName.capitalize()}**: __[{weaponData[colName]}]({self.bot.enWikiUrl}{weaponData['cartridgeUrl']})__"
                        elif colName == "発射機構":
                            infoStr += f"\n**{colName.capitalize()}**:"
                            for firingMode in weaponData[colName]:
                                infoStr += f"\n・__{firingMode}__"
                        elif colName == "販売元":
                            infoStr += f"\n**{colName.capitalize()}**: __[{weaponData[colName]}]({self.bot.enWikiUrl}{weaponData['soldByUrl']})__"
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
                                infoStr += f"\n・__[{ammunition}]({self.bot.enWikiUrl}{ammunition.replace(' ','_')})__"
                            self.ammunition_figure_generation(
                                self.bot.ammoData, weaponData["口径"]
                            )
                        elif colName == "リコイル":
                            infoStr += f"\n**{colName.capitalize()}**:"
                            for key, value in weaponData[colName].items():
                                infoStr += f"\n・**{key}**: __{value}__"
                        else:
                            infoStr += f"\n**{colName.capitalize()}**: __{weaponData[colName]}__"
                    embed = discord.Embed(
                        title=weaponData["名前"],
                        url=f"{self.bot.enWikiUrl}{weaponData['cartridgeUrl']}",
                        description=infoStr,
                        timestamp=self.bot.updateTimestamp,
                    )
                    embed.set_footer(
                        text=f"Source: The Official Escape from Tarkov Wiki 最終更新"
                    )
                    embed.set_image(url=weaponData["imageUrl"])
                    sendMessage = await ctx.send(embed=embed)
                    await sendMessage.add_reaction("❌")
                    if self.ammoChartCheck:
                        embed = discord.Embed(
                            title=f'{weaponData["名前"]}弾薬表',
                            url=f"{self.bot.enWikiUrl}{weaponData['weaponUrl']}",
                            description="Discordのバグ修正後、上記武器Embedと統合予定です",
                            timestamp=self.bot.updateTimestamp,
                        )
                        embed.set_footer(
                            text=f"Source: The Official Escape from Tarkov Wiki 最終更新"
                        )
                        embed.set_image(url="attachment://ammo.png")
                        sendMessage = await ctx.send(embed=embed, file=self.file)
                        await sendMessage.add_reaction("❌")
                        os.remove("ammo.png")
                else:
                    await self.bot.on_command_error(
                        ctx, commands.CommandNotFound("weapon")
                    )

            else:
                embeds = []
                for n, (index, values) in enumerate(self.bot.weaponsData.items()):
                    embed = discord.Embed(
                        title=f"武器一覧({n+1}/{len(self.bot.weaponsData)})",
                        url=f"{self.bot.enWikiUrl}Weapons",
                        timestamp=self.bot.updateTimestamp,
                    )
                    embed.add_field(
                        name=f"{index}",
                        value=f"[{index} Wikiリンク]({self.bot.enWikiUrl}Weapons#{index.replace(' ', '_')})",
                        inline=False,
                    )
                    for value in values:
                        embed.add_field(
                            name=value["名前"],
                            value=f"[海外Wikiリンク]({self.bot.enWikiUrl}{value['weaponUrl']})",
                            inline=False,
                        )
                    embed.set_footer(
                        text=f"Source: The Official Escape from Tarkov Wiki 最終更新"
                    )
                    embeds.append(embed)
                for embed in embeds:
                    sendMessage = await ctx.send(embed=embed)
                    await sendMessage.add_reaction("❌")


# Bot本体側からコグを読み込む際に呼び出される関数。
def setup(bot):
    bot.add_cog(Weapon(bot))  # TestCogにBotを渡してインスタンス化し、Botにコグとして登録する。
