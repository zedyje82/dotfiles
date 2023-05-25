#!/bin/sh

function run {
  if ! pgrep $1 ;
  then
    $@&
  fi
}

run xrandr --output DP-0 --mode 1920x1080 --rate 75 &
run nvidia-settings -l &
run udiskie -A -t &
run dunst &
run /usr/lib/polkit-gnome/polkit-gnome-authentication-agent-1 &
