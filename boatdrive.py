import RPi.GPIO as GPIO
import time

# Define GPIO pin numbers
button_pin = 17    # The pin connected to the button
output_pins = [18, 23, 24]  # Pins connected to the LEDs or other outputs

# Set up the GPIO board
GPIO.setmode(GPIO.BCM)                   # Use BCM pin numbering
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Button pin with pull-up resistor

# Set up the output pins as outputs
for pin in output_pins:
    GPIO.setup(pin, GPIO.OUT)

try:
    while True:
        # Check if the button is pressed
        button_state = GPIO.input(button_pin)
        
        if button_state == GPIO.LOW:   # Button pressed (LOW due to pull-up resistor)
            for pin in output_pins:
                GPIO.output(pin, GPIO.HIGH)  # Turn on each output pin
            print("Button pressed, all output pins activated.")
        else:
            for pin in output_pins:
                GPIO.output(pin, GPIO.LOW)   # Turn off each output pin
            print("Button not pressed, all output pins deactivated.")
        
        time.sleep(0.1)  # Small delay to stabilize the readings

except KeyboardInterrupt:
    # Cleanup GPIO settings when exiting
    GPIO.cleanup()
    print("GPIO cleanup done.")
