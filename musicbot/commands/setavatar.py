import aiohttp

from musicbot.commands.command import Command
from musicbot import exceptions

class SetAvatarCommand(Command):
    """
    Usage:
        {command_prefix}setavatar [url]

    Changes the bot's avatar.
    Attaching a file and leaving the url parameter blank also works.
    """

    trigger = 'setavatar'
    aliases = []

    def __init__(self):
        super().__init__()
        self.owner_only = True

    async def run(self):

        # Check if leftover args are empty
        if not self.leftover_args:
            raise exceptions.CommandError("Please provide a url", expire_in=20)

        # Get url
        url = self.leftover_args.pop(0)

        if self.message.attachments:
            thing = self.message.attachments[0]['url']
        else:
            thing = url.strip('<>')

        # Get url contents and change avatar
        try:
            with aiohttp.Timeout(10):
                async with self.bot.aiosession.get(thing) as res:
                    await self.bot.edit_profile(avatar=await res.read())

        except Exception as e:
            raise exceptions.CommandError("Unable to change avatar: %s" % e, expire_in=20)

        await self.bot.safe_send_message(self.channel, ":ok_hand:", expire_in=20)
