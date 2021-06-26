import discord
from discord.ext import commands


class Chart(commands.Cog):

    # TestCogクラスのコンストラクタ。Botを受取り、インスタンス変数として保持。
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="recovery", description="回復早見表")
    async def recovery(self, ctx):
        async with ctx.typing():
            recoveryImages = [
                "https://cdn.discordapp.com/attachments/803425039864561675/804873530335690802/image0.jpg",
                "https://cdn.discordapp.com/attachments/803425039864561675/804873530637811772/image1.jpg",
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
                embed = discord.Embed(
                    title=f"({n+1}/{len(recoveryImages)})回復早見表",
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

    @commands.command(name="itemvalue", description="アイテム価格早見表")
    async def itemvalue(self, ctx):
        async with ctx.typing():
            itemValueImages = [
                "https://cdn.discordapp.com/attachments/616231205032951831/805997840140599366/image0.jpg",
                "https://media.discordapp.net/attachments/808820772536582154/814055787898077215/image1.webp",
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
                embed = discord.Embed(
                    title=f"({n+1}/{len(itemValueImages)})アイテム価格早見表",
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

    @commands.command(name="taskitem", description="タスク使用アイテム早見表")
    async def taskitem(self, ctx):
        async with ctx.typing():
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

    @commands.command(name="tasktree", description="タスクツリー早見表")
    async def taskitem(self, ctx):
        async with ctx.typing():
            taskItemImages = [
                "https://cdn.discordapp.com/attachments/806055934211653632/858391797121810442/image0.jpg",
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
                embed = discord.Embed(
                    title=f"({n+1}/{len(taskItemImages)})タスクツリー早見表",
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

    @commands.command(name="armor", description="アーマー早見表")
    async def armor(self, ctx):
        async with ctx.typing():
            armorImages = [
                "https://cdn.discordapp.com/attachments/806055934211653632/826790299619426354/image3.jpg",
                "https://cdn.discordapp.com/attachments/806055934211653632/826790298649624586/image0.jpg",
                "https://cdn.discordapp.com/attachments/806055934211653632/826790298918453268/image1.jpg",
                "https://cdn.discordapp.com/attachments/806055934211653632/826790299299872798/image2.jpg",
            ]
            for n, url in enumerate(armorImages):
                embed = discord.Embed(
                    title=f"({n+1}/{len(armorImages)})アーマー早見表",
                    color=0x808080,
                    url=f"{self.bot.enWikiUrl}Armor_vests",
                )
                embed.set_image(url=url)
                embed.set_author(
                    name="Twitter: @N7th_WF",
                    url="https://twitter.com/N7th_WF",
                )
                embed.set_footer(
                    text="提供元: https://twitter.com/N7th_WF/status/1376825476598013957?s=20"
                )
                sendMessage = await ctx.send(embed=embed)
                await sendMessage.add_reaction("❌")


# Bot本体側からコグを読み込む際に呼び出される関数。
def setup(bot):
    bot.add_cog(Chart(bot))  # TestCogにBotを渡してインスタンス化し、Botにコグとして登録する。