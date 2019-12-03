################################################################################
# ks_log - Functions to log events for debugging.
################################################################################
# Used by key_sounds_menu.py, a program that uses keystrokes to play wave files.
# Written by A.Hornof - 10/13/2019
################################################################################

# Packages
import multiprocessing
import simpleaudio
import time

# Set a start time in case timestamp logging is turned on.
START_TIME = time.time()

################################################################################
# Log events.
# Create an event log with a timestamp. Add it to the multiprocessing.JoinableQueue().
# The queue name gets passed in. It seems too risky to try to access it globally.
# In the tuple: The first element is a string, and the second element is a float.
################################################################################

def log(event_text, log_queue):
		# Logging can be turned off by setting the log_queue to 'None'.
    if log_queue:
        log_queue.put((event_text, time.time())) # A tuple (an immutable list)
    # If the queue name is 'False' or 'None', then no log data are recorded.
    else:
        pass

################################################################################
# output_log()
################################################################################
# Called from the main thread iff a log_queue was set.
# Creates a thread to access and output that queue.

def output_log(log_queue):

	# If log_queue was initialied as a JoinableQueue(), and thus
	#   filled with timestamp logs...
    #   (If the queue was set to 'None' then logging was suppressed.)
    if log_queue:

        # Start the process to show the JoinableQueued timestamped log items.
        cons_p2 = multiprocessing.Process(target=output_timestamps_JoinableQueue,
                    args=(log_queue,))
        cons_p2.daemon=True
        cons_p2.start()

        # Block the main thread until the log_timestamp_queue items are output.
        log_queue.join()


################################################################################
# Output the timestamp logs.
################################################################################

# Go through the JoinableQueue of play_sounds timestamps (the input parameter q).
# As soon as the queue is empty, this thread will self-terminate.
# THIS RUNS IN A SEPARATE THIRD THREAD.
def output_timestamps_JoinableQueue(q):
    while (True):
        # Get the timestamp tuple
        t_stamp = q.get()
        time_stamp = '{0:8.5f}'.format( t_stamp[1] - START_TIME )
        print (t_stamp[0], '\t', time_stamp)
        q.task_done()
