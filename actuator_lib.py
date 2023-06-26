import serial
import struct

port = serial.Serial(
    port="/dev/ttyUSB1",
    baudrate=9600,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE,
    )

port.close()
command = struct.pack('<BBBBBBBB', 0xCC, 0x00, 0x20, 0x00, 0x00, 0xDD, 0xC9, 0x01)
port.open()
port.write(b'\xCC\x00\x20\x00\x00\xdd\xc9\x01')
# port.write(command)
print(port.read(8))
port.close()
# command = struct.pack('<BBBBBBBB', 0xCC, 0x00, 0x44, 0x01, 0x00, 0xDD, 0xEE, 0x01)
# port.open()
# port.write(command)