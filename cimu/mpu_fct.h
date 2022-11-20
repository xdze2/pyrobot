#ifndef _MPU_FCT_H_
#define _MPU_FCT_H_

typedef struct {
    int pi;
    unsigned int handle;
} I2cInterface;

I2cInterface open_i2c();
int close_i2c(I2cInterface* i2c);

// void write_single_bit(int pi, unsigned int handle, unsigned int reg_addr,
//                       int idx, int bit_value);

// void write_bits(int pi, unsigned int handle, unsigned int reg_addr, int idx,
//                 int length, int value);

// int read_single_bit(int pi, unsigned int handle, unsigned int reg_addr,
//                     int idx);

// int read_bits(int pi, unsigned int handle, unsigned int reg_addr, int idx,
//               int length);

unsigned int read_byte(I2cInterface* i2c, unsigned int reg_addr);
#endif