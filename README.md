# pmc-thermo
Arduino Portenta Machine Control IIot thermocouple examples

## Installation
Clone the repo to your PC:
```
https://github.com/milnepe/pmc-thermo.git
```

## Compile and upload
Open the example you want to flash to the PMC and use the Arduino CLI to comple and flash

For the M7 core:
```
$ arduino-cli compile --fqbn arduino:mbed_portenta:envie_m7
$ arduino-cli upload -p /dev/ttyACM0 --fqbn arduino:mbed_portenta:envie_m7
```

For the M4 core:
```
$ arduino-cli compile --fqbn arduino:mbed_portenta:envie_m7 --board-options "target_core=cm4"
$ arduino-cli upload -p /dev/ttyACM0 --fqbn arduino:mbed_portenta:envie_m7 --board-options "target_core=cm4"
```
