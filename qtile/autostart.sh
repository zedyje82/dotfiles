#!/bin/sh

setxkbmap -layout br &
nvidia-settings -l &
udiskie -A -t &
exec /usr/lib/polkit-dumb-agent/polkit-dumb-agent-responder &
