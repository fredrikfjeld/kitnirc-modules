import logging

import csv
import time
from random import randint

from kitnirc.client import Channel, User
from kitnirc.modular import Module
from kitnirc.contrib.admintools import is_admin

# This is the standard way to get a logger for your module
# via the Python logging library.

_log = logging.getLogger(__name__)

# KitnIRC modules always subclass kitnirc.modular.Module
class D20Module(Module):
    """A basic KitnIRC module which responds to messages."""

    def add_command(self, client, command, event, helptext=None):
        self.trigger_event("ADDCOMMAND", client, [command, event, helptext])

    def remove_command(self, client, command, event):
        self.trigger_event("REMOVECOMMAND", client, [command, event])

    @Module.handle("COMMANDS")
    def register_commands(self, client, *args):
        _log.info("Registering commands...")
        self.add_command(client, "d20", "THROWDICE", "Throw the dice!")
        self.add_command(client, "winstats", "WINNERS", "Show highscores.")
        self.add_command(client, "failstats", "LOSERS", "Show most fails.")

    def unregister_commands(self, client):
        _log.info("Unregistering commands...")
        self.remove_command(client, "d20", "THROWDICE")
        self.remove_command(client, "winstats", "WINNERS")
        self.remove_command(client, "failstats", "LOSERS")


    def start(self, *args, **kwargs):
        self.register_commands(self.controller.client)

    def stop(self, *args, **kwargs):
        self.unregister_commands(self.controller.client)

    @Module.handle('THROWDICE')
    def dice(self, client, actor, recipient, *args):
        actor = User(actor)
        timestamp = int(time.time())

        if isinstance(recipient, Channel):
            self.reply_to = recipient
        else:
            self.reply_to = actor

        if len(args) == 0:
            _log.info("Throwing dice for %s" % actor)
            # TODO: More randomness
            diceresult = randint(1,20)

            client.emote(recipient, "%s throws d20... %r" % (actor.nick, diceresult))

            if diceresult == 20:
                client.mode(recipient, add={'v': [actor.nick]})

                with open('winstats.csv', 'a+') as csvfile:
                    logwriter = csv.writer(csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                    logwriter.writerow([timestamp, recipient, actor.nick, "win"])

                client.reply(recipient, actor, "Yay! :)")

            elif diceresult == 1:

                with open('winstats.csv', 'a+') as csvfile:
                    logwriter = csv.writer(csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                    logwriter.writerow([timestamp, recipient, actor.nick, "fail"])
                client.reply(recipient, actor, "TODO: Kick :)")

        else:
            client.reply(recipient, actor, "Denne kommandoen tar ingen argumenter.")

    @Module.handle('WINNERS')
    def winners(self, client, actor, recipient, *args):
        actor = User(actor)
        with open('winstats.csv', 'rb') as csvfile:
            reader = csv.reader(csvfile,delimiter=';')
            rownum = 0
            winners = {}
            for row in reader:
                colnum = 0
                for col in row:
                    _log.info("Col number %r" % colnum)
                    if colnum == 2:
                        nick = col
                    elif colnum == 3:
                        if col == "win":
                            if nick in winners:
                                winners[nick] += 1
                            else:
                                winners[nick] = 1

                    colnum += 1

                rownum += 1

            for (player, score) in winners.items():
                #TODO: Sort this list
                client.msg(recipient, "%s -> %r win(s)" % (player, score))

    @Module.handle('LOSERS')
    def losers(self, client, actor, recipient, *args):
        actor = User(actor)
        with open('winstats.csv', 'rb') as csvfile:
            reader = csv.reader(csvfile,delimiter=';')
            rownum = 0
            failers = {}
            for row in reader:
                colnum = 0
                for col in row:
                    _log.info("Col number %r" % colnum)
                    if colnum == 2:
                        nick = col
                    elif colnum == 3:
                        if col == "fail":
                            if nick in failers:
                                failers[nick] += 1
                            else:
                                failers[nick] = 1

                    colnum += 1

                rownum += 1

            for (player, score) in failers.items():
                #TODO: Sort this list
                client.msg(recipient, "%s -> %r fail(s)" % (player, score))

# Let KitnIRC know what module class it should be loading.
module = D20Module

# vim: set ts=4 sts=4 sw=4 et:
