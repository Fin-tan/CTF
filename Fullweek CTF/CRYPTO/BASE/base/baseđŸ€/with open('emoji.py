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
