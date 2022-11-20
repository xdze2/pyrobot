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

  struct timespec start, end;
  int delta_us;

  set_ZGyro_FIFO_enabled(&i2c, 1);

  reset_fifo(&i2c);
  set_fifo_enabled(&i2c, 1);

  int NBR_TO_READ = 64;
  int length;
  uint8_t data[64];

  uint8_t c;
  for (int k = 0; k < 100; k++) {

    length = get_fifo_count(&i2c);
    printf("fifo length: %d \n", length);

    if (length > NBR_TO_READ) {
      timespec_get(&start, TIME_UTC);
      for (int i = 0; i < NBR_TO_READ; i++) {
        data[i] = get_fifo_byte(&i2c);
      }
      timespec_get(&end, TIME_UTC);
      delta_us = (end.tv_sec - start.tv_sec) * 1000000 +
                 (end.tv_nsec - start.tv_nsec) / 1000;
      printf("read time: %d us\n", delta_us);
    }
  }
  // printf("# start...\n");
  // for (int k = 0; k < 2000; k++) {

  //   // int16_t data[7];
  //   // read_all_data(&i2c, data);
  //   // for (int i = 0; i < 7; i++) {
  //   //   printf("\t%d", data[i]);
  //   // }
  //   // printf("\n");

  //   int16_t wZ_raw = read_wZ(&i2c);
  //   double wZ = (double)wZ_raw / sensitivity;
  //   printf("\t%f \n", wZ);
  //   sleep(1);
  // }

  turn_off_imu(&i2c);
  close_i2c(&i2c);
}