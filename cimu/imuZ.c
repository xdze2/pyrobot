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
  device_reset(&i2c);
  printf("# device reset...");
  sleep(1);
  int res = configure_imu(&i2c);

  sleep(1); // warmup

  const double sensitivity = 131.0; // LSB/deg/s
  const double dt = 0.001;          // s
  // freq = 1kHz

  struct timespec tic, toc;
  int delta_us;

  set_fifo_enabled(&i2c, 0);

  // set_XGyro_FIFO_enabled(&i2c, 1);
  set_ZGyro_FIFO_enabled(&i2c, 1);
  reset_fifo(&i2c);
  set_fifo_enabled(&i2c, 1);

  int NBR_TO_READ = 128;
  int fifo_length;
  double raw[NBR_TO_READ];
  double data;
  double offset = 0.0;
  double ratio = 0.995;
  double angle = 0;
  timespec_get(&toc, TIME_UTC);
  for (int k = 0; k < 15000; k++) {

    fifo_length = get_fifo_count(&i2c);

    if (fifo_length > 2 * NBR_TO_READ) {

      // Read FIFO

      for (int i = 0; i < NBR_TO_READ; i++) {
        raw[i] = (double)read_fifo_burst(&i2c) / sensitivity;
      }
      timespec_get(&tic, TIME_UTC);
      delta_us = (tic.tv_sec - toc.tv_sec) * 1000000 +
                 (tic.tv_nsec - toc.tv_nsec) / 1000;
      toc.tv_sec = tic.tv_sec;
      toc.tv_nsec = tic.tv_nsec;
      printf("loop freq: %f kHz \n",
             2000.0 * (double)NBR_TO_READ / (double)delta_us);

      for (int i = 0; i < NBR_TO_READ; i++) {
        if (k < 1000) {
          offset = ratio * offset + (1 - ratio) * raw[i];
        } else {
          angle = angle + (raw[i] - offset) * dt; // deg
        }
      }
      printf("offset: %f  angle: %f\n", offset, angle);
    }
  }

  // 50ms / 64 bytes...
  // after set t 400kHz -> 25292 us /64

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