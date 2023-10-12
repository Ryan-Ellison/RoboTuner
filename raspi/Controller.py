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
import time

import pyaudio
import statistics as stat
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
TOLERANCE = .85


# Create audio stream
p = pyaudio.PyAudio()

audio_stream = p.open(
    rate=SAMPLING_RATE,
    channels=NUM_CHANNELS,
    format=FORMAT,
    input=True,
    frames_per_buffer=FRAMES_PER_BUFFER
)
prev_note = None
# Take in an audio sample each iteration and print musical note value and cents sharp
while True:

    # Used for tracking how long each note is played
    start = time.time()
    pitch = tuner(audio_stream, SAMPLING_RATE, NUM_CHANNELS,
                  FRAMES_PER_BUFFER, TOLERANCE, p.get_sample_size(FORMAT))

    if not pitch[1] or not pitch[0]:
        continue

    midi = int(round(stat.median(pitch[1])))
    frequency = stat.median(pitch[0])
    nearest_note = notes[midi - 24]
    tendency = nearest_note.get_cents(frequency)
    nearest_note.adjust_tendency(tendency)

    end = time.time()
    print("Note = " + nearest_note.name + " Cents: " + str(tendency) +
          " Average tendency " + str(nearest_note.get_tendency()) +
          " Times Played: " + str(nearest_note.total_times_played) +
          " Time elapsed: " + str(end - start))

    # Use to slow down print statements for easier reading
    # time.sleep(0.5)
