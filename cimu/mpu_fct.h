#ifndef _MPU_FCT_H_
#define _MPU_FCT_H_




void write_single_bit(int pi, unsigned int handle, unsigned int reg_addr,
                      int idx, int bit_value);
void write_bits(int pi, unsigned int handle, unsigned int reg_addr, int idx,
                int length, int value);

int read_byte(int pi, unsigned int handle, unsigned int reg_addr);
int read_bits(int pi, unsigned int handle, unsigned int reg_addr, int idx,
              int length);

int read_bit(int pi, unsigned int handle, unsigned int reg_addr, int idx);


#endif