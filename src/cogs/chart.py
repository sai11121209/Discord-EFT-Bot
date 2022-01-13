import config
import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext


class Chart(commands.Cog):
    guild_ids = [config.guild_ids]
    # TestCogクラスのコンストラクタ。Botを受取り、インスタンス変数として保持。
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_subcommand(
        base="chart",
        name="recovery",
        description="回復早見表",
        guild_ids=guild_ids,
    )
    async def chart_recovery(self, ctx: SlashContext):
        recoveryImages = [
            "abnormal_state.jpg",
            "recovery.jpg",
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
        ]
        for n, (url, author) in enumerate(zip(recoveryImages, authorList)):
            file = discord.File(f"../imgs/chart/health/{url}")
            embed = discord.Embed(
                title=f"({n+1}/{len(recoveryImages)})回復早見表",
                color=0x808080,
                url=author["link"],
            )
            embed.set_image(url=f"attachment://{url}")
            embed.set_author(
                name=author["author"]["name"],
                url=author["author"]["url"],
            )
            embed.set_footer(text=f"提供元: {author['link']}")
            sendMessage = await ctx.send(embed=embed, file=file)
            await sendMessage.add_reaction("❌")

    @cog_ext.cog_subcommand(
        base="chart",
        name="itemvalue",
        description="アイテム価格早見表",
        guild_ids=guild_ids,
    )
    async def chart_itemvalue(self, ctx: SlashContext):
        itemValueImages = [
            "pyramid.jpg",
            "chart.jpg",
        ]
        authorList = [
            {
                "author": {
                    "name": "Reddit: CALLSIGN-ASTRO",
                    "url": "https://www.reddit.com/user/CALLSIGN-ASTRO/",
                },
                "link": "https://www.reddit.com/r/EscapefromTarkov/comments/eu0pmi/i_tried_to_make_quick_barter_items_price_list_but/?utm_source=share&utm_medium=web2x",
            },
            {
                "author": {
                    "name": "Tarkov Tools",
                    "url": "https://tarkov-tools.com/",
                },
                "link": "https://tarkov-tools.com/loot-tier/",
            },
        ]
        for n, (url, author) in enumerate(zip(itemValueImages, authorList)):
            file = discord.File(f"../imgs/chart/item/{url}")
            embed = discord.Embed(
                title=f"({n+1}/{len(itemValueImages)})アイテム価格早見表",
                color=0x808080,
                url=author["link"],
            )
            embed.set_image(url=f"attachment://{url}")
            embed.set_author(
                name=author["author"]["name"],
                url=author["author"]["url"],
            )
            embed.set_footer(text=f"提供元: {author['link']}")
            sendMessage = await ctx.send(embed=embed, file=file)
            await sendMessage.add_reaction("❌")

    @cog_ext.cog_subcommand(
        base="chart",
        name="taskitem",
        description="タスク使用アイテム早見表",
        guild_ids=guild_ids,
    )
    async def chart_taskitem(self, ctx: SlashContext):
        taskItemImages = [
            "https://static.wikia.nocookie.net/escapefromtarkov_gamepedia/images/1/19/QuestItemRequirements.png/revision/latest?cb=20210212192637&format=original",
            "https://static.wikia.nocookie.net/escapefromtarkov_gamepedia/images/f/f8/QuestItemsInRaid.png/revision/latest?cb=20210212192627&format=original",
        ]
        authorList = [
            {
                "author": {
                    "name": "Official Escape from Tarkov Wiki",
                    "url": "https://escapefromtarkov.fandom.com/wiki/Quests",
                },
                "link": "https://escapefromtarkov.fandom.com/wiki/Quests",
            },
            {
                "author": {
                    "name": "Official Escape from Tarkov Wiki",
                    "url": "https://escapefromtarkov.fandom.com/wiki/Quests",
                },
                "link": "https://escapefromtarkov.fandom.com/wiki/Quests",
            },
        ]
        for n, (url, author) in enumerate(zip(taskItemImages, authorList)):
            embed = discord.Embed(
                title=f"({n+1}/{len(taskItemImages)})タスク使用アイテム早見表",
                color=0x808080,
                url=author["link"],
            )
            embed.set_image(url=url)
            embed.set_author(
                name=author["author"]["name"],
                url=author["author"]["url"],
            )
            embed.set_footer(text=f"提供元: {author['link']}")
            sendMessage = await ctx.send(embed=embed)
            await sendMessage.add_reaction("❌")

    @cog_ext.cog_subcommand(
        base="chart",
        name="tasktree",
        description="タスクツリー早見表",
        guild_ids=guild_ids,
    )
    async def chart_tasktree(self, ctx: SlashContext):
        taskItemImages = [
            "tree.jpg",
        ]
        authorList = [
            {
                "author": {
                    "name": "Twitter: @morimoukorigori",
                    "url": "https://twitter.com/morimoukorigori",
                },
                "link": "https://twitter.com/morimoukorigori/status/1357008341940064256",
            },
        ]
        for n, (url, author) in enumerate(zip(taskItemImages, authorList)):
            file = discord.File(f"../imgs/chart/task/{url}")
            embed = discord.Embed(
                title=f"({n+1}/{len(taskItemImages)})タスクツリー早見表",
                color=0x808080,
                url=author["link"],
            )
            embed.set_image(url=f"attachment://{url}")
            embed.set_author(
                name=author["author"]["name"],
                url=author["author"]["url"],
            )
            embed.set_footer(text=f"提供元: {author['link']}")
            sendMessage = await ctx.send(embed=embed, file=file)
            await sendMessage.add_reaction("❌")

    @cog_ext.cog_subcommand(
        base="chart",
        name="armor",
        description="アーマー早見表",
        guild_ids=guild_ids,
    )
    async def chart_armor(self, ctx: SlashContext):
        armorImages = [
            "class4.jpg",
            "class5.jpg",
            "class6.jpg",
            "graph.jpg",
        ]
        for n, url in enumerate(armorImages):
            file = discord.File(f"../imgs/chart/armor/{url}")
            embed = discord.Embed(
                title=f"({n+1}/{len(armorImages)})アーマー早見表",
                color=0x808080,
                url=f"{self.bot.enWikiUrl}Armor_vests",
            )
            embed.set_image(url=f"attachment://{url}")
            embed.set_author(
                name="Twitter: @N7th_WF",
                url="https://twitter.com/N7th_WF",
            )
            embed.set_footer(
                text="提供元: https://twitter.com/N7th_WF/status/1376825476598013957?s=20"
            )
            sendMessage = await ctx.send(embed=embed, file=file)
            await sendMessage.add_reaction("❌")

    @cog_ext.cog_subcommand(
        base="chart",
        name="headset",
        description="ヘッドセット早見表",
        guild_ids=guild_ids,
    )
    async def chart_headset(self, ctx: SlashContext):
        headsetImages = [
            "chart.PNG",
            "gssh_comtac2.PNG",
            "sordin_tactical.PNG",
            "razor_xcel.PNG",
            "m32_rac.PNG",
        ]
        for n, url in enumerate(headsetImages):
            file = discord.File(f"../imgs/chart/headset/{url}")
            embed = discord.Embed(
                title=f"({n+1}/{len(headsetImages)})ヘッドセット早見表",
                color=0x808080,
                url=f"{self.bot.enWikiUrl}Headsets",
            )
            embed.set_image(url=f"attachment://{url}")
            embed.set_author(
                name="セヴンスGaming",
                url="https://www.youtube.com/channel/UCZpSzN3ozBUnJrXLmx50qVA",
            )
            embed.set_footer(
                text="提供元: [ EFT 解説 ] ヘッドセットの選び方ガイド②考察編【タルコフ】 https://www.youtube.com/watch?v=LyVGpyBZ0EU"
            )
            sendMessage = await ctx.send(embed=embed, file=file)
            await sendMessage.add_reaction("❌")

    @cog_ext.cog_subcommand(
        base="chart",
        name="lighthousetask",
        description="Lighthouseタスク早見表",
        guild_ids=guild_ids,
    )
    async def chart_lighthousetask(self, ctx: SlashContext):
        lighthousetaskImages = [
            "lighthouse_1.jpg",
            "lighthouse_2.jpg",
            "lighthouse_3.jpg",
            "lighthouse_4.jpg",
        ]
        for n, url in enumerate(lighthousetaskImages):
            file = discord.File(f"../imgs/chart/task/{url}")
            embed = discord.Embed(
                title=f"({n+1}/{len(lighthousetaskImages)})ヘッドセット早見表",
                color=0x808080,
            )
            embed.set_image(url=f"attachment://{url}")
            sendMessage = await ctx.send(embed=embed, file=file)
            await sendMessage.add_reaction("❌")


# Bot本体側からコグを読み込む際に呼び出される関数。
def setup(bot):
    bot.add_cog(Chart(bot))  # TestCogにBotを渡してインスタンス化し、Botにコグとして登録する。
