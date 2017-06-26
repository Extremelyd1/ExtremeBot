class Command:
    """
    The super Command class. All commands should extend this class.
    It contains all information needed for the command.
    """

    owner_only = False

    def __init__(self):

        # Properties every command can access
        self.bot = None
        self.message = None
        self.channel = None
        self.author = None
        self.server = None
        self.player = None
        self.permissions = None
        self.user_mentions = None
        self.channel_mentions = None
        self.voice_channel = None

        # Leftover arguments
        self.leftover_args = None

    async def run(self):
        """
        Run the command when either the trigger, or one of the aliases was used
        to call the command.
        """
        print("Something went wrong, the super Command.run() method was executed")

    @classmethod
    def get_class_name(cls):
        return cls.__name__
