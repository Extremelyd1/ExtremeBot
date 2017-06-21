class Command:
    """
    The super Command class. All commands should extend this class. It provided
    functionality to register commands, check if commands exist and get the actual
    commands. It contains all information needed for the command, as well as a
    list of all available commands.
    """

    commands = []

    def __init__(self):
        self.trigger = None
        self.aliases = []
        self.bot = None
        self.message = None
        self.channel = None
        self.auther = None
        self.server = None
        self.player = None
        self.permissions = None
        self.user_mentions = None
        self.channel_mentions = None
        self.voice_channel = None
        self.leftover_args = None

    async def run(self):
        """
        Run the command when either the trigger, or one of the aliases was used
        to call the command.
        """
        print("Something went wrong, the super Command.run() method was executed")

    @staticmethod
    def register_command(command):
        """
        Register a new command

        Keyword arguments:
        command -- The command to register
        """
        # Check if trigger and aliases are unique
        for _command in Command.commands:
            if _command.trigger == command.trigger:
                print("ERROR: Command %s and %s have the same trigger. Disregarding the first." % command.__class__.__name__, _command.__class__.__name__)
            elif set(_command.aliases) & set(command.aliases):
                print("ERROR: Command %s and %s have (partially) the same aliases. Disregarding the first" % command.__class__.__name__, _command.__class__.__name__)

        # Register command
        print("Registered command %s" % command.__class__.__name__)
        Command.commands.append(command)

    @staticmethod
    def has_command(command_string):
        """
        Checks if the command specified by the command_string exists

        Keyword argumetns:
        command_string -- Either the trigger or an alias of the command the user
                          tries to trigger
        """
        return Command.get_command(command_string)

    @staticmethod
    def get_command(command_string):
        """
        Returns the actual command specified by the command_string

        Keyword arguments:
        command_string -- Either the trigger or an alias of the command the user
                          tries to trigger
        """
        for command in Command.commands:
            if command.trigger == command_string:
                return command
            elif command_string in command.aliases:
                return command
        return None
