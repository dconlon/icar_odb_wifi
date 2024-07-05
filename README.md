# iCar OBD WiFi
I needed to make the EV battery state of charge % from my vehicle accessible programatically to allow smart charging.  

## Vgate iCar Pro WiFi

The [Vgate iCar 2 WiFi](https://www.vgatemall.com/products-detail/i-14/) is [available on Amazon](https://www.amazon.co.uk/Vgate-interface-diagnostics-android-windows/dp/B00OY0X8IS/ref=pd_day0fbt_d_sccl_2/262-5009615-3485139) for < £30 .  It plugs into the ODB2 port of the vehicle and is small and unobtrusive enough to leave plugged in inside the car permanently.

Internally it consists of: 

1. ELM327 ODB to RS232 interpreter ([manual](https://www.elmelectronics.com/DSheets/ELM327DSH.pdf))
2. [Hi-Flying LPT230](http://www.hi-flying.com/hf-lpt230) UART to WiFi module - 1MB flash version ([manual](https://fccid.io/2ACSV-HF-LPT230/User-Manual/Users-Manual-3552381.pdf))

Out of the box the LPT230 is configured as an AP broadcasting an open network with SSID “V-Link”.  After connecting to the WiFi network the LPT230 is 192.168.0.10 and its TCP port 35000 provides transparent bi-directional access to the RS232 side of the ELM327.

## LPT230 Configuration

Considering that the vehicle OBD2 port is writable, I didn’t want to leave the iCar plugged in permanently broadcasting an open WiFi network.  

The 1MB flash version of the LPT230 unfortunately does not have a full web interface but it is sufficient to change WiFi configuration to station mode to have the LPT230 connect to your home WiFi instead of it being an open AP.  Whilst connected to the V-Link WiFi open a web browser to http://192.168.0.10 login with username “guest” password “”:

Using the web interface method above only the WiFi mode is changed so the LPT230 remains as a TCP server on port 35000 of whatever IP your DHCP server gives it.  To change any other configuration Hi Flying offer a (Windows only) tool which will send any of the AT commands documented in the manual above to the MAC of the LPT230.  Options are available to configure it as an AP with WPA2 security and/or have it be a TCP or UDP client that sends data to a socket on your home server.

If at any point you loose network access to the LPT230 you must open up the iCar 2 and jumper together pins 12 (nReload) and 16 (Gnd) of the LPT230 for 4 seconds after which the default configuration (open WiFi network) will return.

## ELM327 Configuration

The iCar 2 will turn off WiFi when ELM327 enters lower power mode and can the only be awoken by pressing the power button on it.  Out of the box this is after 20 mins of inactivity.  The Programmable Parameters (PP) section of the ELM327 manual documents all configuration options including PP 0E - a bitmap of power control options.

Using @dailab’s [fork of python-OBD](https://github.com/dailab/python-OBD-wifi/tree/master) (which connects to ELM327 over TCP instead of serial port) the following code will disable the low power functions:



The iCar 2 now stays on permanently and connects to my home WiFi when the car arrives home and is in range of my WiFi.

## Communicating with the vehicle

My use case is to fetch EV battery state of charge but you can read any parameter you know the OBD2 PID for.

For my vehicle (2021 Range Rover Velar PHEV) certain parameters including EV state of charge seem to be always accessible whilst others (e.g. petrol fuel level) become inaccessible a few minutes after the ignition is turned off.
