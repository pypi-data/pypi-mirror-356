#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Smart bot

- Author: Rex Zhou <879582094@qq.com>
- Created Time: 2025/6/5 16:28
- Copyright: Copyright © 2025 Rex Zhou. All rights reserved.
"""
from pathlib import Path
from re import compile as re_compile, MULTILINE
from typing import Dict, List, Type, TypeVar, Union, Callable

from ._abstract import AbstractBot, FilePathLike
from .file import FileBot
from .image import ImageBot
from .markdown import MarkdownBot, MarkdownBotV2
from .news import NewsBot
from .template_card.news import NewsCardBot
from .template_card.text import TextCardBot
from .text import TextBot
from .voice import VoiceBot
from .._deco import verify_file

# pylint: disable=protected-access
_Colors: List[str] = [_.lower() for _ in MarkdownBot._Color.get_valid_codes()]
_BotT = TypeVar('_BotT', bound='AbstractBot')


class SmartBot(AbstractBot):
    """Smart Wecom Group Bot"""

    _MD_COMMON_REGEXES: List[str] = [
        r'^#{1,6}\s+.+$',  # Title
        r'\*\*.+\*\*',  # Bold
        r'`[^`]+`',  # Inner line code
        r'\[[^\]]+\]\([^\)]+\)',  # Link
        r'^>\s+.+$',  # Reference
    ]
    _MD_REGEXES: List[str] = [
        rf'<font color="({"|".join(_Colors)})">[^<]+</font>',  # Color
    ]
    _MDv2_REGEXES: List[str] = [
        *_MD_COMMON_REGEXES,
        r'\*.+\*',  # Italics
        r'^(\s*[-*+]\s+.+(\n\s{2,}\S.*)*)+$',  # Unordered list
        r'^\d+\.\s+.+$',  # Ordered List
        r'!\[[^\]]+\]\([^\)]+\)',  # Picture
        r'^(>+) .+$',  # References (multi-level support)
        r'^-{3,}$',  # Dividing line
        r'^```[\s\S]+?```$',  # Code block
        r'^\|.+\|(\n\|?[-:]+[-|: ]+)+\n(\|.+\|)+$',  # Table
    ]

    @property
    def _doc_key(self) -> str:
        return "如何使用群机器人"

    def _verify_markdown(
            self,
            string: str) -> Union[Type[MarkdownBot], Type[MarkdownBotV2], bool]:
        r"""
        Verify whether the string is Markdown format.

        For v1 version:
        - Title 1 - 6:                  r'^#{1,6}\s+.+$'
        - Bold:                         r'\*\*.+\*\*'
        - Link:                         r'\[[^\]]+\]\([^\)]+\)'
        - Code:                         r'`[^`]+`'
        - Reference:                    r'^>\s+.+$'
        - Color (** Uniq feature **):   r'<font color="(info|comment|warning)">[^<]+</font>'

        For v2 version:
        - Title 1 - 6:          r'^#{1,6}\s+.+$'
        - Bold:                 r'\*\*.+\*\*'
        - Link:                 r'\[[^\]]+\]\([^\)]+\)'
        - Code:                 r'`[^`]+`'
        - Italics:              r'\*.+\*'
        - Unordered list:       r'^(\s*[-*+]\s+.+(\n\s{2,}\S.*)*)+$'
        - Ordered List:         r'^\d+\.\s+.+$'
        - Picture:              r'!\[[^\]]+\]\([^\)]+\)'
        - References (multi):   r'^(>+) .+$'
        - Dividing line:        r'^-{3,}$'
        - Code block:           r'^```[\s\S]+?```$'
        - Table:                r'^\|.+\|(\n\|?[-:]+[-|: ]+)+\n(\|.+\|)+$'

        :param string: Raw string.
        :return: Whether the string is Markdown format.
        """
        # Top priority to detect the uniq feature for v1.
        regex = '|'.join(f'(?:{reg})' for reg in self._MD_REGEXES)
        regex = re_compile(r'(' + regex + r')', MULTILINE)
        if regex.search(string):
            return MarkdownBot
        # Try to use v2 to match content
        regex = '|'.join(f'(?:{reg})' for reg in self._MDv2_REGEXES)
        regex = re_compile(r'(' + regex + r')', MULTILINE)
        if regex.search(string):
            return MarkdownBotV2
        # Return `False` when can't match content
        return False

    def _guess_message_bot(self, *args, **kwargs) -> Type[_BotT]:
        """
        Guess whether the bot type is Text or Markdown.
        :param args: Positional arguments.
        :param kwargs: Keyword arguments.
        :return: Subclass of AbstractBot.
        """
        if "mentioned_list" in kwargs or "mentioned_mobile_list" in kwargs:
            return TextBot
        if bot := self._verify_markdown(args[0]):
            return bot
        return TextBot

    @verify_file
    def _guess_file_bot(self, file_path: FilePathLike) -> Type[_BotT]:
        """
        Guess whether the bot type is File or Image or Voice.
        :param file_path: File path.
        :return: Subclass of AbstractBot.
        """
        suffix = Path(file_path).suffix
        if suffix == ".amr":
            bot = VoiceBot
        elif suffix in (".jpg", ".png"):
            bot = ImageBot
        else:
            bot = FileBot
        return bot

    def _verify_arguments(self, *args, **kwargs) -> Type[_BotT]:
        r"""
        Intelligent selection bot, follow the following rules:

        1. Provide `args`, which MUST be either Text or Markdown;

        There are 2 situations:

            Section A:
                Also provide `mentioned_list` or `mentioned_mobile_list` from kwargs;
                This MUST be Text.

            Section B:
                Distinguish using regex to verify whether the `msg` is Markdown format;

        2. Provide `file_path` from kwargs, which MUST be File / Image / Voice;
        Distinguish using file suffix.

            - Voice: MUST be `.amr` file.
            - Image: Either `.png` or `.jpg`.
            - File: Other suffixes.

        3. Provide `articles` from kwargs, which MUST be News;

        4. Complex kwargs, which MUST be either TextCard or NewsCard;
        Distinguish using bot's own required parameters.

            - NewsCard: MUST have `card_image` in kwargs.
            - TextCard: Otherwise default bot.

        :param args: Positional arguments.
        :param kwargs: Keyword arguments.
        :return: Subclass of AbstractBot.
        """
        if args:
            return self._guess_message_bot(*args, **kwargs)
        if "file_path" in kwargs and kwargs["file_path"]:
            return self._guess_file_bot(kwargs["file_path"])
        if "articles" in kwargs and kwargs["articles"]:
            return NewsBot
        if "card_image" in kwargs:
            return NewsCardBot
        return TextCardBot

    def _convert_arguments(self, *args, **kwargs) -> AbstractBot:
        bot_type: Type[_BotT] = args[0]
        return bot_type(self.key)

    def send(self,
             msg: str = None,
             /,
             articles: List[Dict[str, str]] = None,
             file_path: FilePathLike = None,
             **kwargs) -> dict:
        """
        Automatic select correct type of bot, then send the content.
        :param msg: Message to send. Valid for Text or Markdown.
        :param articles: Articles to send. Valid for News.
        :param file_path: File to send. Valid for Image | Voice | File.
        :param kwargs: Other keyword arguments. Valid for Text(mention) | TextCard | NewsCard.
        :return:
        """
        if msg is not None:
            bot_type = self._verify_arguments(msg, **kwargs)
            bot = self._convert_arguments(bot_type)
        else:
            bot_type = self._verify_arguments(articles=articles,
                                              file_path=file_path,
                                              **kwargs)
            bot = self._convert_arguments(bot_type)
        result = bot.send(msg, articles=articles, file_path=file_path, **kwargs)
        return result

    # pylint: disable=too-few-public-methods
    class _MarkdownFeatureProxy:
        """Proxy that routes method calls to appropriate Markdown type."""

        @property
        def green(self) -> Callable:
            """
            Return v1 feature.
            :return:
            """
            return MarkdownBot.green

        @property
        def gray(self) -> Callable:
            """
            Return v1 feature.
            :return:
            """
            return MarkdownBot.gray

        @property
        def orange(self) -> Callable:
            """
            Return v1 feature.
            :return:
            """
            return MarkdownBot.orange

        @property
        def list2table(self) -> Callable:
            """
            Return v2 feature.
            :return:
            """
            return MarkdownBotV2.list2table

    markdown_feature = _MarkdownFeatureProxy()
