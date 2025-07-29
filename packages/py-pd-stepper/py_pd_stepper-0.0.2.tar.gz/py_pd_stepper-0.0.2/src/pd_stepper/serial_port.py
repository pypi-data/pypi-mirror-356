from serial import Serial, SerialTimeoutException
from .utils import lock_threading_lock
from threading import Lock
import time

class SerialPort:
    def __init__(self, port: str, timeout: float = 5.0, baudrate: int = 115200):
        self.__serial = Serial(port, baudrate=baudrate,  timeout=timeout, write_timeout=timeout)
        self.__connected = True
        self.open_serial()
        self.__port = port
        self.__lock = Lock()
        self.__timeout = timeout

    def open_serial(self):
        if not self.__connected:
            self.__serial.open()
            time.sleep(2)

    def close_serial(self):
        if self.__connected:
            self.__serial.close()

    def communicate(self, command: str):
        with lock_threading_lock(self.__lock, timeout=self.__timeout):
            self.__serial.reset_input_buffer()
            if self.__serial.in_waiting > 0:
                self.__serial.read(self.__serial.in_waiting)

            if isinstance(command, str):
                command = command.encode('utf-8') + b'\r'
            else:
                raise Exception("Command must be a string")

            try:
                self.__serial.write(command)
                print(f"Command sent: {command.decode('utf-8')}")
                time.sleep(0.5)

                response = self.__serial.readline().decode('utf-8')
                if not response:
                    print("No response received.")
                    raise Exception("No response received.")

                print(f"Response: {response}")

            except SerialTimeoutException as e:
                print(f"Timeout error: {e}")
                raise Exception("Serial timeout occurred")

            except Exception as e:
                print(f'Errrror: {e}')
                raise Exception("Could not send command")