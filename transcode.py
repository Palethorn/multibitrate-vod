#!/usr/bin/env python

import yaml
import sys
import os

pass1 = 'ffmpeg -y -i {0} -vf drawtext=\"fontfile=/usr/share/fonts/ubuntu/Ubuntu-B.ttf: text=\'{4}\': fontcolor=white: fontsize=48: box=1: boxcolor=black: x=0: y=0\" -c:a libfdk_aac -ac 2 -ab {1} -c:v libx264 -preset:v veryfast -threads 0 -r 25 -g 48 -keyint_min 48 -sc_threshold 0 -x264opts bframes=1 -pass 1 -b:v {2} -profile:v {3} -s {4} -f mp4 {5}'
pass2 = 'ffmpeg -y -i {0} -vf drawtext=\"fontfile=/usr/share/fonts/ubuntu/Ubuntu-B.ttf: text=\'{4}\': fontcolor=white: fontsize=48: box=1: boxcolor=black: x=0: y=0\" -c:a libfdk_aac -ac 2 -ab {1} -c:v libx264 -preset:v fast -threads 0 -r 25 -g 48 -keyint_min 48 -sc_threshold 0 -x264opts bframes=1 -pass 2 -b:v {2} -profile:v {3} -s {4} -f mp4 {5}'

for file in sys.argv:

    if os.path.exists(file + '.yml') == False:
        continue

    stream = open(file + '.yml', 'r')
    qualities = yaml.load(stream)['qualities']
    for q in qualities:
        command = pass1.format(file, qualities[q]['audio_bitrate'], qualities[q]['bitrate'], qualities[q]['profile'], qualities[q]['size'], file.replace('.mp4', '') + '_' + q + '.mp4')
        os.system(command)
        command = pass2.format(file, qualities[q]['audio_bitrate'], qualities[q]['bitrate'], qualities[q]['profile'], qualities[q]['size'], file.replace('.mp4', '') + '_' + q + '.mp4')
        os.system(command)
