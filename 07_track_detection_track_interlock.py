# 07_track_detection.py
# Paul Clark 02 Oct 2016
# Ver 1.0
# includes change to red if track set against signal
# From the code for the Electronics Starter Kit for the Raspberry Pi by MonkMakes.com

import RPi.GPIO as GPIO
import time, math

# Configure the Pi to use the BCM (Broadcom) pin names, rather than the pin positions
GPIO.setmode(GPIO.BCM)

# This project uses a photoresistor, a component whose resistance varies with the light falling on it.
# To measure its resistance, the code records the time it takes for a capacitor to fill  
# when supplied by a current passing through the resistor. The lower the resistance the faster 
# it fills up. 
#
# You can think of a capacitor as a tank of electricity, and as it fills with charge, the voltage
# across it increases. We cannot measure that voltage directly, because the Raspberry Pi
# does not have an analog to digital convertor (ADC or analog input). However, we can time how long it
# takes for the capacitor to fill with charge to the extent that it gets above the 1.65V or so
# that counts as being a high digital input. 
# 
# For more information on this technique take a look at: 
# learn.adafruit.com/basic-resistor-sensor-reading-on-raspberry-pi
# The code here is based on that in the Raspberry Pi Cookbook (Recipes 12.1 to 12.3)

# set up signal delays
red_delay = 4
amber_delay = 4

# Pin a charges the capacitor through a fixed 1k resistor and the thermistor in series
# pin b discharges the capacitor through a fixed 1k resistor 
a_pin = 18
b_pin = 23

# setup signal indicators
red_pin = 24
amber_pin = 25
green_pin = 8

# setup switch
red_switch_pin = 7

# set up output pins
GPIO.setup(red_pin, GPIO.OUT)
GPIO.setup(amber_pin, GPIO.OUT)
GPIO.setup(green_pin, GPIO.OUT)

# set up input pin for switch
GPIO.setup(red_switch_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# initalise signal to show red
GPIO.output(green_pin, False)  # put off green to off  
GPIO.output(red_pin, False)     # put off red light  
GPIO.output(amber_pin, False)   # put off amber
GPIO.output(green_pin, True)     # put on green light  

# set light threshold value for detection of trains
threshold = 32

# empty the capacitor ready to start filling it up
def discharge():
    GPIO.setup(a_pin, GPIO.IN)
    GPIO.setup(b_pin, GPIO.OUT)
    GPIO.output(b_pin, False)
    time.sleep(0.01)

# return the time taken for the voltage on the capacitor to count as a digital input HIGH
# than means around 1.65V
def charge_time():
    GPIO.setup(b_pin, GPIO.IN)
    GPIO.setup(a_pin, GPIO.OUT)
    GPIO.output(a_pin, True)
    t1 = time.time()
    while not GPIO.input(b_pin):
        pass
    t2 = time.time()
    return (t2 - t1) * 1000000

# Take an analog readin as the time taken to charge after first discharging the capacitor
def analog_read():
    discharge()
    return charge_time()

# Convert the time taken to charge the cpacitor into a value of resistance
# To reduce errors, do it 20 times and take the average.
def read_resistance():
    n = 20
    total = 0;
    for i in range(1, n):
        total = total + analog_read()
    reading = total / float(n)
    resistance = reading * 6.05 - 939
    return resistance

def light_from_r(R):
    # Log the reading to compress the range
    return math.log(1000000.0/R) * 10.0 


# Update the reading
def update_reading():
    global reading_str
    global light
    light = light_from_r(read_resistance())
    reading_str = "{:.0f}".format(light)
    return reading_str

# signal timer control
def signal_timer_control():

    GPIO.output(green_pin, False)  # reset green to off  
    GPIO.output(red_pin, True)     # put on re light for timed period 
    time.sleep(red_delay)             
    GPIO.output(red_pin, False) 
    GPIO.output(amber_pin, True)   # show amber light for timed period 
    time.sleep(amber_delay)             
    GPIO.output(amber_pin, False)
    GPIO.output(green_pin, True)   # show green light
    return

# turn signal to red
def change_signal_red():
    GPIO.output(red_pin, True)     
    GPIO.output(green_pin, False)
    GPIO.output(amber_pin, False)
    return

# turn signal to green
def change_signal_green():
    GPIO.output(red_pin, False)     
    GPIO.output(green_pin, True)
    GPIO.output(amber_pin, False)
    return
    
try:
    while True:
        if not GPIO.input(red_switch_pin): # if switch is on
            # print ('switch on')
            change_signal_red()

        if GPIO.input(red_switch_pin):     # if switch is off
            # print ('switch off')
            analog_read()
            update_reading()
            if light < threshold:
                signal_timer_control()
            else:
                change_signal_green()    
finally:  
    print("Cleaning up")
    GPIO.cleanup()
