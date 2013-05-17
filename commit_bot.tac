from functools import partial
from twisted.application import service, internet
from twisted.internet.protocol import ReconnectingClientFactory

import private as config
from commit_bot import CommitBot

application = service.Application('kenaan')

factory = ReconnectingClientFactory.forProtocol(
		partial(CommitBot, nickname=config.NICKNAME, password=config.PASSWORD))

svc = internet.TCPClient(config.IRC_SERVER, config.IRC_PORT, factory)
svc.setServiceParent(application)
