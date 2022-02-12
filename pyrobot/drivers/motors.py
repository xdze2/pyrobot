import time
import RPi.GPIO as GPIO


# Motor names
MOTOR_LEFT = 0
MOTOR_RIGHT = 1
NUM_MOTORS = 2

# Motor driver pins, via DRV8833PWP Dual H-Bridge
MOTOR_EN_PIN = 26
MOTOR_LEFT_P = 8
MOTOR_LEFT_N = 11
MOTOR_RIGHT_P = 10
MOTOR_RIGHT_N = 9


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)


# Setup motor driver
GPIO.setup(MOTOR_EN_PIN, GPIO.OUT)
GPIO.setup(MOTOR_LEFT_P, GPIO.OUT)
GPIO.setup(MOTOR_LEFT_N, GPIO.OUT)
GPIO.setup(MOTOR_RIGHT_P, GPIO.OUT)
GPIO.setup(MOTOR_RIGHT_N, GPIO.OUT)

# https://www.ti.com/lit/ds/symlink/drv8833.pdf?HQS=dis-mous-null-mousermode-dsf-pf-null-wwe&ts=1644518569384&ref_url=https%253A%252F%252Fwww.mouser.com%252F
GPIO.output(MOTOR_EN_PIN, True)

GPIO.output(MOTOR_LEFT_P, True)
GPIO.output(MOTOR_LEFT_N, False)
time.sleep(1)

GPIO.output(MOTOR_LEFT_P, True)
GPIO.output(MOTOR_LEFT_N, True)

time.sleep(1)
GPIO.output(MOTOR_EN_PIN, False)

exit()
motor_left_p_pwm = GPIO.PWM(MOTOR_LEFT_P, 100)
motor_left_p_pwm.start(0)

motor_left_n_pwm = GPIO.PWM(MOTOR_LEFT_N, 100)
motor_left_n_pwm.start(0)

motor_right_p_pwm = GPIO.PWM(MOTOR_RIGHT_P, 100)
motor_right_p_pwm.start(0)

motor_right_n_pwm = GPIO.PWM(MOTOR_RIGHT_N, 100)
motor_right_n_pwm.start(0)
motor_pwm_mapping = {
    MOTOR_LEFT_P: motor_left_p_pwm,
    MOTOR_LEFT_N: motor_left_n_pwm,
    MOTOR_RIGHT_P: motor_right_p_pwm,
    MOTOR_RIGHT_N: motor_right_n_pwm,
}


def set_motor_speed(motor, speed):
    """Sets the speed of the given motor.
    motor: the ID of the motor to set the state of
    speed: the motor speed, between -1.0 and 1.0
    """
    if type(motor) is not int:
        raise TypeError("motor must be an integer")

    if motor not in range(2):
        raise ValueError(
            """motor must be an integer in the range 0 to 1. For convenience, use the constants:
            MOTOR_LEFT (0), or MOTOR_RIGHT (1)"""
        )

    # Limit the speed value rather than throw a value exception
    speed = max(min(speed, 1.0), -1.0)

    GPIO.output(MOTOR_EN_PIN, True)
    pwm_p = None
    pwm_n = None
    if motor == 0:
        # Left motor inverted so a positive speed drives forward
        pwm_p = motor_pwm_mapping[MOTOR_LEFT_N]
        pwm_n = motor_pwm_mapping[MOTOR_LEFT_P]
    else:
        pwm_p = motor_pwm_mapping[MOTOR_RIGHT_P]
        pwm_n = motor_pwm_mapping[MOTOR_RIGHT_N]

    if speed > 0.0:
        pwm_p.ChangeDutyCycle(100)
        pwm_n.ChangeDutyCycle(100 - (speed * 100))
    elif speed < 0.0:
        pwm_p.ChangeDutyCycle(100 - (-speed * 100))
        pwm_n.ChangeDutyCycle(100)
    else:
        pwm_p.ChangeDutyCycle(100)
        pwm_n.ChangeDutyCycle(100)


def set_motor_speeds(l_speed: float, r_speed: float):
    """Sets the speeds of both motors at once.
    l_speed: the left motor speed, between -1.0 and 1.0
    r_speed: the right motor speed, between -1.0 and 1.0
    """
    set_motor_speed(MOTOR_LEFT, l_speed)
    set_motor_speed(MOTOR_RIGHT, r_speed)


# set_motor_speeds(0.1, -0.1)
# time.sleep(.4)
set_motor_speeds(0, 0)

