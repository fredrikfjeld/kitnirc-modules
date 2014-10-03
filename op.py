import logging

from kitnirc.client import Channel, User
from kitnirc.modular import Module
import sys


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
        self.add_command(client, "op", "OP", "OP someone!")

    def unregister_commands(self, client):
        self.remove_command(client, "op", "OP")

    def start(self, *args, **kwargs):
        self.register_commands(self.controller.client)

    def stop(self, *args, **kwargs):
        self.unregister_commands(self.controller.client)

    @Module.handle('OP')
    def op(self, client, actor, recipient, *args):
        actor = User(actor)
        if isinstance(recipient, Channel):
            self.reply_to = recipient
        else:
            self.reply_to = actor

        client.reply(recipient, actor, "Op til deg! Op til deg! Op til ALLE SAMMEN!")

        _log.info("OP requested by %s" % actor)


# Let KitnIRC know what module class it should be loading.
module = OpModule

# vim: set ts=4 sts=4 sw=4 et:
