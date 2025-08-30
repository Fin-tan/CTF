# CHALLENGE
- Logical Thiniking is need for everything.
## SOLUTION
- Encode
```
process_flag(FileName) :-
    open(FileName, read, Stream),           
    read_string(Stream, _, Content),        
    close(Stream),                          
    string_codes(Content, Codes),           
    transform_codes(Codes, 1, Transformed),
    string_codes(NewString, Transformed),   
    writeln(NewString).                     


transform_codes([], _, []).
transform_codes([H|T], Index, [NewH|NewT]) :-
    NewH is H + Index,                      
    NextIndex is Index + 1,                  
    transform_codes(T, NextIndex, NewT).     


%EXECUTE
%?- process_flag('flag.txt').
```
- Đọc flag và chuyển mỗi từ sang mã ASCII sau đó + index với index là số tăng dần với bước nhảy là 1
### Decode
```python
s = "gyhgyl|qoj\\>@@xqDD|zyJyg}UD¡"
result=""
i=1
for c in s:
    result+=chr(ord(c)-i)
    i=i+1
print(result)
```
- lấy enc đem đi chuyển sang mã thập phân sau đó trừ đi index với bước nhảy là 1 rồi chuyển lại sang chữ 
## FLAG
- fwectf{the_Pr010g_10gica1_Languag3!}