from typing import Callable

import zmq
from pynput import keyboard

ip_address = "192.168.1.72"


context = zmq.Context()
publisher = context.socket(zmq.PAIR)
publisher.setsockopt(zmq.LINGER, 0)
publisher.connect(f"tcp://{ip_address}:5564")


class KeyState:
    def __init__(self, on_change: Callable):
        self.white_list = 'ijkl'
        self.on_change = on_change
        self.state = set()
        self.listener = keyboard.Listener(
            on_press=self._on_press, on_release=self._on_release
        )
        self.listener.start()

    def _on_press(self, key):

        try:
            key = key.char  
            # print("alphanumeric key {0} pressed".format(key.char))
            if key is not None and key in self.white_list and key not in self.state:
                self.state.add(key)
                self.update_state()
            else:
                print('{key} skipped')
        except AttributeError:
            # print("special key {0} pressed".format(key))
            pass

    def _on_release(self, key):
        # print("{0} released".format(key))
        try:
            if key.char in self.state:
                self.state.remove(key.char)
                self.update_state()
        except AttributeError:
            pass

    def update_state(self):
        print("state:", self.state)
        self.on_change(self.state)


def on_new_state(state: str):
    str_state = "".join(sorted(state))
    publisher.send(str_state.encode("utf-8"))


keyboard_state = KeyState(on_new_state)

print('Use z q s d keys...')
keyboard_state.listener.join()
# # ...or, in a non-blocking fashion:
# listener = keyboard.Listener(on_press=on_press, on_release=on_release)
# listener.start()
