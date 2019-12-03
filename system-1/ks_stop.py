################################################################################
# ks_stop - Function to stop sounds.
################################################################################
# Used by key_sounds_menu.py, a program that uses keystrokes to play wave files.
# Written by A.Hornof - 10/13/2019
################################################################################

# Packages
import time

# Local imports - "ks" stands for "key_sounds".
import ks_log

################################################################################
# stop_sounds() - Helper function to stop the sounds and clear the event queue.
# ONLY CALLED FROM, AND ONLY RUNS IN, THE MAIN keystroke_processor() THREAD.
# NOT CALLED FROM, AND DOES NOT RUN IN, THE play_sounds() THREAD.
# Inputs: sound_q: a JoinableQueue of WaveObjects
#         hold_queue_e: a stop-modifying-the-queue multiprocessing.Event
#         stop_playing_e: a stop-playing-sounds multiprocessing.Event
################################################################################
def stop_sounds(sound_q, log_q, hold_queue_e, stop_playing_e):

    ks_log.log("stop_sounds: START", log_q)

    # Set an event to stop any other currently playing.
    stop_playing_e.set()

    # Set an event to hold the queue of sounds so play_sounds can access it.
    hold_queue_e.set()

    ks_log.log("stop_sounds: after setting stop and hold events", log_q)

    while not sound_q.empty() :

        ks_log.log("stop_sounds: 1. about to remove a sound", log_q)

        # Remove, but do not play, the next sound in the queue.
        s_obj_removed = sound_q.get().name
        sound_q.task_done()

        ks_log.log("stop_sounds: 2. just removed sound " + s_obj_removed, log_q)

        # A tiny delay is needed, evidently for queue.empty() to get updated.
        time.sleep(0.001)

    # Set events so that play_sounds() can access the queue and continue playing.
    hold_queue_e.clear()

    ks_log.log("stop_sounds: END", log_q)

