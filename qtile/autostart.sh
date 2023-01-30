#!/bin/sh

setxkbmap -layout br &
nvidia-settings -l &
exec /usr/lib/policykit-1-gnome/polkit-gnome-authentication-agent-1 &
