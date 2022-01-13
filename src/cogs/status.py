import json
import time
import pytz
import config
import discord
import datetime
import requests as rq
from pytz import timezone
from discord.ext import commands
from datetime import datetime as dt
from discord_slash import cog_ext, SlashContext


class Status(commands.Cog):
    guild_ids = [config.guild_ids]
    # TestCogクラスのコンストラクタ。Botを受取り、インスタンス変数として保持。
    def __init__(self, bot):
        self.bot = bot
        self.status_name = [
            "Success",
            "Update",
            "Warning",
            "Error",
        ]
        self.status_color = [
            0x70B035,
            0x90C1EB,
            0xCA8A00,
            0xD42929,
        ]
        self.status_urls = {
            "status": "https://status.escapefromtarkov.com/api/global/status",
            "service": "https://status.escapefromtarkov.com/api/services",
            "datacenter": "https://status.escapefromtarkov.com/api/datacenter/list",
            "information": "https://status.escapefromtarkov.com/api/message/list",
        }
        self.status_data = {
            "status": None,
            "service": None,
            "datacenter": None,
            "information": None,
        }

    @cog_ext.cog_slash(
        name="status",
        description="EscapeTarkovサーバのステータスを表示",
        guild_ids=guild_ids,
    )
    async def status(self, ctx: SlashContext):
        for key, value in self.status_urls.items():
            res = rq.get(value)
            self.status_data[key] = json.loads(res.text)
        embed = discord.Embed(
            title=f"EscapeTarkovServerStatus",
            color=self.status_color[self.status_data["status"]["status"]],
            url="https://status.escapefromtarkov.com/",
            timestamp=datetime.datetime.utcfromtimestamp(
                dt.now(pytz.timezone("Asia/Tokyo")).timestamp()
            ),
        )
        for key, values in self.status_data.items():
            if key == "status":
                embed.add_field(
                    name=f"ステータス: {self.status_name[values['status']]}",
                    value=f"> {values['message']}",
                    inline=False,
                )
            if key == "service":
                text = ""
                for value in values:
                    text += (
                        f"> **{value['name']}** : {self.status_name[value['status']]}\n"
                    )
                embed.add_field(
                    name="各種サービスステータス",
                    value=text,
                    inline=False,
                )
            if key == "information":
                infoStr = ""
                text = values[0]["content"]
                # 翻訳前言語
                source = "en"
                # 翻訳後言語
                Target = "ja"
                gasUrl = f"https://script.google.com/macros/s/AKfycbxvCS-29LVgrm9-cSynGl19QUIB7jTpzuvFqflus_P0BJtXX80ahLazltfm2rbMGVVs/exec?text={text}&source={source}&target={Target}"
                res = rq.get(gasUrl).json()
                if res["code"] == 200:
                    text = res["text"]
                infoStr += f"\n> {values[0]['content']}\n"
                infoStr += f"\n> {text}"
                infoStr += "\n> Google翻訳"
                embed.add_field(
                    name=f"アナウンス最終更新 {dt.fromisoformat(values[0]['time']).astimezone(timezone('Asia/Tokyo')).strftime('%Y-%m-%d %H:%M:%S')}",
                    value=f"{infoStr} ",
                    inline=False,
                )
        embed.set_thumbnail(url="https://status.escapefromtarkov.com/favicon.ico")
        embed.set_footer(text=f"Source: Escape from Tarkov Status 最終更新")
        embed.set_author(
            name="EFT(Escape from Tarkov) Wiki Bot",
            url="https://github.com/sai11121209",
        )
        sendMessage = await ctx.send(embed=embed)
        await sendMessage.add_reaction("❌")


# Bot本体側からコグを読み込む際に呼び出される関数。
def setup(bot):
    bot.add_cog(Status(bot))  # TestCogにBotを渡してインスタンス化し、Botにコグとして登録する。
