from pkg_resources import Requirement, resource_filename
from beadprocessor import BeadProcessorHardwareSetup

path_to_config = resource_filename(Requirement.parse("beadprocessor"), "config/beadprocessor.config")
hardware = BeadProcessorHardwareSetup()
hardware.configValidation(path_to_config)
hardware.initializeConfig('PC')

applyMagnets = hardware.subunits['UI'].applyMagnets
removeMagnets = hardware.subunits['UI'].removeMagnets
changePlate  = hardware.subunits['UI'].changePlate
sleep = hardware.subunits['UI'].sleep
pump = hardware.subunits['PUMPS'][0]
wells_per_pump = hardware.subunits['WELLS_PER_PUMP']

sample_volume = 900 * wells_per_pump
dispense_volume = 200 * wells_per_pump
wash_volume = 900 * wells_per_pump
agitate_volume = 10 * wells_per_pump

dispense_cycles = int(dispense_volume/agitate_volume)

applyMagnets()
changePlate('Sample Plate')
pump.aspirate(sample_volume)
changePlate('Wash Plate 1')
pump.aspirate(wash_volume)
changePlate('Wash Plate 2')
removeMagnets()
pump.dispense(agitate_volume)
pump.aspirate(agitate_volume)
sleep(5)
pump.dispense(agitate_volume)
applyMagnets()
pump.aspirate(agitate_volume)
sleep(10)
pump.aspirate(wash_volume)
changePlate('Destination Plate')
removeMagnets()
for i in range(0, dispense_cycles):
    sleep(10)
    pump.dispense(agitate_volume)
print('Protocol complete!')
