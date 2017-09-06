from textwrap import dedent

from musicbot.commands.command import Command
from musicbot.commands.command_manager import get_command, get_commands

class HelpCommand(Command):
    """
    Usage:
        {command_prefix}help [command]
    Prints a help message.
    If a command is specified, it prints a help message for that command.
    Otherwise, it lists the available commands.
    """

    trigger = 'help'
    aliases = ['?']

    def __init__(self):
        super().__init__()

    async def run(self):

        command = None

        if len(self.leftover_args) == 1:
            command = self.leftover_args[0]

        if command:
            cmd = get_command(command)
            if cmd:
                await self.bot.safe_send_message_check(
                    self.channel,
                    "```\n{}```".format(
                        dedent(cmd.__doc__).format(
                        command_prefix=self.bot.config.command_prefix
                    )),
                    expire_in=60,
                    also_delete=self.message
                )
            else:
                await self.bot.safe_send_message_check(
                    self.channel,
                    'No such command',
                    expire_in=10,
                    also_delete=self.message
                )

        else:
            helpmsg = "**Commands**\n```"
            commands = []

            for cmd in get_commands():
                commands.append("{}{}".format(self.bot.config.command_prefix, cmd.trigger))

            helpmsg += ", ".join(commands)
            helpmsg += "```"

            await self.bot.safe_send_message_check(
                self.channel,
                '%s, ' % self.author.mention + helpmsg,
                expire_in=60,
                also_delete=self.message
            )
