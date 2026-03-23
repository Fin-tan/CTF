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

# Colonel
Tác giả cho ta một file dump và bắt tìm flag nhưng lần này là của Linux 
Dùng vol để phân tích  
```
└─$ python3 vol.py -f /mnt/hgfs/share/CTF/Tamu/colonel/memory.dump linux.bash.Bash
Volatility 3 Framework 2.28.0
Progress:  100.00               Stacking attempts finished            
PID     Process CommandTime     Command

4269    bash    2026-02-14 21:48:53.000000 UTC  ls
4269    bash    2026-02-14 21:48:53.000000 UTC  ls /tmp
4269    bash    2026-02-14 21:48:53.000000 UTC  exit
4269    bash    2026-02-14 21:48:56.000000 UTC  cd validate/
4269    bash    2026-02-14 21:49:03.000000 UTC  sudo insmod check_service.ko key_path=validation
4269    bash    2026-02-14 21:49:09.000000 UTC  sudo rmmod check_service
4269    bash    2026-02-14 21:49:11.000000 UTC  sudo insmod check_service.ko key_path=validation2
```                                                                              
Ta có thể thấy được các lệnh đã thực hiện, vào file validate và chèn một kernel check_service.ko vào hệ thống kèm theo tham số sau đó loại bỏ module đó ra rồi lại chèn vào một module khác với tham số là validation2 
Ta sẽ tiến hành đọc validation2 này bằng 
```
strings /mnt/hgfs/share/CTF/Tamu/colonel/memory.dump | grep -iE -A 5 -B 5 "validation2" 
```
Lệnh này sẽ đọc 5 dòng phía trước và sau của dòng chữ này 
```
2026-02-14T21:49:05.592890+00:00 ubuntuvm kernel: check_service: module verification failed: signature and/or required key missing - tainting kernel
2026-02-14T21:49:05.594253+00:00 ubuntuvm kernel: Reading from validation
2026-02-14T21:49:05.594264+00:00 ubuntuvm kernel: Error: Invalid key 51782b4b765251314e32525236364978534d35566a6b72474b67303946483266, indices 9 21 31 incorrect
2026-02-14T21:49:05.594265+00:00 ubuntuvm kernel: Validation failed
2026-02-14T21:49:09.229154+00:00 ubuntuvm kernel: Module unloaded
2026-02-14T21:49:11.781287+00:00 ubuntuvm kernel: Reading from validation2
2026-02-14T21:49:11.781303+00:00 ubuntuvm kernel: Error: Invalid key 58782b4b765251314e51525235364978534d35566a6a72524b673039466c3265, indices 0 12 23 29 incorrect
```
Ta có thể thấy được cảnh báo sai mật khẩu 2 lần tại vị trí 9 21 31 0 12 23 29 kết hợp 2 lần sau này lại là ta có được key 
51782b4b765251314e51525236364978534d35566a6a72474b67303946483265
Kết hợp với IV đã cho ta có được flag 
gigem{bl3ss3d_4r3_th3_c010n31_m33k}