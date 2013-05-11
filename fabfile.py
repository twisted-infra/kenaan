"""
Support for DNS service installation and management.
"""

from fabric.api import run, settings, env, cd, abort, puts, put
from fabric.contrib import files

from twisted.python.filepath import FilePath

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
            run('/bin/ln -nsf {}/start {}/start'.format(self.configDir, self.binDir))
            for bin in ['alert', 'commit', 'message', 'ticket']:
                run('/bin/ln -nsf {1}/{0} {2}/{0}'.format(bin, self.configDir, self.binDir))
            self.task_update()
            cron.install(self.serviceUser, '{}/crontab'.format(self.configDir))
            if env.get('installTestData'):
                self.task_installTestData()
            elif env.get('installPrivateData'):
                self.task_installPrivateData()


    def task_installTestData(self, force=None):
        """
        Do test environment setup (with fake passwords, etc).
        """
        if env.get('environment') == 'production':
           abort("Don't use testInit in production.")

        with settings(user=self.serviceUser), cd(self.configDir):
            if force or not files.exists('private.py'):
                puts('Using sample private.py')
                run('/bin/cp private.py.sample private.py')


    def task_installPrivateData(self, private='private.py'):
        """
        Install private config.
        """
        with settings(user=self.serviceUser):
            if FilePath(private).exists():
                put(private, '{}/private.py', mode=0600)
            else:
                abort('Missing private config.')


    def task_update(self):
        """
        Update config.
        """
        with settings(user=self.serviceUser):
            git.branch('https://github.com/twisted-infra/kenaan', self.configDir)


globals().update(Kenaan('kenaan').getTasks())
