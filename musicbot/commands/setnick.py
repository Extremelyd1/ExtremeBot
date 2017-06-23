from musicbot.commands.command import Command
from musicbot import exceptions

class SetNickCommand(Command):
    """
    Usage:
        {command_prefix}setnick nick

    Changes the bot's nickname.
    """

    trigger = 'setnick'
    aliases = ['setnickname']
    owner_only = True

    def __init__(self):
        super().__init__()

    async def run(self):

        # Check permissions
        if not self.channel.permissions_for(self.server.me).change_nickname:
            raise exceptions.CommandError("Unable to change nickname: no permission.")

        # Check if leftover args are not empty
        if not self.leftover_args:
            raise exceptions.CommandError("Please provide a nickname")

        # Build nickname
        nick = ' '.join([*self.leftover_args])

        # Change nickname
        try:
            await self.bot.change_nickname(self.server.me, nick)
        except Exception as e:
            raise exceptions.CommandError(e, expire_in=20)

        await self.bot.safe_send_message(self.channel, ":ok_hand:", expire_in=20)
