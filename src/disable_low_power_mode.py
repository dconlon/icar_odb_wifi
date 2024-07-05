import obd

icar = obd.OBD("192.168.1.134", 35000)  # IP of LPT230 on network

elm327 = icar.interface

# Out of the box my iCar had FA at PP0E (11111010), toggle first bit to 
# disable all low power (01111010 = 7A)
elm327.send_and_parse(b"ATPP0ESV7A")

# Save the new setting
elm327.send_and_parse(b"ATPP0EON")
