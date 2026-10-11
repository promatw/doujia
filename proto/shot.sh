#!/bin/bash
# usage: shot.sh <hash> <out.png> [budget]
google-chrome --headless=new --no-sandbox --disable-gpu --hide-scrollbars --force-device-scale-factor=2 --window-size=390,844 --virtual-time-budget=${3:-1500} --autoplay-policy=no-user-gesture-required --screenshot="$2" "file:///workspace/doujia/proto/index.html#$1" >/dev/null 2>&1
