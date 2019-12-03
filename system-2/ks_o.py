################################################################################
# ks_o - key_sounds objects - Classes to hold sound objects and other things.
# Used by ks_main.py, a program that uses keystrokes to play wave files, one
#   sound per keystroke.
# A.Hornof - 10-13-2019

# Modified by Derek Strobel - 10-20-2019
################################################################################

# Packages
import simpleaudio # simpleaudio-1.0.2
import ks_stop
import ks_log
import os
import re
################################################################################
# A sound_object has the following member variables:
#   waveobject: a simpleaudio WaveObject, which can get played with play()
#   name: a string of the filename (including the ".wav" extension)
################################################################################

class sound_object:

    def __init__(self, path, filename, page=None, cc=None):
        # Create a simpleaudio.WaveObject for playing the sound using the filename.
        self.waveobject = simpleaudio.WaveObject.from_wave_file(os.path.join(path, filename))
        # object name
        self.name = filename # For tracing and debugging.
        self.page = page # page chapter, and cc added for filtering capability
        self.cc = cc

    # define equality operator to enable "in"
    def __eq__(self, other):
        return self.name == other.name
################################################################################
# Student-defined classes below.
################################################################################

class SFX:
    '''
    Helper class containing simple sound effects.
    '''
    filenames = ('ascend', 'descend', 'pause',
        'error', 'ascend_small', 'descend_small', 'unsupplied_audio', 'infomenu',
        'choose_a_book', 'choose_a_chapter', 'l_for_help', 'controls',
        'current_book_title', 'current_chapter_title', "exit_help")

    def __init__(self, path):
        self.loaddir(path)

    def loaddir(self, path):
        # Load files as attributes of the SFX object; allows for sfx.ascend
        for f in self.filenames:
            setattr(self, f, sound_object(path, '{}.wav'.format(f)))



class Button:
    '''
    Static enum class to label buttons.
    '''
    PLAYPAUSE  = 0
    SKIPB      = 1
    SKIPF      = 2
    INFO       = 3
    MENU       = 4

class Audiobook:

    class AudiobookChapter:
        def __init__(self, nameSound):
            self.nameSound = nameSound
            self.data = {}

        def push(self, seq, sentence):
            self.data[seq] = sentence

    '''
    Data structure organizing all of the audio files for a particular audiobook.
    '''
    def __init__(self, path):
        self.path = path
        self.chapters = {}
        self.title=None
        self._load_files()
        self.state = {
            'sequence': 0, # The sequence number of the current book segment (e.g. 1 for '001')
            'chapter': 0, # The chapter number of the current book segment (e.g. 1 for '001')
            'page': 0, # The page number of the current book segment (e.g. 34)
        }
        self.state['chapter'] = min(self.chapters.keys())

    def __repr__(self):
        return 'Audiobook(title={}, chapters={})'.format(self.title, self.chapters)

    # book loader function (reimplemented to support arbitrary book paths)
    def _load_files(self):
        # load book title
        self.title = sound_object(self.path, 'Book_Title.wav')

        # load all files from each chapter
        tcPath = os.path.join(self.path, 'Text_Content')
        for chapter in os.listdir(tcPath):
            # chapterData = {'name': None, 'data': {}}
            if chapter.startswith('.'):
                continue
            # load chapter title audio file
            chapterNameSound = sound_object(os.path.join(self.path, 'Chapter_Names'), '{}.wav'.format(chapter))
            chapterData = self.AudiobookChapter(chapterNameSound)
            # chTitleFile = os.path.join(self.path, 'Chapter_Names', '{}.wav', chapter)
            mcn = re.search('Ch(\d{2})', chapter)
            if mcn is not None:
                ch_num = mcn.groups()[0]
            else:
                raise ValueError('Unable to parse chapter number from chapter "{}"'.format(chapter))
            # else:
            #     raise ValueError('No chapter title file found for chapter {}'.format(chapter))
            # load chapter text content
            chPath = os.path.join(tcPath, chapter)
            for sentence in os.listdir(chPath):
                if chapter.startswith('.'):
                    continue
                m = re.search('([0-9]{3})_(CN|SH|TS|RP)_([0-9]{2})\.wav', sentence)
                if m is not None:
                    # create sound_object with audio data
                    seq, cc, page = m.groups()
                    chapterData.data[int(seq)] = sound_object(chPath, sentence, int(page), cc)
            self.chapters[int(ch_num)] = chapterData


class AudiobookPlayer:
    '''
    The main controller class of the system.
    @param books: a list of paths to book audio file directories
    '''
    def __init__(self, books, sound_q, hold_q_e, stop_q_e, log_q=None):
        self.mode_stack = [MainMenuMode(self)] # Mode selection is implemented as a stack, to facilitate "back" functionality
        self.books = [Audiobook(b) for b in books]
        self.sound_q = sound_q
        self.log_q = log_q
        self.hold_q_e = hold_q_e
        self.stop_q_e = stop_q_e
        self.sfx = SFX('sfx/')
        self.book_index = 0
        self.book = self.books[0] if 0 < len(self.books) else None
        self.mode().on_enter()

    def stop_and_clear(self):
        ks_stop.stop_sounds(self.sound_q, self.log_q, self.hold_q_e, self.stop_q_e)

    def play(self, sound):
        self.sound_q.put(sound)

    def mode(self):
        return self.mode_stack[-1]

    def push_mode(self, mode, sound=True):
        '''
        (AudiobookMode, sound_object or bool) -> None
        if sound is True, an ascend tone is played.
        if sound is a sound_object, sound is played.
        '''
        sound = self.sfx.ascend if sound is True else sound
        self.stop_and_clear()
        if sound:
            self.play(sound)
        self.mode().on_exit()
        self.mode_stack.append(mode)
        self.mode().on_enter()

    def pop_mode(self, sound=True):
        '''
        (sound_object or bool) -> None
        if sound is True, a descend tone is played.
        if sound is a sound_object, sound is played.
        '''
        sound = self.sfx.descend if sound is True else sound
        self.stop_and_clear()
        if sound:
            self.play(sound)

        if len(self.mode_stack) > 1:
            self.mode().on_exit()
            self.mode_stack.pop()
            self.mode().on_enter()
        else:
            raise ValueError('Mode Stack Empty')

    def on_button(self, i):
        self.mode().on_button(i)

class AudiobookMode:
    '''
    Abstract class representing a mode of the system and its behaviour
    '''
    def __init__(self, player):
        self.player = player

    def on_enter(self):
        '''
        Implement to trigger any events which always occur while entering this state (e.g. sound effects)
        '''
        pass

    def on_exit(self):
        '''
        Implement to trigger any events which always occur while exiting this state (e.g. sound effects)
        '''
        pass

    def on_button(self, b):
        '''
        Implement to trigger an event upon an actuation of button {b} from within this mode
        '''
        if b is Button.PLAYPAUSE:
            pass
        elif b is Button.SKIPF:
            pass
        elif b is Button.SKIPB:
            pass
        elif b is Button.INFO:
            pass


class MainMenuMode(AudiobookMode):
    def on_enter(self):
        ks_log.log('Entered MainMenuMode', self.player.log_q)
        self.player.play(self.player.sfx.choose_a_book)
        self.player.play(self.player.sfx.l_for_help)

    def on_button(self, b):
        if b is Button.PLAYPAUSE:
            self.player.push_mode(PausedMode(self.player))
        elif b is Button.SKIPF or b is Button.SKIPB:
            #skip forward or backward a book
            #get next book number
            cur_book = self.player.book_index
            next_book = cur_book + 1 if b is Button.SKIPF else cur_book - 1
            next_book = max(0, next_book)
            # get next book title sound or error sound if out of bounds

            try:
                next_book_title = self.player.books[next_book].title
                self.player.book_index = next_book
            except IndexError:
                if b is Button.SKIPB:
                    next_book_title = self.player.books[cur_book].title
                else:
                    next_book_title = self.player.sfx.error
            # play next book title sound
            self.player.stop_and_clear()
            self.player.play(next_book_title)
        elif b is Button.INFO:
            pass

class PausedMode(AudiobookMode):
    '''PausedMode
    PausedMode describes a state in which continuous audio playback of the selected
    book is paused. When in PausedMode, a user can skip through the book with high granularity;
    that is to say, at the chapter level.
    '''
    def on_enter(self):
        ks_log.log('Entered PausedMode', self.player.log_q)
        self.player.play(self.player.sfx.choose_a_chapter)
        self.player.play(self.player.sfx.l_for_help)
        # player.sound_q.put() # play pause sound effect

    def on_button(self, b):
        if b is Button.PLAYPAUSE:
            self.player.push_mode(PlayMode(self.player), sound=self.player.sfx.ascend_small)
        elif b is Button.SKIPF or b is Button.SKIPB:
            #skip forward or backward a chapter
            #get next chapter number
            cur_ch = self.player.book.state['chapter']
            next_ch = cur_ch + 1 if b is Button.SKIPF else cur_ch - 1
            # get next chapter title sound or error sound if out of bounds
            try:
                # next_ch_sound = self.player.book.chapter_names[next_ch]
                next_ch_sound = self.player.book.chapters[next_ch].nameSound
                self.player.book.state['chapter'] = next_ch
            except KeyError:
                if b is Button.SKIPB:
                    next_ch_sound = self.player.book.chapters[cur_ch].nameSound
                else:
                    next_ch_sound = self.player.sfx.error
            # play next chapter title sound
            self.player.stop_and_clear()
            self.player.play(next_ch_sound)

        elif b is Button.INFO:
            pass


class PlayMode(AudiobookMode):
    ''' PlayMode
    The primary mode used to play the bulk of audiobook content.
    On enter, this mode enqueues all audiobook content past the
    audiobook's current saved state.
    '''
    def on_enter(self):
        ch = self.player.book.state['chapter']
        for s in sorted(self.player.book.chapters[ch].data.keys()):
            if s >= self.player.book.state['sequence']:
                self.player.sound_q.put(self.player.book.chapters[ch].data[s])

    # def on_exit(self):
    #     ch = self.player.book.state['chapter']
    #     # print(dir(self.player.sound_q))
    #     print(self.player.sound_q.qsize())
    #     # seq = len(self.player.book.chapters[ch].data.keys()) - len(self.player.sound_q._unfinished_tasks)
    #     # print(seq)

    def on_button(self, b):
        if b is Button.PLAYPAUSE:
            self.player.pop_mode(sound=self.player.sfx.pause)
            if not isinstance(self.player.mode(), PausedMode):
                raise ValueError('PauseMode should always be directly beneath PlayMode in mode stack; stack ',
                    str(self.player.mode_stack))
        elif b is Button.SKIPF:
            pass
        elif b is Button.SKIPB:
            pass
        elif b is Button.INFO:
            pass

class InfoMode(AudiobookMode):
    def on_enter(self):
        self.player.play(self.player.sfx.infomenu)

    def on_button(self, b):
        '''
        Implement to trigger an event upon an actuation of button {b} from within this mode
        '''
        if b is Button.SKIPB:
            # controls
            self.player.stop_and_clear()
            self.player.play(self.player.sfx.controls)
        elif b is Button.SKIPF:
            # book information
            self.player.stop_and_clear()
            self.player.play(self.player.sfx.current_book_title)
            self.player.play(self.player.book.title)
            self.player.play(self.player.sfx.current_chapter_title)
            self.player.play(self.player.book.chapters[self.player.book.state['chapter']].nameSound )
            pass
        elif b is Button.INFO:
            self.player.stop_and_clear()
            self.on_enter()
