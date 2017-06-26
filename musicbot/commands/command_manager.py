import importlib.util

from .command import Command

commands = []

# All commands to load, only used in super Command class
toload = ['Link', 'SetAvatar', 'SetNick', 'SetName', 'JoinServer', 'Help', 'Play', 'Search', 'Queue', 'Clean',
    'Clear', 'Blacklist', 'Restart', 'Disconnect', 'Shutdown', 'Skip', 'NowPlaying', 'Pause', 'Resume', 'Shuffle',
    'ListIds', 'Summon', 'Volume', 'Pldump', 'Perms', 'Id']

def register_command(command):
    """
    Register a new command

    Keyword arguments:
    command -- The command class to register
    """

    for _command in commands:
        if _command.trigger == command.trigger:
            print("ERROR: Command %s and %s have the same trigger. Disregarding the first." % (command.get_class_name(), _command.get_class_name()))
        elif set(_command.aliases) & set(command.aliases):
            print("ERROR: Command %s and %s have (partially) the same aliases. Disregarding the first" % (command.get_class_name(), _command.get_class_name()))

    # Register command
    #print("Registered command %s" % command.__class__.__name__)
    commands.append(command)

def register_all_commands():

    commands = []

    # Loop through all command names to load them
    for commandName in toload:

        # Get spec from file location
        spec = importlib.util.spec_from_file_location(commandName + 'Command', 'musicbot/commands/' + commandName.lower() + '.py')

        # Get module from spec, module is the file.py itself
        module = importlib.util.module_from_spec(spec)

        # I think this imports the file so that we can use it
        spec.loader.exec_module(module)

        commandClass = None

        # For all names that are within the module
        for name in dir(module):
            # Get the object corresponding with that name
            obj = getattr(module, name)
            try:
                # It has to be the class itself, so a subclass of Command,
                # but not Command itself, otherwise we get the Command class
                # instead of NameCommand
                if issubclass(obj, Command) and not obj == Command:
                    commandClass = obj
                    break
            except TypeError:
                pass

        # This is the class within the module, that we can now register
        register_command(commandClass)

def has_command(command_string):
    """
    Checks if the command specified by the command_string exists

    Keyword argumetns:
    command_string -- Either the trigger or an alias of the command the user
                      tries to trigger
    """
    return get_command(command_string)

def get_command(command_string):
    """
    Returns the actual command specified by the command_string

    Keyword arguments:
    command_string -- Either the trigger or an alias of the command the user
                      tries to trigger
    """

    # Since we are dealing with classes,
    # we return the class to the method caller
    for command in commands:
        if command.trigger == command_string:
            return command
        elif command_string in command.aliases:
            return command
    return None
