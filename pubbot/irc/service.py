# Copyright 2008-2013 the original author or authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from geventirc.irc import Client
from geventirc import handlers, replycode

from pubbot import service
from pubbot.irc.models import Network
from pubbot.irc.handlers import GhostHandler, UserListHandler, InviteProcessor, ConversationHandler, JoinHandler


class Channel(service.BaseService):

    def __init__(self, channel):
        super(Channel, self).__init__(channel.name)
        self.channel = channel

    def start(self):
        self.parent.add_handler(JoinHandler(self.channel.name))


class Connection(service.BaseService):

    def __init__(self, network):
        super(Connection, self).__init__(network.server)
        self.network = network

    def start(self):
        logger.info("Connecting to '%s' on port '%d'" % (self.network.server, int(self.network.port)))
        self.client = Client(self.network.server, self.network.nick, port=str(self.network.port), ssl=self.network.ssl)

        # self.client.add_handler(handlers.print_handler)
        self.client.add_handler(handlers.ping_handler, 'PING')

        if self.network.nickserv_password:
            self.client.add_handler(GhostHandler(self.network.nick, self.network.nickserv_password))
        else:
            self.client.add_handler(handlers.nick_in_use_handler, replycode.ERR_NICKNAMEINUSE)

        self.client.add_handler(UserListHandler())
        self.client.add_handler(InviteProcessor())

        # Channels to join
        for room in network.rooms.all():
            self.add_child(Channel(room))

        # Inject conversation data into queue
        self.client.add_handler(ConversationHandler())


class Service(service.BaseService):

    def start(self):
        print "Starting irc services"
        self.group = []
        for network in Network.objects.all():
            self.add_child(Connection(network))
