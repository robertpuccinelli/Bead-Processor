'''
The pump controller module provides a class and utilities for controlling the flow of the bead processor.
'''

from time import sleep

class Pump():
    '''Pump base class.

    Parameters
    ----------
    vol_per_rev : float
        The volume displaced by one revolution of the pump.
    initial_flow_rate : float
        The initial volume to displace per minute of runtime.

    Attributes
    ----------
    flow_rate : float
        Current volume per minute.
    running : bool
        Current state of the pump.
    '''

    def __init__(self, vol_per_rev, initial_flow_rate):
        self._vol_per_rev = vol_per_rev
        self.flow_rate = initial_flow_rate

    @property
    def flow_rate(self):
        '''Microliters per minute.'''
        return self._revs_per_min * self._vol_per_rev

    @flow_rate.setter
    def flow_rate(self,target_flow_rate):
        self._revs_per_min = target_flow_rate / self._vol_per_rev
        self._updateFlowRate(self._revs_per_min)

    @property
    def is_running(self):
        return self._status()

    def aspirate(self, volume, blocking=True):
        self._pump(abs(volume), blocking)

    def dispense(self, volume, blocking=True):
        self._pump(-abs(volume), blocking)

    def stopPump(self):
        self._stop()

    def _pump(self, volume, blocking):
        raise NotImplementedError()

    def _setVolPerRev(self, vol_per_rev):
        raise NotImplementedError()

    def _status(self):
        raise NotImplementedError()

    def _stop(self):
        raise NotImplementedError()

    def _updateFlowRate(self):
        raise NotImplementedError()


class PumpTic(Pump):
    '''A pump class driven by a Tic stepper driver board.

    Paramters
    ---------
    MotorObj : TicStepper
        Object interfacing with motor hardware
    ul_per_rev : int
        Microliters displaced by one revolution of the pump.
    
    '''
    def __init__(self, MotorObj, vol_per_rev, initial_flow_rate):
        self._motor = MotorObj
        self._motor.enable = True
        super().__init__(vol_per_rev=vol_per_rev, initial_flow_rate=initial_flow_rate)

    def _pump(self, volume, blocking):
        self._motor.moveRelDist(volume)
        if blocking:
            sleep(.02)
            while(self._motor.isMoving()==True):
                pass


    @property
    def _vol_per_rev(self):
        return self._motor.dist_per_rev

    @_vol_per_rev.setter
    def _vol_per_rev(self, vol_per_rev):
        self._motor.dist_per_rev = vol_per_rev

    def _status(self):
        return self._motor.isMoving()

    def _stop(self):
        self._motor.stop()

    def _updateFlowRate(self, flow_rate):
        self._motor.rpm = flow_rate
