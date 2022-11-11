from smbus import SMBus
import time
import MPU6050_register as reg


def to_bin_str(byte: int) -> str:
    """From integer to string of '0' and '1'."""
    return f"{bin(byte)[2:]:>08}"


def to_int(bin_str: str) -> int:
    """From string of '0' and '1' to integer."""
    return int(bin_str, 2)


def set_bit(bin_str: str, bit_idx_from_right: int, bit_value: bool):
    bit_idx_from_left = len(bin_str) - bit_idx_from_right - 1
    bit_char = "1" if bit_value else "0"
    return "".join(
        b if idx != bit_idx_from_left else bit_char for idx, b in enumerate(bin_str)
    )


i2c = SMBus(1)


def write_bit(devAddr: int, reg_addr: int, bit_7_to_0: int, value: bool):
    output = i2c.read_byte_data(devAddr, reg_addr)
    output_str = to_bin_str(output)
    to_write = set_bit(output_str, bit_7_to_0, value)
    # print(output_str, '-->', to_write)
    i2c.write_byte_data(devAddr, reg_addr, to_int(to_write))


def read_bit(devAddr: int, reg_addr: int, bit_7_to_0: int) -> bool:
    output = i2c.read_byte_data(devAddr, reg_addr)
    output_str = to_bin_str(output)
    bit_idx = len(output_str) - bit_7_to_0 - 1
    return output_str[bit_idx] == "1"


MPU6050_DEFAULT_ADDRESS = 0x68  # MPU6050 default i2c address w/ AD0 low
devAddr = MPU6050_DEFAULT_ADDRESS


# def initialize() -> None:
#     """Power on and prepare for general usage.
#     This will activate the device and take it out of sleep mode (which must be done
#     after start-up). This function also sets both the accelerometer and the gyroscope
#     to their most sensitive settings, namely +/- 2g and +/- 250 degrees/sec, and sets
#     the clock source to use the X Gyro for reference, which is slightly better than
#     the default internal clock source.
#     """
#     setClockSource(reg.MPU6050_CLOCK_PLL_XGYRO)
#     setFullScaleGyroRange(reg.MPU6050_GYRO_FS_250)
#     setFullScaleAccelRange(reg.MPU6050_ACCEL_FS_2)
#     set_sleep_enabled(False)  # thanks to Jack Elston for pointing this one out!


# def setClockSource(source: int) -> None:
#     """Set clock source setting.
#     An internal 8MHz oscillator, gyroscope based clock, or external sources can
#     be selected as the MPU-60X0 clock source. When the internal 8 MHz oscillator
#     or an external source is chosen as the clock source, the MPU-60X0 can operate
#     in low power modes with the gyroscopes disabled.

#     Upon power up, the MPU-60X0 clock source defaults to the internal oscillator.
#     However, it is highly recommended that the device be configured to use one of
#     the gyroscopes (or an external clock source) as the clock reference for
#     improved stability. The clock source can be selected according to the following table:

#     <pre>
#         CLK_SEL | Clock Source
#         --------+--------------------------------------
#         0       | Internal oscillator
#         1       | PLL with X Gyro reference
#         2       | PLL with Y Gyro reference
#         3       | PLL with Z Gyro reference
#         4       | PLL with external 32.768kHz reference
#         5       | PLL with external 19.2MHz reference
#         6       | Reserved
#         7       | Stops the clock and keeps the timing generator in reset
#     </pre>

#     """
#     i2c.write_byte_data(
#         devAddr,
#         reg.MPU6050_RA_PWR_MGMT_1,
#         reg.MPU6050_PWR1_CLKSEL_BIT,
#         reg.MPU6050_PWR1_CLKSEL_LENGTH,
#         source,
#     )


def getDeviceID() -> int:
    """WHO_AM_I register. Get Device ID.
    This register is used to verify the identity of the device (0b110100, 0x34).
    return Device ID (6 bits only! should be 0x34)
    """
    output = i2c.read_byte_data(devAddr, reg.MPU6050_RA_WHO_AM_I)
    return hex(output)


def get_sleep_enabled() -> bool:
    """Get sleep mode status.
    Setting the SLEEP bit in the register puts the device into very low power
    sleep mode. In this mode, only the serial interface and internal registers
    remain active, allowing for a very low standby current. Clearing this bit
    puts the device back into normal mode. To save power, the individual standby
    selections for each of the gyros should be used if any gyro axis is not used
    by the application.
    """
    return read_bit(devAddr, reg.MPU6050_RA_PWR_MGMT_1, reg.MPU6050_PWR1_SLEEP_BIT)


def set_sleep_enabled(enabled: bool) -> None:
    """Set sleep mode status."""
    print(f"Set SLEEP mode to {enabled}")
    write_bit(devAddr, reg.MPU6050_RA_PWR_MGMT_1, reg.MPU6050_PWR1_SLEEP_BIT, enabled)


def get_FIFO_Enabled() -> bool:
    """/** Get FIFO enabled status.
    * When this bit is set to 0, the FIFO buffer is disabled. The FIFO buffer
    * cannot be written to or read from while disabled. The FIFO buffer's state
    * does not change unless the MPU-60X0 is power cycled.
    * @return Current FIFO enabled status
    * @see MPU6050_RA_USER_CTRL
    * @see MPU6050_USERCTRL_FIFO_EN_BIT
    */"""
    output = read_bit(
        devAddr, reg.MPU6050_RA_USER_CTRL, reg.MPU6050_USERCTRL_FIFO_EN_BIT
    )
    return output


def set_FIFO_enabled(enabled: bool) -> None:
    """/** Set FIFO enabled status.
    * @param enabled New FIFO enabled status
    * @see getFIFOEnabled()
    * @see MPU6050_RA_USER_CTRL
    * @see MPU6050_USERCTRL_FIFO_EN_BIT
    */"""
    print(f"Set Enable FIFO to {enabled}")
    write_bit(
        devAddr, reg.MPU6050_RA_USER_CTRL, reg.MPU6050_USERCTRL_FIFO_EN_BIT, enabled
    )


def get_accel_FIFO_enabled() -> bool:
    """Get accelerometer FIFO enabled value.
    When set to 1, this bit enables ACCEL_XOUT_H, ACCEL_XOUT_L, ACCEL_YOUT_H,
    ACCEL_YOUT_L, ACCEL_ZOUT_H, and ACCEL_ZOUT_L (Registers 59 to 64) to be
    written into the FIFO buffer.
    """
    output = i2c.read_byte_data(
        devAddr, reg.MPU6050_RA_FIFO_EN
    )  # , reg.MPU6050_ACCEL_FIFO_EN_BIT, buffer);
    return to_bin_str(output)


def set_accel_FIFO_enabled(enabled: bool) -> None:
    """Set accelerometer FIFO enabled value."""
    print(f"Set Accel FIFO enable to {enabled}")
    write_bit(devAddr, reg.MPU6050_RA_FIFO_EN, reg.MPU6050_ACCEL_FIFO_EN_BIT, enabled)


"""FIFO_R_W register

Get byte from FIFO buffer.
This register is used to read and write data from the FIFO buffer. Data is
written to the FIFO in order of register number (from lowest to highest). If
all the FIFO enable flags (see below) are enabled and all External Sensor
Data registers (Registers 73 to 96) are associated with a Slave device, the
contents of registers 59 through 96 will be written in order at the Sample
Rate.

The contents of the sensor data registers (Registers 59 to 96) are written
into the FIFO buffer when their corresponding FIFO enable flags are set to 1
in FIFO_EN (Register 35). An additional flag for the sensor data registers
associated with I2C Slave 3 can be found in I2C_MST_CTRL (Register 36).

If the FIFO buffer has overflowed, the status bit FIFO_OFLOW_INT is
automatically set to 1. This bit is located in INT_STATUS (Register 58).
When the FIFO buffer has overflowed, the oldest data will be lost and new
data will be written to the FIFO.

If the FIFO buffer is empty, reading this register will return the last byte
that was previously read from the FIFO until new data is available. The user
should check FIFO_COUNT to ensure that the FIFO buffer is not read when
empty.
"""


def getFIFOByte() -> int:
    output = i2c.read_byte_data(devAddr, reg.MPU6050_RA_FIFO_R_W)
    return bin(output)


def get_FIFO_block(lenght: int) -> int:
    output = i2c.read_i2c_block_data(devAddr, reg.MPU6050_RA_FIFO_R_W, lenght)
    return output


def get_IntFIFO_BufferOverflow_Status() -> bool:
    """/** Get FIFO Buffer Overflow interrupt status.
    * This bit automatically sets to 1 when a Free Fall interrupt has been
    * generated. The bit clears to 0 after the register has been read.
    * @return Current interrupt status
    * @see MPU6050_RA_INT_STATUS
    * @see MPU6050_INTERRUPT_FIFO_OFLOW_BIT
    */
    """
    return read_bit(
        devAddr, reg.MPU6050_RA_INT_STATUS, reg.MPU6050_INTERRUPT_FIFO_OFLOW_BIT
    )


def get_FIFO_count() -> int:
    """/** Get current FIFO buffer size.
    * This value indicates the number of bytes stored in the FIFO buffer. This
    * number is in turn the number of bytes that can be read from the FIFO buffer
    * and it is directly proportional to the number of samples available given the
    * set of sensor data bound to be stored in the FIFO (register 35 and 36).
    * @return Current FIFO buffer size
    */"""
    output_H = i2c.read_byte_data(devAddr, reg.MPU6050_RA_FIFO_COUNTH)
    output_H = i2c.read_byte_data(devAddr, reg.MPU6050_RA_FIFO_COUNTH)
    output_L = i2c.read_byte_data(devAddr, reg.MPU6050_RA_FIFO_COUNTL)
    return to_bin_str(output_H) + to_bin_str(output_L)


def reset_FIFO():
    """Reset the FIFO.
    * This bit resets the FIFO buffer when set to 1 while FIFO_EN equals 0. This
    * bit automatically clears to 0 after the reset has been triggered.
    """
    write_bit(
        devAddr, reg.MPU6050_RA_USER_CTRL, reg.MPU6050_USERCTRL_FIFO_RESET_BIT, True
    )


def getClockSource() -> int:
    """Get clock source setting.
    @return Current clock source setting
    * @see MPU6050_RA_PWR_MGMT_1
    * @see MPU6050_PWR1_CLKSEL_BIT
    * @see MPU6050_PWR1_CLKSEL_LENGTH
    */"""
    output = i2c.read_byte_data(devAddr, reg.MPU6050_RA_PWR_MGMT_1)
    # I2Cdev::readBits(devAddr, MPU6050_RA_PWR_MGMT_1, MPU6050_PWR1_CLKSEL_BIT, MPU6050_PWR1_CLKSEL_LENGTH, buffer);
    print("clock bit", reg.MPU6050_PWR1_CLKSEL_BIT, reg.MPU6050_PWR1_CLKSEL_LENGTH)
    return to_bin_str(output)


def reset():
    """/** Trigger a full device reset.
    * A small delay of ~50ms may be desirable after triggering a reset.
    * @see MPU6050_RA_PWR_MGMT_1
    * @see MPU6050_PWR1_DEVICE_RESET_BIT
    */"""
    print("Full device reset")
    write_bit(
        devAddr, reg.MPU6050_RA_PWR_MGMT_1, reg.MPU6050_PWR1_DEVICE_RESET_BIT, True
    )


reset()
time.sleep(0.6)

print("Device ID:", getDeviceID())


print()


print("sleep status:", get_sleep_enabled())
set_sleep_enabled(False)
print("sleep status:", get_sleep_enabled())


print()


print("get_FIFO_Enabled()", get_FIFO_Enabled())
set_FIFO_enabled(True)
print("get_FIFO_Enabled()", get_FIFO_Enabled())


print("sleep status:", get_sleep_enabled())
set_sleep_enabled(True)
print("sleep status:", get_sleep_enabled())
set_sleep_enabled(False)
print("get_FIFO_Enabled()", get_FIFO_Enabled())

print()

# time.sleep(.5)


print("getAccelFIFOEnabled:", get_accel_FIFO_enabled())
count = get_FIFO_count()
print("get_FIFO_count()=", to_int(count))

time.sleep(0.5)
set_accel_FIFO_enabled(True)


print("get_IntFIFO_BufferOverflow_Status", get_IntFIFO_BufferOverflow_Status())
print("getAccelFIFOEnabled:", get_accel_FIFO_enabled())
tic = time.perf_counter()
for k in range(40):
    toc = time.perf_counter()
    print("buff:", get_FIFO_block(16), f"{(toc-tic)*1000}")
    tic = toc
    print("get_IntFIFO_BufferOverflow_Status", get_IntFIFO_BufferOverflow_Status())


count = get_FIFO_count()
print("get_FIFO_count()", count, to_int(count))


i2c.close()
