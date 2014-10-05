import logging

from kitnirc.client import Channel, User
from kitnirc.modular import Module
from kitnirc.contrib.admintools import is_admin

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
        self.add_command(client, "topic", "TOPIC", "Set topic!")

    def unregister_commands(self, client):
        _log.info("Unregistering commands...")
        self.remove_command(client, "op", "OP")
        self.remove_command(client, "topic", "TOPIC")

    def start(self, *args, **kwargs):
        self.register_commands(self.controller.client)

    def stop(self, *args, **kwargs):
        self.unregister_commands(self.controller.client)

    @Module.handle('OP')
    def op(self, client, actor, recipient, *args):
        _log.error("op-kommando")
        actor = User(actor)
        if not is_admin(self.controller, client, actor):
          _log.info("Unauthorized OP request by %s" % actor)
          client.reply(recipient, actor, "Du er ikke definert som en admin. Din snik.")
          return True

        if isinstance(recipient, Channel):
            self.reply_to = recipient
        else:
            self.reply_to = actor

        if len(args) == 0:
          # Gi OP til den som sendte kommandoen
          client.mode(recipient, add={'o': [actor.nick]})
          _log.info("OP given to %s" % actor)
          client.emote(recipient, "gave OP.")

        elif len(args) == 1:
          # Gi OP til nicket som kommer etter op-kommandoen
          client.mode(recipient, add={'o': [args[0]]})
          _log.info("OP given to %s by %s" % (args[0], actor))
          client.reply(recipient, actor, "Wish granted.")

        elif len(args) > 1:
          # Gi OP til nickene som kommer etter op-kommandoen
          for item in args:
            client.mode(recipient, add={'o': [item]})
            _log.info("OP given to %s by %s" % (item, actor))
          client.reply(recipient, actor, "Wishes granted.")

        else:
          client.reply(recipient, actor, "Neineinei, dette var bare tull.")

    @Module.handle('TOPIC')
    def topic(self, client, actor, recipient, *args):
        actor = User(actor)
        if not is_admin(self.controller, client, actor):
          _log.info("Unauthorized TOPIC attempt by %s" % actor)
          client.reply(recipient, actor, "Du er ikke definert som en admin. Din snik.")
          return True

        if isinstance(recipient, Channel):
            self.reply_to = recipient
        else:
            self.reply_to = actor

        topicString = " ".join(args)

        # Sett TOPIC
        client.topic(recipient, topicString)
        _log.info("TOPIC set to %s by %s" % (topicString, actor))

        # else:
        #   # Hvis feil antall argumenter
        #   _log.info("%s needs some help using the TOPIC-command" % actor)
        #   client.reply(recipient, actor, "No, that's not how you do it.")

# Let KitnIRC know what module class it should be loading.
module = OpModule

# vim: set ts=4 sts=4 sw=4 et:
