from led import Led
from notes import Notes


class NoteLedContainer:

    def __init__(self, strip_number:int, led_number:int):
        self.strip_number = strip_number
        self.led_nuber = led_number

        self.led = Led(led_number=led_number, strip_number=strip_number)
        self.notes = Notes()

        self.has_been_assigned = False

    def check_if_container_has_been_assigned(self):
        return self.has_been_assigned

    def assign_container(self):
        self.has_been_assigned = True

    # reinitialize the objs of the container
    def reset_container(self):
        self.has_been_assigned = False
        self.led = Led(led_number=led_number, strip_number=strip_number)
        self.notes = Notes()