#include <pigpio.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define SHUTDOWN_REGISTER 0x00
#define SET_PWM_REG 0x01 // first led addr
#define LED_CTRL_REGISTER1 0x13
#define LED_CTRL_REGISTER2 0x14
#define LED_CTRL_REGISTER3 0x15
#define UPDATE_REGISTER 0x16
#define RESET_REGISTER 0x17
#define SN3218_ADDR 0x54

#define EN_GPIO 7

void set_rgbled_color(int handle, int rgb_led_idx, int *color) {
  printf("Set color for led %d: (%d %d %d)\n", rgb_led_idx, color[0], color[1],
         color[2]);
  for (int c = 0; c < 3; c++) {
    int leg_reg = SET_PWM_REG + 3 * rgb_led_idx + c;
    i2cWriteByteData(handle, leg_reg, color[c]);
  }
  i2cWriteByteData(handle, UPDATE_REGISTER, 0xff);
  gpioDelay(2000);
}

int *random_color() {
  static int color[3];
  for (int i = 0; i < 3; i++) {
    color[i] = (int)((float)rand() / (float)RAND_MAX * 255);
  }
  return color;
}

int main() {
  int handle;

  srand(time(NULL));

  if (gpioInitialise() < 0)
    return 1;

  gpioSetMode(EN_GPIO, PI_OUTPUT);
  gpioWrite(EN_GPIO, 1);

  handle = i2cOpen(1, SN3218_ADDR, 0);
  printf("open i2c bus\n");

  // start
  unsigned int shutdown = SHUTDOWN_REGISTER;
  unsigned int update = UPDATE_REGISTER;
  unsigned int enable1 = LED_CTRL_REGISTER1;
  unsigned int enable2 = LED_CTRL_REGISTER2;
  unsigned int enable3 = LED_CTRL_REGISTER3;

  int rgb_led_idx = 1;
  unsigned int color[3] = {125, 0, 255};

  i2cWriteByteData(handle, RESET_REGISTER, 0x01);
  i2cWriteByteData(handle, shutdown, 0x1); // normal operation

  i2cWriteByteData(handle, enable1, 0xff);
  i2cWriteByteData(handle, enable2, 0xff);
  i2cWriteByteData(handle, enable3, 0xff);

  set_rgbled_color(handle, 0, random_color());
  set_rgbled_color(handle, 1, random_color());
  set_rgbled_color(handle, 2, random_color());
  set_rgbled_color(handle, 3, random_color());
  set_rgbled_color(handle, 4, random_color());
  set_rgbled_color(handle, 5, random_color());

  printf("yo\n");
  gpioDelay(2000000);

  i2cWriteByteData(handle, shutdown, 0x0); // shutdown
  i2cClose(handle);
  gpioTerminate();
}