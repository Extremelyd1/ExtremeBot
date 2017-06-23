from musicbot.commands.command import Command
from musicbot import exceptions

class JoinServerCommand(Command):
    """
    Usage:
        {command_prefix}joinserver invite_link

    Asks the bot to join a server.  Note: Bot accounts cannot use invite links.
    """

    trigger = 'joinserver'
    aliases = []
    owner_only = True

    def __init__(self):
        super().__init__()

    async def run(self):
        if self.bot.user.bot or True:
            url = await self.bot.generate_invite_link()
            await self.bot.safe_send_message(
                self.channel,
                self.author.mention + ", Bot accounts can't use invite links!  Click here to invite me: \n{}".format(url),
                expire_in=30
            )

        server_link = None
        try:
            # Check if array is not empty
            if leftover_args:
                server_link = leftover_args[0]
                if server_link:
                    await self.bot.accept_invite(server_link)
                    await self.bot.safe_send_message(self.channel, ":+1:", expire_in=30)

        except:
            raise exceptions.CommandError('Invalid URL provided:\n{}\n'.format(server_link), expire_in=30)
