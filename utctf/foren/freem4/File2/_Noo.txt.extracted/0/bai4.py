with open("NotaFlag.txt", "rb") as f:
    content = f.read()

# Chuyển đổi: Space -> '0', Tab -> '1', dùng xuống dòng làm dấu phân cách
binary_str = ""
for byte in content:
    if byte == 0x20: # Space
        binary_str += "0"
    elif byte == 0x09: # Tab
        binary_str += "1"
    elif byte == 0x0a: # Newline
        binary_str += " "

# Chuyển từ nhị phân sang ký tự
flag = "".join([chr(int(b, 2)) for b in binary_str.split() if b])
print(f"Flag của bạn đây: {flag}")
