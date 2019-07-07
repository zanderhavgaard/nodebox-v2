from led_controller import LedController
from serial_radio_interface import SerialRadioInterface
from note_led_row import NoteLedRow
from note_led_container import NoteLedContainer
from serial_message_parser import SerialMessageParser
from serial_message import SerialMessage
from sound_player import SoundPlayer
from backing_track_loader import BackingTrackLoader
import time

# prints debug messages
debug = False
# prints all led/note values for each beat
debug_print_all_values = False

class MusicBoxController:

    global debug, debug_print_all_values

    def __init__(self):

        #  ___ ___ _____ _____ ___ _  _  ___ ___
        # / __| __|_   _|_   _|_ _| \| |/ __/ __|
        # \__ \ _|  | |   | |  | || .` | (_ \__ \
        # |___/___| |_|   |_| |___|_|\_|\___|___/

        # the current position in the beat
        self.beat = 0

        # the number of beats to go through, should be something divisible by 4 eg: 4, 8, 16
        self.number_of_beats = 8

        # beats per minute, should be a float
        # self.bpm = 90.0
        self.bpm = 60.0

        # the length of each beat in ms
        self.beat_length = 0

        # the sample sheet to be used eg. 'default01' located in ../sample_sheets/
        self.sample_sheet = 'test_sample_sheet'

        # mutes the soundplayer
        self.mute = False

        # plays samples in each beat
        self.sound_player = SoundPlayer(sample_sheet=self.sample_sheet, mute=self.mute)

        # name of the xml file of the backing track to be loaded located in ../backing_tracks/
        self.backing_track_file = 'simple_drums_backing_track'
        # loads a backing track
        self.backing_track_loader = BackingTrackLoader(backing_track_file=self.backing_track_file)

        # for debug
        # self.backing_track_loader.print_xml_structure()

        # set the number of led strips and the number of leds per strip,
        # number of led strips should be the same as the number of beats
        self.number_of_led_strips = 8
        self.leds_per_strip = 5

        # highlight current beat or only light up the current beat
        # self.display_mode = 'only_current'
        self.display_mode = 'highlight'

        # initialize led controller and serial interface
        self.led_controller = LedController(display_mode=self.display_mode,
                                            number_of_led_strips=self.number_of_led_strips,
                                            number_of_leds_per_strip=self.leds_per_strip)
        self.serial_interface = SerialRadioInterface()
        self.serial_parser = SerialMessageParser()

        # we hold incoming messages as a list of strings that we then send to the parser
        self.messages_to_be_parsed = []

        # the messages that have been parsed and are ready to be assigned
        self.parsed_messages = []

        # initialize the list containing the led rows
        self.led_note_rows = []

        # create the note_led_rows and initialize the note_led_containers
        for i in range(self.number_of_led_strips):
            self.led_note_rows.append(NoteLedRow(leds_per_strip=self.leds_per_strip, strip_number=i))

        # run setup once on start-up
        # self.setup()

        # start infinite loop executing the code
        # self.main_loop()

    #  ___ ___ _____ _   _ ___
    # / __| __|_   _| | | | _ \
    # \__ \ _|  | | | |_| |  _/
    # |___/___| |_|  \___/|_|

    def setup(self):
        print('*** Setting up NodeBox ***')

        if debug:
            print('Initilizing led strip...')

        # start the leds
        self.led_controller.initialize_led_strip()

        # we start the beat on count 0 for simplicity's sake
        self.beat = 0

        # get the beat length in ms
        self.beat_length = self.calculate_beat_length()

        if debug:
            print('Calculated beat length: ', self.beat_length)

        if debug:
            print('initializing the first row of leds')

        # load in the backing track and turn on the first row of leds
        self.initialize_first_led_row()

        if debug:
            print('Loading sample_sheet...')

        self.sound_player.load_samples_from_sample_sheet()

        if debug:
            print('Loading the backing track...')

        self.load_backing_track()

        self.assign_first_row_containers()

        print('\nDone setting up the NodeBox.\n')

        # for debug shows contents of all leds and notes
        self.debug_print_all_led_note_data()

    #  _    ___   ___  ___
    # | |  / _ \ / _ \| _ \
    # | |_| (_) | (_) |  _/
    # |____\___/ \___/|_|

    def main_loop(self):
        while True:
            # iterate the beat
            self.iterate_beat_count()
            print('Beat # {}'.format(self.beat))

            if debug:
                print('Recieving messages...')

            # first receive serial messages from the interface
            self.recieve_serial_messages()

            if debug:
                print('Recieved messages.')

            if debug:
                print('Parsing messages...')

            # then we parse the received messages and act upon them
            self.parse_serial_messages()

            if debug:
                print('Done parsing messages.')

            if debug:
                print('Assigning parsed messages...')

            self.assign_parsed_messages()

            if debug:
                print('Done assigning parsed messages.')

            if debug:
                print('Will now update the led strip...')

            # update the colors of the led strips
            self.update_led_strips()

            if debug:
                print('Done updating led strip.')

            if debug:
                print('Will now play the samples of the current beat')

            # play the samples attached to this beat
            self.play_samples_of_beat()

            if debug:
                print('Done playing samples.')

            if debug:
                print('Will now wait beat length...')
                print('Beat length: ', self.beat_length)

            # wait the length of the beat
            self.wait_beat_length()

            if debug:
                print('Done waiting beat length, will now iterate to next beat...')

            if debug:
                print('End of beat cycle\n')

            if debug_print_all_values:
                self.debug_print_all_led_note_data()

            # when we reach the last beat we start over
            if self.beat == self.number_of_beats:
                self.beat = 0

    #  __  __ ___ _____ _  _  ___  ___  ___
    # |  \/  | __|_   _| || |/ _ \|   \/ __|
    # | |\/| | _|  | | | __ | (_) | |) \__ \
    # |_|  |_|___| |_| |_||_|\___/|___/|___/

    # calculate how long a delay there should be before the beat iterates
    # and the new tones will be played, returns seconds as floats
    def calculate_beat_length(self):
        return 60.0 / self.bpm

    # set all the container objs as assigned of the backing track
    def assign_first_row_containers(self):
        for led_row in self.led_note_rows:
            led_row.row[0].assign_container()

    # set all leds in the first row to be white to indicate the backing track
    def initialize_first_led_row(self):
        for led_row in self.led_note_rows:
            led_row.row[0].led.set_color_and_display('white')

    # loads in the backing track and places the notes in the first note container
    def load_backing_track(self):
        beat_dict_list = self.backing_track_loader.return_backing_track_as_list_of_dicts()
        for beat_dict in beat_dict_list:
            index = int(beat_dict['beat_number']) - 1  # subtract one to get list index
            note_obj = self.led_note_rows[index].row[0].notes
            note_obj.owner = 'backing_track'
            for key in beat_dict.keys():
                if 'sample' in key:
                    note_obj.samples.append(beat_dict[key])


    def assign_parsed_messages(self):
        current_row = self.led_note_rows[self.beat-1].row
        if debug:
            print('Current index, ', str(self.beat-1), 'row: ', current_row)
        for message in self.parsed_messages:
            for i in range(len(current_row)):
                current_container = current_row[i]
                if not current_container.check_if_container_has_been_assigned():
                    if debug:
                        print('New message should be assigned to container # ', i)
                    self.assign_message(message=message, container=current_container)
                    break

    def assign_message(self, message:SerialMessage, container:NoteLedContainer):
        # led
        container.led.set_color_and_display('white')
        # note
        container.notes.owner = message.controller_number
        container.notes.char = message.note_char
        # assign the container
        container.assign_container()

    def parse_serial_messages(self):
        if debug:
            print('Messages to be parsed: ', self.messages_to_be_parsed)
        # self.parsed_messages = [] # make sure we delete the old messages..
        self.parsed_messages = self.serial_parser.parse_messages(self.messages_to_be_parsed)

    def recieve_serial_messages(self):
        self.messages_to_be_parsed = self.serial_interface.recieve_messages()

    def update_led_strips(self):
        self.led_controller.set_current_beat(beat=self.beat)
        self.led_controller.update_led_strips(led_note_rows=self.led_note_rows)

    def iterate_beat_count(self):
        self.beat += 1

    def reset_beat_count(self):
        self.beat = 0

    def wait_beat_length(self):
        time.sleep(self.beat_length)

    def play_samples_of_beat(self):
        self.sound_player.play_samples_of_beat(led_note_row=self.led_note_rows[self.beat-1])

    # for debug..
    def debug_print_all_led_note_data(self):
        print('Printing all led note data')
        num_rows = 0
        for row in self.led_note_rows:
            num_rows += 1
            print('Row: ', num_rows)
            led_num = 0
            for container in row.row:
                print('Container_has_been_assigned: ', container.check_if_container_has_been_assigned())
                led_num += 1
                print('\tLed num: {} has color: {}'.format(led_num, container.led.color))
                for sample in container.notes.samples:
                    print('\tSample: ', sample)
                print('\tChar: ', container.notes.char)
                print()
            print()
