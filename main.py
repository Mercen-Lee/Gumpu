import config, discord, data, time, random

intents = discord.Intents.all()
client = discord.Client(intents=intents)
token = config.token

@client.event
async def on_ready():
    print(client.user.name + ", Starting Now...")
    await client.change_presence(activity = discord.Game("공놀이"))
    global math, timeleft
    math, timeleft = {}, {}

@client.event
async def on_message(message):

    global math, timeleft

    # Functions
    async def send(title, description=None, color=0xFFD200):
        embed = discord.Embed(title=title, description=description, color=color)
        await message.reply(embed=embed)

    async def warning():
        await send(":warning: 잔액이 부족하다멍!", color=0xFF0000)

    async def helper(msg: str):
        await send(f":warning: {msg}", "이렇게 해달라멍!", color=0xFF0000)

    def fmt(num): return format(int(num), ",")

    async def betting(money):
        data = data.DB(author)
        current = data.fetch("Coins")

        if current <= 0 or current < money:
            await warning()
            return
        elif random.choice([True, False]):
            data.update("Coins", current + money)
            title = ":slight_smile: 성공했다멍!"
            description = f"`+{fmt(money)} 코인`"
        else:
            data.update("Coins", current - money)
            title = ":cry: 실패했다멍!"
            description = f"`-{fmt(money)} 코인`"

        await send(title, description)

    # Message Actions
    if message.author.bot: return
    author = message.author.id

    try:
        if math[author] == int(message.content):
            money = random.randint(1000, 2000)

            del math[author]
            timeleft[author] = round(time.time())

            data = data.DB(author)
            data.update("Coins", data.fetch("Coins") + money)

            await send(":thumbsup: 정답이다멍!", description=f"`+{fmt(money)} 코인`")
            return
    except: pass

    msg = message.content.split(" ")
    if msg[0] not in config.command: return

    data = data.DB(author)

    # Admin Commands
    if msg[1] in ["돈내놔", "ㄷㄴㄴ"]:
        if message.author.id == config.admin:
            try:
                data.update("Coins", data.fetch("Coins") + int(msg[2]))
                await send(":cry: 내놨다멍!", description=f"`+{fmt(int(msg[2]))} 코인`")
            except:
                await helper("검푸야 돈내놔 [금액]")
        else:
            await send(":warning: 너는 내 주인이 아니다멍!", color=0xFF0000)

    # Normal Commands
    if msg[1] in ["버전", "ㅂㅈ"]:
        title = ":bone: 2023.1.26 Poodle v0.2"
        description = "Gumpu Developed by Mercen Lee"
        await send(title, description)

    if msg[1] in ["돈", "ㄷ"]:
        title = f":coin: {fmt(data.fetch('Coins'))} 코인"
        description = []
        for t in ["BTC", "ETH"]:
            fetched = data.fetch(t)
            if fetched: description.append(f"` {fmt(data.fetch(t))} {t}`")
        await send(title, ", ".join(description))

    if msg[1] in ["돈받기", "ㄷㅂㄱ"]:
        if author in list(timeleft.keys()):
            left = round(time.time()) - timeleft[author]
            if left < 60:
                await send(f":warning: {60 - left}초 남았다멍!", color=0xFF0000)
                return

        num = []
        for x in range(0, 2): num.append(random.randint(1, 10))

        temp = {"+": num[0] + num[1], "-": num[0] - num[1], "×": num[0] * num[1]}
        chosen = random.choice(list(temp.keys()))

        math[author] = temp[chosen]
        
        await send(f":regional_indicator_q: {num[0]} {chosen} {num[1]}", color=0x5287BE)

    if msg[1] in ["올인", "ㅇㅇ"]: await betting(data.fetch("Coins"))

    if msg[1] in ["하프", "ㅎㅍ"]: await betting(data.fetch("Coins") // 2)

    if msg[1] in ["도박", "ㄷㅂ"]:
        try: await betting(int(msg[2]))
        except: await helper("검푸야 도박 [금액]")

client.run(token)