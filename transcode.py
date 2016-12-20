import yaml
import sys
import os
from jinja2 import Template

drawtext = '-vf drawtext=\"fontfile=/usr/share/fonts/ubuntu/Ubuntu-B.ttf: text=\'{{ text }}\': fontcolor=white: fontsize=48: box=1: boxcolor=black: x=0: y=0\"'

pass1 = Template('ffmpeg -y -i {{ input_file }} -t 00:5:00 -c:a aac -ac 2 -ab {{ audio_bitrate }} -c:v libx264 -preset:v veryfast -threads 0 -r {{ fps }} -g {{ gop }} -keyint_min {{ gop }} -sc_threshold 0 -x264opts bframes=1 -pass 1 -b:v {{ bitrate }} -profile:v {{ profile }} -s {{ size }} -f mp4 {{ output_file }}')
pass2 = Template('ffmpeg -y -i {{ input_file }} -t 00:5:00 -c:a aac -ac 2 -ab {{ audio_bitrate }} -c:v libx264 -preset:v fast -threads 0 -r {{ fps }} -g {{ gop }} -keyint_min {{ gop }} -sc_threshold 0 -x264opts bframes=1 -pass 2 -b:v {{ bitrate }} -profile:v {{ profile }} -s {{ size }} -f mp4 {{ output_file }}')

for file in sys.argv:

    if os.path.exists(file + '.yml') == False:
        continue

    stream = open(file + '.yml', 'r')
    qualities = yaml.load(stream)['qualities']

    for q in qualities:
        qualities[q]['input_file'] = file
        qualities[q]['output_file'] = file.replace('.mp4', '') + '_' + q + '.mp4'
        command = pass1.render(qualities[q])
        os.system(command)
        command = pass2.render(qualities[q])
        os.system(command)
