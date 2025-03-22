from machine import Pin, Timer, PWM
import time, random


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
LEDs =[D1,D2,D3,D4,D5,D6,D7,D8,D9,D10]

button = Pin(8, Pin.IN, Pin.PULL_UP)

lastLightTime = 0
randomBlinkDuration = 500 #ms
lastLEDsLit = []
howMany = 2

sunsetCounter = 0
sunrise = True

def randomBlink():
    global lastLightTime, randomBlinkDuration, lastLEDsLit
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
        '''
        randomBlinkDuration -= 10
        print(randomBlinkDuration)
        if randomBlinkDuration == 0:
            randomBlinkDuration = 500
        '''

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

def allOff():
    for led in LEDs:
        led.duty_u16(0)
        
def pulse():
    return
    
    
                         
