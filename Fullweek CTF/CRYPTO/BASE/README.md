# CHALLENGE
- 🪛🔱🛜🫗🚞👞🍁🎩🚎🐒🌬🧨🖱🥚🫁🧶🪛🔱👀🔧🚞👛😄🎩🚊🌡🌬🧮🤮🥚🫐🛞🪛🔱👽🔧🚞🐻🔳🎩😥🪨🌬🩰🖖🥚🫐🪐🪛🔱👿🫗🚞🏵📚🎩🚊🎄🌬🧯🕺🥚🫁📑🪛🔰🐀🫗🚞💿🔳🎩🚲🚟🌬🧲🚯🥚🫁🚰🪛🔱💀🔧🚞🏓🛼🎩🚿🪻🌬🧪🙊🥚🫐🧢🪛🔱🛟🔧🚞🚋🫳🎩😆🏉🌬🧶🚓🥚🫅💛🪛🔱🔌🐃🚞🐋🥍🎩😱🤮🌬🩰🛳🥚🫀📍🪛🔰🐽🫗🚞💿🍁🎩🚊🌋🌬🧵🔷🚀🚀🚀

- [base.zip](https://ctf.fwectf.com/files/cea45fd5eba036a38e4fc577b56bd43e/base.zip?token=eyJ1c2VyX2lkIjo2ODksInRlYW1faWQiOjM4OCwiZmlsZV9pZCI6NTZ9.aLKzlw.jH20s0_BSWDN0q1-AWxuP8Rp5hA)
## SOLUTION
encode
```python
#!/usr/bin/env python🚀

with open('emoji.txt', 'r', encoding='utf-8') as f:
    emoji = list(f.read().strip())

table = {i: ch for i, ch in enumerate(emoji)}

def encode(data):
    bits = ''.join(f'{b:08b}' for b in data)
    pad = (-len(bits)) % 10
    bits += '0' * pad
    out = [table[int(bits[i:i+10], 2)] for i in range(0, len(bits), 10)]
    r = (-len(out)) % 4
    if r:
        out.extend('🚀' * r)
    return ''.join(out)

if __name__ == '__main__':
    msg = 'Hello!'
    enc = encode(msg.encode())
    print('msg:', msg)
    print('enc:', enc)
```
- Các bước Encode
1. Chia dữ liệu vào thành chuỗi 8 bit sau đó ghép lại
2. padding thêm vào cho đủ bit là bội số của 10
3. Cắt chuỗi đó thành chuỗi nhỏ mỗi chuỗi 10 bit sau đó chuyển sang thập phân rồi ánh xạ sang bảng thành emoji
4. Padding thêm emoji 🚀 vào cho đủ số emoji chia hết cho 4
decode
```python
# save as decode_emoji.py and run: python decode_emoji.py
emoji_txt_path = 'emoji.txt'   # chỉnh đường dẫn nếu cần
enc = ("🪛🔰🛏🍈📛🤵🔈🚁📷🦨🥩💇💼🥇🧷🥳🎆🚇🔅👶📷🚇🤧🗣💐🥵🌚🦽🏖🧇🪥🦿🏋🛜🙆🧀🏋🔭🥬🍲🔫🚀🚀🚀")
def decode_with_file(enc, emoji_path):
    with open(emoji_path, 'r', encoding='utf-8') as f:
        emoji = list(f.read().strip())
    table = {i: ch for i, ch in enumerate(emoji)}
    reverse_table = {ch: i for i, ch in table.items()}

    # remove padding rockets
    enc = enc.rstrip('🚀')
    
    # map each emoji to 10-bit chunk
    try:
        bits = ''.join(f'{reverse_table[ch]:010b}' for ch in enc)
    except KeyError as e:
        raise ValueError(f"Emoji {e} not found in emoji.txt. Check that emoji.txt contains all used emoji.") from None

    # split into bytes
    data = []
    for i in range(0, len(bits), 8):
        byte = bits[i:i+8]
        if len(byte) < 8:
            break
        data.append(int(byte, 2))
    return bytes(data)

if __name__ == '__main__':
    try:
        decoded = decode_with_file(enc, emoji_txt_path)
        # try interpreting as utf-8 text
        try:
            print(decoded.decode('utf-8'))
        except UnicodeDecodeError:
            print("Decoded bytes (not valid UTF-8):", decoded)
    except Exception as e:
        print("Error:", e)
```
- Quá trình Decode
1. Xóa padding 🚀
2. Từ emoji ánh xạ sang bảng thành số thập phân 
3. Chuyển mỗi số thành 10bit rồi ghép lại
4. Cắt thành 8bit rồi đổi byte -> text

## FLAG
fwectf{n0_r0ck37_3m0ji_n0_llm}
flag sau khi giải mã 2 lần liên tiếp 

