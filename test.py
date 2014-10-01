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
    def add_command(self, client, command, event, helptext="Hjelpetekst"):
        self.trigger_event("ADDCOMMAND", client, [command, event, helptext])

    def remove_command(self, client, command, event):
        self.trigger_event("REMOVECOMMAND", client, [command, event])

    @Module.handle("COMMANDS")
    def register_commands(self, client, *args):
        _log.info("Registering commands...")
        self.add_command(client, "topic", "TOPIC")

    def unregister_commands(self, client):
        self.remove_command(client, "topic", "TOPIC")

    def start(self, *args, **kwargs):
        super(TestModule, self).start(*args, **kwargs)
        self.register_commands(self.controller.client)

    def stop(self, *args, **kwargs):
        super(TestModule, self).stop(*args, **kwargs)
        self.unregister_commands(self.controller.client)

    @Module.handle("TOPIC")
    def bananas(self, client, actor, recipient, *args):
        client.reply(recipient, actor, "Topic og drit")
        return True


# Let KitnIRC know what module class it should be loading.
module = TestModule

# vim: set ts=4 sts=4 sw=4 et: