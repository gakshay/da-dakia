su - root << EOF
root
echo "Starting CRON daemon..."
/etc/init.d/crond start
EOF
