from musicbot import exceptions
from musicbot.commands.command import Command
from musicbot.utils import write_file

class BlacklistCommand(Command):
    """
    Usage:
        {command_prefix}blacklist [ + | - | add | remove ] @UserName [@UserName2 ...]
    Add or remove users to the blacklist.
    Blacklisted users are forbidden from using bot commands.
    """

    trigger = 'blacklist'
    aliases = ['bl', 'blist']

    def __init__(self):
        super().__init__()

    async def run(self):
        if not self.user_mentions:
            raise exceptions.CommandError("No users listed.", expire_in=20)

        if len(self.leftover_args) == 0:
            raise exceptions.CommandError(
                'No option specified, use +, -, add, or remove', expire_in=20
            )

        option = self.leftover_args.pop(0)

        if option not in ['+', '-', 'add', 'remove']:
            raise exceptions.CommandError(
                'Invalid option "%s" specified, use +, -, add, or remove' % option, expire_in=20
            )

        for user in self.user_mentions.copy():
            if user.id == self.bot.config.owner_id:
                print("[Commands:Blacklist] The owner cannot be blacklisted.")
                self.user_mentions.remove(user)

        old_len = len(self.bot.blacklist)

        if option in ['+', 'add']:
            self.bot.blacklist.update(user.id for user in self.user_mentions)

            write_file(self.bot.config.blacklist_file, self.bot.blacklist)

            await self.bot.safe_send_message(
                self.channel,
                '%s, %s users have been added to the blacklist' % (self.author.mention, len(self.bot.blacklist) - old_len), expire_in=10,
                also_delete=self.message
            )

        else:
            if self.bot.blacklist.isdisjoint(user.id for user in self.user_mentions):
                await self.bot.safe_send_message(
                    self.channel,
                    '%s none of those users are in the blacklist.' % (self.author.mention), expire_in=10,
                    also_delete=self.message
                )

            else:
                self.bot.blacklist.difference_update(user.id for user in self.user_mentions)
                write_file(self.bot.config.blacklist_file, self.bot.blacklist)

                await self.bot.safe_send_message(
                    self.channel,
                    '%s, %s users have been removed from the blacklist' % (self.author.mention, old_len - len(self.bot.blacklist)), expire_in=10,
                    also_delete=self.message
                )
