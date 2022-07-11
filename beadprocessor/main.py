'''
1. Initiate peripherals
2. Set base state
3. Begin loop
    a. listen for inputs
    b. execute state transition

'''
from time import monotonic
from pyconfighandler import validateConfig
import RPi.GPIO as GPIO
from pybuttons import ButtonBase
from pymotors import TicStepper


run_thresh = "FALLING"
run_pin = 


buttonRun = ButtonBase(run_thresh, run_pin, run_debounce)
buttonRun.enable = True

def _initializePumps(config, config_mode):
    steps_rev = 200
    micros = 4
    motor_current = 31
    vol_rev = float(config[config_mode]['PUMP_VOL_REV'])
    time_unit = 'm'
    flowrate = 500
    bus = int(config[config_mode]['BUS'])
    addr = int(config[config_mode]['PUMP_ADDR_START'], 16)

    motor = TicStepper(com_type='I2C', port_params=bus, address=addr, input_dist_per_rev=, input_steps_per_rev=steps_rev, input_rpm=500)
    motor.microsteps = 1 / micros
    motor.setCurrentLimit(motor_current)
    motor.enable = True

    return motor

