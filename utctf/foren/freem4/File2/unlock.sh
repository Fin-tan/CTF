#!/bin/bash

# Mật khẩu dự phòng (nếu gặp file RAR có pass)
PASS="0r4ng3_ArCh1v3_T4bSp4ce!"

echo "[*] Bắt đầu phá đảo chuỗi Archive lồng nhau..."

while true; do
    # 1. Tìm file nén bất kỳ trong thư mục hiện tại (.rar hoặc .tar)
    TARGET=$(ls *.rar *.tar 2>/dev/null | head -n 1)

    if [ -z "$TARGET" ]; then
        echo "[🌐] Không tìm thấy file nén nào nữa. Dừng lại tại đây!"
        ls -la
        break
    fi

    echo "[+] Đang xử lý: $TARGET"

    # 2. Kiểm tra định dạng và giải nén tương ứng
    if [[ "$TARGET" == *.tar ]]; then
        tar -xf "$TARGET" && rm "$TARGET"
    elif [[ "$TARGET" == *.rar ]]; then
        # Thử giải nén không pass, nếu lỗi thì dùng pass
        unrar e -y -p- "$TARGET" > /dev/null 2>&1 || unrar e -y -p"$PASS" "$TARGET" > /dev/null 2>&1
        rm "$TARGET"
    fi

    # Tránh vòng lặp vô tận nếu giải nén ra chính nó
    sleep 0.1
done

echo "[*] Hoàn tất! Nếu thấy file 'flag' hoặc '.txt', hãy 'cat' nó ra."
