from musicbot.commands.command import Command
from musicbot import exceptions

class ClearCommand(Command):
    """docstring for ClearCommand."""
    def __init__(self):
        super().__init__()
        self.trigger = 'clear'
        self.aliases = []

    async def run(self):
        self.player.playlist.clear()
        await self.bot.safe_send_message(
            self.channel,
            ':put_litter_in_its_place:', expire_in=20,
            also_delete=self.message
        )
