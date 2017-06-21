from musicbot.commands.command import Command
from musicbot import exceptions

class VolumeCommand(Command):
    """docstring for VolumeCommand."""
    def __init__(self):
        super().__init__()
        self.trigger = 'volume'
        self.aliases = ['vol']

    async def run(self):

        if len(self.leftover_args) == 0:
            await self.bot.safe_send_message(
                self.channel,
                '%s, Current volume: `%s%%`' % (self.author.mention, int(self.player.volume * 100)),
                expire_in=20,
                also_delete=self.message
            )
            return

        if not len(self.leftover_args) == 1:
            #TODO: display help associated with this command
            return

        new_volume = self.leftover_args[0]

        relative = False
        if new_volume[0] in '+-':
            relative = True

        try:
            new_volume = int(new_volume)

        except ValueError:
            raise exceptions.CommandError('{} is not a valid number'.format(new_volume), expire_in=20)

        if relative:
            vol_change = new_volume
            new_volume += (self.player.volume * 100)

        old_volume = int(self.player.volume * 100)

        if 0 < new_volume <= 100:
            self.player.volume = new_volume / 100.0

            await self.bot.safe_send_message(
                self.channel,
                '%s, updated volume from %d to %d' % (self.author.mention, old_volume, new_volume),
                expire_in=20,
                also_delete=self.message
            )

        else:
            if relative:
                raise exceptions.CommandError(
                    'Unreasonable volume change provided: {}{:+} -> {}%.  Provide a change between {} and {:+}.'.format(
                        old_volume, vol_change, old_volume + vol_change, 1 - old_volume, 100 - old_volume), expire_in=20)
            else:
                raise exceptions.CommandError(
                    'Unreasonable volume provided: {}%. Provide a value between 1 and 100.'.format(new_volume), expire_in=20)
