from .command import Command
from .help import HelpCommand
from .q import QCommand

commands = []

commands.append(QCommand())

def has_command(command_string):
    return get_command(command_string)

def get_command(command_string):
    for command in commands:
        if command.trigger == command_string:
            return command
        elif command_string in command.aliases:
            return command
    return None
