su - root << EOF
root
echo "Starting CRON daemon..."
/etc/init.d/crond stop
sleep 1
/etc/init.d/crond start
EOF
