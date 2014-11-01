import os

# Hostname of the IRC server to which we will connect
IRC_SERVER = os.environ.pop('IRC_SERVER')
IRC_PORT = int(os.environ.pop('IRC_PORT'))

# Nickname to use on that IRC server
BOT_NICK = os.environ.pop('IRC_BOT_NICK')

# Password for this nickname
BOT_PASS = os.environ.pop('IRC_BOT_PASS')
