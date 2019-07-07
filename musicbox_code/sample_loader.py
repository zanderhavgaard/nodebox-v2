# should import a sample_sheet and tell the sound_player what to play

# should contain get methods for mapping sample chars to actual audio files, and return a path to be executed

import xml.etree.ElementTree as ET

debug = False

class SampleLoader:

    global debug

    def __init__(self, sample_sheet_to_load:str):
        self.path_to_sample_sheets = '../sample_sheets/'
        # the filename with the path to the sample sheet to be loaded
        self.sample_sheet_to_load = self.path_to_sample_sheets + sample_sheet_to_load + '.xml'
        # load and parse the xml file
        self.tree = ET.parse(self.sample_sheet_to_load)
        self.root = self.tree.getroot()

        # holds the samples as dict of dicts, where the keys of outer dicts are the subsection names
        # and the keys of the inner dicts are the
        self.sample_map_by_name = {str:str}
        self.dict_of_sample_controller_mappings = {str : {str:str}}


    def load_file(self):
        # load each subsection of the sample sheet
        for subsection in self.root:
            subsection_name = subsection.tag
            self.dict_of_sample_controller_mappings[subsection_name] = self.extract_subsection(subsection)

    def extract_subsection(self, subsection:ET.Element):
        return_dict = {}
        for sample in subsection:
            name, char, full_path = '','',''
            for sample_tag in sample:
                if sample_tag.tag == 'name':
                    name = sample_tag.text
                elif sample_tag.tag == 'char':
                    char = sample_tag.text
                elif sample_tag.tag == 'full_path':
                    full_path = sample_tag.text
            return_dict[char] = full_path
            self.sample_map_by_name[name] = full_path
        return return_dict

    # will return a tuple of two dicts, one with all of the sample names mapped ti filenames
    # and the other a dicts of dicts named after each controller with chars mapped to sample files
    def load_sample_sheet_and_return_tuple(self):
        # load the file and
        self.load_file()

        if debug:
            print('\nPrinting the two dicts of sample names: \n')
            print('sample_map_by_name: \n')
            for key in self.sample_map_by_name.keys():
                print(key, ' : ', self.sample_map_by_name[key])
            print('\nPrinting the dict of sample char mappings: \n')
            for subsection in self.dict_of_sample_controller_mappings.keys():
                print('Subsection: ', subsection, '\n')
                subsection_dict = self.dict_of_sample_controller_mappings[subsection]
                for char in subsection_dict.keys():
                    print('char ', char, ' : ', subsection_dict[char])
            print('\nDone printing sample dicts.\n')


        sample_tuple = (self.sample_map_by_name, self.dict_of_sample_controller_mappings)

        return sample_tuple




