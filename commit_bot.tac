from functools import partial
from twisted.application import service, internet
from twisted.intenet.porotocol import ReconntectingClientFactory

import private as config
from commit_bot import CommitBot

application = service.Application('kenaan')

factory = ReconntectingClientFactory.forProtocol(
		partial(CommitBot, nickname=config.NICKNAME, password=config.PASSWORD))

svc = internet.TCPClient(config.IRC_SERVER, config.IRC_PORT, factory)
svc.setServiceParent(application)
