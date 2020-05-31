# Pwn 1
## General information
Using checksec we can see what kind of protections are active for this binary.
````
timo@ubuntu:~/CSCG/intro_pwn/pwn1$ checksec pwn1
[*] '/home/timo/CSCG/intro_pwn/pwn1/pwn1'
    Arch:     amd64-64-little
    RELRO:    Full RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      PIE enabled
````
There is no stack canary so we can easily do a bufferoverflow, but PIE is enabled so we need some addresses to calculate offsets from.

## The Binary
In the source code we can see that we first call gets with no lenght check, so we have a buffer overflow. We also print this buffer using
it as the first argument to printf, this allows for an format string exploit. We can use that to leak memory addresses and defeat ASLR/PIE.
Later we call gets again so we have a secound buffer overflow, but it has to start with `Expelliarmus` so we don't exit the program. There
is a WIN function that calls a shell, so if we can redirct code exection here we win.

## The Attack
We use the first input to send a format string that looks like "%p|%p|%p|%p|...". Form the recived output we can now extract the leak address
of the main function. We use it to calculate the address of the win function and the address of a return instruction that is used as a rop gadget
to alling the stack.

The second buffer overflow has to start with "Expelliarmus" and we can place a null byte behind it so strcmp stops reading, but gets dosen't
reading after a null byte. After this string there is some padding to fill up the buffer untill we overwrite the return address. We first place
the gadget then the Win function here. We send the complete thing and should get a shell.

The python script that runs the exploit uses pwn-tool for python2, you can find it in the additional files. If we run it we get a shell on the
server and can cat the flag `CSCG{NOW_PRACTICE_MORE}`.
