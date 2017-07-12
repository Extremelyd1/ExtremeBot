import discord
from io import BytesIO
from musicbot.commands.command import Command
from musicbot import exceptions

class ListIdsCommand(Command):
    """
    Usage:
        {command_prefix}listids [categories]
    Lists the ids for various things.  Categories are:
       all, users, roles, channels
    """

    trigger = 'listids'
    aliases = []

    def __init__(self):
        super().__init__()

    async def run(self):

        cats = ['channels', 'roles', 'users']

        if not len(self.leftover_args) in [0, 1]:
            await self.bot.safe_send_message_check(
                self.channel,
                ('%s, Valid categories: ' % self.author.mention) + ' '.join(['`%s`' % c for c in cats]),
                expire_in=25,
                also_delete=self.message
            )
            return

        cat = 'all'

        if len(self.leftover_args) == 1:
            cat = self.leftover_args.pop(0)

        if cat not in cats and cat != 'all':
            await self.bot.safe_send_message_check(
                self.channel,
                ('%s, Valid categories: ' % self.author.mention) + ' '.join(['`%s`' % c for c in cats]),
                expire_in=25,
                also_delete=self.message
            )
            return

        if cat == 'all':
            requested_cats = cats
        else:
            requested_cats = [cat] + [c.strip(',') for c in self.leftover_args]

        data = ['Your ID: %s' % self.author.id]

        for cur_cat in requested_cats:
            rawudata = None

            if cur_cat == 'users':
                data.append("\nUser IDs:")
                rawudata = ['%s #%s: %s' % (m.name, m.discriminator, m.id) for m in self.server.members]

            elif cur_cat == 'roles':
                data.append("\nRole IDs:")
                rawudata = ['%s: %s' % (r.name, r.id) for r in self.server.roles]

            elif cur_cat == 'channels':
                data.append("\nText Channel IDs:")
                tchans = [c for c in self.server.channels if c.type == discord.ChannelType.text]
                rawudata = ['%s: %s' % (c.name, c.id) for c in tchans]

                rawudata.append("\nVoice Channel IDs:")
                vchans = [c for c in self.server.channels if c.type == discord.ChannelType.voice]
                rawudata.extend('%s: %s' % (c.name, c.id) for c in vchans)

            if rawudata:
                data.extend(rawudata)

        with BytesIO() as sdata:
            sdata.writelines(d.encode('utf8') + b'\n' for d in data)
            sdata.seek(0)

            # TODO: Fix naming (Discord20API-ids.txt)
            await self.bot.send_file(self.author, sdata, filename='%s-ids-%s.txt' % (self.server.name.replace(' ', '_'), cat))

        await self.bot.safe_send_message_check(
            self.channel,
            ':mailbox_with_mail:',
            expire_in=20,
            also_delete=self.message
        )
