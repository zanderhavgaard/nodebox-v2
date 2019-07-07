# holds info on what samples to play for this spot in the led row

class Notes:

    def __init__(self):
        # list of samples to play for this led
        self.samples = []

        # who owns these samples - could be used for color-coding saved samples etc.
        self.owner = ''

        # if set by a user, what char was used to load the sample
        self.char = ''
        
