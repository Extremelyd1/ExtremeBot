from datetime import timedelta
from musicbot.commands.command import Command
from musicbot.constants import DISCORD_MSG_CHAR_LIMIT

class QueueCommand(Command):
    """docstring for QueueCommand."""
    def __init__(self):
        super().__init__()
        self.trigger = 'queue'
        self.aliases = ['q', 'queued']

    async def run(self):
        lines = []
        unlisted = 0
        andmoretext = '* ... and %s more*' % ('x' * len(self.player.playlist.entries))

        if self.player.current_entry:
            song_progress = str(timedelta(seconds=self.player.progress)).lstrip('0').lstrip(':')
            song_total = str(timedelta(seconds=self.player.current_entry.duration)).lstrip('0').lstrip(':')
            prog_str = '`[%s/%s]`' % (song_progress, song_total)

            if self.player.current_entry.meta.get('channel', False) and self.player.current_entry.meta.get('author', False):
                lines.append("Now Playing: **%s** added by **%s** %s\n" % (
                    self.player.current_entry.title, self.player.current_entry.meta['author'].name, prog_str))
            else:
                lines.append("Now Playing: **%s** %s\n" % (self.player.current_entry.title, prog_str))

        for i, item in enumerate(self.player.playlist, 1):
            if item.meta.get('channel', False) and item.meta.get('author', False):
                nextline = '`{}.` **{}** added by **{}**'.format(i, item.title, item.meta['author'].name).strip()
            else:
                nextline = '`{}.` **{}**'.format(i, item.title).strip()

            currentlinesum = sum(len(x) + 1 for x in lines)  # +1 is for newline char

            if currentlinesum + len(nextline) + len(andmoretext) > DISCORD_MSG_CHAR_LIMIT:
                if currentlinesum + len(andmoretext):
                    unlisted += 1
                    continue

            lines.append(nextline)

        if unlisted:
            lines.append('\n*... and %s more*' % unlisted)

        if not lines:
            lines.append(
                'There are no songs queued! Queue something with {}play.'.format(self.config.command_prefix))

        message = '\n'.join(lines)
        await self.bot.safe_send_message(
            self.message.channel,
            message,
            expire_in=30 if bot.config.delete_messages else 0,
            also_delete=message if bot.config.delete_invoking else None
        )
