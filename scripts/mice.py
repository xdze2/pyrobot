import struct

# https://thehackerdiary.wordpress.com/2017/04/21/exploring-devinput-1/


# with open( "/dev/input/mice", "rb" ) as f:

#     while True:
#         data = f.read(10)
#         print( struct.unpack('10b', data))


# import struct
# https://stackoverflow.com/a/12286738/8069403

file = open("/dev/input/mice", "rb")

x, y = 0, 0

def getMouseEvent():
    global x, y
    buf = file.read(3)
    button = ord(str(buf[0])[0])
    bLeft = button & 0x1
    bMiddle = (button & 0x4) > 0
    bRight = (button & 0x2) > 0
    dx, dy = struct.unpack("bb", buf[1:])
    # print("L:%d, M: %d, R: %d, x: %d, y: %d" % (bLeft, bMiddle, bRight, dx, dy))
    x += dx
    y += dy
    print(f"xy:\t{x: 5d}\t{y: 5d}")


while True:
    getMouseEvent()

file.close()
