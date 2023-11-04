"""
Tuner
Adam Davis
RoboTune
Last edited 10/18/2023

=====================
This class measures the frequency of an audio sample

"""
import math

from aubio import pitch
from aubio import source
import Note
from Note import Note
import wave


# Creates a list of all notes


def hz_to_midi(hz):
    if (hz < 2) or (hz > 100000):
        return -1
    midi = hz / 440
    midi = math.log2(midi)
    midi *= 12
    midi += 69
    return midi


def initialize_notes():

    note_names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    octaves = [1, 2, 3, 4, 5, 6, 7, 8]
    notes = []

    # midi value and frequency of C1, the first inputted note
    midi = 24
    frequency = 32.70320

    # semitone multiplied by the 12th root of 2 is next semitone
    # 12th root of 2 = 1.0594630943593
    multiplier = 1.0594630943593

    for i in octaves:
        for j in note_names:
            note = Note(j + str(i), frequency, midi)
            notes.append(note)
            midi += 1
            frequency *= multiplier

    for i in notes:
        i.print_note()

    return notes


# Finds the frequency of current audio sample
# Be sure to initialize notes before calling it

def tuner(audio_stream, sampling_rate, num_channels,
          frames_per_buffer, tolerance, sample_size):


    # Window size of fft and size of hop
    win_s = 2048
    hop_s = 512


    # Computes midi and hz values
    pitch_hz_o = pitch("yin", win_s, hop_s, sampling_rate)

    pitch_hz_o.set_unit("Hz")
    pitch_hz_o.set_tolerance(tolerance)

    # Read audio into a buffer
    frames = []
    for i in range(0, int((sampling_rate / frames_per_buffer) * .05)):
        data = audio_stream.read(frames_per_buffer, False)
        frames.append(data)

    a = wave.open('OUTPUT.wav', 'wb')
    a.setnchannels(num_channels)
    a.setsampwidth(sample_size)
    a.setframerate(sampling_rate)
    a.writeframesraw(b''.join(frames))
    a.close()

    # Create or replace output file
    file = 'OUTPUT.wav'

    s = source(file, sampling_rate, hop_s)

    # Initialize lists
    pitches_hz = []
    pitches_midi = []
    confidences = []

    total_frames = 0
    while True:
        samples, read = s()
        pitch_hz = pitch_hz_o(samples)[0]
        pitch_midi = hz_to_midi(pitch_hz)
        confidence = pitch_hz_o.get_confidence()

        if read < hop_s:
            break

        # Will discard if sample is not reliable
        if confidence > tolerance:
            pitches_hz += [pitch_hz]
            pitches_midi += [pitch_midi]
            confidences += [confidence]
            total_frames += read
        else:
            continue
    # returns tuple of (hz value, midi value)
    return pitches_hz, pitches_midi
