from musicbot.commands.command import Command
from musicbot.utils import sane_round_int
from musicbot import exceptions

class SkipCommand(Command):
    """
    Usage:
        {command_prefix}skip
    Skips the current song when enough votes are cast, or by the bot owner.
    """

    trigger = 'skip'
    aliases = []

    def __init__(self):
        super().__init__()

    async def run(self):
        if self.player.is_stopped:
            raise exceptions.CommandError("Can't skip! The player is not playing!", expire_in=20)

        if not self.player.current_entry:
            if self.player.playlist.peek():
                if self.player.playlist.peek()._is_downloading:
                    # print(player.playlist.peek()._waiting_futures[0].__dict__)
                    await self.bot.safe_send_message(
                        self.channel,
                        'The next song (%s) is downloading, please wait.' % self.player.playlist.peek().title, expire_in=20,
                        also_delete=self.message
                    )
                    return

                elif self.player.playlist.peek().is_downloaded:
                    print("The next song will be played shortly.  Please wait.")
                else:
                    print("Something odd is happening.  "
                          "You might want to restart the bot if it doesn't start working.")
            else:
                print("Something strange is happening.  "
                      "You might want to restart the bot if it doesn't start working.")

        if self.author.id == self.bot.config.owner_id \
                or self.permissions.instaskip \
                or self.author == self.player.current_entry.meta.get('author', None):

            self.player.skip()  # check autopause stuff here
            await self.bot._manual_delete_check(self.message)
            return

        # TODO: ignore person if they're deaf or take them out of the list or something?
        # Currently is recounted if they vote, deafen, then vote

        num_voice = sum(1 for m in self.voice_channel.voice_members if not (
            m.deaf or m.self_deaf or m.id in [self.bot.config.owner_id, self.bot.user.id]))

        num_skips = self.player.skip_state.add_skipper(self.author.id, self.message)

        skips_remaining = min(self.bot.config.skips_required,
                              sane_round_int(num_voice * self.bot.config.skip_ratio_required)) - num_skips

        if skips_remaining <= 0:
            self.player.skip()  # check autopause stuff here
            await self.bot.safe_send_message(
                self.channel,
                '{}, your skip for **{}** was acknowledged.'
                '\nThe vote to skip has been passed.{}'.format(
                    self.author.mention,
                    self.player.current_entry.title,
                    ' Next song coming up!' if self.player.playlist.peek() else ''
                ),
                expire_in=20,
                also_delete=self.message
            )

        else:
            # TODO: When a song gets skipped, delete the old x needed to skip messages
            await self.bot.safe_send_message(
                self.channel,
                '{}, your skip for **{}** was acknowledged.'
                '\n**{}** more {} required to vote to skip this song.'.format(
                    self.author.mention,
                    self.player.current_entry.title,
                    skips_remaining,
                    'person is' if skips_remaining == 1 else 'people are'
                ),
                expire_in=20,
                also_delete=self.message
            )
