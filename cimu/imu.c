#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <pigpiod_if2.h>

#include "MPU6050reg.h"

// $ gcc -o imu imu.c -l pigpiod_if2
// $ sudo ./imu > data.csv 


unsigned int chg_bit(unsigned int value, unsigned int idx, int bit) {
  // bits order:  7 ... 0

  int b = (value >> idx) & 1;
  if (b == bit) {
    return value;
  } else if (b == 0) {
    return value | (1 << idx);
  } else {
    return value & ~(1 << idx) & 0xFF;
  }
}

// int u = 3;
// printbin(u); printf("\n");
//
// int b = chg_bit(u, 3, 1);
// b = chg_bit(b, 7, 1);
// printbin(b); printf("\n");

unsigned int chg_bits(unsigned int value, unsigned int start_idx,
                      unsigned int length, int bits) {
  // bits order:  7 ... 0
  bits = bits << start_idx - length + 1;
  int mask = ((1 << length) - 1)
             << start_idx - length + 1; // 1 where "bits" are

  bits = bits & mask; // to be sure bits not bigger than 2^length
  value = value & ~mask;
  value = value | bits;
  return value;
}

// test chg_bits
// int u = 255;
// printbin(u); printf("\n");
// int v = chg_bits(u, 7, 4, 0);
// printbin(v); printf("\n");

void printbin(int val) {
  for (int i = 7; i >= 0; i--) {
    printf("%d", (val >> i) & 1);
  }
}

void write_single_bit(int pi, unsigned int handle, unsigned int reg_addr, int idx,
                      int bit_value) {
  unsigned int prev = i2c_read_byte_data(pi, handle, reg_addr);
  unsigned int new_value = chg_bit(prev, idx, bit_value);
  i2c_write_byte_data(pi, handle, reg_addr, new_value);
}

void write_bits(int pi, unsigned int handle, unsigned int reg_addr, int idx, int length,
                int value) {
  unsigned int prev = i2c_read_byte_data(pi, handle, reg_addr);
  unsigned int new_value = chg_bits(prev, idx, length, value);
  i2c_write_byte_data(pi, handle, reg_addr, new_value);
}

int read_byte(int pi, unsigned int handle, unsigned int reg_addr) {
  unsigned int prev = i2c_read_byte_data(pi, handle, reg_addr);
  return prev;
}

int read_bits(int pi, unsigned int handle, unsigned int reg_addr, int idx, int length) {
  // bits order:  7 ... 0
  unsigned int prev = i2c_read_byte_data(pi, handle, reg_addr);
  prev = prev >> idx - length + 1;
  int mask = ((1 << length) - 1);
  return prev & mask;
}


int read_bit(int pi, unsigned int handle, unsigned int reg_addr, int idx) {
  unsigned int prev = i2c_read_byte_data(pi, handle, reg_addr);
  return (prev >> idx) & 1;
}

int main() {
  int pi, handle;

  pi = pigpio_start(NULL, NULL);
  handle = i2c_open(pi, 1, MPU6050_DEFAULT_ADDRESS, 0);
  // printf("open i2c bus at %x \n", MPU6050_DEFAULT_ADDRESS);

  int device_id;
  device_id = i2c_read_byte_data(pi, handle, MPU6050_RA_WHO_AM_I);
  // printf("device_id: %x \n", device_id);

  /** Power on and prepare for general usage.
   * This will activate the device and take it out of sleep mode (which must be
   * done after start-up). This function also sets both the accelerometer and
   * the gyroscope to their most sensitive settings, namely +/- 2g and +/- 250
   * degrees/sec, and sets the clock source to use the X Gyro for reference,
   * which is slightly better than the default internal clock source.
   */
  // setClockSources(MPU6050_CLOCK_PLL_XGYRO);

  // setSleepEnabled(false); // thanks to Jack Elston for pointing this one out!
  write_single_bit(pi, handle, MPU6050_RA_PWR_MGMT_1, MPU6050_PWR1_SLEEP_BIT, 0);
  int sleep = read_bit(pi, handle, MPU6050_RA_PWR_MGMT_1, MPU6050_PWR1_SLEEP_BIT);
  // printf("# sleep: %x \n", sleep);

  int clock_sel = MPU6050_CLOCK_PLL_XGYRO;
  write_bits(pi, handle, MPU6050_RA_PWR_MGMT_1, MPU6050_PWR1_CLKSEL_BIT,
             MPU6050_PWR1_CLKSEL_LENGTH, clock_sel);

  // setFullScaleGyroRange(MPU6050_GYRO_FS_250);
  write_bits(pi, handle, MPU6050_RA_GYRO_CONFIG, MPU6050_GCONFIG_FS_SEL_BIT,
             MPU6050_GCONFIG_FS_SEL_LENGTH, MPU6050_GYRO_FS_250);
  // setFullScaleAccelRange(MPU6050_ACCEL_FS_2);
  write_bits(pi, handle, MPU6050_RA_ACCEL_CONFIG, MPU6050_ACONFIG_AFS_SEL_BIT,
             MPU6050_ACONFIG_AFS_SEL_LENGTH, MPU6050_ACCEL_FS_2);

  // Read sample rate config
  int divrate = read_byte(pi, handle, MPU6050_RA_SMPLRT_DIV);
  printf("# Rate div: %d \n", divrate + 1);

  // Set digital low pass filter config (DLPF)
  // 3, sample rate
  write_bits(pi, handle, MPU6050_RA_CONFIG, MPU6050_CFG_DLPF_CFG_BIT, MPU6050_CFG_DLPF_CFG_LENGTH, 3);
  int lowpass = read_bits(pi, handle, MPU6050_RA_CONFIG, MPU6050_CFG_DLPF_CFG_BIT, MPU6050_CFG_DLPF_CFG_LENGTH);
  printf("# lowpass: %d \n", lowpass);


  // gpio_delay(1000000); // wait 1s

  const int NBR_MEASURE = 20000;
  int nbr_read;
  char buf[32];
  signed short int data[7];

  struct timespec start, end;
  int delta_us;
  timespec_get(&start, TIME_UTC);

  FILE* f;
  f = fopen("data.txt", "w");

  fprintf(f, "# t_us\tax\tay\taz\tT_mdeg\twx\twy\twz\n");
  printf("start...");
  for (int k = 0; k < NBR_MEASURE; k++) {
    nbr_read = i2c_read_i2c_block_data(pi, handle, MPU6050_RA_ACCEL_XOUT_H, buf, 14);
    timespec_get(&end, TIME_UTC);
    for (int i = 0; i < 7; i++) {
      data[i] = (((int)buf[2 * i]) << 8) | (int)buf[2 * i + 1];
    }

    // Convert to m deg C
    data[3] = (1000 * data[3]) / 340 + 36530;

    delta_us = (end.tv_sec - start.tv_sec) * 1000000 +
               (end.tv_nsec - start.tv_nsec) / 1000;

    // Save line
    fprintf(f, "%d", delta_us);
    for (int i = 0; i < 7; i++) {
      // printf("\t%d", data[i]);
      fprintf(f, "\t%d", data[i]);
    }
    fprintf(f, "\n");

    if (k % 1000 == 0) printf("+1k: %d \n", delta_us);
    // gpioDelay(10);
  }

  int total_delta_us = (end.tv_sec - start.tv_sec) * 1000000 +
                   (end.tv_nsec - start.tv_nsec) / 1000;
  printf("dt: %d us\n", total_delta_us/NBR_MEASURE);

  fclose(f); 
  printf("File saved");
  // Set sleep = 1
  write_single_bit(pi, handle, MPU6050_RA_PWR_MGMT_1, MPU6050_PWR1_SLEEP_BIT, 1);
  i2c_close(pi, handle);
  pigpio_stop(pi);
}