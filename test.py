import logging

from kitnirc.client import Channel
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
    @Module.handle("PRIVSMG")
    def respond(self, client, actor, recipient, message):
        _log.info("recipient is: %s", recipient)
        actor = User(actor)
        if ininstance(recipient, Channel):
            self.reply_to = recipient
        else:
            self.reply_to = actor
        _log.info("Actor is: %s", actor)
        message = message.strip()
        args = message.split(" ")
        command = args[0]
        _log.info("Command: %r - Args: %r", command, args)
        
        if len(args) >= 2:
            args = args[1:]
            if command == '!test':
                self.controller.client.msg(recipient, "Fin test!")


# Let KitnIRC know what module class it should be loading.
module = TestModule

# vim: set ts=4 sts=4 sw=4 et: