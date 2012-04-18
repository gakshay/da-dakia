bus=`lsusb | grep "03f0" | cut -f2 -d " "`
id=`lsusb | grep "03f0" | cut -c16-18`
echo $bus
echo $id
su - root << EOF
root
echo "Removing CUPSD socket..."
sock=/var/run/cups/cups.sock
if [ -S "$sock" ]; then
	rm -rf "$sock"
fi

echo "Starting CUPS daemon..."
chmod a+rw /dev/bus/usb/$bus/$id
echo "Restarting CUPSD ..."
/etc/init.d/cupsd stop
/etc/init.d/cupsd start
EOF
