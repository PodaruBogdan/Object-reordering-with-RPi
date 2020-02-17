#!/bin/bash

bluetoothctl << EOF
connect [98:09:CF:74:9E:4B]
EOF

cho -e 'info 98:09:CF:74:9E:4B' | bluetoothctl > /home/pi/py_projects/dev_details.txt;
con=$(grep Connected: /home/pi/py_projects/dev_details.txt);
len=${#con};
sleep 5;
while true;
do 
	if [ $len == "15" ];
	then
		break
	fi
	echo 'Connecting BT...';
	bluetoothctl << EOF
	connect [98:09:CF:74:9E:4B]
	
	echo -e 'info 98:09:CF:74:9E:4B' | bluetoothctl > /home/pi/py_projects/dev_details.txt;
	con=$(grep Connected: /home/pi/py_projects/dev_details.txt);
	len=${#con};
	sleep 5;

done
EOF