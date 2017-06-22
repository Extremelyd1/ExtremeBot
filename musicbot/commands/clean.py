import asyncio

from musicbot import exceptions
from musicbot.commands.command import Command

class CleanCommand(Command):
    """docstring for CleanCommand."""

    trigger = 'clean'
    aliases = ['purge']

    def __init__(self):
        super().__init__()

    async def run(self):
        if not len(self.leftover_args) in [0, 1]:
            raise exceptions.CommandError('Enter a number. NUMBER. That means digits. `15`. Etc.', expire_in=10)

        search_range = 50 if not len(self.leftover_args) == 1 else self.leftover_args[0]

        try:
            float(search_range)  # lazy check
            search_range = min(int(search_range), 1000)
        except:
            raise exceptions.CommandError('Enter a number. NUMBER. That means digits. `15`. Etc.', expire_in=10)

        await self.bot.safe_delete_message(self.message, quiet=True)

        def is_possible_command_invoke(entry):
            valid_call = any(
                entry.content.startswith(prefix) for prefix in [self.bot.config.command_prefix])  # can be expanded
            return valid_call and not entry.content[1:2].isspace()

        delete_invokes = True
        delete_all = self.channel.permissions_for(self.author).manage_messages or self.bot.config.owner_id == self.author.id

        def check(message):
            if is_possible_command_invoke(message) and delete_invokes:
                return delete_all or message.author == self.author
            return message.author == self.bot.user

        if self.bot.user.bot:
            if self.channel.permissions_for(self.server.me).manage_messages:
                deleted = await self.bot.purge_from(self.channel, check=check, limit=search_range, before=self.message)
                await self.bot.safe_send_message(
                    self.channel,
                    'Cleaned up {} message{}.'.format(len(deleted), 's' * bool(deleted)),
                    expire_in=15,
                    also_delete=self.message
                )
                return

        deleted = 0
        async for entry in self.bot.logs_from(self.channel, search_range, before=self.message):
            if entry == self.bot.server_specific_data[self.server]['last_np_msg']:
                continue

            if entry.author == self.bot.user:
                await self.bot.safe_delete_message(entry)
                deleted += 1
                await asyncio.sleep(0.21)

            if is_possible_command_invoke(entry) and delete_invokes:
                if delete_all or entry.author == self.author:
                    try:
                        await self.bot.delete_message(entry)
                        await asyncio.sleep(0.21)
                        deleted += 1

                    except discord.Forbidden:
                        delete_invokes = False
                    except discord.HTTPException:
                        pass

        await self.bot.safe_send_message(
            self.channel,
            'Cleaned up {} message{}.'.format(deleted, 's' * bool(deleted)),
            expire_in=15,
            also_delete=self.message
        )
