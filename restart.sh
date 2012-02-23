# Make sure we are in the right directory
cd `dirname $0`

# Download bottle module
wget -q -O bottle.py --no-check-certificate https://github.com/defnull/bottle/raw/master/bottle.py
chmod 755 bottle.py

# Start 4 new processes
for n in 0 1 2 3; do
  pidfile="/tmp/bottlepy.$n.pid"
  /sbin/start-stop-daemon --stop --pidfile $pidfile
  /sbin/start-stop-daemon --start --background --chdir `pwd` \
                            --make-pidfile --pidfile $pidfile \
                            --startas ./bottle.py -- \
                            --bind "127.0.0.1:808$n" app:app
done

