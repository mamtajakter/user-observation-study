################################################################################
# GLOBAL.py
# Global variables used by key_sounds_menu.py, which is
#   a program that uses keystrokes to play wave files, one sound per keystroke.
# Written by A.Hornof - 10/13/2019
################################################################################

# Local imports - "ks" stands for "key_sounds".
import ks_load

# Keystroke assignments.
SPACE_BAR = '\x20'  # space bar

# Used for loading files.
WAVE_DIR_PROVIDED = "wav_files_provided/"
NORMAN_DIR = "Book_01_norman/"
CHAPTER_NAME_DIR = "Chapter_Names/"
TEXT_CONTENT_DIR = "Text_Content/Ch02/"

# Sounds.

################################################################################
# Load sound files.
################################################################################
# A lot of sound files are created here using the following steps:
# 1. X is some kind of consistent sound file content, such as NUMBERS or CHAPTERS.
# 2. Three variables are set:
#    X_FILENAMES = a list of text strings corresponding to filenames on disk.
#    X_LOCATION = the path to the files, relative to the main program file.
#    X_SO_LIST = the tuple of sound_object files that ends up getting created.
#                (The lists are converted to tuples for speed and safety.)

# NUMBER_SO_LIST - list of sound-objects that are the numbers 0 to 9

NUMBER_FILENAMES = ("00_f.wav", "01_f.wav", "02_f.wav", "03_f.wav", "04_f.wav",
                    "05_f.wav", "06_f.wav", "07_f.wav", "08_f.wav", "09_f.wav")
NUMBER_LOCATION = WAVE_DIR_PROVIDED + "numbers/"
NUMBER_SO_LIST = list()
ks_load.load_sound_objects(NUMBER_FILENAMES, NUMBER_LOCATION, NUMBER_SO_LIST)
NUMBER_SO_LIST = tuple(NUMBER_SO_LIST)

# CH_NAME_SO_LIST - chapter names put into sound_objects

CH_NAME_FILENAMES = ("Ch01.wav", "Ch02.wav", "Ch03.wav", "Ch04.wav", "Ch05.wav", "Ch06.wav",
                    "Ch07.wav")
CH_NAME_LOCATION = WAVE_DIR_PROVIDED + NORMAN_DIR + CHAPTER_NAME_DIR
CH_NAME_SO_LIST = list()
ks_load.load_sound_objects(CH_NAME_FILENAMES, CH_NAME_LOCATION, CH_NAME_SO_LIST)
CH_NAME_SO_LIST = tuple(CH_NAME_SO_LIST)

# READ_ITEM_LIST - read-item names put into sound_objects.
# This is the sequence of items for reading the entire chapter.
# (It is incomplete as of 10-13-2019)

READ_ITEM_FILENAMES = ("000_CN_34.wav", "001_TS_34.wav", "002_RP_34.wav", "003_SH_34.wav",
	"004_TS_34.wav", "005_RP_34.wav", "006_TS_35.wav", "007_RP_35.wav", "008_TS_35.wav",
	"009_RP_35.wav", "010_TS_35.wav", "011_TS_35.wav", "012_TS_35.wav", "013_RP_35.wav", 
	"014_TS_35.wav", "015_TS_35.wav", "016_RP_35.wav", "017_TS_35.wav", "018_RP_35.wav", 
	"019_TS_35.wav", "020_RP_35.wav", "021_TS_36.wav", "022_RP_36.wav", "023_SH_36.wav", 
	"024_TS_36.wav", "025_RP_36.wav", "026_SH_36.wav", "027_TS_36.wav", "028_RP_36.wav", 
	"029_TS_37.wav", "030_RP_37.wav", "031_TS_37.wav", "032_RP_37.wav", "033_TS_37.wav", 
	"034_RP_37.wav", "035_TS_38.wav", "036_RP_38.wav", "037_TS_38.wav", "038_RP_38.wav", 
	"039_SH_38.wav", "040_TS_38.wav", "041_RP_38.wav", "042_TS_38.wav", "043_RP_38.wav", 
	"044_TS_38.wav", "045_RP_38.wav", "046_TS_38.wav", "047_RP_38.wav", "048_TS_39.wav", 
	"049_RP_39.wav", "050_TS_39.wav", "051_RP_39.wav", "052_TS_39.wav", "053_RP_39.wav", 
	"054_SH_39.wav", "055_TS_39.wav", "056_RP_39.wav", "057_TS_39.wav", "058_RP_39.wav", 
	"059_TS_40.wav", "060_RP_40.wav", "061_TS_40.wav", "062_RP_40.wav")
READ_ITEM_LOCATION = WAVE_DIR_PROVIDED + NORMAN_DIR + TEXT_CONTENT_DIR
READ_ITEM_SO_LIST = list()
ks_load.load_sound_objects(READ_ITEM_FILENAMES, READ_ITEM_LOCATION, READ_ITEM_SO_LIST)
READ_ITEM_SO_LIST = tuple(READ_ITEM_SO_LIST)
