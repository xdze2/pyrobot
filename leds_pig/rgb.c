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

#define DELTA 2 // int step

const int NBR_LED = 16;

void set_rgbled_color(int handle, int rgb_led_idx, int *color) {
  // printf("Set color for led %d: (%d %d %d)\n", rgb_led_idx, color[0],
  // color[1], color[2]);
  for (int c = 0; c < 3; c++) {
    int leg_reg = SET_PWM_REG + 3 * rgb_led_idx + c;
    i2cWriteByteData(handle, leg_reg, color[c]);
  }
}

void set_all_colors(int handle, char* colors){
  i2cWriteBlockData(handle, SET_PWM_REG, colors, NBR_LED);
  i2cWriteByteData(handle, UPDATE_REGISTER, 0x01);
}

int rand255() { return (int)((float)rand() / (float)RAND_MAX * 255); }

int randDelta() {
  int randbool = rand() & 1;
  return (randbool) ? -DELTA : +DELTA;
}

int random_step(int value) {
  value = value + randDelta();
  value = (value > 255) ? 255 : value;
  value = (value < 0) ? 0 : value;
  return value;
}

int *random_color() {
  static int color[3];
  for (int i = 0; i < 3; i++) {
    color[i] = rand255();
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

  i2cWriteByteData(handle, RESET_REGISTER, 0x01);
  i2cWriteByteData(handle, shutdown, 0x1); // normal operation

  i2cWriteByteData(handle, enable1, 0xff);
  i2cWriteByteData(handle, enable2, 0xff);
  i2cWriteByteData(handle, enable3, 0xff);

  // init
  char colors[NBR_LED];
  for (int led_idx = 0; led_idx < NBR_LED; led_idx++) {
      colors[led_idx] = rand255();
  }

  for (int t = 0; t < 10000; t++) {

    for (int led_idx = 0; led_idx < NBR_LED; led_idx++) {
      colors[led_idx] = random_step(colors[led_idx]);
    }
    set_all_colors(handle, colors);
    gpioDelay(5000);
  }

  i2cWriteByteData(handle, shutdown, 0x0); // shutdown
  i2cClose(handle);
  gpioTerminate();
}