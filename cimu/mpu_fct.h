#ifndef _MPU_FCT_H_
#define _MPU_FCT_H_

typedef struct {
  int pi;
  unsigned int handle;
} I2cInterface;

I2cInterface open_i2c();

int close_i2c(I2cInterface *i2c);

void write_single_bit(I2cInterface *i2c, unsigned int reg_addr, int idx,
                      int bit_value);

void write_bits(I2cInterface *i2c, unsigned int reg_addr, int idx, int length,
                int value);

int read_single_bit(I2cInterface *i2c, unsigned int reg_addr, int idx);

int read_bits(I2cInterface *i2c, unsigned int reg_addr, int idx, int length);

unsigned int read_byte(I2cInterface *i2c, unsigned int reg_addr);

int configure_imu(I2cInterface *i2c);
void turn_off_imu(I2cInterface *i2c);
void read_all_data(I2cInterface *i2c, int16_t data[7]);
int16_t read_wZ(I2cInterface *i2c);

#endif