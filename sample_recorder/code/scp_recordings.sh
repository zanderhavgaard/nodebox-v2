#!/usr/bin/env bash

nodebox_ip=...

scp ~/code/recordings/* pi@$nodebox_ip:~/code/nodebox_v2/sound_files/recorded_samples/
