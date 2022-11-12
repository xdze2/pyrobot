#include <pigpio.h>
#include <stdio.h>

#define SHUTDOWN_REGISTER 0x00
#define SET_PWM_REGISTER 0x01
#define LED_CTRL_REGISTER1 0x13
#define LED_CTRL_REGISTER2 0x14
#define LED_CTRL_REGISTER3 0x15
#define UPDATE_REGISTER 0x16
#define RESET_REGISTER 0x17
#define SN3218_ADDR 0x54

#define EN_GPIO 7

int main() {
  int handle;

  if (gpioInitialise() < 0)
    return 1;

  gpioSetMode(EN_GPIO, PI_OUTPUT);
  gpioWrite(EN_GPIO, 1);
  gpioDelay(500000);

  handle = i2cOpen(1, SN3218_ADDR, 0);
  printf("handle: %d\n", handle);

  // start
  unsigned int shutdown = SHUTDOWN_REGISTER;
  unsigned int update = UPDATE_REGISTER;
  unsigned int pwm = SET_PWM_REGISTER;
  unsigned int enable1 = LED_CTRL_REGISTER1;
  unsigned int enable2 = LED_CTRL_REGISTER2;
  unsigned int enable3 = LED_CTRL_REGISTER3;

  i2cWriteByteData(handle, shutdown, 0x1); // normal operation
  i2cWriteByteData(handle, pwm, 0xff);
  i2cWriteByteData(handle, enable1, 0xff);
  i2cWriteByteData(handle, enable2, 0xff);
  i2cWriteByteData(handle, enable3, 0xff);
  i2cWriteByteData(handle, update, 0xff);

  printf("yo\n");

  gpioDelay(1000000);
  i2cWriteByteData(handle, shutdown, 0x0); // shutdown
  i2cClose(handle);
  gpioTerminate();
}