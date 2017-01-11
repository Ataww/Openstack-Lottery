#!/bin/sh
### BEGIN INIT INFO
# Provides:          skeleton
# Required-Start:    $remote_fs $syslog
# Required-Stop:     $remote_fs $syslog
# Should-Start:      $portmap
# Should-Stop:       $portmap
# X-Start-Before:    nis
# X-Stop-After:      nis
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# X-Interactive:     true
# Short-Description: Example initscript
# Description:       This file should be used to construct scripts to be
#                    placed in /etc/init.d.
### END INIT INFO

#Read config file
while read line
do
      var=$line
done < "/etc/init.d/service.conf"

DAEMON="/apps/$var.py"
DAEMONUSER="root"

#Keep only executable name
for i in $(echo $var | tr "/" "\n")
do
  var=$i
done
daemon_NAME="sombrero"

PATH="/sbin:/bin:/usr/sbin:/usr/bin"

case "$1" in
  start)
        start-stop-daemon --background --name $daemon_NAME --start --quiet --chuid $DAEMONUSER --exec $DAEMON --
        ;;
  stop)
        start-stop-daemon --name $daemon_NAME --stop --retry 5 --quiet
        ;;
  *)
        echo "Usage: $0 start|stop" >&2
        exit 3
        ;;
esac