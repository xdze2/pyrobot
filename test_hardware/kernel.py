import iio


for ctxname in iio.scan_contexts():
    ctx = iio.Context(ctxname)
    for dev in ctx.devices:
        if dev.channels:
            for chan in dev.channels:
                print("{} - {} - {}".format(ctxname, dev.name, chan._id))
        else:
            print("{} - {}".format(ctxname, dev.name))


# $ sudo dtoverlay -l
# $ sudo dtoverlay -a|grep mpu
# $ sudo dtoverlay mpu6050
# sudo apt install libiio-utils
# sudo apt install python3-libiio
# pip install pylibiio


ctx = iio.Context('local:')
device = ctx.find_device('mpu6050')

print(device.name)

# dev.channels[0].enabled  = False
# dev.channels[1].enabled  = True
# dev.channels[2].enabled  = False

for chan in device.channels:
    print(chan.id)
    chan.enabled = 1
    break

# https://github.com/analogdevicesinc/libiio/issues/109

# need to sudo

buf = iio.Buffer(device, samples_count=256)

buf.refill()
r = buf.read()

print(r)