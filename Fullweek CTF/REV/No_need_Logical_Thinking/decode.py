s = "gyhgyl|qoj\\>@@xqDD|zyJyg}UD¡"
result=""
i=1
for c in s:
    result+=chr(ord(c)-i)
    i=i+1
print(result)