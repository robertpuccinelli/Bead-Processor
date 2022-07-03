'''
The purpose of this testing script is to calibrate the flow rate of a peristaltic pump and evaluate the linearity of the device over a range of flow rates. The script assumes a PC will be used with a FTDI serial device for evaluating the pump.
'''

#from importlib import resources
from pkg_resources import Requirement, resource_filename
from enum import Enum, auto
from time import sleep
from pymotors import TicStepper
from pyconfighandler import validateConfig


def config_val(param: str):
    return int(config["DEFAULT"][param])


class DefaultConfigFields(Enum):
    PUMP_STEPS_REV = auto()
    PUMP_MICROS = auto()
    PUMP_MOTOR_CURR = auto()
    PUMP_MAX_RPM = auto()
    PUMP_BUS = auto()
    PUMP_BAUD = auto()
    PUMP_NUM_ALIQUOTS = auto()
    PUMP_VOL_ALIQUOTS = auto()


path_to_config = resource_filename(Requirement.parse("beadprocessor"), "config/test_flowrate.config")
required_config_fields = DefaultConfigFields
config, config_options = validateConfig(path_to_config, required_config_fields)

bus = config["DEFAULT"]['PUMP_BUS']
baud = config_val('PUMP_BAUD')
micros = config_val('PUMP_MICROS')
steps_rev = config_val('PUMP_STEPS_REV')
motor_current = config_val('PUMP_MOTOR_CURR')
max_rpm = config_val('PUMP_MAX_RPM')
aliquots = config_val('PUMP_NUM_ALIQUOTS')
target_volume = config_val('PUMP_VOL_ALIQUOTS')


pump = TicStepper(com_type='Serial', port_params=[bus, baud], input_steps_per_rev=steps_rev, input_rpm=max_rpm)
pump.microsteps = 1 / micros
pump.setCurrentLimit(motor_current)
pump.enable = True
min_rpm = max_rpm / aliquots
pump.rpm = min_rpm

input('Pump will cycle through 10 revolutions to calibrate volume. Press `Enter` to continue.')

pump.moveRelDist(10)
sleep(1)
while(pump.isMoving()):
    sleep(1)

calibration_volume = int(input('Volume dispensed : '))
pump.dist_per_rev = calibration_volume / 10
pump.rpm = min_rpm

input('Pump will begin dispensing ({}) {} uL aliquots at various RPMs. Press `Enter` when ready for aliquot 1.'.format(aliquots, target_volume))

pump.moveRelDist(target_volume)
while(pump.isMoving()):
    sleep(1)

for i in range(2, aliquots + 1):
    input('Prepare the next aliquot and press `Enter` when ready.')
    pump.rpm = min_rpm * i
    pump.moveRelDist(target_volume)
