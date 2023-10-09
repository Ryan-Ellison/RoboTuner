"""
Note
Adam Davis
RoboTune
Last edited 10/8/2023

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

    def __truediv__(self, other):
        return self/other

    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)
        return instance

    def print_note(self):
        print(self.name, self.frequency, self.midi)

    def get_cents(self, frequency):
        ratio = (frequency / self.frequency)

        cents = 1200 * math.log2(ratio)
        # 12 being total semitones, 100 being cents per semitones

        return cents
