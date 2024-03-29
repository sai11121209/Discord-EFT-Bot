import discord
import itertools
from discord.ext import commands


class Task(commands.Cog):

    # TestCogクラスのコンストラクタ。Botを受取り、インスタンス変数として保持。
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="タスク一覧表示コマンド")
    async def task(self, ctx, *arg):
        async with ctx.typing():
            arg = list(itertools.chain.from_iterable(arg))
            if len(arg) != 0:
                if "".join(str(x) for x in arg).upper() in self.bot.taskName:
                    infoStr = ""
                    fixtext = "".join(str(x) for x in arg).upper().replace(" ", "")
                    taskData = [
                        value
                        for values in self.bot.taskData.values()
                        for value in values["tasks"]
                        if value["questName"].upper().replace(" ", "") == fixtext
                    ][0]
                    taskImageEmbeds = []
                    for colName, values in taskData.items():
                        if colName == "dealerName":
                            infoStr += f"**ディーラー**: __[{taskData[colName]}]({self.bot.enWikiUrl}{taskData['dealerUrl']})__"
                        elif colName == "type":
                            infoStr += f"\n**タイプ**: __{taskData[colName]}__"
                        elif colName == "objectives":
                            infoStr += f"\n**目的**:"
                            for objective in values:
                                hyperText = objective["text"]
                                for text, link in objective["linkText"].items():
                                    hyperText = hyperText.replace(
                                        f"{text}",
                                        f"[{text}]({self.bot.enWikiUrl}{link})",
                                    )
                                infoStr += f"\n・__{hyperText}__"
                        elif colName == "rewards":
                            infoStr += f"\n**報酬**:"
                            for reward in values:
                                hyperText = reward["text"]
                                for text, link in reward["linkText"].items():
                                    hyperText = hyperText.replace(
                                        f"{text}",
                                        f"[{text}]({self.bot.enWikiUrl}{link})",
                                    )
                                infoStr += f"\n・__{hyperText}__"
                        elif colName == "location":
                            infoStr += f"\n**場所**:"
                            if len(taskData[colName]) == 0:
                                infoStr += f" __-__"
                            elif len(taskData[colName]) == 1:
                                hyperText = taskData[colName][0]["text"]
                                hyperText = hyperText.replace(
                                    f"{taskData[colName][0]['text']}",
                                    f"[{taskData[colName][0]['text']}]({self.bot.enWikiUrl}{taskData[colName][0]['linkText']})",
                                )
                                infoStr += f" __{hyperText}__"
                            else:
                                for location in taskData[colName]:
                                    hyperText = location["text"]
                                    hyperText = hyperText.replace(
                                        f"{location['text']}",
                                        f"[{location['text']}]({self.bot.enWikiUrl}{location['linkText']})",
                                    )
                                    infoStr += f"\n・__{hyperText}__"
                        elif colName == "previousQuest":
                            infoStr += f"\n**事前タスク**:"
                            if len(taskData[colName]) == 0:
                                infoStr += f" __-__"
                            elif len(taskData[colName]) == 1:
                                hyperText = taskData[colName][0]["text"]
                                hyperText = hyperText.replace(
                                    f"{taskData[colName][0]['text']}",
                                    f"[{taskData[colName][0]['text']}]({self.bot.enWikiUrl}{taskData[colName][0]['linkText']})",
                                )
                                infoStr += f" __{hyperText}__"
                            else:
                                for previousQuest in taskData[colName]:
                                    hyperText = previousQuest["text"]
                                    hyperText = hyperText.replace(
                                        f"{previousQuest['text']}",
                                        f"[{previousQuest['text']}]({self.bot.enWikiUrl}{previousQuest['linkText']})",
                                    )
                                    infoStr += f"\n・__{hyperText}__"
                        elif colName == "nextQuest":
                            infoStr += f"\n**事後タスク**:"
                            if len(taskData[colName]) == 0:
                                infoStr += f" __-__"
                            elif len(taskData[colName]) == 1:
                                hyperText = taskData[colName][0]["text"]
                                hyperText = hyperText.replace(
                                    f"{taskData[colName][0]['text']}",
                                    f"[{taskData[colName][0]['text']}]({self.bot.enWikiUrl}{taskData[colName][0]['linkText']})",
                                )
                                infoStr += f" __{hyperText}__"
                            else:
                                for nextQuest in taskData[colName]:
                                    hyperText = nextQuest["text"]
                                    hyperText = hyperText.replace(
                                        f"{nextQuest['text']}",
                                        f"[{nextQuest['text']}]({self.bot.enWikiUrl}{nextQuest['linkText']})",
                                    )
                                    infoStr += f"\n・__{hyperText}__"
                        elif colName == "taskImage":
                            for n, (imageName, imageUrl) in enumerate(values.items()):
                                embed = discord.Embed(
                                    title=f"({n + 1}/{len(values)}){taskData['questName']}",
                                    url=f"{self.bot.enWikiUrl}{taskData['questUrl']}",
                                    description=f"{imageName}",
                                    timestamp=self.bot.updateTimestamp,
                                )
                                embed.set_footer(
                                    text=f"Source: The Official Escape from Tarkov Wiki 最終更新"
                                )
                                embed.set_thumbnail(url=taskData["taskThumbnail"])
                                embed.set_image(url=imageUrl)
                                taskImageEmbeds.append(embed)
                    embed = discord.Embed(
                        title=taskData["questName"],
                        url=f"{self.bot.enWikiUrl}{taskData['questUrl']}",
                        description=infoStr,
                        timestamp=self.bot.updateTimestamp,
                    )
                    embed.set_footer(
                        text=f"Source: The Official Escape from Tarkov Wiki 最終更新"
                    )
                    embed.set_thumbnail(url=taskData["dealerThumbnail"])
                    embed.set_image(url=taskData["taskThumbnail"])
                    sendMessage = await ctx.send(embed=embed)
                    await sendMessage.add_reaction("❌")
                    for embed in taskImageEmbeds:
                        sendMessage = await ctx.send(embed=embed)
                        await sendMessage.add_reaction("❌")
                else:
                    await self.bot.on_command_error(
                        ctx, commands.CommandNotFound("weapon")
                    )

            else:
                embeds = []
                for n, (index, values) in enumerate(self.bot.taskData.items()):
                    embed = discord.Embed(
                        title=f"タスク一覧({n+1}/{len(self.bot.taskData)})",
                        url=f"{self.bot.enWikiUrl}Quests",
                        timestamp=self.bot.updateTimestamp,
                    )
                    embed.add_field(
                        name=f"{index}",
                        value=f"[{index} 海外Wikiリンク]({self.bot.enWikiUrl}{values['dealerUrl']})",
                        inline=False,
                    )
                    for value in values["tasks"]:
                        embed.add_field(
                            name=value["questName"],
                            value=f"[{value['questName']} 海外Wikiリンク]({self.bot.enWikiUrl}{value['questUrl']})",
                            inline=False,
                        )
                    embed.set_thumbnail(url=value["dealerThumbnail"])
                    embed.set_footer(
                        text=f"Source: The Official Escape from Tarkov Wiki 最終更新"
                    )
                    embeds.append(embed)
                for embed in embeds:
                    sendMessage = await ctx.send(embed=embed)
                    await sendMessage.add_reaction("❌")


# Bot本体側からコグを読み込む際に呼び出される関数。
def setup(bot):
    bot.add_cog(Task(bot))  # TestCogにBotを渡してインスタンス化し、Botにコグとして登録する。
