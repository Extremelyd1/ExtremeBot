from musicbot import exceptions
from musicbot.commands.command import Command

class RestartCommand(Command):
    """docstring for RestartCommand."""
    def __init__(self):
        super().__init__()
        self.trigger = 'restart'
        self.aliases = ['reboot']

    async def run(self):
        await self.bot.safe_send_message(self.channel, ":wave:")
        await self.bot.disconnect_all_voice_clients()
        raise exceptions.RestartSignal
