# Nodebox program starter

import sys
from music_box_controller import MusicBoxController

print('\n\t*** Starting NodeBox ***\n')
print('\tPress ctrl-c to quit.\n')

# the controller
music_box_controller = MusicBoxController()

# start the program

# run setup once
music_box_controller.setup()

# then start the infinite loop
try:
    music_box_controller.main_loop()
except KeyboardInterrupt:
    music_box_controller.led_controller.clear_led_strip()
    sys.exit('\n\tExiting Nodebox..')
