from machine import Pin
import time



sensorPins = [
    Pin('D5', Pin.IN),
    Pin('D6', Pin.IN),
    Pin('D7', Pin.IN),
    Pin('D8', Pin.IN),
    Pin('D9', Pin.IN),
    Pin('D10', Pin.IN),
    Pin('D11', Pin.IN),
    Pin('D12', Pin.IN)
]


while True:
    global sensorValues
    sensorValues = [0]*8

    for p in sensorPins:
        p.init(Pin.OUT)
        p.value(1)

    time.sleep_us(15)
    
    for p in sensorPins:
        p.init(Pin.IN)

    start = time.ticks_us()

    while True:
        t = time.ticks_diff(time.ticks_us(), start)

        for i, p in enumerate(sensorPins):
            if p.value() == 0 and sensorValues[i] == 0:
                sensorValues[i] = t

        if t > 2000:
            break
    print(sensorValues)
    #time.sleep(.1)