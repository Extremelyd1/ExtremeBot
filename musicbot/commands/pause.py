from musicbot.commands.command import Command
from musicbot import exceptions

class PauseCommand(Command):
    """docstring for PauseCommand."""
    def __init__(self):
        super().__init__()
        self.trigger = 'pause'
        self.aliases = []

    async def run(self):
        if self.player.is_playing:
            self.player.pause()

        else:
            raise exceptions.CommandError('Player is not playing.', expire_in=30)
