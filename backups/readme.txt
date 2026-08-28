# .desktop File
# location: ~/.config/autostart
# Purpose: Upon starting up the gaming device, immediately launches the pygame application by calling start_gamingdevice.sh
# Contents:
[Desktop Entry]
Type=Application
Name=Gaming Device
Exec=/home/gaming/gamingdevice/start_gamingdevice.sh
X-GNOME-Autostart-enabled=true


# cmdline.txt
# location:
# Purpose: Sets the screen configuration, 720x720
# Contents: (needs to be all one line)
console=serial0,115200 console=tty3 root=PARTUUID=8eee7c95-02 rootfstype=ext4 fsck.repair=yes rootwait quiet loglevel=3 vt.global_cursor_default=0 splash plymouth.ignore-serial-consoles ds=nocloud;i=rpi-imager-1776025705027 
cfg80211.ieee80211_regdom=US video=HDMI-A-1:720x720M@60,rotate=180


# start_gamingdevice.sh
# location: gamingdevice
# Purpose: launches pygame
#!/bin/bash
export DISPLAY=:0 
export XAUTHORITY=/home/gaming/.Xauthority 
export  XDG_RUNTIME_DIR=/run/user/1000 
exec  /home/gaming/gamingdevice/gaming_venv/bin/python /home/gaming/gamingdevice/homescreen.py >> /home/gaming/gamingdevice/homescreen.log 2>&1

# controller_pi.py
# location: gamingdevice
# Purpose: settings for the controller/joystick


