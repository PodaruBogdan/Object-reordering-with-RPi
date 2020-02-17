#!/bin/bash

rfkill unblock bluetooth;
sudo systemctl daemon-reload;
sudo systemctl restart bluetooth.service;
echo -e 'connect 98:09:CF:74:9E:4B' | sudo bluetoothctl -a;
var="$(hcitool con)";

echo -e 'info 98:09:CF:74:9E:4B' | bluetoothctl > /home/pi/py_projects/dev_details.txt;
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
	echo -e 'connect 98:09:CF:74:9E:4B' | sudo bluetoothctl -a;
	echo -e 'info 98:09:CF:74:9E:4B' | bluetoothctl > /home/pi/py_projects/dev_details.txt;
	con=$(grep Connected: /home/pi/py_projects/dev_details.txt);
	len=${#con};
	sleep 5;

done