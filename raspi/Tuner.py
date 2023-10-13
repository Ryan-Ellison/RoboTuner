"""
Tuner
Adam Davis
RoboTune
Last edited 10/8/2023

=====================
This class measures the frequency of an audio sample

"""

from aubio import source
import pyaudio
import Note
from Note import Note
import wave


# Creates a list of all notes
def initialize_notes():

    NOTE_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    OCTAVES = [1, 2, 3, 4, 5, 6, 7, 8]
    notes = []

    # midi value and frequency of C1, the first inputted note
    midi = 24
    frequency = 32.70320

    # semitone multiplied by the 12th root of 2 is next semitone
    # 12th root of 2 = 1.0594630943593
    MULTIPLIER = 1.0594630943593

    for i in OCTAVES:
        for j in NOTE_NAMES:
            note = Note(j + str(i), frequency, midi)
            notes.append(note)
            midi += 1
            frequency *= MULTIPLIER
    for i in notes:
        i.print_note()

    return notes


# Finds the frequency of current audio sample
# Be sure to initialize notes before calling it
def tuner(audio_stream, sampling_rate, num_channels,
          frames_per_buffer, tolerance, sample_size):
    from aubio import pitch

    # Window size of fft and size of hop
    win_s = 2048
    hop_s = 512


    # Computes midi and hz values
    #pitch_hz_o = pitch("specacf", win_s, hop_s, sampling_rate)
    #pitch_midi_o = pitch("specacf", win_s, hop_s, sampling_rate)

    pitch_hz_o = pitch("yin", win_s, hop_s, sampling_rate)
    pitch_midi_o = pitch("yin", win_s, hop_s, sampling_rate)

    pitch_hz_o.set_unit("Hz")
    pitch_hz_o.set_tolerance(tolerance)

    pitch_midi_o.set_unit("midi")
    pitch_midi_o.set_tolerance(tolerance)

    frames = []

    for i in range(0, int((sampling_rate / frames_per_buffer) * .2)):
        data = audio_stream.read(frames_per_buffer)
        frames.append(data)

    a = wave.open('OUTPUT.wav', 'wb')
    a.setnchannels(num_channels)
    a.setsampwidth(sample_size)
    a.setframerate(sampling_rate)
    a.writeframesraw(b''.join(frames))
    a.close()

    FILE = 'OUTPUT.wav'

    s = source(FILE, sampling_rate, hop_s)

    pitches_hz = []
    pitches_midi = []
    confidences = []

    total_frames = 0

    while True:
        samples, read = s()
        pitch_hz = pitch_hz_o(samples)[0]
        pitch_midi = pitch_midi_o(samples)[0]

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
