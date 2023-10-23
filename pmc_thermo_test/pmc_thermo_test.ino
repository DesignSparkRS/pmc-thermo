/*
  Machine Control - Thermocouples Read Sensors

  This example reads the temperatures measured by the thermocouples
  connected to the Machine Control Carrier's temp probe inputs and prints
  them to the Serial Monitor once a second.

  The circuit:
   - Portenta H7
   - Portenta Machine Control Carrier
   - Two K Type thermocouple temperature sensors connected to
      TEMP PROBES CH0 and CH1 on the Machine Control
   - A J Type thermocouple temperature sensor connected to
     TEMP PROBES CH3 on the Machine Control

  This example code is in the public domain.
*/

#include <Arduino_MachineControl.h>

using namespace machinecontrol;

void setup() {
  Serial.begin(9600);
  // Initialize temperature probes
  temp_probes.tc.begin();
  Serial.println("Temperature probes initialization done");
  // Enables Thermocouples chip select
  temp_probes.enableTC();
  Serial.println("Thermocouples enabled");
}

void sample_thermocouple(int channel, int t_couple) {
  //Set channel, each has internal 150 ms delay
  temp_probes.selectChannel(channel);
  //Take CH0 measurement
  float degrees = temp_probes.tc.readTemperature(t_couple);
  Serial.print("Temperature CH");
  Serial.print(channel);
  Serial.print(" [°C]: ");
  Serial.println(degrees);  
}

void loop() {
  sample_thermocouple(0, PROBE_K);
  sample_thermocouple(1, PROBE_K);
  sample_thermocouple(2, PROBE_J);
  Serial.println();
}