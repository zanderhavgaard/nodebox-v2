from note_led_container import NoteLedContainer

class NoteLedRow:

    def __init__(self, leds_per_strip:int, strip_number:int):
        self.leds_per_strip = leds_per_strip
        self.strip_number = strip_number

        self.row = []

        for i in range(self.leds_per_strip):
            self.row.append(NoteLedContainer(self.strip_number, i))
