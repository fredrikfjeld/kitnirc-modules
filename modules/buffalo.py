import logging

from kitnirc.modular import Module


_log = logging.getLogger(__name__)


class BuffaloModule(Module):
    """A basic KitnIRC module which registers commands."""

    def add_command(self, client, command, event, helptext=None):
        self.trigger_event("ADDCOMMAND", client, [command, event, helptext])

    def remove_command(self, client, command, event):
        self.trigger_event("REMOVECOMMAND", client, [command, event])

    @Module.handle("COMMANDS")
    def register_commands(self, client, *args):
        _log.info("Registering commands...")
        self.add_command(client, "buffalo", "BUFFALO", "Buffalo!")

    def unregister_commands(self, client):
        self.remove_command(client, "buffalo", "BUFFALO")

    def start(self, *args, **kwargs):
        super(BuffaloModule, self).start(*args, **kwargs)
        self.register_commands(self.controller.client)

    def stop(self, *args, **kwargs):
        super(BuffaloModule, self).stop(*args, **kwargs)
        self.unregister_commands(self.controller.client)

    @Module.handle("BUFFALO")
    def buffalo(self, client, actor, recipient, *args):
        client.reply(recipient, actor, "Buffalo buffalo Buffalo buffalo buffalo buffalo Buffalo buffalo.")
        return True


module = BuffaloModule

# vim: set ts=4 sts=4 sw=4 et:
