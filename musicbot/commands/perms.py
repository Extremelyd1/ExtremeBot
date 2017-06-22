from musicbot.commands.command import Command

class PermsCommand(Command):
    """docstring for PermsCommand."""

    trigger = 'perms'
    aliases = ['permissions', 'permission', 'perm']

    def __init__(self):
        super().__init__()
        
    async def run(self):
        lines = ['Command permissions in %s\n' % self.server.name, '```', '```']

        for perm in self.bot.permissions.__dict__:
            if perm in ['user_list'] or self.bot.permissions.__dict__[perm] == set():
                continue

            lines.insert(len(lines) - 1, "%s: %s" % (perm, self.bot.permissions.__dict__[perm]))

        await self.bot.send_message(self.author, '\n'.join(lines))
        await self.bot.safe_send_message(
            self.channel,
            ':mailbox_with_mail:'
            , expire_in=20,
            also_delete=self.message
        )
