from .command import Command

class HelpCommand(Command):
    """docstring for HelpCommand."""
    def __init__(self):
        super().__init__()
        self.trigger = 'help'
        self.aliases = ['hulp']

    def run(self):
        print('help ' + self.message)
