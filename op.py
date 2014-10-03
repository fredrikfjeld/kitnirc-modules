import logging

from kitnirc.client import Channel, User
from kitnirc.modular import Module


# This is the standard way to get a logger for your module
# via the Python logging library.
_log = logging.getLogger(__name__)


# KitnIRC modules always subclass kitnirc.modular.Module
class OpModule(Module):
    """A basic KitnIRC module which responds to messages."""

    # This decorator tells KitnIRC what events to route to the
    # function it decorates. The name of the function itself
    # doesn't matter - call it what makes sense.
    @Module.handle("PRIVMSG")
    def respond(self, client, actor, recipient, message):
        # Only pay attention if command starts with "!"
        if not message.startswith("!"):
            return

        message = message.strip()
        args = message.split(" ")

        if len(args) == 2:
          command = args[0]
          argument = args[1]

          #_log.info("Got command: %r - Argument: %r", args[0], args[1])
          _log.info("%s wants to give %s OP in %s." % actor, argument, recipient)
          #client.reply(recipient, actor, "Fin kommando! Kommandoen var %r og argumentet var %r." % (args[0], args[1]))

          return True

        elif len(args) == 1:
          command = args[0]

          _log.info("%s wants to be OP in %s." % (actor, recipient))

          return True

        else:
          _log.error("That's not right.")
          return True


# Let KitnIRC know what module class it should be loading.
module = OpModule

# vim: set ts=4 sts=4 sw=4 et:
