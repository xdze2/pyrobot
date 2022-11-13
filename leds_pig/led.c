#include <pigpio.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

//  $ gcc -o led led.c -l pigpio
//  not necessary: gcc -Wall -pthread -o led led.c -lpigpio -lrt
//  $ sudo ./led

// gpio 22 is LED_B on the pimoroni bot

int main() {
  int gpio;
  printf("Running ... \n");

  gpioInitialise();

  gpio = 22;
  for (int i = 0; i < 10 ; i++){
    gpioSetMode(gpio, PI_OUTPUT);
    gpioWrite(gpio, 1);
    gpioDelay(500000);

    gpioWrite(gpio, 0);
    gpioDelay(500000);
  }
  return 0;
}
