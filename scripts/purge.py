from pkg_resources import Requirement, resource_filename
from beadprocessor import BeadProcessorHardwareSetup

path_to_config = resource_filename(Requirement.parse("beadprocessor"), "config/beadprocessor.config")
hardware = BeadProcessorHardwareSetup()
hardware.configValidation(path_to_config)
hardware.initializeConfig('PC')
pump = hardware.subunits['PUMPS'][0]
pump.flow_rate = 500*100
input('Press `Enter` to begin purging lines.')
pump.dispense(1000000)
input('Press `Enter` once lines have been purged.')
pump.stopPump()
pump.dispense(150)
