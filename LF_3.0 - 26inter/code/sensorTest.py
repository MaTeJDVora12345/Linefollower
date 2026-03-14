from machine import Pin
import time



sensorR4 = Pin('D5', Pin.IN)
sensorR3 = Pin('D6', Pin.IN)
sensorR2 = Pin('D7', Pin.IN)
sensorR1 = Pin('D8', Pin.IN)
sensorL4 = Pin('D9', Pin.IN)
sensorL3 = Pin('D10', Pin.IN)
sensorL2 = Pin('D11', Pin.IN)
sensorL1 = Pin('D12', Pin.IN)


while True:
    print(sensorR4.value() , sensorR3.value() , sensorR2.value() , sensorR1.value() , sensorL1.value() , sensorL2.value() , sensorL3.value() , sensorL4.value())
    time.sleep(.2)