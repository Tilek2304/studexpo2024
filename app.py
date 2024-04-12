from flask import Flask, render_template, request
import RPi.GPIO as GPIO

app = Flask(__name__)

# Настройка GPIO
GPIO.setmode(GPIO.BCM)
motors = {
    'Motor1': {'EN': 21, 'IN1': 7, 'IN2': 11},
    'Motor3': {'EN': 22, 'IN1': 12, 'IN2': 13},
    'Motor2': {'EN': 23, 'IN1': 15, 'IN2': 16},
    'Motor4': {'EN': 24, 'IN1': 18, 'IN2': 19}
}
for motor, pins in motors.items():
    GPIO.setup(pins['EN'], GPIO.OUT)
    GPIO.setup(pins['IN1'], GPIO.OUT)
    GPIO.setup(pins['IN2'], GPIO.OUT)
    motors[motor]['PWM'] = GPIO.PWM(pins['EN'], 100)
    motors[motor]['PWM'].start(0)

def set_motor(motor, speed, direction):
    pins = motors[motor]
    pwm = pins['PWM']
    if direction == 'forward':
        GPIO.output(pins['IN1'], GPIO.HIGH)
        GPIO.output(pins['IN2'], GPIO.LOW)
    elif direction == 'backward':
        GPIO.output(pins['IN1'], GPIO.LOW)
        GPIO.output(pins['IN2'], GPIO.HIGH)
    elif direction == 'stop':
        GPIO.output(pins['IN1'], GPIO.LOW)
        GPIO.output(pins['IN2'], GPIO.LOW)
    pwm.ChangeDutyCycle(abs(int(speed)))

def rotate(direction, speed):
    if direction == 'left':
        set_motor('Motor1', speed, 'forward')
        set_motor('Motor3', speed, 'forward')
        set_motor('Motor2', speed, 'backward')
        set_motor('Motor4', speed, 'backward')
    elif direction == 'right':
        set_motor('Motor2', speed, 'forward')
        set_motor('Motor4', speed, 'forward')
        set_motor('Motor1', speed, 'backward')
        set_motor('Motor3', speed, 'backward')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/control', methods=['POST'])
def control():
    motor = request.form['motor']
    action = request.form['action']
    speed = request.form['speed']
    set_motor(motor, speed, action)
    return ('', 204)

@app.route('/rotate', methods=['POST'])
def handle_rotate():
    direction = request.form['action']
    speed = request.form['speed']
    rotate(direction, speed)
    return ('', 204)

@app.route('/stop', methods=['POST'])
def stop():
    for motor in motors.keys():
        set_motor(motor, 0, 'stop')
    return ('', 204)

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=80, debug=True)
    finally:
        for motor in motors.values():
            motor['PWM'].stop()
        GPIO.cleanup()