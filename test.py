import logging

from kitnirc.client import Channel, User
from kitnirc.modular import Module


# This is the standard way to get a logger for your module
# via the Python logging library.
_log = logging.getLogger(__name__)


# KitnIRC modules always subclass kitnirc.modular.Module
class TestModule(Module):
    """A basic KitnIRC module which responds to messages."""

    # This decorator tells KitnIRC what events to route to the
    # function it decorates. The name of the function itself
    # doesn't matter - call it what makes sense.
    @Module.handle("PRIVMSG")
    def respond(self, client, actor, recipient, message):
        if isinstance(recipient, Channel):
            # Only pay attention if addressed directly in channels
            if not message.startswith("!"):
                return
        else:
            if not message.startswith("!"):
                return

        message = message.strip()
        args = message.split(" ")

        _log.info("Got command: %r - Argument: %r", args[0], args[1])

        client.reply(recipient, actor, "Fin kommando! Kommandoen var '%r' og argumentet var '%r'.", args[0], args[1])

        return True


# Let KitnIRC know what module class it should be loading.
module = TestModule

# vim: set ts=4 sts=4 sw=4 et:
