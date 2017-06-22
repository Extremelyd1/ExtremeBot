from musicbot.commands.command import Command

class IdCommand(Command):
    """docstring for IdCommand."""

    trigger = 'id'
    aliases = []

    def __init__(self):
        super().__init__()

    async def run(self):
        if not self.user_mentions:
            await self.bot.safe_send_message(
                self.channel,
                '%s, your id is `%s`' % (self.author.mention, self.author.id),
                expire_in=35,
                also_delete=self.message
            )
        else:
            usr = self.user_mentions[0]
            await self.bot.safe_send_message(
                self.channel,
                "%s's id is `%s`" % (usr.name, usr.id),
                expire_in=35,
                also_delete=self.message
            )
