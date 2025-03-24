'''
   _  __           ________             ___  ____
  / |/ /__ _______/ / __/ /__ ________ |_  |/ __/
 /    / -_) __/ _  / _// / _ `/ __/ -_) __//__ \ 
/_/|_/\__/_/  \_,_/_/ /_/\_,_/_/  \__/____/____/ 

Firmware Version 1.0
'''

from machine import Pin, Timer, PWM
import time, random

#Set LED Pins
D1 = PWM(Pin("GP16"))
D1.freq(1000)
D1.duty_u16(0)
D2 = PWM(Pin("GP15"))
D2.freq(1000)
D2.duty_u16(0)
D3 = PWM(Pin("GP14"))
D3.freq(1000)
D3.duty_u16(0)
D4 = PWM(Pin("GP13"))
D4.freq(1000)
D4.duty_u16(0)
D5 = PWM(Pin("GP12"))
D5.freq(1000)
D5.duty_u16(0)
D6 = PWM(Pin("GP11"))
D6.freq(1000)
D6.duty_u16(0)
D7 = PWM(Pin("GP17"))
D7.freq(1000)
D7.duty_u16(0)
D8 = PWM(Pin("GP18"))
D8.freq(1000)
D8.duty_u16(0)
D9 = PWM(Pin("GP19"))
D9.freq(1000)
D9.duty_u16(0)
D10 = PWM(Pin("GP20"))
D10.freq(1000)
D10.duty_u16(0)

#LEDs =[D1,D2,D3,D4,D5,D6,D7,D8,D9,D10]
#Ordering to support marquee modes
LEDs =[D1,D2,D3,D4,D5,D6,D10,D9,D8,D7]

#Set Button Pin
button = Pin(8, Pin.IN, Pin.PULL_UP)

#Random Blink State Variables
lastLightTime = 0
randomBlinkDuration = 500 #ms
lastLEDsLit = []
howMany = 2

#Sunset/Sunrise State Variables
sunsetCounter = 0
sunrise = True

#Marquee Modes State Variables
marqueeTime = 0
lastMarqueeLED = 0
even = True

#TODO: Test this
def randomBlinkBadges(numBadges=0):
    global howMany, randomBlinkDuration

    if numBadges == 0:
        howMany = 2
        randomBlinkDuration = 500
    if numBadges > 0 and numBadges < 3:
        howMany = 2
        randomBlinkDuration = 250
    if numBadges > 2 and numBadges < 5:
        howMany = 3
        randomBlinkDuration = 125
    if numBadges > 4:
        howMany = 4
        randomBlinkDuration = 75      

#Random Blink selects up to 'howMany' LEDs at random
#An illuminates them for 'randomBlinkDuration' milleseconds
#This is a non-blocking (no delay) function, using CPU ticks
#to determine when to change state.
def randomBlink(numBadges=0):
    global lastLightTime, randomBlinkDuration, lastLEDsLit

    randomBlinkBadges(numBadges)
    currentTime = time.ticks_ms()
    #Have we waited long enough to change the LEDs
    if time.ticks_diff(currentTime, lastLightTime) > randomBlinkDuration:
        #Turn the current on LEDs off
        for i in lastLEDsLit:
            LEDs[i].duty_u16(0)
        
        lastLEDsLit = []
            
        #Pick new LEDs and turn  on
        for i in range(howMany):
            led = random.randint(0,len(LEDs)-1)
            lastLEDsLit.append(led)
            LEDs[led].duty_u16(65536)
        lastLightTime = currentTime

#Sunrise slowly illuminates the LEDs to mimic a sunrise
#After the rise, it resets
#This mode is non-blocking (no delays)
def sunrise():
    #SUN: D1, D2, D3
    global sunsetCounter
    
    #TODO: We should do a sunset instead of off
    if sunsetCounter == 65536:
        sunsetCounter = 0
        D4.duty_u16(0)
        D5.duty_u16(0)
        D6.duty_u16(0)
        D7.duty_u16(0)
        D8.duty_u16(0)
        D9.duty_u16(0)
        D10.duty_u16(0)  
        
    sunsetCounter += 1
    
    D1.duty_u16(sunsetCounter)
    D2.duty_u16(sunsetCounter)
    D3.duty_u16(sunsetCounter)
    if sunsetCounter > int(65536*(1/4)):
        D4.duty_u16(sunsetCounter - int(65536*(1/4)))
        D7.duty_u16(sunsetCounter - int(65536*(1/4)))
    if sunsetCounter > int(65536*(1/2)):
        D5.duty_u16(sunsetCounter - int(65536*(1/2)))     
        D8.duty_u16(sunsetCounter - int(65536*(1/2)))
    if sunsetCounter > int(65536*(3/4)):
        D6.duty_u16(sunsetCounter - int(65536*(3/4)))
        D9.duty_u16(sunsetCounter - int(65536*(3/4))) 
        D10.duty_u16(sunsetCounter - int(65536*(3/4))) 
 

#Sunrise/Sunset fades the LEDs in and out to mimic a sunrise, then sunset
#This is a non-blocking (no delay) function, using a 16-bit counter
#to track the state (brightness) of the LEDs
def sunrise_sunset():
    
    global sunsetCounter, sunrise
    
    if sunsetCounter == 65536:
        sunrise = False
    if sunsetCounter == 0:
        sunrise = True

    if sunrise: 
        sunsetCounter += 1
    else: #sunset
        sunsetCounter -= 1

    #SUN: D1, D2, D3
    D2.duty_u16(sunsetCounter)
    if sunsetCounter > int(8192):
      D1.duty_u16(sunsetCounter - 8192)
      D3.duty_u16(sunsetCounter - 8192)
    if sunsetCounter > int(65536*(1/4)):
        D4.duty_u16(sunsetCounter - int(65536*(1/4)))
        D7.duty_u16(sunsetCounter - int(65536*(1/4)))
    if sunsetCounter > int(65536*(1/2)):
        D5.duty_u16(sunsetCounter - int(65536*(1/2)))     
        D8.duty_u16(sunsetCounter - int(65536*(1/2)))
    if sunsetCounter > int(65536*(3/4)):
        D6.duty_u16(sunsetCounter - int(65536*(3/4)))
        D9.duty_u16(sunsetCounter - int(65536*(3/4))) 
        D10.duty_u16(sunsetCounter - int(65536*(3/4))) 

#Turn all LEDs off
def allOff():
    for led in LEDs:
        led.duty_u16(0)

#Turn all LEDs on (max brightness by defult)
def allOn(brightness=65536):
    for led in LEDs:
        led.duty_u16(brightness)

#TODO
def pulse():
    return

#Marquee modes: Moves 'photons' around the edge of badge. 
#These are non-blocking functions (no delay) that use CPU ticks to
#change LED state.

#Marquee Mode 1: Single LED
def marquee():
    global marqueeTime, lastMarqueeLED
    currentTime = time.ticks_ms()
    #Have we waited long enough to change the LEDs
    if time.ticks_diff(currentTime, marqueeTime) > 100:
        #Turn the current on LEDs off
        LEDs[lastMarqueeLED].duty_u16(0)
        lastMarqueeLED = (lastMarqueeLED + 1) % len(LEDs)
        LEDs[lastMarqueeLED].duty_u16(65536)
        marqueeTime = currentTime
        
#Marquee Mode 2: Even/Odd LEDs alternate
def marquee2():
    global marqueeTime, even
    currentTime = time.ticks_ms()
    #Have we waited long enough to change the LEDs
    if time.ticks_diff(currentTime, marqueeTime) > 500:
        if even:
            for led in range(len(LEDs)):
                LEDs[led].duty_u16(0)
            for led in [num for num in range(len(LEDs)) if num % 2 == 0]:
                LEDs[led].duty_u16(65536)
        else:
            for led in range(len(LEDs)):
                LEDs[led].duty_u16(0)
            for led in [num for num in range(len(LEDs)) if num % 2 != 0]:
                LEDs[led].duty_u16(65536)
        even = not even

        marqueeTime = currentTime

#Marquee Mode 3: Two equidistant, negative (off) photons  chase eachother.
def marquee3():
    global marqueeTime, lastMarqueeLED
    currentTime = time.ticks_ms()
    #Have we waited long enough to change the LEDs
    if time.ticks_diff(currentTime, marqueeTime) > 200:
        allOn()
        lastMarqueeLED = (lastMarqueeLED + 1) % len(LEDs)
        LEDs[lastMarqueeLED].duty_u16(0)
        lastMarqueeLED = (lastMarqueeLED + 5) % len(LEDs)
        LEDs[lastMarqueeLED].duty_u16(0)
        marqueeTime = currentTime

