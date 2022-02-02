#!/usr/bin/python3

from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.formatted_text import HTML

"""
.. moduleauthor:: shellchocolat <shellchocolat@no-mail.com>
"""


class AutoCompletion(Completer):
    """This class is used to define the completion of the command line
    """
    def __init__(self, commands, command_family, family_colors, meta):
        self.commands = commands
        self.command_family = command_family
        self.family_colors = family_colors
        self.meta = meta

    def get_completions(self, document, complete_event):
        word = document.get_word_before_cursor()
        for command in self.commands:
            if command.startswith(word):
                if command in self.command_family:
                    family = self.command_family[command]
                    family_color = self.family_colors.get(family, 'default')

                    display = HTML(
                        '%s<b>:</b> <ansired>(<' + family_color + '>%s</' + family_color + '>)</ansired>'
                        ) % (command, family)
                else:
                    display = command

                yield Completion(
                    command,
                    start_position=-len(word),
                    display=display,
                    display_meta=self.meta.get(command)
                )
