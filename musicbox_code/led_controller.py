# Manages the initialization of led strip object and controls of the led strips

from neopixel import Adafruit_NeoPixel
import time

debug = False

class LedController:

    global debug

    def __init__(self, display_mode:str, number_of_led_strips:int, number_of_leds_per_strip:int):

        self.current_beat_index = 0

        self.note_led_rows = []

        self.number_of_led_strips = number_of_led_strips
        self.number_of_leds_per_strip = number_of_leds_per_strip

        # holds the rgb values of each led
        self.all_colors_as_str = []
        self.all_led_rgb_value_lists = []

        # colors as [R, G, B]
        self.color_dict = {
            'off': [0, 0, 0],
            'white': [255, 255, 255],
            'red': [255, 0, 0],
            'blue': [0, 0, 255],
            'green': [0, 255, 0]
        }

        # choose whether or not to highlight the current beat and dim the rest = 'highlight'
        # or only show the colors of the current beat = 'only_current'
        self.display_mode = display_mode
        # self.display_mode = 'only_current'
        # self.display_mode = 'highlight'
        # the other leds will be divided by this factor
        self.display_mode_highlight_factor = 10

        self.led_strip = None

        # led strip settings
        self.number_of_leds_total = self.number_of_led_strips * self.number_of_leds_per_strip
        self.led_pin = 21  # uses PCM
        self.frequency_hz = 800000
        self.dma = 10
        self.led_brightness = 100
        self.led_inverted = False
        self.led_pin_channel = 0

        if debug:
            print('Settings for LedController(): ')
            print('Mode: ', self.display_mode)
            print('Brightness: ', self.led_brightness)
            print('Number of led strips: ', self.number_of_led_strips)
            print('Number of leds per strip: ', self.number_of_leds_per_strip)
            print('Total number of leds: ', self.number_of_leds_total)

    def initialize_led_strip(self):
        self.led_strip = Adafruit_NeoPixel(num=self.number_of_leds_total,
                                           pin=self.led_pin,
                                           freq_hz=self.frequency_hz,
                                           dma=self.dma,
                                           invert=self.led_inverted,
                                           brightness=self.led_brightness,
                                           channel=self.led_pin_channel
                                           )
        self.led_strip.begin()

        if debug:
            print('\nInitialized Led strip... Obj: ', self.led_strip)
            print()

    def remove_strip_obj(self):
        self.led_strip = None

    def set_current_beat(self, beat:int):
        self.current_beat_index = beat - 1

    # will set leds to be the colors from the led obj, depending on the display mode
    def set_led_colors(self):
        # choose whether to only show the current beat leds, or to highlight it

        if debug:
            print('Setting led colors... using display mode: ', self.display_mode)

        if self.display_mode == 'only_current':
            if debug:
                print('Mode is ', self.display_mode)
            self.only_show_colors_from_current_beat()
            self.convert_color_str_to_rgb()
        elif self.display_mode == 'highlight':
            if debug:
                print('Mode is ', self.display_mode)
            self.highlight_current_beat_leds()

    def only_show_colors_from_current_beat(self):
        index = 0
        for note_led_row in self.note_led_rows:
            if index == self.current_beat_index:
                for note_led_container in note_led_row.row:
                    led = note_led_container.led
                    if led.is_displayed():
                        self.all_colors_as_str.append(led.get_color())
                    else:
                        self.all_colors_as_str.append('off')
            else:
                for note_led_container in note_led_row.row:
                        self.all_colors_as_str.append('off')
            index += 1

    # convert color str to lists of three rgb values
    def convert_color_str_to_rgb(self):
        for color_str in self.all_colors_as_str:
            rgb_list = self.color_dict[color_str]
            self.all_led_rgb_value_lists.append(rgb_list)

    # the leds of the current beat will be displayed at full brightness, the other beats at half
    def highlight_current_beat_leds(self):
        index = 0
        for note_led_row in self.note_led_rows:
            if index == self.current_beat_index:
                for note_led_container in note_led_row.row:
                    led = note_led_container.led
                    if led.is_displayed():
                        color_str = led.get_color()
                        self.all_colors_as_str.append(color_str)
                        self.add_color_to_rgb_list(color=color_str)
                    else:
                        color_str = 'off'
                        self.all_colors_as_str.append(color_str)
                        self.add_color_to_rgb_list(color=color_str)
            else:
                for note_led_container in note_led_row.row:
                    led = note_led_container.led
                    if led.is_displayed():
                        color_str = led.get_color()
                        self.all_colors_as_str.append(color_str)
                        self.add_color_to_rgb_list(color=color_str, reduced_brightness=True)
                    else:
                        color_str = 'off'
                        self.all_colors_as_str.append(color_str)
                        self.add_color_to_rgb_list(color=color_str)
            index += 1

    def add_color_to_rgb_list(self, color:str, reduced_brightness=False):
        rgb_list = self.color_dict[color]
        output_list = []
        # if reduced brightness we divide by a factor
        if reduced_brightness:
            index = 0
            for rgb_val in rgb_list:
                if not (rgb_val == 0):
                    rgb_val = int(float(rgb_val) / float(self.display_mode_highlight_factor))
                output_list.append(rgb_val)
                index += 1
        else:
            output_list = rgb_list
        self.all_led_rgb_value_lists.append(output_list)

    # set the values for each led in the strip obj
    def update_led_strip_colors(self):
        led_index = 0
        for rgb_list in self.all_led_rgb_value_lists:
            r = rgb_list[0]
            g = rgb_list[1]
            b = rgb_list[2]
            self.led_strip.setPixelColorRGB(n=led_index, red=r, green=g, blue=b)
            led_index += 1

    # actually output the color values to the strip
    def display_updated_leds(self):
        if debug:
            print('Updating the output of the leds')
        self.led_strip.show()

    def clear_led_strip(self):
        for i in range(self.number_of_leds_total):
            self.led_strip.setPixelColorRGB(n=i, red=0, green=0, blue=0)
            time.sleep(0.01)
            self.led_strip.show()

    # main function to control the led hardware
    def update_led_strips(self, led_note_rows:list):
        if debug:
            print('Will now update the colors of the ledstrips')

        # reset the lists
        self.note_led_rows = led_note_rows
        self.all_colors_as_str = []
        self.all_led_rgb_value_lists = []

        self.set_led_colors()
        self.update_led_strip_colors()

        if debug:
            # print('note_led_rows: ', self.note_led_rows)
            # print('all_colors_as_str: ', self.all_colors_as_str)
            print('all_led_rgb_value_list: ', self.all_led_rgb_value_lists)

        self.display_updated_leds()

