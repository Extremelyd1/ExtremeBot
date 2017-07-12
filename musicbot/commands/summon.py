from musicbot.commands.command import Command
from musicbot import exceptions

class SummonCommand(Command):
    """
    Usage:
        {command_prefix}summon
    Call the bot to the summoner's voice channel.
    """

    trigger = 'summon'
    aliases = []

    def __init__(self):
        super().__init__()

    async def run(self):
        if not self.author.voice_channel:
            raise exceptions.CommandError('You are not in a voice channel!')

        voice_client = self.bot.the_voice_clients.get(self.channel.server.id, None)
        if voice_client and voice_client.channel.server == self.author.voice_channel.server:
            await self.bot.move_voice_client(self.author.voice_channel)
            return

        # move to _verify_vc_perms?
        chperms = self.author.voice_channel.permissions_for(self.author.voice_channel.server.me)

        if not chperms.connect:
            self.bot.safe_print("Cannot join channel \"%s\", no permission." % self.author.voice_channel.name)
            await self.bot.safe_send_message_check(
                self.channel,
                '```Cannot join channel \"%s\", no permission.```' % self.author.voice_channel.name,
                expire_in=25,
                also_delete=self.message
            )
            return

        elif not chperms.speak:
            self.bot.safe_print("Will not join channel \"%s\", no permission to speak." % self.author.voice_channel.name)
            await self.bot.safe_send_message_check(
                self.channel,
                '```Cannot join channel \"%s\", no permission to speak.```' % self.author.voice_channel.name,
                expire_in=25,
                also_delete=self.message
            )
            return

        player = await self.bot.get_player(self.author.voice_channel, create=True)

        if player.is_stopped:
            player.play()

        if self.bot.config.auto_playlist:
            await self.bot.on_player_finished_playing(player)

        return
