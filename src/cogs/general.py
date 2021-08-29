# -*- coding: utf-8 -*-
import math
import os
import platform
import random
from datetime import datetime
from typing import NoReturn

import discord
import psutil
import wikipedia
from discord.ext import commands
from discord.ext.commands import Bot, Context

from cogs.utils import Commands, Config, Logger, Settings, Strings, Utils
from scripts import blacklist

CONFIG = Config()


class General(commands.Cog, name="General"):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.name = "General"
        self.process = psutil.Process(os.getpid())

    # @commands.command()
    # @commands.guild_only()
    # async def help(self, ctx: Context, command: str = None) -> NoReturn:
    # """Shows help for a specific command, or displays a complete list of commands.

    # Attributes:
    # -----------
    # - `command` - the command to display help for.
    # If `command` is empty, displays a complete list of commands.
    # If the command does not exist, writes that the command was not found.

    # """
    # s = await Settings(ctx.guild.id)
    # lang = await s.get_field('locale', CONFIG['default_locale'])
    # prefix = await s.get_field('prefix', CONFIG['default_prefix'])
    # STRINGS = Strings(lang)
    # COMMANDS = Commands(lang)

    # if command == None:
    # embed = discord.Embed(
    # itle=STRINGS['general']['commands_list'], description=STRINGS['general']['help_list_description'].format(prefix), color=0xef940b)
    # for i in COMMANDS:
    # title = COMMANDS[i]['title']

    # description = ', '.join(
    # [f'`{j}`' for j in COMMANDS[i]['commands']])

    # if self.bot.get_cog(i) != None:
    # embed.add_field(
    # name=title, value=description, inline=False)
    # embed.set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar_url)
    # await ctx.send(embed=embed)

    # elif command != '':
    # for i in COMMANDS:
    # for j in COMMANDS[i]['commands']:
    # if command == j:
    # embed = discord.Embed(
    # title=STRINGS['general']['helpsystemtitle'].format(f'`{prefix}{j}`'), color=0xef940b)

    # embed.add_field(
    # name=STRINGS['general']['description'], value=COMMANDS[i]['commands'][j]['description'], inline=False)

    # embed.add_field(
    # name=STRINGS['general']['usage'], value=COMMANDS[i]['commands'][j]['usage'].format(prefix), inline=False)

    # if len(COMMANDS[i]['commands'][j]['aliases']) > 0:
    # aliases = ', '.join(
    # [f'`{alias}`' for alias in COMMANDS[i]['commands'][j]['aliases']])
    # embed.add_field(
    # name=STRINGS['general']['aliases'], value=aliases, inline=False)

    # embed.set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar_url)

    # await ctx.send(embed=embed)
    # return
    # else:
    # await ctx.send(embed=Utils.error_embed(STRINGS['error']['command_not_found']))

    @commands.guild_only()
    @commands.command(description="Echo Commands")
    async def echo(self, ctx: Context, *, content):
        s = await Settings(ctx.guild.id)
        lang = await s.get_field("locale", CONFIG["default_locale"])
        prefix = await s.get_field("prefix", CONFIG["default_prefix"])
        STRINGS = Strings(lang)
        for item in blacklist.list:
            if content in item:
                await ctx.message.delete()
                embed = discord.Embed(
                    title=STRINGS["general"]["blacklistwarntitle"],
                    description=STRINGS["general"]["blacklistwarndesc"],
                    color=0xFF0000,
                )
                embed.set_footer(
                    text=STRINGS["general"]["blacklistwarnfooter"])
                return await ctx.send(embed=embed)
        else:
            return await ctx.send(content)

    @commands.guild_only()
    @commands.command(description="Generate Embed")
    async def embed(self, ctx: Context, name, *, content):
        s = await Settings(ctx.guild.id)
        lang = await s.get_field("locale", CONFIG["default_locale"])
        prefix = await s.get_field("prefix", CONFIG["default_prefix"])
        STRINGS = Strings(lang)
        for item in blacklist.list:
            if content in item:
                await ctx.message.delete()
                embed = discord.Embed(
                    title=STRINGS["general"]["blacklistwarntitle"],
                    description=STRINGS["general"]["blacklistwarndesc"],
                    color=0xFF0000,
                )
                embed.set_footer(
                    text=STRINGS["general"]["blacklistwarnfooter"])
                return await ctx.send(embed=embed)
        else:
            creator = discord.Embed(title=name, description=content)
            await ctx.send(embed=creator)

    @commands.command(description="Search Wikipedia")
    @commands.is_nsfw()
    async def wiki(self, ctx: Context, *, searcher=None):
        try:
            wikipedia.set_lang("en")
            req = wikipedia.page(searcher)
            wikip = discord.Embed(
                title=req.title,
                description="Wikipedia search results",
                url=req.url,
                color=0x269926,
            )
            wikip.set_thumbnail(url=req.images[0])
            await ctx.send(embed=wikip)
        except wikipedia.exceptions.PageError:
            wikierror = discord.Embed(
                title="Wikipedia Error",
                description="Page not found or some other error",
            )
            wikierror.add_field(
                name="If you are still having this error",
                value=
                "Report the issue on github or ask in bot support server about it",
                inline=True,
            )
            wikierror.set_footer(text="Try again ")
            await ctx.send(embed=wikierror)
        except:
            await ctx.send(
                "bot: Missing argument or permissions to do the command")

    @commands.guild_only()
    @commands.command()
    async def about(self, ctx: Context) -> NoReturn:
        """Shows a short description of the bot."""
        s = await Settings(ctx.guild.id)
        lang = await s.get_field("locale", CONFIG["default_locale"])
        STRINGS = Strings(lang)
        path = "scripts/version.txt"
        with open(path, "r") as file:
            ver = file.readline()
        ramUsage = self.process.memory_full_info().rss / 1024**2
        pythonVersion = platform.python_version()
        dpyVersion = discord.__version__
        servercount = len(self.bot.guilds)
        embed = discord.Embed(
            title=STRINGS["general"]["abouttitle"],
            description=STRINGS["general"]["aboutdesc"],
            color=0xFF6900,
        )
        embed.add_field(name=STRINGS["general"]["aboutver"],
                        value=f"```{ver}```",
                        inline=True)
        embed.add_field(name="Python Version:",
                        value=f"```{pythonVersion}```",
                        inline=True)
        embed.add_field(name="Library", value="```discord.py```", inline=True)
        embed.add_field(name="Discord.Py Version", value=f"```{dpyVersion}```")
        embed.add_field(name="RAM Usage",
                        value=f"```{ramUsage:.2f} MB```",
                        inline=True)
        embed.add_field(
            name="Servers",
            value=f"```{servercount}```",
            inline=True,
        )
        embed.add_field(
            name=STRINGS["general"]["aboutauthor"],
            value=STRINGS["general"]["aboutauthortext"],
            inline=True,
        )

        # embed.add_field(name=STRINGS['general']['aboutthanks'], value=STRINGS['general']['aboutthankstext'],inline=False)
        embed.set_footer(text=self.bot.user.name,
                         icon_url=self.bot.user.avatar_url)
        await ctx.send(embed=embed)

    @commands.guild_only()
    @commands.command()
    async def privacy(self, ctx: Context):
        s = await Settings(ctx.guild.id)
        lang = await s.get_field("locale", CONFIG["default_locale"])
        STRINGS = Strings(lang)
        embed = discord.Embed(
            title=STRINGS["privacy"]["privtitle"],
            description=STRINGS["privacy"]["privdesc"],
            color=0xFF8040,
        )
        embed.add_field(
            name=STRINGS["privacy"]["terminologytitle"],
            value=STRINGS["privacy"]["terminologydesc"],
            inline=True,
        )
        embed.add_field(
            name=STRINGS["privacy"]["datacollecttitle"],
            value=STRINGS["privacy"]["datacollectdesc"],
            inline=True,
        )
        embed.add_field(
            name=STRINGS["privacy"]["dctitlecont"],
            value=STRINGS["privacy"]["datacollectcont"],
            inline=True,
        )
        embed.add_field(
            name=STRINGS["privacy"]["loggingtitle"],
            value=STRINGS["privacy"]["loggingdesc"],
            inline=True,
        )
        embed.add_field(
            name=STRINGS["privacy"]["securitytitle"],
            value=STRINGS["privacy"]["securitydesc"],
            inline=True,
        )
        embed.add_field(
            name=STRINGS["privacy"]["datadeletepoltitle"],
            value=STRINGS["privacy"]["datadeletepoldesc"],
            inline=True,
        )
        embed.set_footer(text=self.bot.user.name,
                         icon_url=self.bot.user.avatar_url)
        await ctx.send(embed=embed)


def setup(bot: Bot) -> NoReturn:
    bot.add_cog(General(bot))
    Logger.cog_loaded(bot.get_cog("General").name)
