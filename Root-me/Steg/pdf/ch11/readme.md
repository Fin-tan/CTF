# PDF - Embedded

1. Khảo sát File PDF này bằng cách mở lên thì không có thông tin gì trong file này, vì thể ta sẽ dùng binwalk để trích xuất những file bị ẩn ra 

```
──(kali㉿Fintan)-[/mnt/…/Foren/pdf/ch11/_epreuve_BAC_2004.pdf.extracted]
└─$ ls
105          145DA9       1D5B4B       33F         4BB       7B3         DBB62
105.zlib     145DA9.zlib  1D5B4B.zlib  33F.zlib    4BB.zlib  7B3.zlib    DBB62.zlib
10B639       17529A       2112CE       3F990       579       83E60
10B639.zlib  17529A.zlib  2112CE.zlib  3F990.zlib  579.zlib  83E60.zlib
1266BC       193480       233212       3FD         637       871
1266BC.zlib  193480.zlib  233212.zlib  3FD.zlib    637.zlib  871.zlib
139D         1C3          281          49          6F5       A6E1E
139D.zlib    1C3.zlib     281.zlib     49.zlib     6F5.zlib  A6E1E.zlib
```
Toàn là file zlib điều này cho thấy file PDF có chứa các stream ẩn. Tuy nhiên, để xem xét cấu trúc logic của PDF một cách rõ ràng hơn, ta sẽ chuyển sang dùng pdf-parser, tool này sẽ mổ xẻ cấu trúc trong của một file PDF mà không mở file lên 
```
└─$ pdf-parser -a epreuve_BAC_2004.pdf
This program has not been tested with this version of Python (3.13.7)
Should you encounter problems, please use Python version 3.12.2
Comment: 3
XREF: 1
Trailer: 1
StartXref: 1
Indirect object: 78
Indirect objects with a stream: 5, 12, 18, 24, 30, 36, 42, 48, 54, 60, 66, 72, 8, 14, 20, 26, 32, 38, 44, 50, 56, 62, 68, 74, 77
  61: 5, 6, 12, 13, 18, 19, 24, 25, 30, 31, 36, 37, 42, 43, 48, 49, 54, 55, 60, 61, 66, 67, 72, 73, 9, 10, 8, 15, 16, 14, 21, 22, 20, 27, 28, 26, 33, 34, 32, 39, 40, 38, 45, 46, 44, 51, 52, 50, 57, 58, 56, 63, 64, 62, 69, 70, 68, 75, 76, 74, 2
 /Catalog 1: 1
 /Embeddedfile 1: 77
 /ExtGState 1: 7
 /Filespec 1: 78
 /Page 12: 4, 11, 17, 23, 29, 35, 41, 47, 53, 59, 65, 71
 /Pages 1: 3
```
Ta sẽ xem qua 2 trường quan trọng này 
/Filespec 1: 78: Có 1 object File Specification (Thông số file đính kèm) nằm tại Object 78. Object này làm nhiệm vụ khai báo tên file, định dạng, và trỏ tới nơi chứa dữ liệu của file đính kèm.

/Embeddedfile 1: 77: Có 1 Embedded File (File được nhúng thẳng vào trong PDF), nằm ở Object 77.
Ta sẽ xem qua 2 file này 
```
This program has not been tested with this version of Python (3.13.7)
Should you encounter problems, please use Python version 3.12.2
obj 78 0
 Type: /Filespec
 Referencing: 77 0 R

  <<
    /F (Hidden_b33rs.txt)
    /Type /Filespec
    /EF
      <<
        /F 77 0 R
      >>
  >>
```
File tại object 78 này trỏ đến 77 và có tên là hidden_b33rs.txt chắc chắn object 77 này chứa flag, ta sẽ xuất file này ra
Nội dung của file này không phải là văn bản bình thường mà là một chuỗi khổng lổ bắt đầu bằng /9j/4A ..., theo như tìm hiểu thì đây là một chuỗi chữ ký của một file hình ảnh jpeg đã được mã hóa sang base64 vì thế ta sẽ trích xuất và giải mã base64 thành ảnh bằng awk
```
awk '/^\/9j/{flag=1} /^endstream/{flag=0} flag' extracted_attachment.txt | base64 -d > flag.jpg
```
Mở ảnh lên và có flag:Hidden-embedded_Fil

