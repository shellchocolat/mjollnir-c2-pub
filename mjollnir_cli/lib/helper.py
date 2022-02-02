#!/usr/bin/python3

"""
.. moduleauthor:: shellchocolat <shellchocolat@no-mail.com>
"""

class Helper(object):
    """This class is used to display a custom help during the use of the tool.
    """
    def __init__(self):
        self.ok = 'ok'

    def helpMenu(self, command):
        """This function checks if the command is not null, and if it isn't, displays the appropriate help for the specified command.

        :param command: the command for which the help is requested
        :type command: str
        :returns: bool
        """
        if command == '':
            print('main help')
        else:
            print(command)

        return True
