import serial
import time
import struct

port = serial.Serial(port="/dev/ttyUSB0",
                     baudrate=9600,
                     bytesize=serial.EIGHTBITS,
                     parity=serial.PARITY_NONE,
                     stopbits=serial.STOPBITS_ONE,
                     )
port.close()
# command = struct.pack('<BBBBBBBB', 0xCC, 0x00, 0x42, 0x00, 0x00, 0xDD, 0xE8, 0x01)
try:
    port.open()
except Exception:
    port.open()
command = ("/1A6000OA0R" + '\r\n').encode()
# command = ("/1ZR" + '\r\n').encode()
port.write(command)
print(port.readline())
port.close()