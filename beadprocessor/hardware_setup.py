from pkg_resources import Requirement, resource_filename
from enum import Enum, auto
from pymotors import TicStepper
from pyconfighandler import validateConfig
from beadprocessor import PumpTic, UIPC

class DefaultConfigFields(Enum):
    WELLS_NUM = auto()
    PUMP_STEPS_REV = auto()
    PUMP_MICROS = auto()
    PUMP_CURR = auto()
    PUMP_VOL_REV = auto()
    PUMP_FLOW_RATE_WELL = auto()

class BeadProcessorHardwareSetup():
    def __init__(self):
        self._config = None
        self.config_options = None
        self.config_valid = False

        self.pumps = []
        self.ui = []

        self.pumps_standby = False
        self.ui_standby = False

    def configValidation(self, path_to_config, required_fields=DefaultConfigFields):
        self._config, self.config_options = validateConfig(path_to_config, required_fields)
        self.config_valid = True

    def initializeConfig(self, config_mode: str):
        if self.config_valid is False:
            return
        
        if config_mode not in self.config_options:
            raise ValueError('Config option {} not found. Available options: {}'.format(config_mode, self.config_options))

        self.pumps = self._initializePumps(self._config, config_mode)
        self.pumps_standby = True

        self.ui = self._initializeUI(self._config, config_mode)
        self.ui_standby = True

        self.subunits = {**self.pumps,
                         **self.ui,
                         }

    def reset(self):
        self.__init__()

    @staticmethod
    def _initializePumps(config, config_mode):
        pump_mode = config[config_mode]['PUMP_MODE']
        num_wells = int(config[config_mode]['WELLS_NUM'])
        num_pumps = int(config[config_mode]['PUMP_NUM'])
        steps_rev = int(config[config_mode]['PUMP_STEPS_REV'])
        micros = int(config[config_mode]['PUMP_MICROS'])
        curr = int(config[config_mode]['PUMP_CURR'])
        vol_rev = int(config[config_mode]['PUMP_VOL_REV'])
        well_flow_rate = int(config[config_mode]['PUMP_FLOW_RATE_WELL'])

        wells_per_pump = num_wells / num_pumps
        flow_rate = wells_per_pump * well_flow_rate

        pumps = []

        for i in range(0, num_pumps):
            if pump_mode is 'SERIAL':
                port = config[config_mode]['PUMP_PORT']
                baud = int(config[config_mode]['PUMP_BAUD'])
                motor = TicStepper(com_type='Serial', port_params=[port,baud], input_steps_per_rev=steps_rev, input_rpm = 500)
            motor.microsteps = 1/micros
            motor.setCurrentLimit(curr)
            motor.enable = True

            pumps.append(PumpTic(motor, vol_per_rev=vol_rev, initial_flow_rate=flow_rate))

        return {'PUMPS': pumps, 'PUMP_FLOW_RATE': flow_rate, 'WELLS_PER_PUMP': wells_per_pump}


    @staticmethod
    def _initializeUI(config, config_mode):

        ui = None

        if config_mode is 'PC':
            ui = UIPC()

        return {'UI': ui}