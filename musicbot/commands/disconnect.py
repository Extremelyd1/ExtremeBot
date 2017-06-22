from musicbot.commands.command import Command

class DisconnectCommand(Command):
    """docstring for DisconnectCommand."""

    trigger = 'disconnect'
    aliases = ['dc']

    def __init__(self):
        super().__init__()

    async def run(self):
        await self.bot.disconnect_voice_client(self.server)
        await self.bot.safe_send_message(
            self.channel,
            ":hear_no_evil:",
            delete_after=20,
            also_delete=self.message
        )
