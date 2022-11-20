#include <pigpiod_if2.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <unistd.h>

#include "MPU6050reg.h"
#include "mpu_fct.h"

int main() {

  I2cInterface i2c = open_i2c();

  // printf("open i2c bus at %x \n", MPU6050_DEFAULT_ADDRESS);

  int res = configure_imu(&i2c);

  sleep(1); // warmup


  double sensitivity = 131.0; // LSB/deg/s

  printf("# start...\n");
  for (int k = 0; k < 2000; k++) {

    // int16_t data[7];
    // read_all_data(&i2c, data);
    // for (int i = 0; i < 7; i++) {
    //   printf("\t%d", data[i]);
    // }
    // printf("\n");

    int16_t wZ_raw = read_wZ(&i2c);
    double wZ = (double)wZ_raw / sensitivity;
    printf("\t%f \n", wZ);
    sleep(1);
  }

  turn_off_imu(&i2c);
  close_i2c(&i2c);
}