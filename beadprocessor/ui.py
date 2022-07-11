from time import sleep

class UIBase():


    def applyMagnets(self):
        raise NotImplementedError()

    def removeMagnets(self):
        raise NotImplementedError()

    def changePlate(self, plate_type: str):
        raise NotImplementedError()

    def sleep(self, seconds: int):
        sleep(seconds)


class UIPC(UIBase):


    def applyMagnets(self):
        input('Slide magnets towards tubing. Press `Enter` to continue.')

    def removeMagnets(self):
        input('Slide magnets away from tubing. Press `Enter` to continue.')

    def changePlate(self, plate_type: str):
        input('Change the well plate to {}. Press `Enter` to continue.'.format(plate_type))