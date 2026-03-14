from machine import Pin, PWM
import time

# ===== Encoder =====
enc_b = Pin('D4', Pin.IN, Pin.PULL_UP)

positionMotoru = 0

def encoder_irq(pin):
    global positionMotoru
    if enc_b.value() == 0:
        positionMotoru += 1

enc_b.irq(trigger=Pin.IRQ_RISING, handler=encoder_irq)

# ===== QTR-8RC sensor pins =====
sensor_pins = [
    Pin('D5', Pin.IN),
    Pin('D6', Pin.IN),
    Pin('D7', Pin.IN),
    Pin('D8', Pin.IN),
    Pin('D9', Pin.IN),
    Pin('D10', Pin.IN),
    Pin('D11', Pin.IN),
    Pin('D12', Pin.IN)
]

sensor_values = [0]*8

# ===== Motor pins =====
motorL1 = Pin('D1', Pin.OUT)
motorL2 = Pin('D2', Pin.OUT)

motorR1 = Pin('D13', Pin.OUT)
motorR2 = Pin('D14', Pin.OUT)

motorPWMLeft = PWM(Pin('D3'))
motorPWMRight = PWM(Pin('D15'))

motorPWMLeft.freq(1000)
motorPWMRight.freq(1000)

# ===== PID =====
base_speed = 18000

Kp = 9000
Ki = 0
Kd = 30000

error = 0
previous_error = 0
integral = 0

time.sleep(3)

# ===== Read QTR sensors =====
def read_sensors():

    global sensor_values
    sensor_values = [0]*8

    for p in sensor_pins:
        p.init(Pin.OUT)
        p.value(1)

    time.sleep_us(10)

    for p in sensor_pins:
        p.init(Pin.IN)

    start = time.ticks_us()

    while True:

        t = time.ticks_diff(time.ticks_us(), start)

        for i,p in enumerate(sensor_pins):
            if p.value() == 0 and sensor_values[i] == 0:
                sensor_values[i] = t

        if t > 3000:
            break

    return sensor_values


# ===== Calculate line position =====
def read_position():

    values = read_sensors()

    weights = [-3500,-2500,-1500,-500,500,1500,2500,3500]

    weighted_sum = 0
    total = 0

    for i in range(8):

        value = max(0,3000-values[i])

        weighted_sum += value * weights[i]
        total += value

    if total == 0:
        return None

    return weighted_sum / total


# ===== Motor control =====
def set_motor(left_speed,right_speed):

    left_speed = max(min(int(left_speed),65535),-65535)
    right_speed = max(min(int(right_speed),65535),-65535)

    if left_speed >= 0:
        motorL1.high()
        motorL2.low()
    else:
        motorL1.low()
        motorL2.high()

    if right_speed >= 0:
        motorR1.high()
        motorR2.low()
    else:
        motorR1.low()
        motorR2.high()

    motorPWMLeft.duty_u16(abs(left_speed))
    motorPWMRight.duty_u16(abs(right_speed))


# ===== Soft start =====
i = 0

while i < base_speed:
    motorPWMLeft.duty_u16(int(i))
    motorPWMRight.duty_u16(int(i))
    i += 100


# ===== MAIN LOOP =====
while True:

    # --- encoder speed correction ---
    if positionMotoru > 16000 and positionMotoru < 17000:
        if base_speed > 18000:
            base_speed -= 5

    if positionMotoru > 17000:
        if base_speed < 18000:
            base_speed += 5

    # --- read line position ---
    position = read_position()

    if position is not None:

        error = position / 3500

        integral += error
        integral = max(min(integral,100),-100)

        derivative = error - previous_error

        correction = Kp*error + Ki*integral + Kd*derivative

        left_speed = base_speed + correction
        right_speed = base_speed - correction

        set_motor(left_speed,right_speed)

        previous_error = error


# ===== stop motors =====
while base_speed > 0:

    motorPWMRight.duty_u16(base_speed)
    motorPWMLeft.duty_u16(base_speed)

    base_speed -= 200

    time.sleep(0.01)

print("STOP")
