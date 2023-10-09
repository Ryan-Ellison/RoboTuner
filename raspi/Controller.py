"""
Controller
Adam Davis
RoboTune
Last edited 10/8/2023

=====================

This class takes in a pitch, matches it to a note,
and determines how flat or sharp it is. It then
sends instructions to the tuner that tell it
what to do

"""

import pyaudio
import statistics as stat
import time
import Tuner
from Tuner import tuner


# Creates a list of all notes
notes = Tuner.initialize_notes()

# Initializes variables

NUM_CHANNELS = 1
FRAMES_PER_BUFFER = 1024
SAMPLING_RATE = 44100
FORMAT = pyaudio.paInt16

# Confidence threshold for sample
TOLERANCE = .8

win_s = 4096  # fft window size
hop_s = 512  # hop_size

# Create audio stream
p = pyaudio.PyAudio()

audio_stream = p.open(
    rate=SAMPLING_RATE,
    channels=NUM_CHANNELS,
    format=FORMAT,
    input=True,
    frames_per_buffer=FRAMES_PER_BUFFER
)

# Take in an audio sample each iteration and print musical note value and cents sharp
while True:
    pitch = tuner(audio_stream, SAMPLING_RATE, NUM_CHANNELS,
                  FRAMES_PER_BUFFER, TOLERANCE, p.get_sample_size(FORMAT))
    if not pitch[1] or not pitch[0]:
        continue
        
    midi = int(round(stat.median(pitch[1])))
    frequency = stat.median(pitch[0])

    nearest_note = notes[midi - 24]
    tendency = nearest_note.get_cents(frequency)

    print("Note = " + nearest_note.name + " " + str(tendency))

    # Use to slow down print statements for easier reading
    # time.sleep(0.5)
