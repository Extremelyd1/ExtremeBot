from musicbot.commands.command import Command
from musicbot import exceptions

class ClearCommand(Command):
    """
    Usage:
        {command_prefix}clear
    Clears the playlist.
    """

    trigger = 'clear'
    aliases = []

    def __init__(self):
        super().__init__()

    async def run(self):
        self.player.playlist.clear()
        await self.bot.safe_send_message(
            self.channel,
            ':put_litter_in_its_place:', expire_in=20,
            also_delete=self.message
        )
