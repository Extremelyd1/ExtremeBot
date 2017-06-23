from musicbot.commands.command import Command
from musicbot import exceptions

class ShutdownCommand(Command):
    """
    Usage:
        {command_prefix}shutdown
    Shuts the bot down.
    """

    trigger = 'shutdown'
    aliases = ['terminate']

    def __init__(self):
        super().__init__()

    async def run(self):
        await self.bot.safe_send_message(self.channel, ":wave:")
        await self.bot.disconnect_all_voice_clients()
        raise exceptions.TerminateSignal
