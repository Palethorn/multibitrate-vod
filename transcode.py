import yaml
import sys
import os
from jinja2 import Template
import argparse

backend = {
    'cpu': {
        'pass1': 'ffmpeg -hide_banner -loglevel error -y -i {{ input_file }} -an -c:v libx264 -preset:v {{ preset }} -threads 0 -r {{ fps }} -g {{ gop }} -keyint_min {{ gop }} -sc_threshold 0 -x264opts bframes=1 -pass 1 -b:v {{ bitrate }} -profile:v {{ profile }} -s {{ size }} -f mp4 {{ output_file }}',
        'pass2': 'ffmpeg -hide_banner -loglevel error -y -i {{ input_file }} -strict -2 -c:a aac -ac 2 -ab {{ audio_bitrate }} -c:v libx264 -preset:v {{ preset }} -threads 0 -r {{ fps }} -g {{ gop }} -keyint_min {{ gop }} -sc_threshold 0 -x264opts bframes=1 -pass 2 -b:v {{ bitrate }} -profile:v {{ profile }} -s {{ size }} -f mp4 {{ output_file }}'
    },
    'nvidia': {
        'pass1': 'ffmpeg -hide_banner -loglevel error -y -hwaccel cuvid -i {{ input_file }} -an -c:v h264_nvenc -preset:v {{ preset }} -pix_fmt yuv420p -movflags faststart -bf 2 -coder 1 -threads 0 -r {{ fps }} -g {{ gop }} -keyint_min {{ gop }} -sc_threshold 0 -pass 1 -b:v {{ bitrate }} -profile:v {{ profile }} -s {{ size }} -f mp4 {{ output_file }}',
        'pass2': 'ffmpeg -hide_banner -loglevel error -y -hwaccel cuvid -i {{ input_file }} -strict -2 -c:a aac -ac 2 -ab {{ audio_bitrate }} -c:v h264_nvenc -preset:v {{ preset }} -pix_fmt yuv420p -movflags faststart -bf 2 -coder 1 -threads 0 -r {{ fps }} -g {{ gop }} -keyint_min {{ gop }} -sc_threshold 0 -pass 2 -b:v {{ bitrate }} -profile:v {{ profile }} -s {{ size }} -f mp4 {{ output_file }}'
    }
}

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--config')
parser.add_argument('-b', '--backend', choices=['cpu', 'nvidia'])
parser.add_argument('files', nargs='+')
args = parser.parse_args()

pass1 = Template(backend[args.backend]['pass1'])
pass2 = Template(backend[args.backend]['pass2'])

if os.path.exists(args.config) == False:
    print('Config file %s not found' % args.config)
    sys.exit(1)

stream = open(args.config, 'r')
config = yaml.load(stream)
qualities = config['qualities']

for file in args.files:

    if os.path.exists(file) == False:
        print('File %s not found' % file)
        continue

    first_pass_done = False

    for q in qualities:
        qualities[q]['input_file'] = file
        qualities[q]['output_file'] = file.replace('.mp4', '') + '_' + q + '.mp4'

        if first_pass_done == False:
            command = pass1.render(qualities[q])
            print(command)
            os.system(command)
            first_pass_done = True
        
        command = pass2.render(qualities[q])
        print(command)
        os.system(command)
