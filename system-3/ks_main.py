################################################################################
# ks_menu.py
# "ks" stands for "keystroke sounds"
# A program that uses keystrokes to play wave files.
# If one sound is being played when a new sound is requested, the new sound
#   can either top and replace the current sounds, or get queued.
# Stoping a currently-playing sound also clears the queue.
#
# Uses python 3.6
# Written by A.Hornof - 10/13/2019
#
# Sources: https://pypi.org/project/simpleaudio/
#          https://pypi.org/project/readchar/
#          https://docs.python.org
#          Beazley (2009) Python Essential Reference
################################################################################

################################################################################
# This program uses the producer-and-consumer design pattern to separate the two
#   main components of the program.
#   The code is adapted from Beazley (2009) Python Essential Reference, p. 419.
# The two main components are:
#   (a) the keystroke-catching-and-processing method (the producer).
#   (b) the sound-playing method (the consumer).
# Each of these two components needs to maintain independent control of its
#   subprocesses. This is accomplished by having each run in a separate process.
#   Because the only coordination that needed between the two of them is that
#   messages get passed from the producer to the consumer, this can be
#   accomplished by simply using a multiprocessing.JoinableQueue. See:
#   https://docs.python.org/3/library/multiprocessing.html
# Note that "join" in this case does not mean that processes can connect to
#   the queue, but rather that the queue process can be connected to the main
#   program process such that sthe queue process must finish its execution before
#   the main process terminates.
# The use of this software pattern permits threading to be used in a relatively
#   simple and straightforward manner, with minimal programming overhead.
#   The only coordination needed, and used, is thread-safe message passing.
# Additional communication is accomplished with two multiprocessing.Events.
################################################################################

################################################################################
# How to debug. It should be OK to add print statements here (and also to
#   ks_o.py) provided that you do not also add print statements that runs in
#   other processes. The processes could compete for the std output.
# (See 17.2.1.4 at https://docs.python.org/3.6/library/multiprocessing.html)
################################################################################

# Packages
import multiprocessing # standard python package
import time            # standard python package
import readchar # version 2.0.1
# Also uses simpleaudio-1.0.2

# Local imports
# These are other python source code files required for this program to run.
# "ks" stands for "key_sounds" to informally connect the local files.
# The complete list of local python source code dependencies is: ks_GLOBAL.py,
# ks_load.py, ks_log.py, ks_main.py, ks_play.py, ks_so.py, ks_stop.py

import ks_log
import ks_play
import ks_stop
import ks_GLOBAL
import ks_o

# Global variables

# For additional global variables, see GLOBAL.py
def write_file(begin, elapsed,keyStrokes,ksNumber):

    outF = open(str(begin)+".txt", "w")
    line = "Time Elapsed: " + str(elapsed) + "\nNumber of Key Strokes: " + str(ksNumber) + "\n" + str(keyStrokes)
    outF.write(line)
    outF.write("\n")
    outF.close()
################################################################################
# Function to process user input. (This is a "producer".)
# Catch the keystrokes from the user, and process the keystrokes.
# Inputs: sound_q: a JoinableQueue of sound-objects.
#         log_q: a JoinableQueue for capturing timestamped events.
#         hold_q_e: a stop-modifying-the-queue multiprocessing.Event
#         stop_play_e: a stop-playing-sounds multiprocessing.Event
################################################################################

def keystroke_processor(sound_q, log_q, hold_q_e, stop_play_e):

    # Provide a visual prompt for input, though this should not be relied upon.
    # The user should be trained the basic i/o scheme of the interface before
    #   starting to use it. The point is to avoid any sort of visual display.
    print("Press <SPACE>, <J>, <K>, <L>, or <;>. Press <;> to quit.")

    books = ['wav_files_provided/Book_01_norman/']
    player = ks_o.AudiobookPlayer(books, sound_q, hold_q_e, stop_play_e, log_q)
    begin = time.time()
    keystrokes=""
    ksNumber=0
    # print(player.book.chapters[2].data)
    # Keep looping. Wait for the next keystoke, and process it when it arrives.
    while (True):

        # Wait for the next keystroke.
        key = readchar.readkey()

        # Process each keystroke as specified here.
        # Button "0"
        if (key == ks_GLOBAL.SPACE_BAR):
            keystrokes += str(key)
            keystrokes += "\n"
            ksNumber += 1
            player.on_button(0)

        # Button "1"
        elif (key == 'j' or key == 'J'):
            keystrokes += str(key)
            keystrokes += "\n"
            ksNumber += 1
            # # Stop any currently playing sounds, and clear the queue.
            # ks_stop.stop_sounds(sound_q, log_q, hold_q_e, stop_play_e)
            # # Play "Chapter 1"
            # sound_q.put(ks_GLOBAL.CH_NAME_SO_LIST[0])
            player.on_button(1)

        # Button "2"
        elif (key == 'k' or key == 'K'):
            keystrokes += str(key)
            keystrokes += "\n"
            ksNumber += 1
            # Put "Chapter 2" in the play-queue.
            # sound_q.put(ks_GLOBAL.CH_NAME_SO_LIST[1])
            player.on_button(2)

        # Button "3"
        elif (key == 'l' or key == 'L'):
            keystrokes += str(key)
            keystrokes += "\n"
            ksNumber += 1
            # Put all of the text for the chapter on the play-queue.
            # for s_obj in ks_GLOBAL.READ_ITEM_SO_LIST:
            #     sound_q.put(s_obj)
            if isinstance(player.mode(), ks_o.InfoMode):
                player.on_button(3)
            else:
                player.push_mode(ks_o.InfoMode(player))
        # Button "4"
        elif (key == ';' or key == ':'):
            keystrokes += str(key)
            keystrokes += "\n"
            ksNumber += 1
            # Stop any currently playing sounds, and clear the queue.
            # ks_stop.stop_sounds(sound_q, log_q, hold_q_e, stop_play_e)
            # # Play " Chapter 4"
            # sound_q.put(ks_GLOBAL.CH_NAME_SO_LIST[3])
            # break # Break out of the loop.
            try:
                player.pop_mode()
            except ValueError:
                end = time.time()
                elapsed = end - begin
                write_file(begin, elapsed,keystrokes,ksNumber)
                break

        else:
            # This should not actually occur in normal usage.
            print("Press <SPACE>, <J>, <K>, <L>, or <;>. Press <;> to quit.")


################################################################################
# Set up and start the program.
################################################################################

# This if-statement is an idiom that is used to delimit code that should only be
# run if the program is run, and should not be run if the module is imported.

if __name__ == '__main__':

    # Load sounds.
    # ks_load.load_sounds()

    # Create a sound-objects-to-play queue.
    sound_queue = multiprocessing.JoinableQueue()
    # Create a timestamp-log queue.
    # (If logging is to be done, it must be done with a JoinableQueue() because
    #   there is no way to directly recturn data from the play_sounds() subprocess.)
    # The var is initialized to 'None' to suppress the logging.
    # log_queue = multiprocessing.JoinableQueue()
    log_queue = None

    # Create a "hold the queue" message-passing event.
    # Permits the keystroke-catching process to tell the sound-playing process to
    #   temporarily stop removing items from the queue.
    hold_queue_e = multiprocessing.Event()

    # Create a "stop-playing" message-passing event.
    # Permits the keystroke-catching process to tell the sound-playing process to
    #   stop playing a sound that may be playing.
    stop_playing_e = multiprocessing.Event()

    # Launch the play_sounds() consumer process in a second process.
    cons_p1 = multiprocessing.Process(target=ks_play.play_sounds,
                args=(sound_queue, log_queue, hold_queue_e, stop_playing_e))
    cons_p1.daemon=True
    cons_p1.start()

    # Start up the keystroke catcher, in the main process, not in a new process.
    # The main program sits on this line until the "break" from keystroke_processor()
    keystroke_processor(sound_queue, log_queue, hold_queue_e, stop_playing_e)

    # After returning from the keystroke catching and processing loop...
    # Block (stop) this main process until all queue items have be processed by
    #   the consumer process.
    sound_queue.join()

    # Output the timestamp-log queue if log_queue was initialized as a JoinableQueue.
    ks_log.output_log(log_queue)
