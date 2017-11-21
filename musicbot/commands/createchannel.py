import asyncio
import discord

from discord import utils
from musicbot import exceptions
from musicbot.commands.command import Command

class CreateChannel(Command):
    """
    Usage:
        {command_prefix}createchannel [size] <@person1> <@person2> ...
    Creates a voice channel with capacity [size] and join permission for you and whoever you mention.
    """

    trigger = 'createchannel'
    aliases = ['cc', 'private']
    owner_only = True

    channels = []

    def __init__(self):
        super().__init__()

    async def run(self):

        user_limit = None
        force = False

        if (len(self.leftover_args) > 0):
            try :
                user_limit = int(self.leftover_args[0])
            except ValueError:
                pass
            if ('-f' in self.leftover_args or '-force' in self.leftover_args):
                if not self.author.id == self.bot.config.owner_id:
                    raise exceptions.PermissionsError("Only the owner can use this command", expire_in=30)
                else:
                    force = True

        deny_perms = discord.PermissionOverwrite(connect=False)
        allow_perms = discord.PermissionOverwrite(connect=True)

        channel = await self.bot.create_channel(self.server, 'Private {}'.format(len(self.bot.channels) + 1), (self.server.default_role, deny_perms), (self.author, allow_perms), type=discord.ChannelType.voice) # TODO: Add permissions based on mentions

        if (user_limit):
            await self.bot.edit_channel(channel, user_limit=user_limit);

        if (self.user_mentions):
            for user in self.user_mentions:
                await self.bot.edit_channel_permissions(channel, discord.utils.find(lambda m : m.id == user.id, self.server.members), allow_perms)
                if force:
                    await self.bot.move_member(discord.utils.find(lambda m : m.id == user.id, self.server.members), channel)

        await self.bot.move_channel(channel, 1)

        self.bot.channels.append(channel.id)

        asyncio.ensure_future(self.bot._wait_delete_channel(channel.id, channel.server, 30))

        await self.bot.safe_delete_message(self.message, quiet=True)

        await self.bot.safe_send_message_check(
            self.channel,
            'Created voice channel "%s"' % (channel.name), # TODO: Format with number of channel
            expire_in=15
        )
