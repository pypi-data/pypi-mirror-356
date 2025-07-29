#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Markdown type message sender


- Author: Rex Zhou <879582094@qq.com>
- Created Time: 2025/5/27 15:12
- Copyright: Copyright © 2025 Rex Zhou. All rights reserved.
"""
from enum import Enum
from typing import Union, List

from ._abstract import ConvertedData, AbstractBot
from .text import check_args


class MarkdownBot(AbstractBot):
    """Markdown type message Wecom Group Bot"""

    _MAX_LENGTH: int = 4096

    class _Color(Enum):
        """Markdown _color enum"""
        INFO = "green"
        COMMENT = "gray"
        WARNING = "orange"

        @classmethod
        def get_valid_colors(cls):
            """Return list of valid colors"""
            return [_.value for _ in cls]

        @classmethod
        def get_valid_codes(cls):
            """Return list of valid codes"""
            return [_.name for _ in cls]

    @property
    def _doc_key(self) -> str:
        return "markdown类型"

    def _verify_arguments(self, *args, **kwargs) -> None:
        """
        Verify the arguments passed.
        :param args: Positional arguments passed.
        :param kwargs: Keyword arguments passed.
        :return:
        """
        check_args(*args, maximum=self._MAX_LENGTH)

    def _convert_arguments(self, *args, **kwargs) -> ConvertedData:
        """
        Convert the message to Markdown format data.
        :param args: Positional arguments.
        :param kwargs: Other keyword arguments.
        :return: Converted data.
        """
        result = ({
            "msgtype": "markdown",
            "markdown": {
                "content": args[0].strip()
            }
        },)
        return result, kwargs

    @classmethod
    def _color(cls, raw: str, color: Union[str, _Color]) -> str:
        """
        Convert normal string to colorful string.
        :param raw: Raw string.
        :param color: Specify _color. Support: green | gray | orange
        :return: Colorized string.
        """
        if isinstance(color, str):
            try:
                color = cls._Color(color.lower())
            except ValueError as error:
                valid_colors = cls._Color.get_valid_colors()
                raise ValueError(
                    f"Invalid color '{color}'. Valid options: {valid_colors}"
                ) from error
        result = f'<font color="{color.name.lower()}">{raw}</font>'
        return result

    @classmethod
    def green(cls, text: str) -> str:
        """
        Return a green text string.
        :param text: Text to be converted.
        :return:
        """
        return cls._color(text, cls._Color.INFO)

    @classmethod
    def gray(cls, text: str) -> str:
        """
        Return a gray text string.
        :param text: Text to be converted.
        :return:
        """
        return cls._color(text, cls._Color.COMMENT)

    @classmethod
    def orange(cls, text: str) -> str:
        """
        Return an orange text string.
        :param text: Text to be converted.
        :return:
        """
        return cls._color(text, cls._Color.WARNING)


class MarkdownBotV2(AbstractBot):
    """Markdown V2 type message Wecom Group Bot"""

    _MAX_LENGTH: int = 4096

    @property
    def _doc_key(self) -> str:
        return "markdown-v2类型"

    def _verify_arguments(self, *args, **kwargs) -> None:
        """
        Verify the arguments passed.
        :param args: Positional arguments passed.
        :param kwargs: Keyword arguments passed.
        :return:
        """
        check_args(*args, maximum=self._MAX_LENGTH)

    def _convert_arguments(self, *args, **kwargs) -> ConvertedData:
        """
        Convert the message to Markdown format data.
        :param args: Positional arguments.
        :param kwargs: Other keyword arguments.
        :return: Converted data.
        """
        result = ({
            "msgtype": "markdown_v2",
            "markdown_v2": {
                "content": args[0].strip()
            }
        },)
        return result, kwargs

    @classmethod
    def list2table(cls, table: List[List[str]]) -> str:
        """
        Convert list of list to Markdown table string.
        :param table: List of lists to convert.
        :return: Markdown table string.
        """
        if not table or len(table) < 2:
            return ""

        # Parse headers and rows
        headers, rows = table[0], table[1:]

        # Generate header line
        header_line = "| " + " | ".join(headers) + " |"

        # Generate split line
        separator = "|"
        for i in range(len(headers)):
            if i == 0:
                separator += " :----- |"
            elif i == len(headers) - 1:
                separator += " -------: |"
            else:
                separator += " :----: |"

        # Generate data rows
        data_lines = []
        for row in rows:
            data_lines.append("| " + " | ".join(row) + " |")

        # Merge all rows
        markdown_table = "\n".join([header_line, separator] + data_lines)
        return markdown_table
