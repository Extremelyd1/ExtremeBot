from datetime import timedelta
from musicbot.commands.command import Command

class NowPlayingCommand(Command):
    """
    Usage:
        {command_prefix}np
    Displays the current song in chat.
    """

    trigger = 'np'
    aliases = ['nowplaying']

    def __init__(self):
        super().__init__()

    async def run(self):
        if self.player.current_entry:
            last_np_embed = self.bot.server_specific_data[self.server]['last_np_embed']

            song_progress = str(timedelta(seconds=self.player.progress)).lstrip('0').lstrip(':')
            song_total = str(timedelta(seconds=self.player.current_entry.duration)).lstrip('0').lstrip(':')
            prog_str = '`[%s/%s]`' % (song_progress, song_total)

            if self.player.current_entry.meta.get('channel', False) and self.player.current_entry.meta.get('author', False):
                author = self.player.current_entry.meta.get('author', False)
                last_np_embed.set_footer(text='Requested by %s' % author.name, icon_url=author.avatar_url)
            else:
                last_np_embed.set_footer()

            last_np_embed.set_field_at(1, name='Status', value='Playing %s' % prog_str)

            await self.bot._manual_delete_check(self.message)

            last_np_msg = self.bot.server_specific_data[self.server]['last_np_msg']

            if last_np_msg:
                self.bot.server_specific_data[self.server]['last_np_msg'] = await self.bot.safe_edit_message(last_np_msg, new_content='Current song:', embed=last_np_embed)
            else:
                self.bot.server_specific_data[self.server]['last_np_msg'] = await self.bot.safe_send_message(self.channel, content='Current song:', embed=last_np_embed)

            self.bot.server_specific_data[self.server]['last_np_embed'] = last_np_embed
        else:
            await self.bot.safe_send_message_check(
                self.channel,
                'There are no songs queued! Queue something with {}play.'.format(self.bot.config.command_prefix),
                expire_in=30,
                also_delete=self.message
            )
