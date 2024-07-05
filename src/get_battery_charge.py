import obd

from obd.OBDCommand import OBDCommand
from obd.decoders import percent
from obd.protocols import ECU

icar = obd.OBD("192.168.1.134", 35000)

# Command specification for ODB PID 015B
battery = OBDCommand("BATTERY_LEVEL", "Battery Level", b"015B", 3, percent, ECU.ENGINE, True)

response = icar.query(battery)

print(f"Battery level: {response.value}")
