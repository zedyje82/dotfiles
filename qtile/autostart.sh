#!/bin/sh

function run {
  if ! pgrep $1 ;
  then
    $@&
  fi
}

run nvidia-settings -l &
run udiskie -A -t &
run /usr/lib/polkit-gnome/polkit-gnome-authentication-agent-1 &
