# APNG - Just A PNG
Đây là 1 file APNG chúng ta sẽ dùng exiftool để xem các hint mà đề bài cho 
```
ExifTool Version Number         : 13.25
File Name                       : ch21.apng
Directory                       : .
File Size                       : 996 kB
File Modification Date/Time     : 2026:04:06 20:41:48+07:00
File Access Date/Time           : 2026:04:06 20:42:35+07:00
File Inode Change Date/Time     : 2026:04:06 20:41:48+07:00
File Permissions                : -rwxrwxrwx
File Type                       : APNG
File Type Extension             : apng
MIME Type                       : image/apng
Image Width                     : 512
Image Height                    : 512
Bit Depth                       : 8
Color Type                      : RGB with Alpha
Compression                     : Deflate/Inflate
Filter                          : Adaptive
Interlace                       : Noninterlaced
Animation Frames                : 13
Animation Plays                 : inf
Warning                         : [minor] Text/EXIF chunk(s) found after APNG IDAT (may be ignored by some readers)
Software                        : APNG Assembler 2.91
Image Size                      : 512x512
Megapixels                      : 0.262
```
Trong này có 2 kết quả: 
1. Là Frames của ảnh này gồm 13 có nghĩa nó sẽ chứa 13 ảnh khác nhau trong này
2. Warning đã tìm thấy chunks ở sau dữ liệu file APNG 

- Ta sẽ dùng apngdis để trích xuất các file ẩn trong này ra 
```
─$ ls
apngframe01.png  apngframe02.png  apngframe03.png  apngframe04.png  apngframe05.png  apngframe06.png  apngframe07.png  apngframe08.png  apngframe09.png  apngframe10.png  apngframe11.png  apngframe12.png  apngframe13.png  ch21.apng
apngframe01.txt  apngframe02.txt  apngframe03.txt  apngframe04.txt  apngframe05.txt  apngframe06.txt  apngframe07.txt  apngframe08.txt  apngframe09.txt  apngframe10.txt  apngframe11.txt  apngframe12.txt  apngframe13.txt  readme.md
```
- Trong này gồm các file png gồm các frame ảnh và các file .txt là thời gian delay giữa các ảnh 
```
└─$ cat *.txt
delay=70/10
delay=76/10
delay=65/10
delay=71/10
delay=58/10
delay=80/10
delay=51/10
delay=80/10
delay=111/10
delay=70/10
delay=82/10
delay=111/10
delay=71/10
```
Ta sẽ lấy các giá trị này chuyển đổi sang ASCII và lấy được *FLAG:P3PoFRoG*
