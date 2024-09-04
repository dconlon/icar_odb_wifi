import obd

from obd.OBDCommand import OBDCommand
from obd.decoders import uas
from obd.protocols import ECU

icar = obd.OBD("192.168.1.134", 35000)

# Command specification for ODB PID 01A6
odometer = OBDCommand("ODOMETER", "Odometer", b"01A6", 6, uas(0x25), ECU.ENGINE, True)

response = icar.query(odometer, force=True) # force to avoid checking if commands is in obd.commands

print(f"Odometer: {response.value}")
