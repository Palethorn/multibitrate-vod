# multibitrate-vod
Python wrapper for ffmpeg. Transcodes specified video files to h264 + aac into mp4 container. It performs 2-pass encoding for keyframe alignment and better quality.

# Installation
## Requirements
### ffmpeg
#### Linux
There are several options available. It's recommended that you build it from source. There is a comprehensive compilation guide in this link https://trac.ffmpeg.org/wiki/CompilationGuide. Alternatively, you can install it from repository.

#### Windows
There are prebuilt versions of ffmpeg for Windows out there, and the most popular is Zeranoe build. You can find it here https://ffmpeg.zeranoe.com/builds/. I recommend downloading static build for your arhitecture. Unpack it and put it somewhere easily accessible like C:\ffmpeg. You should then update your PATH variable with C:\ffmpeg\bin or wherever you've moved ffmpeg folder. You can test it by invoking CMD or Powershell, and typing ffmpeg. Output such as this means that it's working:

```
>ffmpeg
ffmpeg version N-83507-g8fa18e0 Copyright (c) 2000-2017 the FFmpeg developers
  built with gcc 5.4.0 (GCC)
  configuration: --enable-gpl --enable-version3 --enable-cuda --enable-cuvid --enable-d3d11va --enable-dxva2 --enable-libmfx --enable-nvenc --enable-avisynth --enable-bzlib --enable-fontconfig --enable-frei0r --enable-gnutls --enable-iconv --enable-libass --enable-libbluray --enable-libbs2b --enable-libcaca --enable-libfreetype --enable-libgme --enable-libgsm --enable-libilbc --enable-libmodplug --enable-libmp3lame --enable-libopencore-amrnb --enable-libopencore-amrwb --enable-libopenh264 --enable-libopenjpeg --enable-libopus --enable-librtmp --enable-libsnappy --enable-libsoxr --enable-libspeex --enable-libtheora --enable-libtwolame --enable-libvidstab --enable-libvo-amrwbenc --enable-libvorbis --enable-libvpx --enable-libwavpack --enable-libwebp --enable-libx264 --enable-libx265 --enable-libxavs --enable-libxvid --enable-libzimg --enable-lzma --enable-zlib
  libavutil      55. 47.100 / 55. 47.100
  libavcodec     57. 80.100 / 57. 80.100
  libavformat    57. 66.102 / 57. 66.102
  libavdevice    57.  2.100 / 57.  2.100
  libavfilter     6. 73.100 /  6. 73.100
  libswscale      4.  3.101 /  4.  3.101
  libswresample   2.  4.100 /  2.  4.100
  libpostproc    54.  2.100 / 54.  2.100
Hyper fast Audio and Video encoder
usage: ffmpeg [options] [[infile options] -i infile]... {[outfile options] outfile}...

Use -h to get full help or, even better, run 'man ffmpeg'
```

### python
#### Linux
If you're on linux there is a high chance that you already have python installed. Otherwise please install it using your package manager. You will also need python-jinja2 and python-yaml package so make sure you also install that using distribution package manager or pip.

#### Windows
There are python releases for Windows which you can choose from here https://www.python.org/downloads/windows/. Script supports python version 2, so please download and install corresponding release. Python for windows comes with a handy package manager which you can use to install additional packages for python. Ones you need are jinja2 and pyyaml. You can install it using the following commands:

```
pip install pyyaml
pip install jinja2
```

## Usage

Example command:

```
python transcode.py video1 video2 video3
```

To use this script, you need profiles definition. One example is in the repository, but I will explain how to actually make use of it and what do those parameters mean.

Example profiles definition:

```
qualities:
    360p:
        bitrate: '500k'
        size: '640x360'
        audio_bitrate: '64k'
        profile: 'baseline'
        fps: 25
        gop: 12
        preset: 'medium'
    540p:
        bitrate: '800k'
        size: '960x540'
        audio_bitrate: '64k'
        profile: 'main'
        fps: 25
        gop: 12
        preset: 'medium'
    720p:
        bitrate: '1000k'
        size: '1280x720'
        audio_bitrate: '128k'
        profile: 'high'
        fps: 25
        gop: 12
        preset: 'medium'
```

Filename of this definition must match the filename of the video file you want to transcode using following rule: 

```
<video_filename>.<extension>.yml
```

So if you have a video file called funny_cat.mp4 then you should create a profile definition with a file name funny_cat.mp4.yml.
This script will create one video file for each of those profiles specified by the following rule:

```
<video_filename>_<quality>.mp4
```

Quality placeholder represents each one from the profile definition: 360p, 540p, 720p etc. Finally you get these new files:

```
funny_cat_360p.mp4
funny_cat_540p.mp4
funny_cat_720p.mp4
```

Multibitrate VODs are typically used for adaptive streaming over the web using some kind of streaming server. I won't go into that. If you just need a single quality for youtube upload, or whatever, you can specify a single profile in definition as such:

```
    1080p:
        bitrate: '12000k'
        size: '1920x1080'
        audio_bitrate: '128k'
        profile: 'high'
        preset: 'medium'
        fps: 60
        gop: 30
```

And the script will produce a single file using specified parameters. Script also supports multiple inputs, so you can consecutively transcode multiple sources.

### Parameters
You can set these values based on youtube recommendations for their upload engine if you want to keep it simple https://support.google.com/youtube/answer/1722171?hl=en

- bitrate - Specify how much information do you want to keep in a resulting video track. Higher the number, higher the quality, but also, larger the file. You can tinker with this value to find optimal settings.
- size - Represents frame size or video resolution. You should keep width and height divisible by 16 for best quality as it's a recommended value for h264 encoding, but keep the original aspect ration as best as possible.
- audio_bitrate - Specify how much information do you want to keep in a resulting audio track. Again, higher number, higher quality, but higher filesize.
- profile - More information here https://en.wikipedia.org/wiki/H.264/MPEG-4_AVC#Profiles and here https://trac.ffmpeg.org/wiki/Encode/H.264#Alldevices
- preset - From here https://trac.ffmpeg.org/wiki/Encode/H.264#a2.Chooseapreset: A preset is a collection of options that will provide a certain encoding speed to compression ratio. A slower preset will provide better compression (compression is quality per filesize).
- fps - Specify which framerate to target or, in other words, how many frames per second do you wish to have in a resulting video. Generally this should not be higher than a source framerate.
- gop - GOP stands for Group of Pictures. It represents the distance between I-frames, or how many P-Frames and B-Frames can sit between full information I-Frame. If you want to know more, you can read about it here https://en.wikipedia.org/wiki/Inter_frame