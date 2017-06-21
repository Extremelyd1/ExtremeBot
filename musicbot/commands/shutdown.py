from musicbot.commands.command import Command
from musicbot import exceptions

class ShutdownCommand(Command):
    """docstring for ShutdownCommand."""
    def __init__(self):
        super().__init__()
        self.trigger = 'shutdown'
        self.aliases = ['terminate']

    async def run(self):
        await self.bot.safe_send_message(self.channel, ":wave:")
        await self.bot.disconnect_all_voice_clients()
        raise exceptions.TerminateSignal
