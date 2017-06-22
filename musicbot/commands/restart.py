from musicbot import exceptions
from musicbot.commands.command import Command

class RestartCommand(Command):
    """docstring for RestartCommand."""

    trigger = 'restart'
    aliases = ['reboot']

    def __init__(self):
        super().__init__()

    async def run(self):
        await self.bot.safe_send_message(self.channel, ":wave:")
        await self.bot.disconnect_all_voice_clients()
        raise exceptions.RestartSignal
