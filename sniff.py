import struct
import socket
from socket import *

KEYPAD_PACKET_HEADER = ['01', 'af', 'f8', '57', '2e', '00']
KEYPAD_PACKET_LENGTH = 16

KEYPADS = {
    ('50','e4'): 'gym',
    ('43','6a'): 'living room',
    ('4d','c5'): 'bedroom',
    ('4d','cb'): 'bathroom',
}


def parse_keepalive(message):
    binary = ''.join(b.decode('hex') for b in message[2:4])
    sequence = struct.unpack('!H', binary)
    return "keepalive %s" % sequence

def parse_buttonpress(message):
    binary = ''.join(b.decode('hex') for b in message[4:6])
    sequence = struct.unpack('>H', binary)[0]
    print sequence
    mapper = {
        '1': bool(sequence & (1 << 1)),
        '2': bool(sequence & (1 << 2)),
        '3': bool(sequence & (1 << 3)),
        '4': bool(sequence & (1 << 4)),
        '5': bool(sequence & (1 << 5)),
        'down': bool(sequence & (1 << 6)),
        'up': bool(sequence & (1 << 7)),
    }
    mapper = {k:v for (k,v) in mapper.items() if v}
    return "button pressed %s" % mapper

MESSAGES = {
    ('00','00'): parse_keepalive,
    ('00','01'): parse_buttonpress,
}

def parse(packet):
    if len(packet) != KEYPAD_PACKET_LENGTH or packet[0:6] != KEYPAD_PACKET_HEADER:
        print "nope %s" % packet
        return #not the packet we are looking for
    keypad = KEYPADS[tuple(packet[6:8])]
    message = packet[8:]
    print message
    try:
        print "found packet from %s: %s" % (keypad, MESSAGES[tuple(message[0:2])](message))
    except KeyError:
        print "found mystery packet from %s: %s" % (keypad, message)


s=socket(AF_INET, SOCK_DGRAM)
s.bind(('',39707))
while(1):
    data, addr = s.recvfrom(4096)
    print addr
    parse([x.encode('hex') for x in data])
