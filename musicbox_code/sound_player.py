# plays mp3 files

from note_led_row import NoteLedRow
from sample_loader import SampleLoader
from notes import Notes
import os

debug = False

class SoundPlayer:

    global debug

    def __init__(self, sample_sheet:str, mute=False):

        # will mute the playing of sound files
        self.mute = mute

        # the sample sheet to play samples from
        self.sample_sheet = sample_sheet

        # list of the notes objs from the current beat
        self.notes_of_current_beat = [Notes]

        # this should be generated by the sampleloader
        # maps sample names to actual files to be played
        # can be used to map a sample name to a file, if a note obj has no char,
        # but has one or more sample names
        self.sample_map_by_name = {str:str}

        # a dict of dicts with the controller number or name as key
        # eg. 'controller01' 'backing' 'default'
        # dicts holding sample mappings should be sample char (the one recieved from the controller
        # and the full path to the audio file to be played
        self.sample_maps_by_controller_and_chars = {str : {str:''}}


    def load_samples_from_sample_sheet(self):
        sample_loader = SampleLoader(sample_sheet_to_load=self.sample_sheet)
        sample_tuple = sample_loader.load_sample_sheet_and_return_tuple()
        self.sample_map_by_name = sample_tuple[0]
        self.sample_maps_by_controller_and_chars = sample_tuple[1]

    def extract_notes(self, led_note_row:list):
        for container in led_note_row:
            self.notes_of_current_beat.append(container.notes)

    def play_notes(self):
        # play samples of all note objects
        for note_obj in self.notes_of_current_beat:
            # if the note obj has sample names use those to play samples, otherwise use the char
            if len(note_obj.samples) > 0:  # play sample by sample name in samples list
                if debug:
                    print('\tPlaying sample by sample_name.')
                for sample in note_obj.samples:
                    self.play_sample(filename_with_relative_path=self.sample_map_by_name[sample])
            elif not (note_obj.char == ''):  # play sample by char
                if debug:
                    print('\tPlaying sample by char.')
                # get the right dir to play notes from
                if note_obj.owner in self.sample_maps_by_controller_and_chars.keys():
                    sample_dir = self.sample_maps_by_controller_and_chars[note_obj.owner]
                else: # if no controller specific subsection is defined, then play from default
                    sample_dir = self.sample_maps_by_controller_and_chars['default']
                sample_to_play = sample_dir[note_obj.char]
                self.play_sample(filename_with_relative_path=sample_to_play)
            else:  # if obj has no samples attached, do nothing
                if debug:
                    print('\tNotes obj has no samples attached.')

    def play_sample(self, filename_with_relative_path:str):
        if debug:
            print('Playing sample: ', filename_with_relative_path)
        if not self.mute:
            # use SOX player to play sample
            os.system('play {} & disown'.format(filename_with_relative_path))


    def play_samples_of_beat(self, led_note_row:NoteLedRow):
        row = led_note_row.row
        # reset the lists holding sample data
        self.notes_of_current_beat = []

        # extract the samples to be played
        self.extract_notes(led_note_row=row)

        if debug:
            print('\nPlaying samples ...')

        # play the samples of the note objs in this beat
        self.play_notes()
