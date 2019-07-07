

class SerialMessage:

    def __init__(self, recieved_str:str, initialize_parameters_list=False):

        # the whole recieved str
        self.whole_string = recieved_str

        # the number of the controller that send the message
        self.controller_number = 0

        # command to be executed should be either 'p' or 's'
        # 'p' = play this note once on this bear
        # 's' = save this note on this beat and play it for each consecutive beat
        self.command = ''

        # since we want to support the potential for an arbitrary number of parameters, we will hold all of them as a
        # list and then let the parser decide what to do with them
        if initialize_parameters_list:
            self.parameters = []
        else:
            self.parameters = [] # todo figure out what went wrong here?

        # the note to be played, should be the first parameter, should be a char
        self.note_char = ''

    def print_all_message_data(self):
        print('Printing contents of SerialMessage obj: ')
        print('Whole_string: ', self.whole_string)
        print('Controller_number: ', self.controller_number)
        print('Command: ', self.command)
        print('Parameters: ', self.parameters)
        print('Note_char: ', self.note_char)

    # should evaluate if the data put into the message are valid and if not discard this message to
    # alleviate potential errors from interference
    def evaluate_message(self):

        # todo implement...
        # raise NotImplementedError

        return True
