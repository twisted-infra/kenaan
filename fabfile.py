"""
Support for DNS service installation and management.
"""

from fabric.api import run, settings

from braid import git, cron
from braid.twisted import service

# TODO: Move these somewhere else and make them easily extendable
from braid import config
_hush_pyflakes = [ config ]


class Kenaan(service.Service):
    def task_install(self):
        """
        Install kenaan, an irc bot.
        """
        # Bootstrap a new service environment
        self.bootstrap()

        with settings(user=self.serviceUser):
            run('ln -nsf {}/start {}/start'.format(self.configDir, self.binDir))
            for bin in ['alert', 'commit', 'message', 'ticket']:
                run('ln -nsf {1}/{0} {2}/{0}'.format(bin, self.configDir, self.binDir))
            self.task_update()
            cron.install(self.serviceUser, '{}/crontab'.format(self.configDir))

    def task_update(self):
        """
        Update config.
        """
        with settings(user=self.serviceUser):
            git.branch('https://github.com/twisted-infra/kenaan', self.configDir)


globals().update(Kenaan('kenaan').getTasks())
