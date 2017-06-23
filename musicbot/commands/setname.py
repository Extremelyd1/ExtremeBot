from musicbot.commands.command import Command
from musicbot import exceptions

class SetNameCommand(Command):
    """
    Usage:
        {command_prefix}setname name

    Changes the bot's username.
    Note: This operation is limited by discord to twice per hour.
    """

    trigger = 'setname'
    aliases = []
    owner_only = True

    def __init__(self):
        super().__init__()

    async def run(self):

        # Check if leftover args are empty
        if not self.leftover_args:
            raise exceptions.CommandError("Please provide a name", expire_in=20)

        # Build name
        name = ' '.join([*self.leftover_args])

        # Change name, limited to twice an hour
        try:
            await self.bot.edit_profile(username=name)
        except Exception as e:
            raise exceptions.CommandError(e, expire_in=20)

        await self.bot.safe_send_message(self.channel, ":ok_hand:", expire_in=20)
