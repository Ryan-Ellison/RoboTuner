
import time
import sys

from pathlib import Path
pyaudioPath = str(Path(__file__).parent.parent) + "/raspi"
print(pyaudioPath)
sys.path.insert(0, pyaudioPath)
import pyaudio
import statistics as stat
import Tuner
from Tuner import tuner

class NoteReader():
    def __init__(self):

        # Creates a list of all notes
        self.notes = Tuner.initialize_notes()

        # Initializes variables

        self.NUM_CHANNELS = 1
        self.FRAMES_PER_BUFFER = 1024
        self.SAMPLING_RATE = 44100
        self.FORMAT = pyaudio.paInt16

        # Confidence threshold for sample
        self.TOLERANCE = .85


        # Create audio stream
        self.p = pyaudio.PyAudio()

        self.audio_stream = self.p.open(
            rate=self.SAMPLING_RATE,
            channels=self.NUM_CHANNELS,
            format=self.FORMAT,
            input=True,
            frames_per_buffer=self.FRAMES_PER_BUFFER
        )
        self.prev_note = None
    
    def getNote(self):
        # Take in an audio sample each iteration and print musical note value and cents sharp
        # Used for tracking how long each note is played
        while True:
            start = time.time()
            pitch = tuner(self.audio_stream, self.SAMPLING_RATE, self.NUM_CHANNELS,
                          self.FRAMES_PER_BUFFER, self.TOLERANCE, self.p.get_sample_size(self.FORMAT))

            if not pitch[1] or not pitch[0]:
                continue

            midi = int(round(stat.median(pitch[1])))
            frequency = stat.median(pitch[0])
            nearest_note = self.notes[midi - 24]
            tendency = nearest_note.get_cents(frequency)
            nearest_note.adjust_tendency(tendency)

            end = time.time()
            print("Note = " + nearest_note.name + " Cents: " + str(tendency) +
                  " Average tendency " + str(nearest_note.get_tendency()) +
                  " Times Played: " + str(nearest_note.total_times_played) +
                  " Time elapsed: " + str(end - start))

            # Use to slow down print statements for easier reading
            # time.sleep(0.5)
            return nearest_note.name, tendency
        return None
