################################################################################
# ks_o - key_sounds objects - Classes to hold sound objects and other things.
# Used by ks_main.py, a program that uses keystrokes to play wave files, one
#   sound per keystroke.
# A.Hornof - 10-13-2019
################################################################################

# Packages
import simpleaudio # simpleaudio-1.0.2

################################################################################
# A sound_object has the following member variables:
#   waveobject: a simpleaudio WaveObject, which can get played with play()
#   name: a string of the filename (including the ".wav" extension)
################################################################################

class sound_object:

    def __init__(self, path, filename):
        # Create a simpleaudio.WaveObject for playing the sound using the filename.
        self.waveobject = simpleaudio.WaveObject.from_wave_file(path + filename)
        # object name
        self.name = filename # For tracing and debugging.

################################################################################
# Student-defined classes below.
################################################################################


