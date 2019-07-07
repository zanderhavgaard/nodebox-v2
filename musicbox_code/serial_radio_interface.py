# Facilitates serial communication with controller over radio

import serial

debug = False

class SerialRadioInterface:

    global debug

    def __init__(self):

        if debug:
            print('Initializing serial radio interface ...')

        # serial port to recieve bytes on
        self.serial_port = '/dev/ttyS0'

        # baudrate of serial port
        self.baudrate = 9600

        # timeout for serial port
        self.timeout = 0.5

        # raw bytes read in a beat
        self.raw_bytes = b''

        # decoded bytes of beat
        self.decoded_bytes = ''

        # the number of bytes to attempt to read in each beat
        self.bytes_to_read_per_beat = 100

        # the messages recieved in this beas
        self.serial_messages = []

        # open the serial connection
        self.serial_interface = serial.Serial(port=self.serial_port,
                                              baudrate=self.baudrate,
                                              timeout=self.timeout)

        # list of 'raw' messages to be returned to parser
        self.messages_list = []

    def read_serial_bytes(self):
        self.raw_bytes =  self.serial_interface.read(self.bytes_to_read_per_beat)


    def slice_messages_and_return_list(self, messages_as_one_str:str):
        decoded_bytes = messages_as_one_str
        if debug:
            print('Decoded_bytes: ', decoded_bytes)

        start_index = None
        end_index = None

        sliced_messages = []

        for i in range(len(decoded_bytes)):

            if decoded_bytes[i] == '$':
                start_index = i
            elif decoded_bytes[i] == '^':
                end_index = i
            else:
                continue

            if not (start_index is None) and not (end_index is None) and (start_index < end_index):

                end_index += 1

                if debug:
                    print('Indices: ', start_index, end_index)

                sliced_str = decoded_bytes[start_index:end_index]

                sliced_messages.append(sliced_str)

                if debug:
                    print('sliced str: ', sliced_str)

                start_index = None
                end_index = None

                # remove new sliced str from bytes str
                # decoded_bytes = decoded_bytes[:end_index]

                # if debug:
                #     print('Whole decoded byte str after slicing: ', decoded_bytes)

        return sliced_messages

    # returns a list of strings
    def recieve_messages(self):

        self.read_serial_bytes()

        try:
            self.decoded_bytes = self.raw_bytes.decode()
        except UnicodeDecodeError: # don't crash if the bytes are gibberish...
            if debug:
                print('\n*** cannot decode these bytes... continuing.')

        messages_to_be_parsed = self.slice_messages_and_return_list(messages_as_one_str=self.decoded_bytes)

        if debug:
            print('\nSerial_Radio_interface done with beat.')
            print('Messages ready to be parsed: ')
            print(messages_to_be_parsed)

        return messages_to_be_parsed



