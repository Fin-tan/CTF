# Deleted
Title: Your cousin found a USB drive in the library this morning. He’s not very good with computers, so he’s hoping you can find the owner of this stick!

The flag is the owner’s identity in the form firstname_lastname

Xác định file này là file tar sau đó ta sẽ giải nén nó được một file USB.image 

```
┌──(kali㉿Fintan)-[/mnt/…/Root-me/Foren/Deleted/ch39]
└─$ file ch39          
ch39: POSIX tar archive (GNU)
                                                                                                                                 
┌──(kali㉿Fintan)-[/mnt/…/Root-me/Foren/Deleted/ch39]
└─$ 


```
Đối với file này ta sẽ  dùng fls trong sleuth kit để liệt kê các file còn và kể cả đã bị xóa, và sử dụng icat để trích xuất nội dung của file đã bị xóa 



```
                                                                                                                                 
┌──(kali㉿Fintan)-[/mnt/…/Root-me/Foren/Deleted/ch39]
└─$ file usb.image
usb.image: DOS/MBR boot sector, code offset 0x3c+2, OEM-ID "mkfs.fat", sectors/cluster 4, reserved sectors 4, root entries 512, sectors 63488 (volumes <=32 MB), Media descriptor 0xf8, sectors/FAT 64, sectors/track 62, heads 124, hidden sectors 2048, reserved 0x1, serial number 0xc7ecde5b, label: "USB        ", FAT (16 bit)
                                                                                                                                 
┌──(kali㉿Fintan)-[/mnt/…/Root-me/Foren/Deleted/ch39]
└─$ fls -r -p usb.image
r/r 3:  USB         (Volume Label Entry)
r/r * 5:        anonyme.png
v/v 1013699:    $MBR
v/v 1013700:    $FAT1
v/v 1013701:    $FAT2
V/V 1013702:    $OrphanFiles
                                                                                                                                 
┌──(kali㉿Fintan)-[/mnt/…/Root-me/Foren/Deleted/ch39]
└─$ icat usb.image 5 > anonyme.png
                                                                                                                                 
┌──(kali㉿Fintan)-[/mnt/…/Root-me/Foren/Deleted/ch39]
└─$ ls
anonyme.png  ch39  usb.image
```
Khi đã có được file png ta sẽ dùng exiftool để biết thêm những thông tin về nó 
```
─$ exiftool anonyme.png 
ExifTool Version Number         : 13.25
File Name                       : anonyme.png
Directory                       : .
File Size                       : 246 kB
File Modification Date/Time     : 2026:03:20 22:33:59+07:00
File Access Date/Time           : 2026:03:20 22:33:59+07:00
File Inode Change Date/Time     : 2026:03:20 22:33:59+07:00
File Permissions                : -rwxrwxrwx
File Type                       : PNG
File Type Extension             : png
MIME Type                       : image/png
Image Width                     : 400
Image Height                    : 300
Bit Depth                       : 8
Color Type                      : RGB
Compression                     : Deflate/Inflate
Filter                          : Adaptive
Interlace                       : Noninterlaced
Gamma                           : 2.2
White Point X                   : 0.3127
White Point Y                   : 0.329
Red X                           : 0.64
Red Y                           : 0.33
Green X                         : 0.3
Green Y                         : 0.6
Blue X                          : 0.15
Blue Y                          : 0.06
Background Color                : 255 255 255
XMP Toolkit                     : Image::ExifTool 11.88
Creator                         : Javier Turcot
Image Size                      : 400x300
Megapixels                      : 0.120
```
Ta xác định được chủ sở hữu là Javier Turcot
Flag: Javier_Turcot