import asyncio
import discord
import praw
import random
from discord.ext import commands
from discord.utils import get
from itertools import cycle

TOKEN = ""

bot = commands.Bot(command_prefix="!")
bot.remove_command("help")
status = ["alone", "Mobile Legends", "herself", "PUBG", "Fortnite"]
players = {}
reddit = praw.Reddit(client_id='SGXSym_4G8Y2DQ',
                     client_secret='j4NPUfG0TmHJM-9YDPL5IHXuzXM',
                     user_agent='nabbot')


async def change_status():
    await bot.wait_until_ready()
    messages = cycle(status)

    while not bot.is_closed:
        current_status = next(messages)
        await bot.change_presence(game=discord.Game(name=current_status))
        await asyncio.sleep(10)


@bot.event
async def on_ready():
    print("Let's go!")


@bot.event
async def on_message(message):
    word_filter = ['FUCK', 'BITCH']
    member = discord.Member
    contents = message.content.split(" ")
    for words in contents:
        if words.upper() in word_filter:
            await bot.send_message(message.channel, "That's **ILLEGAL**!")
            await bot.delete_message(message)
    await bot.process_commands(message)

@bot.event
async def on_member_join(member):
    server = member.server
    await bot.send_message(server, f"{member}, Welcome to {server}!")

@bot.command()
async def pewd():
    memes_submission = reddit.subreddit('PewdiepieSubmissions').hot()
    post_to_pick = random.randint(1, 100)
    for i in range(0, post_to_pick):
        submission = next(x for x in memes_submission if not x.stickied)

    await bot.say(submission.url)

@bot.command()
async def sub(name = ""):
    if name:
        pics = reddit.subreddit(str(name)).hot()
        post_to_pick = random.randint(1, 100)
        for i in range(0, post_to_pick):
            submission = next(x for x in pics if not x.stickied)

        await bot.say(submission.url)

    else:
        pics = reddit.subreddit('anime').hot()
        post_to_pick = random.randint(1, 100)
        for i in range(0, post_to_pick):
            submission = next(x for x in pics if not x.stickied)

        await bot.say(submission.url)

@bot.command()
async def motivate():
    motivations = reddit.subreddit('GetMotivated').top()
    post_to_pick = random.randint(1, 100)
    for i in range(0, post_to_pick):
        submission = next(x for x in motivations if not x.stickied)

    await bot.say(submission.url)

@bot.command()
async def meme():
    memes = reddit.subreddit('memes').hot() or reddit.subreddit('dankmemes').hot()
    post_to_pick = random.randint(1, 100)
    for i in range(0, post_to_pick):
        submission = next(x for x in memes if not x. stickied)

    await bot.say(submission.url)

@bot.command(pass_context=True)
async def join(ctx):
    channel = ctx.message.author.voice.voice_channel
    await bot.join_voice_channel(channel)

@bot.command(pass_context=True)
async def leave(ctx):
    server = ctx.message.server
    voice_client = bot.voice_client_in(server)
    await voice_client.disconnect()

@bot.command(pass_context=True)
async def play(ctx, url):
    channel = ctx.message.author.voice.voice_channel
    if channel:
        await bot.join_voice_channel(channel)
        server = ctx.message.server
        await bot.say("Music now playing...")
        voice_client = bot.voice_client_in(server)
        player = await voice_client.create_ytdl_player(url, ytdl_options={'default_search': 'auto'}, after = lambda: check_queue(server.id))
        players[server.id] = player
        player.start()
    else:
        await bot.say("Please join a voice channel.")
        if channel:
            await bot.say("Music now playing...")
            voice_client = bot.voice_client_in(server)
            player = await voice_client.create_ytdl_player(url, ytdl_options={'default_search': 'auto'},
                                                           after=lambda: check_queue(server.id))
            players[server.id] = player
            player.start()

@bot.command(pass_context=True)
async def pause(ctx):
    id = ctx.message.server.id
    players[id].pause()
    await bot.say("Music is paused!")

@bot.command(pass_context=True)
async def resume(ctx):
    id = ctx.message.server.id
    players[id].resume()
    await bot.say("Music is resumed!")

@bot.command(pass_context=True)
async def stop(ctx):
    id = ctx.message.server.id
    players[id].stop()
    await bot.say("Music is stopped!")

@bot.command(pass_context=True)
async def help(ctx):
    author = ctx.message.author

    embed = discord.Embed(
        description = "Help is here!",
        colour = 11393254
    )

    embed.set_author(name="Your friendly ThotBot to the rescue!")
    embed.add_field(name="!nani", value="Returns everybody's favourite line.", inline= False)
    embed.add_field(name="!echo", value="Repeats what is typed after the command.", inline=False)
    embed.add_field(name="!info", value="General info about ThotBot.", inline=False)
    embed.add_field(name="!clear", inline=False
                    , value="Clear the chat box, specify a number to clear the exact number of chats.")
    embed.add_field(name="!role", value="Type in the username and role after the command to assign that person the "
                                        "role.", inline=False)
    embed.add_field(name="!thot", value="Just a very cool thing.", inline=False)
    embed.add_field(name="!pewd", value="Just LWIAY stuff.", inline=False)
    embed.add_field(name="!meme", value="Only dank memes", inline=False)
    embed.add_field(name="!motivation", value="Daily dose of motivation.", inline=False)
    embed.add_field(name="!sub", value="Type in a subreddit name after the command to get content from that "
                                       "subreddit, it links to the anime subreddit if nothing is being entered at the"
                                       " back.", inline=False)
    embed.add_field(name="!join", value="Invite ThotBot to join your voice channel.", inline=False)
    embed.add_field(name="!leave", value="ThotBot will say goodbye from your voice channel", inline=False)
    embed.add_field(name="!play", value="Music?", inline=False)
    embed.add_field(name="!pause", value="Pause the music.", inline=False)
    embed.add_field(name="!resume", value="Resume the music", inline=False)
    embed.add_field(name="!stop", value="Stop the music.", inline=False)

    await bot.send_message(author, embed=embed)

@bot.command(pass_context=True)
async def info():
    info = discord.Embed(
        title="Created by LKS",
        description="Just for fun bot.",
        colour= 16758465
    )

    info.set_footer(text="Just a cute picture Mai Sakurajima.")
    info.set_image(url="https://images7.alphacoders.com/959/thumb-1920-959381.jpg")
    info.set_thumbnail(url='https://www.samehadaku.tv/wp-content/uploads/2018/11/Opening-Ending-Seishun-Buta-Yarou-wa'
                           '-Bunny-Girl-Senpai-no-Yume-wo-Minai.jpg')
    info.set_author(name="ThotBot",
                    icon_url="https://pre00.deviantart.net/efdc/th/pre/f/2018/286/7/a"
                             "/_render076__mai_sakurajima_by_edgina36-dcpc7ju.png")

    info.add_field(name='Version', value="1.0", inline=False)

    await bot.say(embed=info)


@bot.command(pass_context=True)
async def role(ctx, member: discord.Member, role: discord.Role):
    await bot.replace_roles(member, role)
    await bot.say(f"{member} is now {role}")


@bot.command()
async def nani():
    await bot.say("Omae wa mou shindeiru!")


@bot.command()
async def echo(*arg):
    output = ""
    for words in arg:
        output += words
        output += " "
    await bot.say(output)


@bot.command(pass_context=True)
async def thot(ctx):
    author = str(ctx.message.author).split("#")
    del author[-1]
    name = ""
    x = len(author) - 1  # purely just a number to help in adding spaces between names
    for words in author:
        if len(author) > 1:
            name += words
            if x >= 1:
                name += " "
        else:
            name += words
    await bot.say(f"Thank you {name}, very cool.")


@bot.command(pass_context=True)
async def clear(ctx, amount=99):
    channel = ctx.message.channel
    messages = []
    if amount:
        if amount <= 1 or amount >= 100:
            await bot.say("Please enter a number between 2 and 99!")
        else:
            async for message in bot.logs_from(channel, limit=int(amount) + 1):
                messages.append(message)
            await bot.delete_messages(messages)
            await bot.say("Message cleared!")


bot.loop.create_task(change_status())
bot.run(TOKEN)
