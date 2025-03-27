'''
   _  __           ________             ___  ____
  / |/ /__ _______/ / __/ /__ ________ |_  |/ __/
 /    / -_) __/ _  / _// / _ `/ __/ -_) __//__ \ 
/_/|_/\__/_/  \_,_/_/ /_/\_,_/_/  \__/____/____/ 

Firmware Version 1.1
'''

#from machine import Timer
import time
import aioble
import asyncio
import nerdflare25

DEBUG = True

if DEBUG:
    print("NerdFlare25: Version 1.1")

#How many LED modes are there
NUM_MODES = 4

# BLE Advertising frequency - how long the device advertises
ADV_INTERVAL_MS = 5000  # 5 seconds
TIMEOUT_MS = 10000 #10 seconds
#How long do we remember seen badges before forgeeting htem
TOO_OLD = 10 #10 seconds
BADGE_NAME = "NerdFlare25" #BLE Advertisement Device Name

# a dictionary of badges we've seen recently
# Keyed by their BLE MAC address, vales are the list time we saw them
badges = {} 

#State variables
pressed = False #Is the button currently pressed
mode = 0 #What LED mode are we in

#Asynchronous task that advertises our badge name
#All badges use the same name, but should have different BLE addresses
#Because they never make a connection, they will always timeout in (TIMEOUT_MS)
#This is OK, we use this as an oppurtunity to cleanup our seen badge dictionary
async def do_advertise():
    while True:
        if DEBUG:
            print("Advertising")
        try:
            await aioble.advertise(ADV_INTERVAL_MS, name="NerdFlare25",timeout_ms=TIMEOUT_MS)
        except Exception as e:
            if DEBUG:
                print("Timeout")
            # After every timeout, let's check to see if we've heard from other badges recently
            # This could also be handled with a Timer, probably
            for badge in badges:
                if time.time() - badges[badge] > TOO_OLD:
                    #If the badge is long gone, delete it from our list
                    if DEBUG:
                        print(badge, "is TOO old!")
                    del badges[badge]
                    #and turn off the LEDs in case we need to return to our default mode
                    nerdflare25.allOff()

#Asynchronous task that looks (scans) for other NF25 badges
#If a badge is seen, we add it to our dictionary of seen badges
async def do_scan():
    while True:
        if DEBUG:
            print("Scanning")
        #async with aioble.scan(duration_ms=10000) as scanner:
        #These are magic numbers that seem to work
        async with aioble.scan(5000, interval_us=30000, window_us=30000, active=True) as scanner:
            async for result in scanner:
                if result.name() == BADGE_NAME: #If we see a NF25 badge
                    if result.device.addr_hex() not in badges:
                        if DEBUG:
                            print("See a new badge!", result.device.addr_hex())
                        #its a new badge, so disable lights in case we're in another mode
                        nerdflare25.allOff()
                    badges[result.device.addr_hex()] = time.time() #Add it to our dictionary
                    if DEBUG:
                        print("addr: ", result.device.addr_hex(), "name: ",result.name())


#Each UI mode is a non-blocking loop that changes state
#based on how much time is passed or counter
#Generally we don't want to call delay() in an asychronous task
#as it will block all other tasks from running. We could await if we 
#really need to hold a state.
async def do_ui():
    global mode, pressed
    while True:
        if len(badges) < 1:
            if mode == 0:
                nerdflare25.sunrise_sunset()
            if mode == 1:
                nerdflare25.marquee()
            if mode == 2:
                nerdflare25.marquee2()
            if mode == 3:
                nerdflare25.marquee3()
        else:
            nerdflare25.randomBlink(len(badges))
        
        #The button is on a pull-up resistor so will be False
        #when pressed. If the button has been pressed, dont 
        #change mode again until after the button has been released again.
        if not nerdflare25.button.value() and not pressed:
            pressed = True 
            mode = (mode + 1)%NUM_MODES
            nerdflare25.allOff()
        if nerdflare25.button.value():
            pressed = False
        #Never Sleep!
        await asyncio.sleep_ms(0)

async def main():
    task_scan = asyncio.create_task(do_scan())
    task_advertise = asyncio.create_task(do_advertise())
    task_blink = asyncio.create_task(do_ui())
    await asyncio.gather(task_scan, task_advertise, task_blink)


asyncio.run(main())

'''
#This is some example code that uses a timer to periodically call a function

tim = Timer()

TOCK = True
def tick(timer):
    global TOCK, D

    if TOCK:
        TOCK = False
        for d in D:
            d.duty_u16(65536)
            utime.sleep(0.1)
    else:
        TOCK= True
        for d in D:
            d.duty_u16(0)
            utime.sleep(0.1)  
            
    #D1.toggle()
    #print("tick")
    #D2.toggle()
 
tim.init(freq=2.5, mode=Timer.PERIODIC, callback=tick)
'''

'''
#An asychronous LED blinking function
async def do_blink():
    global flag
    pin = Pin("LED", Pin.OUT)
    while True:
        try:
            if (flag):
                pin.on()
            await asyncio.sleep(1)
            #sleep(1) # sleep 1sec
        except KeyboardInterrupt:
            break
    pin.off()
'''
