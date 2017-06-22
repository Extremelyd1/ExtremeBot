import asyncio
from random import shuffle
from musicbot.commands.command import Command

class ShuffleCommand(Command):
    """docstring for ShuffleCommand."""

    trigger = 'shuffle'
    aliases = []

    def __init__(self):
        super().__init__()

    async def run(self):
        self.player.playlist.shuffle()

        cards = [':spades:',':clubs:',':hearts:',':diamonds:']
        hand = await self.bot.send_message(self.channel, ' '.join(cards))
        await asyncio.sleep(0.6)

        for x in range(4):
            shuffle(cards)
            await self.bot.safe_edit_message(hand, ' '.join(cards))
            await asyncio.sleep(0.6)

        await self.bot.safe_delete_message(hand, quiet=True)
        await self.bot.safe_send_message(
            self.channel,
            ':ok_hand:',
            expire_in=15,
            also_delete=self.message
        )
