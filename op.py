import logging

from kitnirc.client import Channel, User
from kitnirc.modular import Module


# This is the standard way to get a logger for your module
# via the Python logging library.
_log = logging.getLogger(__name__)


# KitnIRC modules always subclass kitnirc.modular.Module
class OpModule(Module):
    """A basic KitnIRC module which responds to messages."""

    def add_command(self, client, command, event, helptext=None):
        self.trigger_event("ADDCOMMAND", client, [command, event, helptext])

    def remove_command(self, client, command, event):
        self.trigger_event("REMOVECOMMAND", client, [command, event])

    @Module.handle("COMMANDS")
    def register_commands(self, client, *args):
        _log.info("Registering commands...")
        self.add_command(client, "op", "OPUSER", "Give OP to user or self.")

    def unregister_commands(self, client):
        self.remove_command(client, "op", "OPUSER")

    def start(self, *args, **kwargs):
        self.register_commands(self.controller.client)

    def stop(self, *args, **kwargs):
        self.unregister_commands(self.controller.client)

    @Module.handle('OPUSER')
    def marketquote(self, client, actor, recipient, *args):
        actor = User(actor)
        if isinstance(recipient, Channel):
            self.reply_to = recipient
        else:
            self.reply_to = actor
        typeName = " ".join(args)

        _log.info("%s wants to give OP in %s." % actor, recipient)
        self.controller.client.msg(recipient, "takk %s, fin test." % actor)

    # def respond(self, client, actor, recipient, message):
    #
    #       #_log.info("Got command: %r - Argument: %r", args[0], args[1])
    #       _log.info("%s wants to give %s OP in %s." % actor, argument, recipient)
    #       #client.reply(recipient, actor, "Fin kommando! Kommandoen var %r og argumentet var %r." % (args[0], args[1]))
    #
    #       return True
    #
    #     elif len(args) == 1:
    #       command = args[0]
    #
    #       _log.info("%s wants to be OP in %s." % (actor, recipient))
    #
    #       return True
    #
    #     else:
    #       _log.error("That's not right.")
    #       return True


# Let KitnIRC know what module class it should be loading.
module = OpModule

# vim: set ts=4 sts=4 sw=4 et:
