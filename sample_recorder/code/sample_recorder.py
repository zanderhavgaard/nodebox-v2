# bash command for recording audio: arecord -D plughw:1 --duration=10 -f cd -vv ~/test_recording.wav

import RPi.GPIO as GPIO
import os
import time

# enable some debug prints
debug = False

# find using "arecord -l"
audio_device_number = 1

# recording duration in seconds
duration = 1

# encoding, we use cd quality, for other options see "man arecord"
encoding = 'cd'

# file format of recording
file_format = 'wav'

# location of recorded samples
sample_location = '~/code/recordings'

# BCM pin of button
button_pin = 23

# setup GPIO
GPIO.setmode(GPIO.BCM)

# setup button
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def loop():
    try:
        while True:
            button_state = GPIO.input(button_pin)
            if button_state == False:
                if debug:
                    print('Button Pressed...')
                record_sample()
                time.sleep(duration + 0.5)
    except KeyboardInterrupt:
        print('Exitting sample_recorder...')
        GPIO.cleanup()
    except:
        GPIO.cleanup()

def record_sample():
    print('Recoding sample...')
    file_name = time.strftime("sample_%Y-%m-%d_%H:%M:%S", time.gmtime())
    if debug:
        print('file_name: ', file_name)
    command = "arecord -D plughw:{} --duration={} -f {} {}/{}.{} & disown".format(
    audio_device_number, duration, encoding, sample_location, file_name, file_format)
    if debug:
        print('command: ', command)
    os.system(command)

loop()
