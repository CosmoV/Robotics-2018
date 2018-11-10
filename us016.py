import pyb


# Pin configuration.
# WARNING: Do not use PA4-X5 or PA5-X6 as the echo pin without a 1k resistor.

class US016:
    def __init__(self, rangePin, outPin, inputVoltage, maxRange):
        self.rangePin = rangePin
        if maxRange <= 1:
            self.k = 1024
            self.rangePin.low()
        else:
            self.k = 3072
            self.rangePin.high()
        self.outPin = outPin
        self.inputVoltage = inputVoltage
        self.maxRange = maxRange

    def distance(self):
        # https://uge-one.com/analog-output-ultrasonic-sensor-us-016.html72
        return pyb.ADC(self.outPin).read() * self.k / self.inputVoltage
