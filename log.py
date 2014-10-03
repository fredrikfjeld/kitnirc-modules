import logging

from kitnirc.client import Channel, User
from kitnirc.modular import Module
from kitnirc.contrib.admintools import is_admin

# This is the standard way to get a logger for your module
# via the Python logging library.

_log = logging.getLogger(__name__)

# KitnIRC modules always subclass kitnirc.modular.Module
class LogModule(Module):
    """A basic KitnIRC module which logs messages."""

    @Module.handle("PRIVMSG")
    def respond(self, client, actor, recipient, message):
        message = message.strip()
        _log.info("Comment by %r in %r: %r", actor, client.Channel, message)

# Let KitnIRC know what module class it should be loading.
module = LogModule

# vim: set ts=4 sts=4 sw=4 et:
