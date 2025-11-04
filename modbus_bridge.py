import minimalmodbus
import threading

class DviModbusBridge:
    def __init__(self, port, slave_id):
        self.instrument = minimalmodbus.Instrument(port, slave_id)
        self.instrument.serial.baudrate = 9600
        self.instrument.serial.bytesize = 8
        self.instrument.serial.parity = minimalmodbus.serial.PARITY_NONE
        self.instrument.serial.stopbits = 1
        self.instrument.serial.timeout = 2
        self.instrument.mode = minimalmodbus.MODE_RTU
        self.lock = threading.Lock()

    def read_input(self, register):
        with self.lock:
            return self.instrument.read_register(register, number_of_decimals=0, functioncode=4)

    def read_via_fc06(self, register):
        with self.lock:
            payload = struct.pack('>HH', register, 0x0000)
            response = self.instrument._perform_command(6, payload)
            _, value = struct.unpack('>HH', response)
            return value

    def read_coils(self):
        with self.lock:
            payload = struct.pack('>HH', 0x0001, 0x000E)
            response = self.instrument._perform_command(1, payload)
            bitmask = (response[2] << 8) | response[1]
            return [(bitmask >> i) & 1 for i in range(16)]
