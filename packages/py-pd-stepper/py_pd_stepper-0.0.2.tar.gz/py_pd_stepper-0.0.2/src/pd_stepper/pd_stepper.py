from .controller_serial import ControllerSerial
from .serial_port import SerialPort

class PDStepper:
    __serial_port: SerialPort
    controller: ControllerSerial
    def __init__(self, port: str) -> None:
        self.__serial_port = SerialPort(port)
        self.__serial_port.open_serial()
        self.controller = ControllerSerial(self.__serial_port)

    def get_serial_port(self) -> SerialPort:
        return self.__serial_port
