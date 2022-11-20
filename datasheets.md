
## Trilobot Doc
- [Assembling your Trilobot](https://learn.pimoroni.com/article/assembling-trilobot#introduction)
- [trilobot-python](https://github.com/pimoroni/trilobot-python/tree/main/library/trilobot)
- [trilobot_schematic.pdf](https://cdn.shopify.com/s/files/1/0174/1800/files/trilobot_schematic.pdf?v=1639566970)


## Datasheets
- [Ultrasonic Ranging Module HC - SR04](https://cdn.sparkfun.com/datasheets/Sensors/Proximity/HCSR04.pdf)


## RGB Leds
- datasheet: [sn3218 - 18 Channel LED driver](https://github.com/pimoroni/sn3218/blob/master/datasheets/sn3218-datasheet.pdf)
- library: [pimoroni/sn3218-python](https://github.com/pimoroni/sn3218-python)

## Motors
- datasheet: [DRV8833 Dual H-Bridge Motor Driver](https://www.ti.com/lit/ds/symlink/drv8833.pdf?HQS=dis-mous-null-mousermode-dsf-pf-null-wwe&ts=1644518569384&ref_url=https%253A%252F%252Fwww.mouser.com%252F)
- doc: [Improve Brushed DC Motor Performance By Jan Goolsbey](https://learn.adafruit.com/improve-brushed-dc-motor-performance)


## Gpio
- [pigpio python library](http://abyz.me.uk/rpi/pigpio/)


## I2C
- `$ sudo i2cdetect -q -y 1`



## IMU mpu6050
- web: [6-axis/mpu-6050](https://invensense.tdk.com/products/motion-tracking/6-axis/mpu-6050/)
- [MPU-6000-Datasheet1.pdf](https://invensense.tdk.com/wp-content/uploads/2015/02/MPU-6000-Datasheet1.pdf)
- [Register Map and Descriptions](https://invensense.tdk.com/wp-content/uploads/2015/02/MPU-6000-Register-Map1.pdf)
- doc: [MPU6050 6-DoF Accelerometer and Gyro By Bryan Siepert](https://learn.adafruit.com/mpu6050-6-dof-accelerometer-and-gyro)
- not official python lib: https://github.com/m-rtijn/mpu6050/blob/master/mpu6050/mpu6050.py
- another python lib, with FIFO and DMP: https://github.com/streamnsight/mpu6050/blob/master/mpu6050/mpu6050.py
- Adafruit lib: https://github.com/adafruit/Adafruit_CircuitPython_MPU6050
- https://stackoverflow.com/questions/60419390/mpu-6050-correctly-reading-data-from-the-fifo-register
- Linux Kernel Driver (iio): 
  * https://elixir.bootlin.com/linux/latest/source/drivers/iio/imu/inv_mpu6050
  * https://www.kernel.org/doc/html/v4.12/driver-api/iio/buffers.html
  * https://github.com/raspberrypi/linux/blob/rpi-4.14.y/arch/arm/boot/dts/overlays/README


On the raspberry:

```
$ sudo dtoverlay mpu6050
$ sudo dtoverlay -l
```

```
$ dtoverlay -h mpu6050
Name:   mpu6050

Info:   Overlay for i2c connected mpu6050 imu

Usage:  dtoverlay=mpu6050,<param>=<val>

Params: interrupt               GPIO pin for interrupt (default 4)
        addr                    I2C address of the device (default 0x68)
```



- How to set, read buffer and use trigger ?

- DMP not accesible, nor documented, but with the Adafruit lib (Jeff rowberg I2cdev) ? https://www.i2cdevlib.com/devices/mpu6050#source
- https://forums.raspberrypi.com/viewtopic.php?p=1829286&hilit=i2cdevlib#p1829286


### libiio python binding
- http://analogdevicesinc.github.io/libiio/master/python/device.html


```
$ sudo apt install libiio-utils
$ iio_info 
```