# WEB
**Luna Auth**
*Infiltrate the LunarAuth admin panel and gain access to the super secret FLAG artifact !*
[chall](https://comet.sunshinectf.games)
## Tóm tắt 
Được cung cấp một địa chỉ web với dạng login và tận dụng request response để lấy password và username
## Khai thác 
1. vào /robots.txt trang web trả về 
![alt text](image.png)
2. chuyển hướng đến /admin ta có được 1 form login 
3. Sử dụng 
![alt text](image-1.png)
4. Sử dụng tool burpsuite để chặn gói tin Get và chuyển nó đến repeater để theo dõi, có được username và password 
![alt text](image-2.png)
5. Giải mã bằng base64 lấy được flag
![alt text](image-3.png)