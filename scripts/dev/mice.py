import struct

# https://thehackerdiary.wordpress.com/2017/04/21/exploring-devinput-1/



with open("/dev/input/mice", "rb" ) as f:
    print("Listen mice...")
    while True:
        buf = f.read(3)
        button = ord(str(buf[0])[0])
        bLeft = button & 0x1
        bMiddle = (button & 0x4) > 0
        bRight = (button & 0x2) > 0
        dx, dy = struct.unpack("bb", buf[1:])
        print(dx, dy)
