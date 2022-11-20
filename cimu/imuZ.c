#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <unistd.h>
#include <pigpiod_if2.h>

#include "MPU6050reg.h"
#include "mpu_fct.h"


int main() {
  int pi, handle;

 I2cInterface i2c = open_i2c();
//   pi = pigpio_start(NULL, NULL);
//   handle = i2c_open(pi, 1, MPU6050_DEFAULT_ADDRESS, 0);
  // printf("open i2c bus at %x \n", MPU6050_DEFAULT_ADDRESS);

    int device_id;
    device_id = read_byte(&i2c, MPU6050_RA_WHO_AM_I);
    printf("device_id: %d \n", device_id);

    close_i2c(&i2c);

}