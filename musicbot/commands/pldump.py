from io import BytesIO
from musicbot.commands.command import Command
from musicbot import exceptions
from collections import defaultdict

class PldumpCommand(Command):
    """
    Usage:
        {command_prefix}pldump url
    Dumps the individual urls of a playlist
    """

    trigger = 'pldump'
    aliases = ['playlistdump']

    def __init__(self):
        super().__init__()

    async def run(self):

        if not len(self.leftover_args) == 1:
            await self.bot.safe_send_message_check(
                self.channel,
                '%s, no playlist specified' % self.author.mention,
                expire_in=20,
                also_delete=self.message
            )
            return

        song_url = self.leftover_args[0]

        try:
            info = await self.bot.downloader.extract_info(self.bot.loop, song_url.strip('<>'), download=False, process=False)
        except Exception as e:
            raise exceptions.CommandError("Could not extract info from input url\n%s\n" % e, expire_in=25)

        if not info:
            raise exceptions.CommandError("Could not extract info from input url, no data.", expire_in=25)

        if not info.get('entries', None):
            # TODO: Retarded playlist checking
            # set(url, webpageurl).difference(set(url))

            if info.get('url', None) != info.get('webpage_url', info.get('url', None)):
                raise exceptions.CommandError("This does not seem to be a playlist.", expire_in=25)
            else:
                return await self.run(self.channel, info.get(''))

        linegens = defaultdict(lambda: None, **{
            "youtube":    lambda d: 'https://www.youtube.com/watch?v=%s' % d['id'],
            "soundcloud": lambda d: d['url'],
            "bandcamp":   lambda d: d['url']
        })

        exfunc = linegens[info['extractor'].split(':')[0]]

        if not exfunc:
            raise exceptions.CommandError("Could not extract info from input url, unsupported playlist type.", expire_in=25)

        with BytesIO() as fcontent:
            for item in info['entries']:
                fcontent.write(exfunc(item).encode('utf8') + b'\n')

            fcontent.seek(0)
            await self.bot.send_file(self.author, fcontent, filename='playlist.txt', content="Here's the url dump for <%s>" % song_url)

        await self.bot.safe_send_message_check(
            self.channel,
            ':mailbox_with_mail:',
            expire_in=20,
            also_delete=self.message
        )
