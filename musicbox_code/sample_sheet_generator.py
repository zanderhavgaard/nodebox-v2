# will generate a sample sheet based on audio files in a specified directory
# samples should be placed in nodebox_v2/sound_files/<some-dir>
# you can parse just one folder or mix multiple
# project currently supports max 37 different samples per. controller,
# though this is a completely arbitrary number (simply because version 1 had that number) and could be expanded.
# if the specified folder(s) have more than 37, the first 37 alphabetically will be used.

import xml.etree.ElementTree as ET
import os
import sys

debug = False

class SampleSheetGenerator:

    global debug

    def __init__(self):

        # accepted values to map samples to as chars
        self.byte_values = ["A","B","C","D","E","F","G","H","I","J","K","L","M",
                            "N","O","P","Q","R","S","T","U","V","W","X","Y","Z",
                            "a","b","c","c","e","f`","g","h","i"]

        # accepted values as numbers as strings
        # self.byte_values = ['1','2','3','4','5','6','7','8','9','10',
        #                     '11','12','13','14','15','16','17','18','19','20',
        #                     '21','22','23','24','25','26','27','28','29','30',
        #                     '31','32','33','34','35']

        # should hold all of the sample file names
        self.sample_file_names_names = []

        # the relative path to sound_files dir
        self.path_to_sound_files = '../sound_files/'

        # where to put generated sample sheets
        self.path_to_sample_sheets = '../sample_sheets/'

        # holds the settings for the generated sample sheet
        self.settings_dict = {}

        # the subsections to be generated, should contains subsection owner : path to dir of audio files
        self.subsections = {}


    def get_file_names_from_dir(self, dir_path:str):
        file_names_generator = [(x[0], x[2]) for x in os.walk(dir_path)]
        file_names_list = file_names_generator[0][1]
        return file_names_list

    # will prompt the user to enter settings when running the script
    def prompt_for_settings(self):
        print('\n\tSampleSheetGenerator for NodeBox_v2\n')
        print('Will generate a sample_sheet based on inputs...')
        print('Use ctrl-c to abort, if filename already exists, sample_sheet will be overwritten.')
        print()

        # get the file name
        self.settings_dict['file_name'] = input('Filename for sample_sheet (without ".xml"): ')
        print()

        print('Adding subsections:')
        print('Subsections map the audio files of a directory to an "owner".')
        print('The owners are eg. the different controllers and the backing track.')
        print('You can add as many subsections as you have controllers, and one for the backing track.')
        print('The subsections should follow the naming convention of "controller<controller number>" eg "controller01", "controller02".')
        print('Alternatively you can call the subsection "default" to map all controllers to use the same samples.')
        print('To map the backing track call the subsection "backing_track".')
        print('The directory with audio files should be located in ../sound_files/')
        print('As a minimum you should have a "default" and a "backing_track" subsections.')
        print()

        # get the subsections to generate
        add_more_subsections = True
        is_valid_subsection_name = False
        while add_more_subsections:
            name = input('Subsection name: ')
            if not self.check_if_valid_subsection_name(subsection_name=name):
                while not self.check_if_valid_subsection_name(subsection_name=name):
                    print('Please specify a subsection name that follows the naming convention.')
                    name = input('Subsection name: ')
            path = input('Relative path to dir with audio files from /sound_files/<path> : ')
            self.subsections[name] = path

            choice = input('Add another subsection? (y/n) ')

            if not ((choice == 'y') or (choice == 'n')):
                while not(choice == 'y') or not (choice == 'n'):
                    choice = input('Add another subsection? (y/n) ')

            if choice == 'n':
                add_more_subsections = False
            elif choice == 'y':
                print('Adding another subsection...')
        print()

        print('The following sheet will be generated: ')
        print('Filename: ', self.settings_dict['file_name'])
        for subsection in self.subsections.keys():
            print('Subsection name: {} path: {}'.format(subsection, self.subsections[subsection]))
        print()

        generate_file = input('Generate sample_sheet file? (y/n) ')

        if not ((generate_file == 'y') or (generate_file == 'n')):
            while not (generate_file == 'y') or not (generate_file == 'n'):
                generate_file = input('Generate sample_sheet file? (y/n) ')

        if generate_file == 'y':
            print('Generating sample_sheet ...')
            return True
        else:
            sys.exit('\n\tExitting sample_sheet generator...')

    def check_if_valid_subsection_name(self, subsection_name:str):
        # should return a bool whether the subsection name follow naming convention.
        valid_names = ['backing_track', 'default', 'controller01',
                       'controller02', 'controller03', 'controller04']
        if subsection_name in valid_names:  # todo: make better check for n number of controllers
            return True
        else:
            return False

    def write_xml_file(self):

        # root
        sample_sheet = ET.Element('sample_sheet')

        for subsection in self.subsections.keys():
            subsection_element = ET.SubElement(sample_sheet, subsection)

            path = self.path_to_sound_files + self.subsections[subsection]
            sample_file_names = self.get_file_names_from_dir(path)

            if debug:
                print('sound files: ', sample_file_names)

            char_index = 0

            for sample in sample_file_names:
                sample_element = ET.SubElement(subsection_element, 'sample')

                dot_index = sample.find('.')
                file_format = sample[dot_index:]
                sample_name = sample[:dot_index]
                full_path = path + sample
                char = self.byte_values[char_index]
                char_index += 1

                sample_full_path_element = ET.SubElement(sample_element, 'full_path')
                sample_full_path_element.text = full_path

                sample_name_element = ET.SubElement(sample_element, 'name')
                sample_name_element.text = sample_name

                sample_file_format_element = ET.SubElement(sample_element,'format')
                sample_file_format_element.text = file_format

                sample_char_element = ET.SubElement(sample_element, 'char')
                sample_char_element.text = char

        file_name = self.path_to_sample_sheets + self.settings_dict['file_name'] + '.xml'

        tree = ET.ElementTree(sample_sheet)
        tree.write(file_name)

    # main method should handle generating the file
    def generate_file(self, prompt_for_settings=False):

        # get filenames in some way
        if prompt_for_settings:
            self.prompt_for_settings()

        # actually write the file
        self.write_xml_file()

# run the generator
generator = SampleSheetGenerator()
# generator can also be run without prompting for settings, but parsing them instead, like from a webinterface
generator.generate_file(prompt_for_settings=True)
