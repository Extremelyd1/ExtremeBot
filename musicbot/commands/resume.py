from musicbot.commands.command import Command
from musicbot import exceptions

class ResumeCommand(Command):
    """docstring for ResumeCommand."""

    trigger = 'resume'
    aliases = []

    def __init__(self):
        super().__init__()

    async def run(self):
        if self.player.is_paused:
            self.player.resume()

        else:
            raise exceptions.CommandError('Player is not paused.', expire_in=30)
