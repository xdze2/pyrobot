from pynput import keyboard
import zmq


context = zmq.Context()
publisher = context.socket(zmq.PAIR)

ip_address = "192.168.1.72"

publisher.connect(f"tcp://{ip_address}:5564")


def on_press(key):
    
    try:
        print("alphanumeric key {0} pressed".format(key.char))
        publisher.send(key.char.encode('utf-8'))
    except AttributeError:
        print("special key {0} pressed".format(key))
        pass


def on_release(key):
    print("{0} released".format(key))
    if key == keyboard.Key.esc:
        # Stop listener
        return False


# Collect events until released
with keyboard.Listener(on_press=on_press, on_release=None) as listener:
    listener.join()

# ...or, in a non-blocking fashion:
listener = keyboard.Listener(on_press=on_press, on_release=on_release)
listener.start()
