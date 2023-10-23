#include "Arduino.h"
#include "RPC.h"
#include <Arduino_MachineControl.h>

using namespace machinecontrol;
using namespace rtos;

#define TCH0 0
#define TCH1 1
#define TCH2 2
#define IOCH00 0

Thread copyTemperatureThread;

float sample_thermocouple(int channel, int t_couple) {
    temp_probes.selectChannel(channel);
    return temp_probes.tc.readTemperature(t_couple);  
}

void callCopyTemperatureFromM4() {
  while (1) {
    delay(1000);  // Wait for next calculation
    float temp_ch0 = sample_thermocouple(TCH0, PROBE_K);
    float temp_ch1 = sample_thermocouple(TCH1, PROBE_K);
    float temp_ch2 = sample_thermocouple(TCH2, PROBE_J);
    auto result = RPC.call("copyTemperature", temp_ch0, temp_ch1, temp_ch2).as<float>();
  }
}

void blink_led(int io_channel) {
  digital_outputs.set(io_channel, HIGH);
  delay(1000);
  digital_outputs.set(io_channel, LOW);
  delay(1000);  
}

void setup() {
  RPC.begin();
  digital_outputs.setLatch();

  temp_probes.tc.begin();
  temp_probes.enableTC();

  copyTemperatureThread.start(callCopyTemperatureFromM4);
}

void loop() {
  blink_led(IOCH00);
}
