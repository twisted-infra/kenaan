FROM ubuntu:14.04
MAINTAINER Jean-Paul Calderone jean-paul@clusterhq.com

# Configure some conventional paths
ENV RUN_DIR /var/run/ircbot

# Install Python and Python libraries required by kenaan.
RUN \
    apt-get update && \
    apt-get install -y python python-pip python-twisted && \
    pip install amptrac && \
    apt-get autoclean

# Install Kenaan
ADD . /srv/kenaan
RUN mkdir "${RUN_DIR}"

# Pass configuration along
# ENV IRC_SERVER
# ENV IRC_PORT
# ENV IRC_BOT_NICK
# ENV IRC_BOT_PASS

CMD \
    twistd \
    --nodaemon \
    --logfile /var/log/ircbot.log \
    --pidfile /var/run/ircbot.pid \
    --rundir "${RUN_DIR}" \
    --python /srv/kenaan/commit_bot.tac
