from app import app
try:
    from RPi import GPIO
except:
    print "Failed to import GPIO driver! Is this running on a Raspberry Pi?"

class LightDriver(object):
    """
    Class for controlling the GPIO Pins and toggling the light on and off
    If you don't specify which pin to control in the constructor, the PIN
    specified in the config file is used.
    """

    def __init__(self, pin=None):
        if not pin:
            self.pin = app.config['PIN']

    def get_pin(self):
        return self.pin

    def set_pin(self, pin):
        try:
            self.pin = pin
            return True
        except Exception as exc:
            print "Failed to set pin: %s" % exc
            return False

    def on(self):
        print "Turning light on"
        self._control_signal(self.pin, True)

    def off(self):
        print "Turning light off"
        self._control_signal(self.pin, False)

    def _control_signal(self, pin, signal):
        """
        Controls the signal going to the specified pin. Accepts two arguments:

        + pin: The number of the GPIO pin to receive the signal
        + signal: Boolean (True or False) indicating whether there should be
                  a current or not going to the specified pin.
        """
        try:
            GPIO.setmode(GPIO.BOARD)
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, signal)

            return signal

        except Exception as exc:
            print "Failed to control GPIO Pins: %s" % exc
            return not signal
