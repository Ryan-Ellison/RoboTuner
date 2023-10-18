"""
Note
Adam Davis
RoboTune
Last edited 10/18/2023

=====================

This class represents a musical note. It is used in the context of
comparing a note to a pitch.

"""


import math


class Note:

    def __init__(self, name, frequency, midi):
        self.name = name
        self.frequency = frequency
        self.midi = midi
        self.total_times_played = 0
        self.tendency = 0
        self.total_cents = 0

    def __truediv__(self, other):
        return self/other


    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)
        return instance


    def print_note(self):
        print(self.name, self.frequency, self.midi)


    def get_cents(self, frequency):
        ratio = (frequency / self.frequency)
        if ratio is 0:
            return 0

        # 12 being total semitones, 100 being cents per semitones
        cents = 1200 * math.log2(ratio)
        return cents


    def adjust_tendency(self, cents):
        if cents is None:
            return
        self.total_times_played += 1
        self.total_cents += cents
        self.tendency = self.total_cents / self.total_times_played


    def get_tendency(self):
        return self.tendency

