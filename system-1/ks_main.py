################################################################################
# ks_main.py
# Original code from A. Hornof - October 13th 2019
#
# Last Edited by Mamtaj Akter Oct. 27, 2019
#
#
# A sample program to select an auditory book and then scroll through the chapter
# list of that book and either continue playing the list of read items or to move
# through the list of read items single keystrokes.
#
################################################################################

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
import multiprocessing  # standard python package
import time            # standard python package
import readchar  # version 2.0.1
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

# Local imports - "ks" stands for "key_sounds".
import ks_load


# Global variables

# Used for loading own files.
WAVE_DIR_PROVIDED = "wav_files_provided/"
NORMAN_DIR = "Book_01_norman/"
MY_WAVE_DIR = "project_wav_files/"
MISC_DIR = "others/"
BOOK_NUMBER_DIR = "book_numbers/"
CHAPTER_NUMBER_DIR = "chapter_numbers/"
PAGE_NUMBER_DIR = "page_numbers/"

READ_ITEMS_NUMBER=62
CHAPTER_NUMBER=6
# Sounds.

################################################################################
# Load sound files.
################################################################################

# BOOK_NUMBER_SO_LIST - book titles put into sound_objects

# I had to put same book title wave files twice, otherwise it was giving error
BOOK_NUMBER_FILENAMES = ("Book_Title.wav", "Book_Title.wav")
BOOK_NUMBER_LOCATION = WAVE_DIR_PROVIDED + NORMAN_DIR
BOOK_NUMBER_SO_LIST = list()
ks_load.load_sound_objects(
    BOOK_NUMBER_FILENAMES, BOOK_NUMBER_LOCATION, BOOK_NUMBER_SO_LIST)
BOOK_NUMBER_SO_LIST = tuple(BOOK_NUMBER_SO_LIST)

# CHAPTER_NUMBER_SO_LIST - list of chapter numbers and put into sound_objects

CHAPTER_NUMBER_FILENAMES = ("chapter_one.wav", "chapter_two.wav", "chapter_three.wav", "chapter_four.wav", "chapter_five.wav",
                            "chapter_six.wav", "chapter_seven.wav")
CHAPTER_NUMBER_LOCATION = MY_WAVE_DIR + CHAPTER_NUMBER_DIR
CHAPTER_NUMBER_SO_LIST = list()
ks_load.load_sound_objects(
    CHAPTER_NUMBER_FILENAMES, CHAPTER_NUMBER_LOCATION, CHAPTER_NUMBER_SO_LIST)
CHAPTER_NUMBER_SO_LIST = tuple(CHAPTER_NUMBER_SO_LIST)

# MISC_SO_LIST - list of miscellaneous auditory messages and put into sound-objects

MISC_FILENAMES = ("press_space_to_select.wav", "press_j_to_schroll_backward.wav", "press_k_to_schroll_forward.wav", "press_l_for_help.wav",  "press_sc_to_quit.wav",  "press_l_again_for_help.wav",
                  "press_sc_again_to_quit.wav",     "exiting_program.wav", "not_available.wav", "you_selected.wav", "select_book.wav", "select_chapter.wav", "select_page.wav", "quit_message.wav", "continue_to_read.wav", "Press_J_to_go_to_the_previous_menu.wav", "select_another_chapter.wav", "press_sc_and_j_to_go_back.wav","press_space_to_select_book.wav","press_space_to_select_chapter.wav", "press_j_or_k_to_scroll_books.wav","press_j_or_k_to_scroll_chapters.wav", "press_j_previous_item.wav","press_k_next_item.wav")
MISC_LOCATION = MY_WAVE_DIR + MISC_DIR
MISC_SO_LIST = list()
ks_load.load_sound_objects(MISC_FILENAMES, MISC_LOCATION, MISC_SO_LIST)
MISC_SO_LIST = tuple(MISC_SO_LIST)

# Global Variables of the miscellaneous auditory sound objects

PRESS_SPACE = MISC_SO_LIST[0]
PRESS_J = MISC_SO_LIST[1]
PRESS_K = MISC_SO_LIST[2]
PRESS_L = MISC_SO_LIST[3]
PRESS_SC = MISC_SO_LIST[4]
PRESS_L_AGAIN = MISC_SO_LIST[5]
PRESS_SC_AGAIN = MISC_SO_LIST[6]
EXITING_PROGRAM = MISC_SO_LIST[7]
NOT_AVAILABLE = MISC_SO_LIST[8]
YOU_SELECTED = MISC_SO_LIST[9]
SELECT_BOOK = MISC_SO_LIST[10]
SELECT_CHAPTER = MISC_SO_LIST[11]
SELECT_PAGE = MISC_SO_LIST[12]
QUIT_MESSAGE = MISC_SO_LIST[13]
CONTINUE_READING = MISC_SO_LIST[14]
PRESS_J_PREVIOUS_MENU = MISC_SO_LIST[15]
SELECT_ANOTHER_CHAPTER = MISC_SO_LIST[16]
PRESS_SC_J_TO_GO_BACK = MISC_SO_LIST[17]
PRESS_SPACE_SELECT_BOOK = MISC_SO_LIST[18]
PRESS_SPACE_SELECT_CHAPTER = MISC_SO_LIST[19]
SCROLL_BOOK = MISC_SO_LIST[20]
SCROLL_CHAPTER = MISC_SO_LIST[21]
PREVIOUS_ITEM = MISC_SO_LIST[22]
NEXT_ITEM = MISC_SO_LIST[23]
# For additional global variables, see GLOBAL.py


################################################################################
# Announces the program's current state auditorily to the user, given the state
# AND SOUND_Q parameter. For example, if the state value is 1, the program is in
# "CHAPTER SELECTION STATE", and so, it plays 'Select Chapter' to the user.
################################################################################
def play_current_state(state, sound_q):
    if (state == 0):
        # Announce state for selecting the book
        sound_q.put(SELECT_BOOK)
    elif (state == 1):
        # Announce state for selecting the chapter
        sound_q.put(SELECT_CHAPTER)
    # Ignore any other state passed in

################################################################################
# Plays the help message to the user, preceded by which STATE they are in.
# Invoked when the user presses the help key, in any state.
################################################################################

def play_help(state, sound_q):
    if (state == 0):
        # User in "BOOK SELECTION STATE", precede help messages with 'Select book'\
        sound_q.put(SELECT_BOOK)
        sound_q.put(SCROLL_BOOK)
        sound_q.put(PRESS_L)
        sound_q.put(PRESS_SC)
        sound_q.put(PRESS_SPACE_SELECT_BOOK)
    elif (state == 1):
        # User in "CHAPTER SELECTION STATE", precede help messages with just 'SELECT CHAPTER'
        sound_q.put(SELECT_CHAPTER)
        sound_q.put(SCROLL_CHAPTER)
        sound_q.put(PRESS_L)
        sound_q.put(PRESS_SC)
        sound_q.put(PRESS_SPACE_SELECT_CHAPTER)
    elif (state == 2):
        # User in "CONTINUE READING STATE" , play usual help_messages
        sound_q.put(PREVIOUS_ITEM)
        sound_q.put(NEXT_ITEM)
        sound_q.put(PRESS_L)
        sound_q.put(PRESS_SC)

################################################################################
# Plays the complete Introductory Help Message of the user
# "Press <J> to scroll backward\nPress <K> to scroll forward\n
# Press <L> for help\nPress <;> to quit\nPress <SPACE> to select. "
# preceded with just 'Select Book'
################################################################################
def play_intro(sound_q):
    sound_q.put(SELECT_BOOK)
    sound_q.put(SCROLL_BOOK)
    sound_q.put(PRESS_L)
    sound_q.put(PRESS_SC)
    sound_q.put(PRESS_SPACE_SELECT_BOOK)


################################################################################
# Plays the complete selection of the user - "COntinue to Read",
# the given Book title and then continue reading the read_items sounds of that chapter 2
################################################################################
def play_read_items(bookNumber, chapterNumber, sound_q):
    sound_q.put(CONTINUE_READING)
    sound_q.put(BOOK_NUMBER_SO_LIST[bookNumber])
    # Put all of the text for the chapter 2 on the play-queue.
    for s_obj in ks_GLOBAL.READ_ITEM_SO_LIST:
        sound_q.put(s_obj)

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

    # Initialize the current system state and the book, chapter, read_item variables
    # system state: 0 when the system is at the "START" state and also in
    # "BOOK SELECTION STate"
    #
    systemState = 0
    bookNumber = 0
    chapterNumber = 0
    readItemNumber = 0

    # Play introductory full help message at the beginning of the program
    play_intro(sound_q)

    begin = time.time()
    keystrokes=""
    ksNumber=0
    # Keep looping. Wait for the next keystoke, and process it when it arrives.
    while (True):

        # Wait for the next keystroke.
        key = readchar.readkey()


        # Process each keystroke as specified here.

        # User presses the SELECT key : <SPACE> It leads user to go to the next state
        if (key == ks_GLOBAL.SPACE_BAR):
            keystrokes += str(key)
            keystrokes += "\n"
            ksNumber += 1
            systemState += 1
            # if user is in now in the read_items state, play the "Continue to read,
            # <Book_title> <read_items_of_chapter 2>..."
            if (systemState == 2):
                # if user selects chapter 2
                if (chapterNumber == 1):
                    # Stop any currently playing sounds, and clear the queue.
                    ks_stop.stop_sounds(sound_q, log_q, hold_q_e, stop_play_e)
                    # to continue plaing the read items of chapter 2
                    play_read_items(bookNumber, chapterNumber, sound_q)
                    continue
                # if user selects any other chapter than chapter 2,
                else:
                    # Stop any currently playing sounds, and clear the queue.
                    ks_stop.stop_sounds(sound_q, log_q, hold_q_e, stop_play_e)
                    # Play "NOT_AVAILABLE" and "Press <;> and then press <J> to
                    # go to select another chapter"
                    sound_q.put(NOT_AVAILABLE)
                    sound_q.put(PRESS_SC_J_TO_GO_BACK)
            # Reset the systemState back to 0, when the systemState is more than
            # the CONTINUE READING STATE: 2
            if (systemState > 2):
                systemState = 0
            # Stop any currently playing sounds, and clear the queue.
            ks_stop.stop_sounds(sound_q, log_q, hold_q_e, stop_play_e)
            # Announce the current state to the user
            play_current_state(systemState, sound_q)

        # if user presses <J> : the forward key
        elif (key == 'j' or key == 'J'):

            keystrokes += str(key)
            keystrokes += "\n"
            ksNumber += 1
            # if user in BOOK SELECTION STATE, decrement the bookNumber
            if (systemState == 0):
                bookNumber -= 1
                # ensure book number cant be less than 0
                if(bookNumber < 0):
                    bookNumber = 1
                # Stop any currently playing sounds, and clear the queue.
                ks_stop.stop_sounds(sound_q, log_q, hold_q_e, stop_play_e)
                # Put current book's name in the play-queue.
                sound_q.put(BOOK_NUMBER_SO_LIST[bookNumber])
            # if the user is in the state of "CHAPTER SELECTION STATE" then decrease
            # the chapter number
            elif (systemState == 1):
                chapterNumber -= 1
                # chapter number cant be less than 0
                if(chapterNumber < 0):
                    chapterNumber = CHAPTER_NUMBER
                # Stop any currently playing sounds, and clear the queue.
                ks_stop.stop_sounds(sound_q, log_q, hold_q_e, stop_play_e)
                # Put current chapter's name in the play-queue.
                sound_q.put(ks_GLOBAL.CH_NAME_SO_LIST[chapterNumber])
           # if the user is in the state of CONTINUE READING STATE then user can
           # also schroll to previous read_items to listen that
            elif (systemState == 2):
                if (chapterNumber == 1):
                    readItemNumber -= 1
                    # read Item number cant be less than 0, chapter 2 has 62 read items
                    if(readItemNumber < 0):
                        readItemNumber = READ_ITEMS_NUMBER
                    # Stop any currently playing sounds, and clear the queue.
                    ks_stop.stop_sounds(sound_q, log_q, hold_q_e, stop_play_e)
                    # start reading from the previous read items  in the play-queue.
                    for s_obj in ks_GLOBAL.READ_ITEM_SO_LIST[readItemNumber:]:
                        sound_q.put(s_obj)

        # if user presses <K> : the forward key
        elif (key == 'k' or key == 'K'):

            keystrokes += str(key)
            keystrokes += "\n"
            ksNumber += 1
            # if user in BOOK SELECTION STATE, increment the bookNumber
            if (systemState == 0):
                bookNumber += 1
                # book number cant be more than 1
                if(bookNumber > 1):
                    bookNumber = 0
                # Stop any currently playing sounds, and clear the queue.
                ks_stop.stop_sounds(sound_q, log_q, hold_q_e, stop_play_e)
                # Put current book's name in the play-queue.
                sound_q.put(BOOK_NUMBER_SO_LIST[bookNumber])
            # if the user is in the CHAPTER SELECTION STATE then increase the chapter number
            elif (systemState == 1):
                chapterNumber += 1
                # chapter number cant be more than 6, because the Norman book has only 7 chapters
                if(chapterNumber > CHAPTER_NUMBER):
                    chapterNumber = 0
                # Stop any currently playing sounds, and clear the queue.
                ks_stop.stop_sounds(sound_q, log_q, hold_q_e, stop_play_e)
                # Put current chapter's name in the play-queue.
                sound_q.put(ks_GLOBAL.CH_NAME_SO_LIST[chapterNumber])
           # if the user is in the CONTINUE READING STATE then schroll to next read_items
            elif (systemState == 2):
                # if it is chapter 2, then increment the read items
                if (chapterNumber == 1):
                    readItemNumber += 1
                    # read Item number cant be more than 62
                    if(readItemNumber > READ_ITEMS_NUMBER):
                        readItemNumber = 0
                    # Stop any currently playing sounds, and clear the queue.
                    ks_stop.stop_sounds(sound_q, log_q, hold_q_e, stop_play_e)
                    # start reading from next read items  in the play-queue.
                    for s_obj in ks_GLOBAL.READ_ITEM_SO_LIST[readItemNumber:]:
                        sound_q.put(s_obj)

        # User presses the help key: <L>
        elif (key == 'l' or key == 'L'):
            keystrokes += str(key)
            keystrokes += "\n"
            ksNumber += 1
            # Stop any currently playing sounds, and clear the queue.
            ks_stop.stop_sounds(sound_q, log_q, hold_q_e, stop_play_e)
            # play help messages according to the current state
            play_help(systemState, sound_q)

        # User presses QUIT key : <;>
        elif (key == ';'):
            keystrokes += str(key)
            keystrokes += "\n"
            ksNumber += 1
            # Stop any currently playing sounds, and clear the queue.
            ks_stop.stop_sounds(sound_q, log_q, hold_q_e, stop_play_e)
            # if user is in either CHAPTER SELECTION STATE or CONTINUE READING STATE,
            # play "Press <;> again to quit; press <J> To go to the previous menu")
            if (systemState == 1 or systemState == 2):
                sound_q.put(PRESS_SC_AGAIN)
                sound_q.put(PRESS_J_PREVIOUS_MENU)
            # if user is in BOOK SELECTION STATE ,
            # play just "Press <;> again to quit;")
            else:
                sound_q.put(PRESS_SC_AGAIN)
            # Wait for the next keystroke.
            key = readchar.readkey()
            # user presses QUIT key <;> again
            if (key == ';'):
                keystrokes += str(key)
                keystrokes += "\n"
                ksNumber += 1


                # Stop any currently playing sounds, and clear the queue.
                ks_stop.stop_sounds(sound_q, log_q, hold_q_e, stop_play_e)
                # Provide a audio prompt for exiting the program
                sound_q.put(EXITING_PROGRAM)
                end = time.time()
                elapsed = end - begin
                write_file(begin, elapsed,keystrokes,ksNumber)
                break  # Break out of the loop.
            elif(key == 'J' or key == 'j'):
                keystrokes += str(key)
                keystrokes += "\n"
                ksNumber += 1
                # if user is in either CHAPTER SELECTION STATE or CONTINUE READING STATE,
                # lead the user to previous state, and instruct what to select"
                # for example, if user is in CONTINUE READING STATE, this <J> key will take
                # user to the previous state that is CHAPTER SELECTION STATE
                if (systemState == 1 or systemState == 2):
                    systemState -= 1
                    # Stop any currently playing sounds, and clear the queue.
                    ks_stop.stop_sounds(sound_q, log_q, hold_q_e, stop_play_e)
                    # Announce the current state to the user
                    play_current_state(systemState, sound_q)
            ## resolved the matter 2. Funtionality "Some keypresses resulted in no response, such as pressing a non-semi-colon after pressing the semicolon to quit"
            ## this will handle when user presses L/J/K/SPACE after a <;>, give them help message with the current state for what to select
            elif((systemState==0 and (key == 'J' or key == 'j')) or key == 'K' or key == 'k' or key == 'L' or key == 'l'or key == ks_GLOBAL.SPACE_BAR):
                keystrokes += str(key)
                keystrokes += "\n"
                ksNumber += 1
                # Stop any currently playing sounds, and clear the queue.
                ks_stop.stop_sounds(sound_q, log_q, hold_q_e, stop_play_e)
                # play help messages according to the current state
                sound_q.put(PRESS_L)

        # the user presses any other key
        else:
            # Wait for the next keystroke.
            key = readchar.readkey()

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
    cons_p1.daemon = True
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
