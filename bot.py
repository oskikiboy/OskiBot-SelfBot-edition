import logging
import urllib
import os
import sys
import datetime
import pip
import subprocess
import re
import io
from contextlib import redirect_stdout
from urllib.request import urlretrieve

def install(package):
    pip.main(['install', package])
# Try importing libs if already installed
try:
    import strawpoll
except:
    install('strawpoll.py')
    import strawpoll
try:
    import discord
except:
    install('discord.py')
    import discord
try:
    import speedtest
except:
    install('speedtest-cli')

print("-------------------")
print("Discord.py version: {}".format(discord.version_info))
print("-------------------")

prefix = 'o!'
# Zero width space for client.edit_message(message, zero_space, embed=Embed)
zero_space = '\u200b'
logging.basicConfig(level=logging.INFO)
IsAFK = False
RhythmbotInfo = "Rhythmbot Selfbot Edition. Made by Jake Gealer (Jake in SSL. Modified by oskikiboy, aiming to make selfbots an enjoyable experience."
client = discord.Client()

# Thanks to Kelwing for the embed code, it was a bit of a code stealing cycle with Noodles and Arturo Dixionary :P

def make_embed(field_list="", title="", desc="", title_url="", author_url="", inline=True, footer=False, thumb=None, footer_url=None, color=0x00FF00, icon_url=None, set_image=None):
    embed = discord.Embed(title=title, url=title_url, description=desc, colour=color)
    if set_image:
        embed.set_image(url=set_image)
    if not icon_url:
        embed.set_author(name=client.user.name, url=author_url, icon_url=client.user.avatar_url)
    else:
        embed.set_author(name=client.user.name, url=author_url, icon_url=icon_url)
    if not footer:
        footer = footer = ""
    if not field_list == "":
        for field in field_list:
            embed.add_field(name=field[0],value=field[1], inline=inline)
    if thumb:
        embed.set_thumbnail(url=thumb)
    if footer:
        if footer_url:
            embed.set_footer(text=footer, icon_url=footer_url)
        else:
            embed.set_footer(text=footer)
    return embed

@client.event
async def on_message(message):
    global IsAFK
    global RhythmbotInfo
    global zero_space
    if not message.author.bot and message.author == client.user:
        recmp = re.compile("^{}[A-Za-z]+.*".format(prefix))
        if recmp.match(message.content):
            splitmsg = message.content.split(' ')
            cmd = splitmsg[0].lstrip(prefix)

            if cmd == 'lmgtfy':
                DiscordLMGTFY = ' '.join(splitmsg[1:])
                DiscordLMGTFY = urllib.parse.quote(DiscordLMGTFY)
                await client.edit_message(message, 'http://lmgtfy.com/?iie=1&q={}'.format(DiscordLMGTFY))

            elif cmd == 'afk':
                if not IsAFK:
                    GoneAFK = make_embed(title="AFK", desc="I am now AFK and cannot reply to messages until I get back.", color=0x33CCFF)
                    await client.edit_message(message, zero_space, embed=GoneAFK)
                    print("Set AFK enabled")
                    IsAFK = True
                else:
                    NotAFK = make_embed(title="AFK", desc="I am no longer AFK.", color=0x33CCFF)
                    await client.edit_message(message, zero_space, embed=NotAFK)
                    print("Set AFK disabled")
                    IsAFK = False

            elif cmd == 'embed':
                ToEmbed = ' '.join(splitmsg[1:])
                EmbeddedMsg = make_embed(desc=ToEmbed)
                await client.edit_message(message, zero_space, embed=EmbeddedMsg)

            elif cmd == 'smallembed':
                ToEmbedSmall = ' '.join(splitmsg[1:])
                EmbeddedMsgSmall = discord.Embed(description=ToEmbedSmall, colour=0x33CCFF)
                await client.edit_message(message, zero_space, embed=EmbeddedMsgSmall)

            elif cmd == 'support':
                await client.edit_message(message, 'https://www.youtube.com/watch?v=PtXtIivRRKQ')

            elif cmd == 'mssupport':
                await client.edit_message(message, 'https://support.microsoft.com/en-gb')

            elif cmd == 'scriptkiddie':
                await client.edit_message(message, 'https://www.youtube.com/watch?v=fSdXuQGjnKo')

            elif cmd == 'hammer':
                HammerEmbed = make_embed(set_image='http://i.imgur.com/O3DHIA5.gif')
                await client.edit_message(message, zero_space, embed=HammerEmbed)

            elif cmd == 'nobodycares':
                NobodyCares = make_embed(set_image='http://i2.kym-cdn.com/photos/images/newsfeed/000/325/428/264.jpg')
                await client.edit_message(message, zero_space, embed=NobodyCares)

            elif cmd == 'game':
                GameToSet = ' '.join(splitmsg[1:])
                await client.change_presence(game=discord.Game(name=GameToSet))
                GameMsg = make_embed(title="Custom Game", desc='Your "Playing" tag was successfully changed to {}'.format(GameToSet))
                await client.edit_message(message, zero_space, embed=GameMsg)

            elif cmd == 'poll':
                pollname = ' '.join(splitmsg[1:])
                api = strawpoll.API()
                poll = strawpoll.Poll(pollname, ['Yes', 'No'])
                poll = await api.submit_poll(poll)
                PollMsg = make_embed(title="New Poll - " + pollname, desc=str(poll.url))
                await client.edit_message(message, zero_space, embed=PollMsg)

            elif cmd == 'update':
                print("Updating!")
                try:
                    os.remove("RhythmbotSelf.py")
                except:
                    pass
                url = "http://rhythmbot.ga/Rhythmbot-Selfbot-Edition/RhythmbotSelf.py"
                urlretrieve(url, "RhythmbotSelf.py")
                UpdateRestartMsg = make_embed(title="Update", desc='Rhythmbot has updated and changes will be active after the selfbot is restarted.', color=0x00ff00)
                await client.edit_message(message, zero_space, embed=UpdateRestartMsg)

            elif cmd == 'good':
                ToAddGood = ' '.join(splitmsg[1:])
                with open("goodlist.txt", "a+") as f:
                    f.write(ToAddGood)
                GoodMsg = make_embed(title='Good List', desc='User was successfully added to your good list!', color=0x00ff00)
                await client.edit_message(message, zero_space, embed=GoodMsg)

            elif cmd == 'bad':
                ToAddBad = ' '.join(splitmsg[1:])
                with open("badlist.txt", "a+") as f:
                    f.write(ToAddBad)
                BadMsg = make_embed(title='Bad List', desc='User was successfully added to your bad list!', color=0xff0000)
                await client.edit_message(message, zero_space, embed=BadMsg)

            elif cmd == 'time':
                now = datetime.datetime.now()
                TimeMsg = make_embed(title="Time", desc='The local time for me according to my computer clock is {:02}:{:02}'.format(now.hour, now.minute))
                await client.edit_message(message, zero_space, embed=TimeMsg)

            elif cmd == 'pythoneval':
                codetoeval = ' '.join(splitmsg[1:])
                CodeOutput = io.StringIO()
                with redirect_stdout(CodeOutput):
                    try:
                        exec(codetoeval)
                    except:
                        print("ERROR: Code failed to execute!")
                CodeOutputString = "```" + str(CodeOutput.getvalue()) + "```"
                CodeOutputString = CodeOutputString.replace(token, "[token removed]")
                if CodeOutputString == "``````":
                    CodeOutputString = "```This code generated no output.```"
                await client.edit_message(message, CodeOutputString)

            elif cmd == 'calc':
                Calculation = ' '.join(splitmsg[1:])
                if Calculation == "token":
                    Calculation = '''"ERROR: This bot cannot just print the token for security reasons."'''
                CalcOutput = io.StringIO()
                with redirect_stdout(CalcOutput):
                    try:
                        MathCmd = "print(" + Calculation + ")"
                        exec(MathCmd)
                    except:
                        print("ERROR: Calculation failed!")
                CalcOutputString = "```" + str(CalcOutput.getvalue()) + "```"
                CalcOutputString = CalcOutputString.replace(token, "[token removed]")
                await client.edit_message(message, CalcOutputString)

            elif cmd == 'about':
                await client.edit_message(message, "```" + RhythmbotInfo + "```")

            elif cmd == 'speedtest':
                DOWNLOAD_RE = re.compile(r"Download: ([\d.]+) .bit")
                UPLOAD_RE = re.compile(r"Upload: ([\d.]+) .bit")
                PING_RE = re.compile(r"([\d.]+) ms")
                await client.edit_message(message, ":stopwatch: **Running speedtest. This may take a while!** :stopwatch:")
                speedtest_result = str(subprocess.check_output(['speedtest-cli'], stderr=subprocess.STDOUT))
                download = DOWNLOAD_RE.search(speedtest_result).group(1)
                upload = UPLOAD_RE.search(speedtest_result).group(1)
                ping = PING_RE.search(speedtest_result).group(1)
                SpeedtestMsg = make_embed(title="Speedtest", desc="Download Speed: " + download + " mbps\n" + "Upload Speed: " + upload + " mbps\n" + "Ping: " + ping + " ms")
                await client.send_message(message.channel, embed=SpeedtestMsg)

@client.event
async def on_ready():
    print(' ')
    print('------------------')
    print('Logged in as {}'.format(client.user.name))
    print('ID: ' + client.user.id)
    print('------------------')
    print(' ')
with open("token.txt", "r") as f:
    token = f.readline().rstrip()
client.run(token, bot=False)
