from urllib import request
import discord

from discord.ext import commands
from discord.ext.commands.core import after_invoke, command

from youtube_dl import YoutubeDL

from django.core.validators import URLValidator


class music_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.is_playing = False

        self.music_queue = []
        self.YDL_OPTIONS = {"format": "bestaudio", "noplaylist": "True"}
        self.FFMPEG_OPTIONS = {
            "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
            "options": "-vn",
        }

        self.vc = ""

    def search_yt(self, item):
        validate = URLValidator()
        try:
            validate(item)
            is_url = True
        except Exception as exception:
            is_url = False

        if is_url is True:
            with YoutubeDL(self.YDL_OPTIONS) as ydl:
                try:
                    info = ydl.extract_info(item, download=False)
                except Exception:
                    return False
        else:

            with YoutubeDL(self.YDL_OPTIONS) as ydl:
                try:
                    info = ydl.extract_info("ytsearch:%s" % item, download=False)[
                        "entries"
                    ][0]
                except Exception:
                    return False
        return {"source": info["formats"][0]["url"], "title": info["title"]}

    def play_next(self):
        if len(self.music_queue) > 0:
            self.is_playing = True

            m_url = self.music_queue[0][0]["source"]

            self.music_queue.pop(0)

            self.vc.play(
                discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS),
                after=lambda e: self.play_next(),
            )

        else:
            self.is_playing = False
            """self.bot."""

    async def play_music(self):
        if len(self.music_queue) > 0:
            self.is_playing = True

            m_url = self.music_queue[0][0]["source"]

            if self.vc != "" and self.vc.is_connected():
                pass
            else:

                if self.vc == "" or not self.vc.is_connected() or self.vc == None:
                    self.vc = await self.music_queue[0][1].connect()
                else:
                    self.vc = await self.bot.move_to(self.music_queue[0][1])

            self.music_queue.pop(0)

            self.vc.play(
                discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS),
                after=lambda e: self.play_next(),
            )

        else:
            self.is_playing = False

    @commands.command()
    async def p(self, ctx, *args):
        query = " ".join(args)
        print(query)

        voice_channel = ctx.author.voice

        if voice_channel is None:

            await ctx.send("Intra pe un canal mai intai!")
        else:
            voice_channel = voice_channel.channel
            song = self.search_yt(query)
            if type(song) == type(True):
                await ctx.send("Nu am putut descarca melodia!")

            else:
                await ctx.send("Am adaugat melodia!")
                self.music_queue.append([song, voice_channel])

                if self.is_playing == False:
                    await self.play_music()

    @commands.command()
    async def q(self, ctx):
        retval = ""
        for i in range(0, len(self.music_queue)):
            retval += self.music_queue[i][0]["title"] + "\n"

        if retval != "":
            await ctx.send(retval)
        else:
            await ctx.send("Nu ai muzica in coada")

    @commands.command()
    async def skip(self, ctx):
        if self.vc != "":
            self.vc.stop()

            await self.play_music()
