"""
Controller
Adam Davis
RoboTune
Last edited 10/18/2023

=====================

This class takes in a pitch, matches it to a note,
and determines how flat or sharp it is. It then
sends instructions to the tuner that tell it
what to do

"""
import pyaudio
import statistics as stat
import Tuner
from Tuner import tuner


# Initializes variables

NUM_CHANNELS = 1
FRAMES_PER_BUFFER = 1024
SAMPLING_RATE = 44100
FORMAT = pyaudio.paInt16
TOLERANCE = .85 # Confidence threshold


# Creates a list of all notes
notes = Tuner.initialize_notes()

# Create PyAudio Object
p = pyaudio.PyAudio()


# Audio Stream
audio_stream = p.open(
    rate=SAMPLING_RATE,
    channels=NUM_CHANNELS,
    format=FORMAT,
    input=True,
    frames_per_buffer=FRAMES_PER_BUFFER
)


# Take in an audio sample each iteration and print musical note value and cents sharp
while True:

    # Get Pitch
    pitch = tuner(audio_stream,
                  SAMPLING_RATE,
                  NUM_CHANNELS,
                  FRAMES_PER_BUFFER,
                  TOLERANCE,
                  p.get_sample_size(FORMAT)
                  )


    # if pitch not valid, continue
    if not pitch[1] or not pitch[0]:
        continue
    if pitch[1] == 0 or pitch[0] == 0:
        continue


    # Convert pitch to midi value
    midi = int(round(stat.median(pitch[1])))

    # Convert pitch to hz
    frequency = stat.median(pitch[0])

    # Check for invalid midi
    if midi <= 0:
        continue


    # First initialized note is midi 24,
    # so it will go to the note that has
    # the midi value in the array of initialize notes
    nearest_note = notes[midi - 24]

    # The amount in cents flat or sharp
    tendency = nearest_note.get_cents(frequency)

    # Adjust the played note's average tendency
    nearest_note.adjust_tendency(tendency)

    # Print detected note data
    print("Note = " + nearest_note.name + " Cents: " + str(tendency) +
          " Average tendency " + str(nearest_note.get_tendency()) +
          " Times Played: " + str(nearest_note.total_times_played))


