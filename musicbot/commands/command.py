class Command:

    commands = []

    def __init__(self):
        self.trigger = None
        self.aliases = []
        self.bot = None
        self.message = None
        self.player = None
        self.permissions = None
        self.user_mentions = None
        self.channel_mentions = None
        self.voice_channel = None
        self.leftover_args = None

    async def run(self):
        print("Something went wrong")

    @staticmethod
    def register_command(command):
        # TODO: perform checks on trigger and aliases
        Command.commands.append(command)

    @staticmethod
    def has_command(command_string):
        return Command.get_command(command_string)

    @staticmethod
    def get_command(command_string):
        for command in Command.commands:
            if command.trigger == command_string:
                return command
            elif command_string in command.aliases:
                return command
        return None
