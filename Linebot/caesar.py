def encode(text):
    result = []
    for c in text:
        result.append(chr(ord(c) + 3))
    encryption = ''.join(result)
    return encryption


def decode(text):
    result = []
    for c in text:
        result.append(chr(ord(c) - 3))
    enc = ''.join(result)
    return enc


get = input("Enter any text> ")

res = encode(get)
print(res)
orig = decode(res)
print(f"original: {orig}")
