################################################################################
# ks_load - Functions to load sounds.
################################################################################
# Used by key_sounds_menu.py, a program that uses keystrokes to play wave files.
# Written by A.Hornof - 10/13/2019
################################################################################

# Packages
import simpleaudio

# Local imports - "ks" stands for "key_sounds".
import ks_o    # key_sounds sound_object

################################################################################
# load_sound_objects() - Function to create sound objects for soundfiles on disk.
# Input parameters:
#   • list_of_filenames: a list of strings corresponding to filenames on disk.
#   • directory_location: string describing directory on disk where these files exist.
#   • object_list_name: the (empty) list of sound_objects used in the program
# Note: It is important that object_list_name is "changed in place" such as with
#   append(), and not replaced with a new object.
################################################################################
def load_sound_objects(list_of_filenames, directory_location, object_list_name):
    for f in list_of_filenames:
        object_list_name.append(ks_o.sound_object(directory_location, f))

