# Holds info for a single ws2801 led


class Led:

    def __init__(self, strip_number:int, led_number:int, color="off"):
        # the current color of the led, defaults to "off", should be standard colors like, 'white', 'blue' etc.
        self.color = color
        # whether or not the led is being displayed
        self.display = False
        # position in led strip
        self.strip_number = strip_number
        self.led_number = led_number
        # whether the led has been set, so that we check which led in the row is the next to be used for a new note
        self.has_been_activated = False

    def set_color_and_display(self, color:str):
        self.color = color
        self.display = True
        self.has_been_activated = True

    def turn_led_off(self):
        self.display = False

    def get_color(self):
        return self.color

    def check_if_led_is_active(self):
        return self.has_been_activated

    def is_displayed(self):
        return self.display
