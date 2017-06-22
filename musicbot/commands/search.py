import shlex
from musicbot import exceptions
from musicbot.commands.command import Command

class SearchCommand(Command):
    """
    Usage:
        {command_prefix}search [service] [number] query
    Searches a service for a video and adds it to the queue.
    - service: any one of the following services:
        - youtube (yt) (default if unspecified)
        - soundcloud (sc)
        - yahoo (yh)
    - number: return a number of video results and waits for user to choose one
      - defaults to 1 if unspecified
      - note: If your search query starts with a number,
              you must put your query in quotes
        - ex: {command_prefix}search 2 "I ran seagulls"
    """

    trigger = 'search'
    aliases = []

    def __init__(self):
        super().__init__()

    async def run(self):
        if self.permissions.max_songs and self.player.playlist.count_for_user(author) > self.permissions.max_songs:
            raise exceptions.PermissionsError(
                "You have reached your playlist item limit (%s)" % self.permissions.max_songs,
                expire_in=30
            )

        def argcheck():
            if not self.leftover_args:
                raise exceptions.CommandError(
                    "Please specify a search query.\n%s" % dedent(
                        SearchCommand.__doc__.format(command_prefix=self.config.command_prefix)),
                    expire_in=30,
                    also_delete=self.message
                )

        argcheck()

        try:
            self.leftover_args = shlex.split(' '.join(self.leftover_args))
        except ValueError:
            raise exceptions.CommandError("Please quote your search query properly.", expire_in=30)

        service = 'youtube'
        items_requested = 3
        max_items = 10  # this can be whatever, but since ytdl uses about 1000, a small number might be better
        services = {
            'youtube': 'ytsearch',
            'soundcloud': 'scsearch',
            'yahoo': 'yvsearch',
            'yt': 'ytsearch',
            'sc': 'scsearch',
            'yh': 'yvsearch'
        }

        if self.leftover_args[0] in services:
            service = self.leftover_args.pop(0)
            argcheck()

        if self.leftover_args[0].isdigit():
            items_requested = int(self.leftover_args.pop(0))
            argcheck()

            if items_requested > max_items:
                raise exceptions.CommandError("You cannot search for more than %s videos" % max_items)

        # Look jake, if you see this and go "what the fuck are you doing"
        # and have a better idea on how to do this, i'd be delighted to know.
        # I don't want to just do ' '.join(leftover_args).strip("\"'")
        # Because that eats both quotes if they're there
        # where I only want to eat the outermost ones
        if self.leftover_args[0][0] in '\'"':
            lchar = self.leftover_args[0][0]
            self.leftover_args[0] = self.leftover_args[0].lstrip(lchar)
            self.leftover_args[-1] = self.leftover_args[-1].rstrip(lchar)

        search_query = '%s%s:%s' % (services[service], items_requested, ' '.join(self.leftover_args))

        search_msg = await self.bot.send_message(self.channel, "Searching for videos...")
        await self.bot.send_typing(self.channel)

        try:
            info = await self.bot.downloader.extract_info(self.player.playlist.loop, search_query, download=False, process=True)

        except Exception as e:
            await self.bot.safe_edit_message(search_msg, str(e), send_if_fail=True)
            return
        else:
            await self.bot.safe_delete_message(search_msg)

        if not info:
            await self.bot.safe_send_message(
                self.channel,
                'No videos found.',
                expire_in=30,
                also_delete=self.message
            )
            return

        def check(m):
            return (
                m.content.lower()[0] in 'yn' or
                m.content.lower().startswith('{}{}'.format(self.bot.config.command_prefix, SearchCommand.trigger)) or
                m.content.lower().startswith('{}{}'.format(self.bot.config.command_prefix, (alias for alias in SearchCommand.aliases))) or
                m.content.lower().startswith('exit'))

        for e in info['entries']:
            result_message = await self.bot.safe_send_message(self.channel, "Result %s/%s: %s" % (
                info['entries'].index(e) + 1, len(info['entries']), e['webpage_url']))

            confirm_message = await self.bot.safe_send_message(self.channel, "Is this ok? Type `y`, `n` or `exit`")
            response_message = await self.bot.wait_for_message(30, author=self.author, channel=self.channel, check=check)

            if not response_message:
                await self.bot.safe_delete_message(result_message)
                await self.bot.safe_delete_message(confirm_message)
                await self.bot.safe_send_message(
                    self.channel,
                    'Ok nevermind.',
                    expire_in=30,
                    also_delete=self.message
	            )
                return

            # They started a new search query so lets clean up and bugger off
            elif response_message.content.startswith(self.bot.config.command_prefix) or \
                    response_message.content.lower().startswith('exit'):

                await self.bot.safe_delete_message(result_message)
                await self.bot.safe_delete_message(confirm_message)
                await self.bot.safe_delete_message(self.message)

                if response_message.content.lower().startswith('exit'):
                    await self.bot.safe_delete_message(response_message)

                return

            if response_message.content.lower().startswith('y'):
                await self.bot.safe_delete_message(result_message)
                await self.bot.safe_delete_message(confirm_message)
                await self.bot.safe_delete_message(response_message)

                playCommand = Command.get_command('play')
                playCommand.player = self.player
                playCommand.channel = self.channel
                playCommand.author = self.author
                playCommand.permissions = self.permissions
                playCommand.leftover_args = [e['webpage_url']]

                await self.bot.safe_send_message(
                    self.channel,
                    'Alright, coming right up!',
                    expire_in=30,
                    also_delete=self.message
	            )

                await playCommand.run()

                return
            else:
                await self.bot.safe_delete_message(result_message)
                await self.bot.safe_delete_message(confirm_message)
                await self.bot.safe_delete_message(response_message)

        await self.bot.safe_send_message(
            self.channel,
            'Oh well :frowning:',
            expire_in=30,
            also_delete=self.message
        )
