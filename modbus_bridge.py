import minimalmodbus
import struct
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
        try:
            with self.lock:
                return self.instrument.read_register(register, number_of_decimals=0, functioncode=4)
        except Exception as e:
            print(f"FC04 read failed for 0x{register:02X}: {e}")
            return None

    def read_via_fc06(self, register):
        try:
            with self.lock:
                payload = struct.pack('>HH', register, 0x0000)
                response = self.instrument._perform_command(6, payload)
                _, value = struct.unpack('>HH', response)
                return value
        except Exception as e:
            print(f"FC06 read failed for 0x{register:02X}: {e}")
            return None

    def write_register(self, register, value):
        try:
            with self.lock:
                self.instrument.write_register(register, value, 0, functioncode=6)
        except Exception as e:
            print(f"Write failed for 0x{register:02X}: {e}")

    def read_coils(self):
        try:
            with self.lock:
                payload = struct.pack('>HH', 0x0001, 0x000E)
                response = self.instrument._perform_command(1, payload)
                if len(response) < 3 or response[0] != 2:
                    raise ValueError("FC01 response malformed")
                bitmask = (response[2] << 8) | response[1]
                return [(bitmask >> i) & 1 for i in range(16)]
        except Exception as e:
            print(f"FC01 read failed: {e}")
            return []
