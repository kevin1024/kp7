import time
from socket import *

HEADER = ['01','af','f8','57','2e','00']

def decode(packet):
    return ''.join(b.decode('hex') for b in packet)

def set_led(keypad_id, led_id, brightness_percentage):
    sock = socket(AF_INET, SOCK_DGRAM)
    sock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
    packet = HEADER + keypad_id + ['00'] + [str(led_id + 21)] + ['00','00','00'] + ['%0.2X' % brightness_percentage] + ['00','00']
    sock.sendto(decode(packet), ('255.255.255.255', 39708))


while True:
    raw_input()
    set_led(['43','6a'], 0, 100)
    raw_input()
    set_led(['43','6a'], 0, 0)



