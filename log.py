import logging

import time
import csv

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
        timestamp = int(time.time())
        _log.info("Comment by %r in %s at %r: %r", actor, recipient, timestamp, message)

        with open('chatlog.csv', 'ab') as csvfile:
          logwriter = csv.writer(csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
          logwriter.writerow([timestamp, recipient, actor, message])

        return False

# Let KitnIRC know what module class it should be loading.
module = LogModule

# vim: set ts=4 sts=4 sw=4 et:
