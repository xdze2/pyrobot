
#include <pigpiod_if2.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <unistd.h>

#include "MPU6050reg.h"

/* Set value of a single bit. Index order: 7 -> 0. */
unsigned int chg_bit(unsigned int value, unsigned int idx, int bit) {
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

/* Set value of a serie of bits. Index order: 7 -> 0. */
unsigned int chg_bits(unsigned int value, unsigned int start_idx,
                      unsigned int length, int bits) {
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

/* Print 8 bit long string. */
void printbin(int val) {
  for (int i = 7; i >= 0; i--) {
    printf("%d", (val >> i) & 1);
  }
}

// ----------------------------------
//  Read and Write to i2c interfaces
// ----------------------------------

typedef struct {
  int pi;
  unsigned int handle;
} I2cInterface;

/* Open both the pigpio interface and the i2c. */
I2cInterface open_i2c() {
  I2cInterface pi_handle;
  printf("(start $ sudo pigpiod before)\n");
  pi_handle.pi = pigpio_start(NULL, NULL);
  if (pi_handle.pi < 0) {
    printf("Error when starting pigpio...\n");
    printf(pigpio_error(pi_handle.pi));
    printf("\n");
    exit(EXIT_FAILURE);
  }

  pi_handle.handle = i2c_open(pi_handle.pi, 1, MPU6050_DEFAULT_ADDRESS, 0);
  if (pi_handle.handle < 0) {
    printf("Error when starting i2c...\n");
    printf(pigpio_error(pi_handle.handle));
    printf("\n");
    exit(EXIT_FAILURE);
  }
  return pi_handle;
}

int close_i2c(I2cInterface *i2c) {
  i2c_close(i2c->pi, i2c->handle);
  pigpio_stop(i2c->pi);
  return 0;
}

void write_single_bit(I2cInterface *i2c, unsigned int reg_addr, int idx,
                      int bit_value) {
  unsigned int prev = i2c_read_byte_data(i2c->pi, i2c->handle, reg_addr);
  unsigned int new_value = chg_bit(prev, idx, bit_value);
  i2c_write_byte_data(i2c->pi, i2c->handle, reg_addr, new_value);
}

void write_bits(I2cInterface *i2c, unsigned int reg_addr, int idx, int length,
                int value) {
  unsigned int prev = i2c_read_byte_data(i2c->pi, i2c->handle, reg_addr);
  unsigned int new_value = chg_bits(prev, idx, length, value);
  i2c_write_byte_data(i2c->pi, i2c->handle, reg_addr, new_value);
}

int read_single_bit(I2cInterface *i2c, unsigned int reg_addr, int idx) {
  unsigned int prev = i2c_read_byte_data(i2c->pi, i2c->handle, reg_addr);
  return (prev >> idx) & 1;
}

int read_bits(I2cInterface *i2c, unsigned int reg_addr, int idx, int length) {
  // bits order:  7 ... 0
  unsigned int prev = i2c_read_byte_data(i2c->pi, i2c->handle, reg_addr);
  prev = prev >> idx - length + 1;
  int mask = ((1 << length) - 1);
  return prev & mask;
}

/* Read i2c register. */
unsigned int read_byte(I2cInterface *i2c, unsigned int reg_addr) {
  return (unsigned int)i2c_read_byte_data(i2c->pi, i2c->handle, reg_addr);
}

// -------------------
//  MPU6050 functions
// -------------------

int configure_imu(I2cInterface *i2c) {

  int device_id = read_byte(i2c, MPU6050_RA_WHO_AM_I);
  printf("# device id: %d \n", device_id);
  if (device_id != 104) {
    printf("Error bad device id %d \n", device_id);
    exit(EXIT_FAILURE);
  }

  // set sleep enabled to False
  write_single_bit(i2c, MPU6050_RA_PWR_MGMT_1, MPU6050_PWR1_SLEEP_BIT, 0);

  int issleeping =
      read_single_bit(i2c, MPU6050_RA_PWR_MGMT_1, MPU6050_PWR1_SLEEP_BIT);
  printf("# is sleeping: %x \n", issleeping);

  int clock_sel = MPU6050_CLOCK_PLL_XGYRO;
  write_bits(i2c, MPU6050_RA_PWR_MGMT_1, MPU6050_PWR1_CLKSEL_BIT,
             MPU6050_PWR1_CLKSEL_LENGTH, clock_sel);
  printf("# Clock: %d \n", clock_sel);

  // setFullScaleGyroRange(MPU6050_GYRO_FS_250);
  write_bits(i2c, MPU6050_RA_GYRO_CONFIG, MPU6050_GCONFIG_FS_SEL_BIT,
             MPU6050_GCONFIG_FS_SEL_LENGTH, MPU6050_GYRO_FS_250);
  printf("# Gyro range: %d \n", MPU6050_GYRO_FS_250);

  // setFullScaleAccelRange(MPU6050_ACCEL_FS_2);
  write_bits(i2c, MPU6050_RA_ACCEL_CONFIG, MPU6050_ACONFIG_AFS_SEL_BIT,
             MPU6050_ACONFIG_AFS_SEL_LENGTH, MPU6050_ACCEL_FS_2);
  printf("# Acc range: %d \n", MPU6050_ACCEL_FS_2);

  // Read sample rate config
  int div_rate = read_byte(i2c, MPU6050_RA_SMPLRT_DIV);
  printf("# Rate div: %d \n", div_rate + 1);

  // Set digital low pass filter config (DLPF)
  // 3, sample rate
  write_bits(i2c, MPU6050_RA_CONFIG, MPU6050_CFG_DLPF_CFG_BIT,
             MPU6050_CFG_DLPF_CFG_LENGTH, 3);
  int lowpass = read_bits(i2c, MPU6050_RA_CONFIG, MPU6050_CFG_DLPF_CFG_BIT,
                          MPU6050_CFG_DLPF_CFG_LENGTH);
  printf("# low pass: %d \n", lowpass);
  return 0;
}

/* Set sleep bit to 1 */
void turn_off_imu(I2cInterface *i2c) {
  write_single_bit(i2c, MPU6050_RA_PWR_MGMT_1, MPU6050_PWR1_SLEEP_BIT, 1);
}

/* Device RESET */
void device_reset(I2cInterface *i2c) {
  write_single_bit(i2c, MPU6050_RA_PWR_MGMT_1, MPU6050_PWR1_DEVICE_RESET_BIT,
                   1);
}

/* Read all data registers Acc, Temp and Gyro. */
void read_all_data(I2cInterface *i2c, signed short int data[7]) {

  uint8_t buf[16];
  int nbr_read = i2c_read_i2c_block_data(i2c->pi, i2c->handle,
                                         MPU6050_RA_ACCEL_XOUT_H, buf, 14);
  for (int i = 0; i < 7; i++) {
    data[i] = (((int16_t)buf[2 * i]) << 8) | buf[2 * i + 1];
  }

  if (nbr_read != 14) {
    printf("Error when reading data...");
  }
}

/* Read only GyroZ data register. */
int16_t read_wZ(I2cInterface *i2c) {
  uint8_t buf[2];
  int nbr_read = i2c_read_i2c_block_data(i2c->pi, i2c->handle,
                                         MPU6050_RA_GYRO_ZOUT_H, buf, 2);
  if (nbr_read != 2) {
    printf("Error when reading data... %d \n", nbr_read);
    printf("%c \n", pigpio_error(nbr_read));
  }
  return (((int16_t)buf[0]) << 8) | buf[1];
}

// FIFO

/* Set FIFO enabled status. */
void set_fifo_enabled(I2cInterface *i2c, int enabled) {
  write_single_bit(i2c, MPU6050_RA_USER_CTRL, MPU6050_USERCTRL_FIFO_EN_BIT,
                   enabled);
}

/* Reset the FIFO. */
void reset_fifo(I2cInterface *i2c) {
  write_single_bit(i2c, MPU6050_RA_USER_CTRL, MPU6050_USERCTRL_FIFO_RESET_BIT,
                   1);
}

/** Set gyroscope Z-axis FIFO enabled value. */
void set_ZGyro_FIFO_enabled(I2cInterface *i2c, int enabled) {
  write_single_bit(i2c, MPU6050_RA_FIFO_EN, MPU6050_ZG_FIFO_EN_BIT, enabled);
}

/** Set gyroscope X-axis FIFO enabled value. */
void set_XGyro_FIFO_enabled(I2cInterface *i2c, int enabled) {
  write_single_bit(i2c, MPU6050_RA_FIFO_EN, MPU6050_XG_FIFO_EN_BIT, enabled);
}

/* Get current FIFO buffer size. */
uint16_t get_fifo_count(I2cInterface *i2c) {
  uint8_t buf[2];
  int nbr_read = i2c_read_i2c_block_data(i2c->pi, i2c->handle,
                                         MPU6050_RA_FIFO_COUNTH, buf, 2);
  if (nbr_read != 2) {
    printf("Error when reading data... %d \n", nbr_read);
    printf("%c \n", pigpio_error(nbr_read));
  }
  return (((int16_t)buf[0]) << 8) | buf[1];
}

/* Get byte from FIFO buffer. */
uint8_t get_fifo_byte(I2cInterface *i2c) {
  return read_byte(i2c, MPU6050_RA_FIFO_R_W);
}

int16_t read_fifo_burst(I2cInterface *i2c) {
  uint8_t buf[2];
  int nbr_read = i2c_read_i2c_block_data(i2c->pi, i2c->handle,
                                         MPU6050_RA_FIFO_R_W, buf, 2);
  if (nbr_read != 2) {
    printf("Error when reading data... %d \n", nbr_read);
    printf("%c \n", pigpio_error(nbr_read));
  }
  return (((int16_t)buf[0]) << 8) | (int16_t)buf[1];
}