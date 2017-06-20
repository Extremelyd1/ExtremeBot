class Command:

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
