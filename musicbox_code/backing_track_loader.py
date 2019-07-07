# loads a backing track .xml file located in ../backing_tracks/

import xml.etree.ElementTree as ET

debug = False

class BackingTrackLoader():

    global debug

    def __init__(self, backing_track_file:str):
        self.backing_track_file = backing_track_file
        # the completed path to the xml file
        self.xml_file = '../backing_tracks/' + self.backing_track_file + '.xml'
        # import and parse the xml file
        self.tree = ET.parse(self.xml_file)
        self.root = self.tree.getroot()

    def print_xml_structure(self):
        print(self.root.tag)
        for beat in self.root:
            print(beat.tag, ':', beat.text)
            for beat_data_tag in beat:
                print('\t', beat_data_tag.tag, ':', beat_data_tag.text)

    # returns the backing track as a list of dicts containing the data for each beat in separate dict
    def return_backing_track_as_list_of_dicts(self):
        beat_dict_list = []
        for beat in self.root:
            beat_dict_list.append(self.extract_beat(beat=beat))
        return beat_dict_list

    def extract_beat(self, beat):
        return_dict = {}
        sample_counter = 1
        for beat_data_tag in beat:
            if debug:
                print('extracting... ', beat_data_tag)
            if beat_data_tag.tag == 'beat_number':
                return_dict['beat_number'] = beat_data_tag.text
            if beat_data_tag.tag == 'sample':
                return_dict['sample'+str(sample_counter)] = beat_data_tag.text
                sample_counter += 1
        if debug:
            print('will return this dict..')
            for key in return_dict.keys():
                print(key, ':', return_dict[key])
        return return_dict

