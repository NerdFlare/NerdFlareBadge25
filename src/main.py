from machine import Timer
import utime, time
import aioble
import asyncio
import nerdflare25
import bluetooth


pressed = False
NUM_MODES = 3
mode = 0

# Advertising frequency - how long the device advertises
ADV_INTERVAL_MS = 5000  # 5 seconds
TIMEOUT_MS = 10000 #10 seconds
#How long do we remember seen badges
TOO_OLD = 10 #10 seonds

badges = {} # a dictionary of badges we've seen recently

async def do_advertise():
    while True:
        print("Advertising")
        try:
            await aioble.advertise(ADV_INTERVAL_MS, name="NerdFlare25",timeout_ms=TIMEOUT_MS)
        except Exception as e:
            print("Timeout")
            # After every timeout, let's check to see if we've heard from other badges recently
            #This could also be handled with a Timer, probably
            for badge in badges:
                if time.time() - badges[badge] > TOO_OLD:
                    #If the badge is long gone, delete it from our list
                    print("TOO old!")
                    del badges[badge]
                    #and turn off the LEDs in case we need to return to another mode
                    nerdflare25.allOff()


async def do_scan():
    while True:
        print("Scanning")
        #async with aioble.scan(duration_ms=10000) as scanner:
        #These are magic numbers that seem to work
        async with aioble.scan(5000, interval_us=30000, window_us=30000, active=True) as scanner:
            async for result in scanner:
                if result.name() == "NerdFlare25": #If we see a NF25 badge
                    if result.device.addr_hex() not in badges:
                        #its a new badge, so disable lights in case we're in another mode
                        nerdflare25.allOff()
                    badges[result.device.addr_hex()] = time.time() #Add it to our dictionary
                    print("addr: ", result.device.addr_hex(), "name: ",result.name())



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
        else:
            nerdflare25.randomBlinkDuration = int(500/len(badges))
            nerdflare25.randomBlink()
        
        if not nerdflare25.button.value() and not pressed:
            pressed = True
            mode = (mode + 1)%NUM_MODES
            nerdflare25.allOff()
        if nerdflare25.button.value():
            pressed = False

        await asyncio.sleep_ms(0)

async def main():
    task_scan = asyncio.create_task(do_scan())
    task_advertise = asyncio.create_task(do_advertise())
    task_blink = asyncio.create_task(do_ui())
    #await asyncio.sleep(dur/1000)
    await asyncio.gather(task_scan, task_advertise, task_blink)
    #await asyncio.gather(task_advertise, task_blink)


asyncio.run(main())



'''
tim = Timer()
timset = False
tim2= Timer()


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
 
def flip():
    global D1, D2
    D1.toggle()
    D2.toggle()
    print("flip")
 
'''

'''
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
