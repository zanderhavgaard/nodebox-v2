# Parses serial messages recieved from controllers through the serial_radio_interface module

from serial_message import SerialMessage

debug = False

class SerialMessageParser:

    global debug

    def __init__(self):

        # list of all the raw messages of the current beat
        self.messages_to_be_parsed = []

        # parsed messages to be acted upon
        self.parsed_messages = []

    # this method should input the messages and act upon them:
    # assign note values and turn on the leds of the applicable note and led objects
    def parse_messages(self, messages_to_be_parsed:list):

        self.parsed_messages = []

        self.messages_to_be_parsed = messages_to_be_parsed

        for message in self.messages_to_be_parsed:

            # we only want the index if there is a whole message
            if ('$' in message) and ('^' in message):
                # get the start index of the message
                message_start_index = self.get_message_start_index(message)
            else:
                # if there for some reason is no full message, we break to the next message in the for loop
                break

            # slice away excess chars before the start
            message = message[message_start_index:]

            # actually extract data from the received message
            parsed_message = self.parse_message(message=message, start_index=message_start_index)

            # finally we add the created message to the list
            self.parsed_messages.append(parsed_message)

        # we then evaluate that all of the messages we have parsed are good and will not cause problems
        self.evaluate_parsed_messages(messages=self.parsed_messages)

        if debug:
            print('Parsed message objs:' )
            print(self.parsed_messages)

        return self.parsed_messages

    def parse_message(self, message:str, start_index:int):

        if debug:
            print('The message to be parsed: ', message)

        # the new message obj
        parsed_message = SerialMessage(recieved_str=message)

        # we slice the controller number
        if message.startswith('$'):
            controller_number = message[1:3]
            parsed_message.controller_number = controller_number
            if debug:
                print('Controller_number: ', controller_number)

        # we then remove the 3 chars of the controller number until we get to the command
        message = self.remove_one_char_until_correct_char_is_first(str_to_slice=message, target_char='|')

        if debug:
            print('Message after slicing: ', message)

        # we slice the command
        if message.startswith('|'):
            command = message[1]
            parsed_message.command = command
            if debug:
                print('Command: ', command)

        # we then remove the two chars of the command until we get to the paramter start '#'
        message = self.remove_one_char_until_correct_char_is_first(str_to_slice=message, target_char='#')

        if debug:
            print('Message after slicing: ', message)

        # we add the first parameter, this will always be the color
        if message.startswith('#'):
            # this type casting might crash the program if for some reason the parameter is not correct, we will
            # fix it if it becomes an issue...
            note = message[1:2]
            # note = self.translate_ascii(ascii=note_ascii)
            parsed_message.note_char = note
            if debug:
                print('Note: ', note)

        # if we were using more than one parameter we would simply
        # keep doing the last step until we run out of parameters.

        if debug:
            print()
            parsed_message.print_all_message_data()
            print()

        # finally return the parsed message
        return parsed_message

    @DeprecationWarning # should not have to use this..
    def translate_ascii(self, ascii:int):
        return chr(ascii)

    # returns the index that the message starts at, if the parsed message for
    # some reason does not start at the correct place
    def get_message_start_index(self, message:str):
        index = 0
        for char in message:
            if char == '$':
                return index
            else:
                index += 1

    # recursively removes the first char of the str until it reaches the target char
    def remove_one_char_until_correct_char_is_first(self, str_to_slice:str, target_char:chr, ignore_first_char=False):
        if ignore_first_char:
            str = str_to_slice[1:]
        else:
            str = str_to_slice
        while not (str.startswith(target_char)):
            # we slice away the first char of the str
            str = str[1:]
        return str


    # evaluate that all messages are good to use and will not cause errors
    def evaluate_parsed_messages(self,  messages:list):
        for message in messages:
            message.evaluate_message()
