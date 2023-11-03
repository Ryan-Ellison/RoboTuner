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
from Motor import Motor
import pyaudio
import statistics as stat
import Tuner
from Tuner import tuner
import sys
import time
import os
from gpiozero import Button, TonalBuzzer
from gpiozero.tones import Tone

print(sys.path)

# Initializes variables

NUM_CHANNELS = 1
FRAMES_PER_BUFFER = 1024
SAMPLING_RATE = 44100
FORMAT = pyaudio.paInt16
TOLERANCE = .85 # Confidence threshold

# Initialize buzzer pins for reference pitch
ref_pitch = TonalBuzzer(12, octaves=3)
ref_pitch.stop()
prev_note_freq = None

# button setup to switch between modes
button_timer = 0
mode_switch = False
rp_button = Button(3, hold_time=2, hold_repeat=True)
hold_repeated = False
def switch_modes():
    global hold_repeated
    if not hold_repeated:
        global mode_switch
        mode_switch = not mode_switch
        hold_repeated = True
    else:
        global halt_period
        halt_period = 0.5
        motor.set_led((1, 0, 0))
        time.sleep(0.2)
        motor.set_led((0, 0, 0))
        time.sleep(0.2)
        motor.set_led((1, 0, 0))
        time.sleep(0.2)
        motor.set_led((0, 0, 0))
        time.sleep(0.2)
        motor.set_led((1, 0, 0))
rp_button.when_held = switch_modes

# Creates a list of all notes
notes = Tuner.initialize_notes()

# Get user settings and init Motor class
f = open("/home/pi/config.txt")
max_dist = int(f.readline())
max_speed = int(f.readline())
#max_dist = 70
#max_speed = 60
f.close()

motor = Motor(max_dist)
motor.set_speed(motor.mm_to_steps(max_speed))

# Create PyAudio Object
p = pyaudio.PyAudio()

# where the stepper motor is
current_step = 0

# pull: False, push: True
motor_state = None

# Audio Stream
audio_stream = p.open(
    rate=SAMPLING_RATE,
    channels=NUM_CHANNELS,
    format=FORMAT,
    input=True,
    frames_per_buffer=FRAMES_PER_BUFFER
)

# motor inactivity short timer
timer = 0
timer_set = False

# motor inactivity halt/sleep mode
halt_timer = 0
halt_period = 10

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
        if motor.get_led() != (1, 0, 0):
            if not mode_switch:
                motor.set_led((0, 1, 0))
            else:
                motor.set_led((0, 0, 1))
        if not timer_set:
            timer = halt_timer = time.time()
            timer_set = True
        if timer_set:
            if time.time() - timer > .2:
                if not mode_switch:
                    motor.stop()
                    motor.wait()
                    motor_state = None
                elif prev_note_freq != None:
                    ref_pitch.play(Tone(frequency=prev_note_freq))
                    time.sleep(3)
                    ref_pitch.stop()
                    prev_note_freq = None
            if time.time() - timer > halt_period*60:
                motor.deinit()
                os.system("sudo halt")
        continue
    if pitch[1] == 0 or pitch[0] == 0:
        continue

    timer_set = False

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


    if not mode_switch:
        if (tendency < -2 and motor_state != False):
            motor.pull(max_dist)
            motor_state = False

        elif (tendency > 2 and motor_state != True):
            motor.push(max_dist)
            motor_state = True
    else:
        prev_note_freq = nearest_note.frequency
            
