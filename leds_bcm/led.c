#include <bcm2835.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

//  gcc -o led led.c -l bcm2835
//  sudo ./led

// RPI_V2_GPIO_P1_22
// is LED_B on the pimoroni bot

// don't work...bcs rpi4 ?
// but $ raspi-gpio set 22 op dh  works

int main() {
  int pin;
  printf("Running ... \n");

  if (!bcm2835_init()) {
    printf("bcm2835_init failed. Are you running as root??\n");
    return 1;
  } else {
    printf("init ok\n");
  }

  pin = RPI_BPLUS_GPIO_J8_23;
  bcm2835_gpio_fsel(pin, BCM2835_GPIO_FSEL_OUTP);
  bcm2835_gpio_set(pin);

  if (!bcm2835_close()) {
    printf("eror when closing");
  } else {
    printf("... done!\n");
  }
  return 0;
}
