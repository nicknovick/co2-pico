# Description
MH-Z19C CO2 sensor connected to a Raspberry Pi Pico. CO2 and temperature values are shown on the SH1106 128x64 1,3" OLED display.  
To start the program copy both `main.py` and `sh1106.py` to the root directory of the Pico.

# Connection schematics
[Fritzing file](docs/CO2%20sensor%20on%20Pi%20Pico.fzz) contains the schematics pictured below.<br>
![Connection schematics](docs/CO2%20sensor%20on%20Pi%20Pico.png)

[Source for the SH1106 module](https://github.com/robert-hh/SH1106/blob/master/sh1106.py)
Temperature reading according to the [undocumented reading from MH-Z19C](https://revspace.nl/MHZ19#Command_0x86_.28read_concentration.29)