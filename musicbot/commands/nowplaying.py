from datetime import timedelta
from musicbot.commands.command import Command

class NowPlayingCommand(Command):
    """docstring for NowPlayingCommand."""
    def __init__(self):
        super().__init__()
        self.trigger = 'np'
        self.aliases = ['nowplaying']

    async def run(self):
        if self.player.current_entry:
            if self.bot.server_specific_data[self.server]['last_np_msg']:
                await self.bot.safe_delete_message(self.bot.server_specific_data[self.server]['last_np_msg'])
                self.bot.server_specific_data[self.server]['last_np_msg'] = None

            song_progress = str(timedelta(seconds=self.player.progress)).lstrip('0').lstrip(':')
            song_total = str(timedelta(seconds=self.player.current_entry.duration)).lstrip('0').lstrip(':')
            prog_str = '`[%s/%s]`' % (song_progress, song_total)

            if self.player.current_entry.meta.get('channel', False) and self.player.current_entry.meta.get('author', False):
                np_text = "Now Playing: **%s** added by **%s** %s\n" % (
                    self.player.current_entry.title, self.player.current_entry.meta['author'].name, prog_str)
            else:
                np_text = "Now Playing: **%s** %s\n" % (self.player.current_entry.title, prog_str)

            self.bot.server_specific_data[self.server]['last_np_msg'] = await self.bot.safe_send_message(self.channel, np_text)
            await self.bot._manual_delete_check(self.message)
        else:
            await self.bot.safe_send_message(
                self.channel,
                'There are no songs queued! Queue something with {}play.'.format(self.bot.config.command_prefix),
                expire_in=30,
                also_delete=self.message
            )
