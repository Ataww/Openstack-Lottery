#!/bin/sh

#Read config file
while read line
do
      var=$line
done < "service.conf"

DAEMON="/apps/$var.py"
DAEMONUSER="root"

#Keep only executable name
for i in $(echo $var | tr "/" "\n")
do
  var=$i
done
daemon_NAME="$var.py"

PATH="/sbin:/bin:/usr/sbin:/usr/bin"

test -x $DAEMON || exit 0

. /lib/lsb/init-functions

d_start () {
        log_daemon_msg "Starting system $daemon_NAME Daemon"
        start-stop-daemon --background --name $daemon_NAME --start --quiet --chuid $DAEMONUSER --exec $DAEMON -- $daemon_OPT
        log_end_msg $?
}

d_stop () {
        log_daemon_msg "Stopping system $daemon_NAME Daemon"
        start-stop-daemon --name $daemon_NAME --stop --retry 5 --quiet --name $daemon_NAME
        log_end_msg $?
}

case "$1" in
  start)
        d_start
        ;;
  restart|reload|force-reload)
        echo "Error: argument '$1' not supported" >&2
        exit 3
        ;;
  stop|status)
        # No-op
        d_stop
        ;;
  *)
        echo "Usage: $0 start|stop" >&2
        exit 3
        ;;
esac
