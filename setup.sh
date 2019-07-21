#!/bin/sh

pip3 install -r requirements.txt

cp init.sh /etc/init.d/fishpi

sed -i -e 's/\r$//' /etc/init.d/fishpi

update-rc.d fishpi defaults

systemctl daemon-reload

exit 0