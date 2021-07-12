import discord
import requests as rq
from discord.ext import commands


class Weapon(commands.Cog):

    # TestCogクラスのコンストラクタ。Botを受取り、インスタンス変数として保持。
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="弾薬性能表示")
    async def ammo(self, ctx):
        async with ctx.typing():
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
            if len(arg) == 1:
                if type(arg[0]) == str:
                    argText = arg[0].upper()
                else:
                    argText = " ".join(arg[0].upper())
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
                        elif colName == "リコイル":
                            infoStr += f"\n**{colName.capitalize()}**:"
                            for key, value in weaponData[colName].items():
                                infoStr += f"\n・**{key}**: __{value}__"
                        else:
                            infoStr += f"\n**{colName.capitalize()}**: __{weaponData[colName]}__"
                    embed = discord.Embed(
                        title=weaponData["名前"],
                        url=f"{self.bot.enWikiUrl}{weaponData['weaponUrl']}",
                        description=infoStr,
                        timestamp=self.bot.updateTimestamp,
                    )
                    embed.set_footer(
                        text=f"Source: The Official Escape from Tarkov Wiki 最終更新"
                    )
                    embed.set_image(url=weaponData["imageUrl"])
                    sendMessage = await ctx.send(embed=embed)
                    await sendMessage.add_reaction("❌")
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
