from musicbot.commands.command import Command

class LinkCommand(Command):
    """
    Usage:
        {command_prefix}link
    Displays the link of the current song in chat
    """

    trigger = 'link'
    aliases = []

    def __init__(self):
        super().__init__()

    async def run(self):
        if self.player.current_entry:
            await self.bot.safe_send_message(
                self.channel,
                self.player.current_entry.url,
                expire_in=20,
                also_delete=self.message
            )
        else:
            await self.bot.safe_send_message(
                self.channel,
                "Hold up, fetching song",
                expire_in=20,
                also_delete=self.message
            )
