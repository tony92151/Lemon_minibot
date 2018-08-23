#!/bin/bash
echo 'KERNEL=="ttyUSB*", ATTRS{idVendor}=="1a86", ATTRS{idProduct}=="7523", MODE:="0666", GROUP:="dialout", SYMLINK+="mega_controller"' >/etc/udev/rules.d/lemon_controller.rules

udevadm control --reload-rules
udevadm trigger

