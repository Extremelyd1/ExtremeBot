from musicbot.commands.command import Command
from musicbot import exceptions

class PauseCommand(Command):
    """docstring for PauseCommand."""

    trigger = 'pause'
    aliases = []

    def __init__(self):
        super().__init__()

    async def run(self):
        if self.player.is_playing:
            self.player.pause()

        else:
            raise exceptions.CommandError('Player is not playing.', expire_in=30)
