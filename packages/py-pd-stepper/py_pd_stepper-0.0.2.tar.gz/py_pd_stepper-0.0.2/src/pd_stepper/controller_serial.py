from .serial_port import SerialPort

class ControllerSerial:
    def __init__(self, port: SerialPort):
        self.__serial_port = port

    def get_status(self):
        return self.__serial_port.communicate('status')

    def turn_light_on(self):
        self.__serial_port.communicate('setLight:0')

    def turn_light_off(self):
        self.__serial_port.communicate('setLight:1')

    def set_target_position(self, position: int):
        self.__serial_port.communicate(f'setTarget:{position}')

    def set_voltage(self, voltage: float):
        if voltage != 5 or 9 or 12 or 15 or 20:
            raise ValueError("Voltage must be 5, 9, 12, 15 or 20")
        self.__serial_port.communicate(f'setVoltage:{voltage}')

    def set_speed(self, speed: float):
        self.__serial_port.communicate(f'setSpeed:{speed}')