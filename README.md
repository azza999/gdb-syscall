# gdb-syscall
describe syscall which is being executed


## Install
```
cd ~
git clone https://github.com/azza999/gdb-syscall
echo "source ~/gdb-syscall/gdb-syscall.py" >> ~/.gdbinit
```

## Usage
Sometimes, kernel change $rax as -38 which means error code.
then just enter "sc $syscall" to check syscall arguments.
```
gdb) catch syscall
gdb) c
gdb) sc

gdb-peda$ sc

───────────────[ SYSCALL ]───────────────
  #-38   unknown
  rdi          = 0x3
  rsi          = 0x447800
  rdx          = 0x284c0
  r10(rcx)     = 0x0
  r8           = 0x0
  r9           = 0x0
──────────────────────────────────────────
gdb-peda$ sc 0x3

───────────────[ SYSCALL ]───────────────
  #3   sys_close
  rdi          = 0x3    // unsigned int fd
  rsi          = 0x447800
  rdx          = 0x284c0
  r10(rcx)     = 0x0
  r8           = 0x0
  r9           = 0x0
──────────────────────────────────────────


```
