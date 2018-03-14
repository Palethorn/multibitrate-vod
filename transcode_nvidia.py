import yaml
import sys
import os
from jinja2 import Template

pass1 = Template('ffmpeg -y -hwaccel cuvid -i {{ input_file }} -an -c:v h264_nvenc -preset:v {{ preset }} -pix_fmt yuv420p -movflags faststart -bf 2 -coder 1 -threads 0 -r {{ fps }} -g {{ gop }} -keyint_min {{ gop }} -sc_threshold 0 -pass 1 -b:v {{ bitrate }} -profile:v {{ profile }} -s {{ size }} -f mp4 {{ output_file }}')
pass2 = Template('ffmpeg -y -hwaccel cuvid -i {{ input_file }} -c:a aac -ac 2 -ab {{ audio_bitrate }} -c:v h264_nvenc -preset:v {{ preset }} -pix_fmt yuv420p -movflags faststart -bf 2 -coder 1 -threads 0 -r {{ fps }} -g {{ gop }} -keyint_min {{ gop }} -sc_threshold 0 -pass 2 -b:v {{ bitrate }} -profile:v {{ profile }} -s {{ size }} -f mp4 {{ output_file }}')

# pass1 = Template('ffmpeg -y -hwaccel cuvid -i {{ input_file }} -an -c:v h264 -preset:v {{ preset }} -pix_fmt yuv420p -movflags faststart -bf 2 -coder 1 -threads 0 -r {{ fps }} -g {{ gop }} -keyint_min {{ gop }} -sc_threshold 0 -pass 1 -b:v {{ bitrate }} -profile:v {{ profile }} -s {{ size }} -f mp4 {{ output_file }}')
# pass2 = Template('ffmpeg -y -hwaccel cuvid -i {{ input_file }} -an -c:v h264 -preset:v {{ preset }} -pix_fmt yuv420p -movflags faststart -bf 2 -coder 1 -threads 0 -r {{ fps }} -g {{ gop }} -keyint_min {{ gop }} -sc_threshold 0 -pass 2 -b:v {{ bitrate }} -profile:v {{ profile }} -s {{ size }} -f mp4 {{ output_file }}')

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
