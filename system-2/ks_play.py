################################################################################
# ks_play - Function to play sounds and stop sounds.
################################################################################
# Used by key_sounds_menu.py, a program that uses keystrokes to play wave files.
# Written by A.Hornof - 10/13/2019
################################################################################

# Packages
import time

# Local imports - "ks" stands for "key_sounds".
import ks_log

################################################################################
# Function to play sounds
# This is the "consumer". It runs in a separate thread.
# Inputs: input_q: a JoinableQueue of sound_objects
#         input_q: a JoinableQueue for logging
#         hold_queue_e: a stop-modifying-the-queue multiprocessing.Event
#         stop_playing_e: a stop-playing-sounds multiprocessing.Event
################################################################################
def play_sounds(input_q, log_q, hold_queue_e, stop_playing_e):

    ks_log.log("SOUNDS: START", log_q)

    # Loop waiting for a sound to appear in the queue.
    while True:

        # Only continue to get the next item from the queue if the keystroke_processor
        #    is NOT holding the queue to clear it...
        #   (This could occur if a sound is stopped and it loops back around to here.)
        if not hold_queue_e.is_set():

            ks_log.log("SOUNDS: WAITING for queue item", log_q)

            # Wait here for a sound object to get put into the play-queue.
            sound_obj = input_q.get()  # Get the next sound from the queue.
            sound_name = sound_obj.name

            # Clear a stop-playing event() if one is hanging around, uncleared.
            stop_playing_e.clear()

            ks_log.log("SOUNDS: got sound " + sound_name + " from queue", log_q)

            # If the keystroke_processor is holding the queue to clear it...
            if hold_queue_e.is_set():

                # Do nothing with the sound object. It will be cleared after this if-then loop.
                pass

                ks_log.log("SOUNDS: DUMPING sound " + sound_name + "without playing it", log_q)

            # Else the keystroke_processor is NOT holding the queue, so proceed...
            else:

                # Start playing the sound.
                object_playing = sound_obj.waveobject.play()

                ks_log.log("SOUNDS: START sound " + sound_name, log_q)

                # Loop here playing the sound until it is done, unless a stop-playing event was set.
                while object_playing.is_playing():  # and (not input_clear_e.is_set()):

                    # ks_log.log("SOUNDS: playing " + sound_name, log_q)

                    # If a stop-playing event was set.
                    if stop_playing_e.is_set():
                        # Stop playing the sound.
                        object_playing.stop()  # Stop playing the sound.
                        ks_log.log("SOUNDS: STOP sounded " + sound_name + " - stop event", log_q)
                        # Clear the stop-playing event()
                        stop_playing_e.clear()
                        break

                    # Wait 1/100 of a second to ease the burden on the CPU.
                    time.sleep(0.01)

                ks_log.log("SOUNDS: STOP sound " + sound_name + " - finished playing", log_q)

                # End of if-then

            # Signal that this process is done with the sound-object in the queue.
            #   regardless of whether anything was done with the sound-object.
            input_q.task_done()

            ks_log.log('SOUNDS: "task done" for sound ' + sound_name + " - finished playing", log_q)

    ks_log.log("SOUNDS: END", log_q)
    
