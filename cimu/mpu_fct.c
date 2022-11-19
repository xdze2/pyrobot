
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <unistd.h>
#include <pigpiod_if2.h>

#include "MPU6050reg.h"


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

void write_single_bit(int pi, unsigned int handle, unsigned int reg_addr,
                      int idx, int bit_value) {
  unsigned int prev = i2c_read_byte_data(pi, handle, reg_addr);
  unsigned int new_value = chg_bit(prev, idx, bit_value);
  i2c_write_byte_data(pi, handle, reg_addr, new_value);
}

void write_bits(int pi, unsigned int handle, unsigned int reg_addr, int idx,
                int length, int value) {
  unsigned int prev = i2c_read_byte_data(pi, handle, reg_addr);
  unsigned int new_value = chg_bits(prev, idx, length, value);
  i2c_write_byte_data(pi, handle, reg_addr, new_value);
}

int read_byte(int pi, unsigned int handle, unsigned int reg_addr) {
  unsigned int prev = i2c_read_byte_data(pi, handle, reg_addr);
  return prev;
}

int read_bits(int pi, unsigned int handle, unsigned int reg_addr, int idx,
              int length) {
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