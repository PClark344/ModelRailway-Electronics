# 02_traffic_lights.py
# From the code for the Electronics Starter Kit for the Raspberry Pi by MonkMakes.com
# new code by Paul Clark 26/09/16

import RPi.GPIO as GPIO
import time

# Configure the Pi to use the BCM (Broadcom) pin names, rather than the pin positions
GPIO.setmode(GPIO.BCM)
red_pin = 18
amber_pin = 23
green_pin = 25

GPIO.setup(red_pin, GPIO.OUT)
GPIO.setup(amber_pin, GPIO.OUT)
GPIO.setup(green_pin, GPIO.OUT)

try:
    def sequence():
        no_lights()
        red_light()
        amber_light()
        green_light()
        red_and_amber_lights()
        red_light()
        return

    def no_lights():
        # put all lights out
        GPIO.output(red_pin, False)
        GPIO.output(amber_pin, False)
        GPIO.output(green_pin, False)
        return
    
    def red_light():
        print ('red light')
        GPIO.output(red_pin, True)
        time.sleep(5)
        GPIO.output(red_pin, False)
        return
    
    def amber_light():
        print ('amber light')
        GPIO.output(amber_pin, True)
        time.sleep(5)
        GPIO.output(amber_pin, False)
        return
    
    def green_light():
        print ('green light')
        GPIO.output(green_pin, True)
        time.sleep(5)
        GPIO.output(green_pin, False)
        return

    def red_and_amber_lights():
        print ('red and amber lights')
        GPIO.output(red_pin, True)
        GPIO.output(amber_pin, True)
        time.sleep(5)
        GPIO.output(red_pin, False)
        GPIO.output(amber_pin, False)
        return

    sequence()

        
finally:  
    print("Cleaning up")
    GPIO.cleanup()
    
    # You could get rid of the try: finally: code and just have the while loop
    # and its contents. However, the try: finally: construct makes sure that
    # when you CTRL-c the program to end it, all the pins are set back to 
    # being inputs. This helps protect your Pi from accidental shorts-circuits
    # if something metal touches the GPIO pins.
