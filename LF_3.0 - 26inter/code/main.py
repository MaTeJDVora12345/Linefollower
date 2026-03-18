from machine import Pin, PWM
import time
#=========declaration=========
#encoder
enc = Pin('D1', Pin.IN, Pin.PULL_UP)

#leds
ledR = Pin('D14', Pin.OUT)
ledG = Pin('D15', Pin.OUT)
ledB = Pin('D13', Pin.OUT)

#sensors
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

#motors
motorLDir = Pin('D4', Pin.OUT)
motorLPwm = PWM(Pin('D3'))

motorRDir = Pin('D29', Pin.OUT)
motorRPwm = PWM(Pin('D28'))

#=========functions=========
def encoderIrq(pin):
    global rotations
    if enc.value() == 0:
        rotations += 1
def setRGB(r, g, b):
    ledR.value(r)
    ledG.value(g)
    ledB.value(b)
    
def readSensors():
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

        if t > 3000:
            break
    return sensorValues

def position():
    global lastVal
    values = readSensors()
    if sum(values) < 2000:
        values = lastVal
        setRGB(1,0,0)
    else:
        setRGB(0,1,0)
    lastVal = values
    weights = [-3.5, -2.5, -1.5, -.5, .5, 1.5, 2.5, 3.5]
    pos = 0
    
    for i in range(8):
        pos += values[i]*weights[i]
    return int(pos + cal)
    
def setSpeed(rSpeed, lSpeed):
    if rSpeed < 0:
        rSpeed = 0
    elif rSpeed > 65535:
        rSpeed = 65535
    if lSpeed < 0:
        lSpeed = 0
    elif lSpeed > 65535:
        lSpeed = 65535
    
    motorRPwm.duty_u16(rSpeed)
    motorLPwm.duty_u16(lSpeed)

#=========prep=========
#enc
rotations = 0
enc.irq(trigger=Pin.IRQ_RISING, handler=encoderIrq)

#motors
motorLPwm.freq(1000)
motorRPwm.freq(1000)

#sensors
sensorValues = [0]*8
cal = 0
lastVal = [0]*8

# ===== PID =====
baseSpeed = 20000

Kp = 20000   
Ki = 0
Kd = 36000

error = 0
previousError = 0
integral = 0


#
setRGB(0,0,1)
time.sleep(2)
#=========main loop=========
#start
setRGB(0,1,1)
#for i in range(0,baseSpeed,1):
 #   setSpeed(i,i)
  #  time.sleep(.0005)
#loop
setRGB(0,1,0)    
while True:
    if rotations > 30:
        if baseSpeed < 30000:
            baseSpeed += 20
    elif rotations > 20:
        if baseSpeed > 20000:
            baseSpeed -= 20
    
    error = position() / 3500

    integral += error
    integral = max(min(integral, 100), -100)

    derivative = error - previousError

    correction = Kp * error + Ki * integral + Kd * derivative

    rightSpeed  = int(baseSpeed + correction *2)
    leftSpeed = int(baseSpeed - correction *2)

    setSpeed(rightSpeed, leftSpeed)
    previousError = error
    
    
    
    #debug
    #position()
    #print(position()/3500)
    #print(rightSpeed, "  |  " ,leftSpeed)
    #time.sleep(.1)