# LED flicker program
# Paul Clark 30/10/16
# from 09_pwm.py code by Simon Monk

import RPi.GPIO as GPIO
import time
import random

# constants
led_pin = 18
GPIO.setmode(GPIO.BCM)
delay_start = 0
delay_finish = 1
expansion_factor = 0.25

# set up LED pin and PWM
GPIO.setup(led_pin, GPIO.OUT)
pwm_led = GPIO.PWM(led_pin, 500)
pwm_led.start(100)

try:
    while True:
        duty = random.randint(0,100)
        pwm_led.ChangeDutyCycle(duty)
        compression_factor = random.randint(1,50)
        delay = expansion_factor/compression_factor
        # print('delay = ' + str(delay))
        time.sleep(delay)
        
finally:  
    print("Cleaning up")
    GPIO.cleanup()
