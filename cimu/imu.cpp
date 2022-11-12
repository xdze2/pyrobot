#include <pigpio.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#include "MPU6050reg.h"

// $ gcc -o imu imu.c -l pigpio



unsigned int chg_bit(unsigned int value, unsigned int idx, int bit) {
    // bits order:  7 ... 0 

    int b = (value>>idx)&1;
    if (b == bit){
        return value;
    } else if (b==0)
    {
        return value | (1 << idx);
    } else {
        return value & ~(1<<idx) & 0xFF;
    }
}

// int u = 3;
// printbin(u); printf("\n");
// 
// int b = chg_bit(u, 3, 1);
// b = chg_bit(b, 7, 1);
// printbin(b); printf("\n");


void printbin(int val) {
    for (int i=7; i>=0; i--){
        printf("%d", (val>>i)&1);
    }
}

void write_bit(unsigned int handle, unsigned int reg_addr, int idx, int bit_value) {
    unsigned int prev = i2cReadByteData(handle, reg_addr);
    unsigned int new_value = chg_bit(prev, idx, bit_value);
    i2cWriteByteData(handle, reg_addr, new_value);
}

int read_bit(unsigned int handle, unsigned int reg_addr, int idx) {
    unsigned int prev = i2cReadByteData(handle, reg_addr);
    return (prev>>idx)&1;
}


int main() {
  int handle;

  if (gpioInitialise() < 0)
    return 1;

  handle = i2cOpen(1, MPU6050_DEFAULT_ADDRESS, 0);

  printf("open i2c bus at %x \n", MPU6050_DEFAULT_ADDRESS);

  int device_id;

  device_id = i2cReadByteData(handle, MPU6050_RA_WHO_AM_I); 
  printf("device_id: %x \n", device_id);

  int sleep = read_bit(handle, MPU6050_RA_PWR_MGMT_1, MPU6050_PWR1_SLEEP_BIT);
  printf("sleep: %x \n", sleep);

  write_bit(handle, MPU6050_RA_PWR_MGMT_1, MPU6050_PWR1_SLEEP_BIT, 1);

  sleep = read_bit(handle, MPU6050_RA_PWR_MGMT_1, MPU6050_PWR1_SLEEP_BIT);
  printf("sleep: %x \n", sleep);

  i2cClose(handle);
  gpioTerminate();
}