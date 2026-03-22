# Time-capsule
Bài này đề cho một file img file này là file disk, ta sẽ dùng sleuth-kit để trích xuất file trong này ra và tìm flag

```
──(kali㉿Fintan)-[/mnt/…/share/CTF/Tamu/Time-capsule]
└─$ fls time-capsule.img      
d/d 13: home
d/d 11: lost+found
V/V 12825:      $OrphanFiles
```

Dùng fls để xem thư mục thì chỉ có thư mục id 13 sẽ có thông tin còn 11 và 12825 không có bất cứ file nào 
```
──(kali㉿Fintan)-[/mnt/…/share/CTF/Tamu/Time-capsule]
└─$ fls time-capsule.img 13               
d/d 14: bob
                                                                                                                                                                                                                   
┌──(kali㉿Fintan)-[/mnt/…/share/CTF/Tamu/Time-capsule]
└─$ fls time-capsule.img 14
d/d 15: nostalgia
                                                                                                                                                                                                                   
┌──(kali㉿Fintan)-[/mnt/…/share/CTF/Tamu/Time-capsule]
└─$ fls time-capsule.img 15
r/r 16: memory_1.jpg
r/r 17: memory_2.jpg
r/r 18: memory_3.jpg
r/r 19: memory_4.jpg
r/r 20: memory_5.png
r/r 21: memory_6.jpg
r/r 22: memory_7.jpg
r/r 23: memory_8.jpg
r/r 24: memory_9.webp
r/r 25: memory_10.jpg
r/r 26: memory_11.jpg
r/r 27: memory_12.webp
r/r 28: memory_13.jpg
r/r 29: memory_14.jpg
r/r 30: memory_15.jpg
r/r 31: memory_16.avif
r/r 32: memory_17.jpg
                                                                                                                                                                                                                   
┌──(kali㉿Fintan)-[/mnt/…/share/CTF/Tamu/Time-capsule]
└─$ 

```
Tiếp tục vào sâu hơn ta có được một chuỗi các tệp ảnh 
có 2 hướng để tiếp tục tìm flag
1. Tìm chuỗi flag thông qua exiftool của tất cả các ảnh + với grep( không thành công)
2. Soi từng ảnh xem có flag trong ảnh không (không thành công )
3. Ta sẽ hiển thị chi tiết tất cả thông tin của hình ảnh này bằng flag -l
```
┌──(kali㉿Fintan)-[/mnt/…/share/CTF/Tamu/Time-capsule]
└─$ fls -l time-capsule.img 15 
r/r 16: memory_1.jpg    2007-01-01 14:01:43 (+07)       2007-01-01 14:01:43 (+07)       2026-03-16 09:49:40 (+07)       2026-03-16 09:49:40 (+07)       32727   0       0
r/r 17: memory_2.jpg    2007-01-01 14:01:45 (+07)       2007-01-01 14:01:45 (+07)       2026-03-16 09:49:40 (+07)       2026-03-16 09:49:40 (+07)       658628  0       0
r/r 18: memory_3.jpg    2007-01-01 14:01:43 (+07)       2007-01-01 14:01:43 (+07)       2026-03-16 09:49:40 (+07)       2026-03-16 09:49:40 (+07)       45808   0       0
r/r 19: memory_4.jpg    2007-01-01 14:01:41 (+07)       2007-01-01 14:01:41 (+07)       2026-03-16 09:49:40 (+07)       2026-03-16 09:49:40 (+07)       48285   0       0
r/r 20: memory_5.png    2007-01-01 14:01:49 (+07)       2007-01-01 14:01:49 (+07)       2026-03-16 09:49:40 (+07)       2026-03-16 09:49:40 (+07)       488162  0       0
r/r 21: memory_6.jpg    2007-01-01 14:02:03 (+07)       2007-01-01 14:02:03 (+07)       2026-03-16 09:49:40 (+07)       2026-03-16 09:49:40 (+07)       20745   0       0
r/r 22: memory_7.jpg    2007-01-01 14:01:38 (+07)       2007-01-01 14:01:38 (+07)       2026-03-16 09:49:40 (+07)       2026-03-16 09:49:40 (+07)       19869   0       0
r/r 23: memory_8.jpg    2007-01-01 14:02:01 (+07)       2007-01-01 14:02:01 (+07)       2026-03-16 09:49:40 (+07)       2026-03-16 09:49:40 (+07)       376166  0       0
r/r 24: memory_9.webp   2007-01-01 14:01:43 (+07)       2007-01-01 14:01:43 (+07)       2026-03-16 09:49:40 (+07)       2026-03-16 09:49:40 (+07)       50564   0       0
r/r 25: memory_10.jpg   2007-01-01 14:00:48 (+07)       2007-01-01 14:00:48 (+07)       2026-03-16 09:49:40 (+07)       2026-03-16 09:49:40 (+07)       49586   0       0
r/r 26: memory_11.jpg   2007-01-01 14:01:50 (+07)       2007-01-01 14:01:50 (+07)       2026-03-16 09:49:40 (+07)       2026-03-16 09:49:40 (+07)       20752   0       0
r/r 27: memory_12.webp  2007-01-01 14:00:51 (+07)       2007-01-01 14:00:51 (+07)       2026-03-16 09:49:40 (+07)       2026-03-16 09:49:40 (+07)       656626  0       0
r/r 28: memory_13.jpg   2007-01-01 14:01:35 (+07)       2007-01-01 14:01:35 (+07)       2026-03-16 09:49:40 (+07)       2026-03-16 09:49:40 (+07)       23262   0       0
r/r 29: memory_14.jpg   2007-01-01 14:00:51 (+07)       2007-01-01 14:00:51 (+07)       2026-03-16 09:49:40 (+07)       2026-03-16 09:49:40 (+07)       9422    0       0
r/r 30: memory_15.jpg   2007-01-01 14:01:54 (+07)       2007-01-01 14:01:54 (+07)       2026-03-16 09:49:40 (+07)       2026-03-16 09:49:40 (+07)       9337    0       0
r/r 31: memory_16.avif  2007-01-01 14:00:52 (+07)       2007-01-01 14:00:52 (+07)       2026-03-16 09:49:40 (+07)       2026-03-16 09:49:40 (+07)       14599   0       0
r/r 32: memory_17.jpg   2007-01-01 14:02:05 (+07)       2007-01-01 14:02:05 (+07)       2026-03-16 09:49:40 (+07)       2026-03-16 09:49:40 (+07)       411177  0       0

```
Nhìn kĩ thì thấy thời gian khá sát nhau khi ta lấy phút và giây cũng lại ta sẽ có điều đặc biệt 
Ví dụ memory_1 ta lấy 1p43s=60+43=103 =(g)
60+45=105(i)
103 105 103 101 109 123 98 121 103 48 110 51 95 51 114 52 125
cứ tiếp tục ta sẽ có flag :gigem{byg0n3_3r4}
