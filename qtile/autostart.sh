#!/bin/sh

nvidia-settings -l &
udiskie -A -t &
/usr/lib/polkit-gnome/polkit-gnome-authentication-agent-1 &
