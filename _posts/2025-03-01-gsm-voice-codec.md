---
layout: post
title: Experimenting with GSM Full Rate and Half Rate Voice Codec
date: 2025-03-22 10:55:00-0400
description: 
tags: GSM Experiments
categories: experiments
giscus_comments: false
related_posts: false
---

A few days ago, while teaching how GSM works to my students, I reached the part where I explained GSM voice codecs. I shared how there’s more than one codec—specifically, the Full Rate codec, which operates at around 13 kbps, and the Half Rate codec, which works at roughly 5.5 kbps.

As far as I know, the Half Rate codec was (or perhaps I should say _is_) almost never used. This got me thinking: why? After all, Half Rate theoretically allows the system to support twice the number of calls. It must be because of the quality loss, right?

But how bad could the quality really be to outweigh the benefit of doubling the system’s capacity? And if the quality was that poor, why even offer the option in the first place? I decided to dig deeper and test it myself.

I started by recording my voice and then went online to look for GSM voice codec software. At first, I wasn’t very hopeful, as it seemed like an obscure task. But to my surprise, it turned out to be easier than I thought.

[VLC](https://www.videolan.org/vlc/) can reproduce GSM-encoded voice (is there anything VLC can’t do?). And [FFmpeg](https://ffmpeg.org) comes with built-in GSM encoding and decoding capabilities. This made me wonder: why do these tools support GSM codecs out-of-the-box? Is there a significant need for people to work with GSM voice codecs? Perhaps it’s related to GSM eavesdropping? But let’s not go down that rabbit hole.

Back to our task, here’s how you do it. Let’s assume that we have an audio file, call it`voice.wav`. You will have to instruct `ffmpeg` to downsample it to 4 kHz, downmix the stereo into mono, code it using `gsm` and save it in a new file called `voice.gsm`
```
ffmpeg -i voice.wav -ar 8000 -ac 1 -g gsm voice.gsm
```

Then open the file with VLC and there you go, you're listening to your voice coded with the GSM voice codec. Thanks for your attention, see you at the next post.

No, wait a second. I didn't specify Full Rate/Half Rate. I recorded around 13 seconds of voice, and got a gsm file of around 176 kbytes. That gives me a bitrate of 13.5 kbps. `ffmpeg` is using Full Rate! But, as i said, I want to use half rate, i want to experience how bad it is.

I searched some more, it seems that `libgsm` (the codec library used by `ffmpeg`) only supports full rate. I couldn't use `ffmpeg` for this. But then I found [GAPK](https://osmocom.org/projects/gapk/wiki), a collection of GSM codecs packed into a command line tool, part of the awesome Osmocom project. `GAPK` supports Half Rate, but we have to install it first. Unfortunately there's no documentation, but the tool is simple enough that we can figure out how it works while using it. 

We must start with the dependencies. This has been tested on ubuntu 22.04.

```
sudo apt update
sudo apt install build-essential libtool libtalloc-dev libsctp-dev shtool autoconf automake git-core pkg-config make gcc gnutls-dev python2-minimal libusb-1.0.0-dev libmnl-dev liburing-dev libpcsclite-dev
```

Now we need to clone and build `libosmocore`:
```
git clone https://gitea.osmocom.org/osmocom/libosmocore.git
cd libosmocore/
autoreconf -i
./configure
make -j $(nproc)
sudo make install
sudo ldconfig -i
cd ..
```

Finally we can move to installing `GAPK`:
```
git clone https://gitea.osmocom.org/osmocom/gapk
cd gapk/
autoreconf -i
./configure --enable-gsmhr
make -j $(nproc)
sudo make install
sudo ldconfig
```

If you get an error that says that some headers were not found during `make`, just run `make` again. That fixed it for me.

Now test if everything went fine with `osmo-gapk -h`. 

`GAPK` can encode `Raw PCM samples Signed 16 bits little endian` into different GSM formats, and viceversa. Unfortunately, there's approximately a 0% probability that your original voice file is a raw PCM file. So we have to prepare it with `ffmpeg` first:
```
ffmpeg -i voice.wav -f s16le -acodec pcm_s16le -ar 8000 -ac 1 voice.pcm
```
That gives us a `voice.pcm` file that can be processed by `GAPK`. Let's encode it using Half Rate:
```
osmo-gapk -i voice.pcm -f rawpcm-s16le -g racal-hr -o voice.hr
```
`voice.hr` is 72.8 kbytes, giving us a bitrate of 5.6 kbps - exactly what we were expecting! 

Unfortunately VLC can't reproduce Half Rate files. We have to decode it back into PCM using `GAPK`:
```
osmo-gapk -i voice.hr -f racal-hr -g rawpcm-s16le -o voice.hr.pcm
```
and then into a VLC-supported format with `ffmpeg`:
```
ffmpeg -f s16le -ar 8000 -ac 1 -i voice.hr.pcm voice.hr.wav
```

Finally we can reproduce `voice.hr.wav`, which contains the uncompressed audio of our voice, which was previously encoded using Half Rate.

And the quality is... good? Really? At least it is from my macbook's speakers. 

All of this didn't prove my theory, but it was a fun way to spend half an hour! 