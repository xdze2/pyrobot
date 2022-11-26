#include <pigpiod_if2.h>
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <unistd.h>

#include "MPU6050reg.h"
#include "mpu_fct.h"

#define BURST_SIZE 32

const double SENSITIVITY = 131.0;            // LSB / deg/s
const double dt = 0.001;                     // s, freq = 1kHz
const double d_theta_bit = dt / SENSITIVITY; // deg/tick

static volatile sig_atomic_t keep_running = 1;

static void sig_handler(int _) {
  // https://stackoverflow.com/a/54267342/8069403
  (void)_;
  keep_running = 0;
}

double sum_buffer(uint8_t fifo_buffer[]) {
  double avg_wZ = 0;
  for (int i = 0; i < BURST_SIZE / 2; i++) {
    int16_t raw_value =
        (((int16_t)fifo_buffer[2 * i]) << 8) | (int16_t)fifo_buffer[2 * i + 1];
    avg_wZ += (double)raw_value; // * SENSITIVITY;
  }
  return avg_wZ;
}

int main() {
  signal(SIGINT, sig_handler);

  I2cInterface i2c = open_i2c();

  device_reset(&i2c);
  msleep(300);
  int res = configure_imu(&i2c);
  msleep(1000); // warmup

  struct timespec tic, toc;
  int delta_us;

  set_fifo_enabled(&i2c, 0);
  set_ZGyro_FIFO_enabled(&i2c, 1);
  reset_fifo(&i2c);
  set_fifo_enabled(&i2c, 1);

  uint8_t fifo_buffer[BURST_SIZE];
  int fifo_length;
  double wZ = 0;
  double offset = 0.0; // deg/s
  double avg_ratio = 0.95;
  double angle = 0;
  double previous_delta = 0;
  int nbr_miss = 0;
  int k = 0;
  timespec_get(&toc, TIME_UTC);
  while (keep_running) {

    fifo_length = get_fifo_count(&i2c);

    if (fifo_length >= BURST_SIZE) {
      // Read FIFO
      k++;
      nbr_miss = 0;
      timespec_get(&toc, TIME_UTC);

      read_fifo_burst(&i2c, fifo_buffer);
      wZ = sum_buffer(fifo_buffer);

      if (k < 1000) {
        offset = avg_ratio * offset + (1 - avg_ratio) * wZ;
        if (k % 20 == 0)
          printf("offset: %f \n", offset * d_theta_bit);
      } else {
        double delta = wZ - offset;
        angle = angle + (delta + previous_delta)/2.0;
        previous_delta = delta;
        if (k % 64 == 0)
          printf("angle: %f (%f)\n", angle * d_theta_bit, delta * d_theta_bit);
      }

      // printf("fifo length %d \n", fifo_length);
      msleep(6);
    } else {
      // int t_to_wait = BURST_SIZE - fifo_length;
      // printf("wait %d \n", t_to_wait);
      // nbr_miss += 1;
      msleep(1);
    }
  }

  turn_off_imu(&i2c);
  close_i2c(&i2c);

  puts("Stopped by signal `SIGINT'");
  return EXIT_SUCCESS;
}