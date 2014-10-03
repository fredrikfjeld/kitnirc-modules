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

    def is_admin(controller, client, actor):
    """Used to determine whether someone issuing a command is an admin.

    By default, checks to see if there's a line of the type nick=host that
    matches the command's actor in the [admins] section of the config file,
    or a key that matches the entire mask (e.g. "foo@bar" or "foo@bar=1").
    """
    config = controller.config
    if not config.has_section("admins"):
        logging.debug("Ignoring is_admin check - no [admins] config found.")
        return False
    for key,val in config.items("admins"):
        if actor == User(key):
            logging.debug("is_admin: %r matches admin %r", actor, key)
            return True
        if actor.nick.lower() == key.lower() and actor.host.lower() == val.lower():
            logging.debug("is_admin: %r matches admin %r=%r", actor, key, val)
            return True
    logging.debug("is_admin: %r is not an admin.", actor)
    return False

    @Module.handle('OP')
    def op(self, client, actor, recipient, *args):
        actor = User(actor)
        if not is_admin(self.controller, client, actor):
            client.reply(recipient, actor, "Din snik.")
            return

        if isinstance(recipient, Channel):
            self.reply_to = recipient
        else:
            self.reply_to = actor

        if len(args) == 1:
          client.reply(recipient, actor, "Ett argument: %s" % args[0])
        elif len(args) == 2:
          client.reply(recipient, actor, "To argumenter: %r og %r" % (args[0], args[1]))
        else:
          client.reply(recipient, actor, "Op til deg! Op til deg! Op til ALLE SAMMEN!")

        _log.info("OP requested by %s" % actor)


# Let KitnIRC know what module class it should be loading.
module = OpModule

# vim: set ts=4 sts=4 sw=4 et:
