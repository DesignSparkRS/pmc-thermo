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

## Python remote client
Flash the `pmc_thermo_m7_rc` version of the Arduino code to the PMC. This has its I/O controlled by the Python remote client.

In the `remote_client` directory, create a virtual python environment and install the dependencies:
```
$ cd remote_client
$ sudo apt install python3-venv
$ python -m venv venv
$ source venv/bin/activate
(venv) pip install pyyaml paho-mqtt
(venv) pip install paho-mqtt
```

Run the remote client Python script:
```
(venv) python3 remote_client.py
```

