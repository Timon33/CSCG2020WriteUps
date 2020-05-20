# eVMoji
## General information

The challange provides us with 2 files:
1. The eVMoji ELF binary
2. code.bin a UTF-8 encoded plain text file

If we open code.bin we can see it contains some strings like `tRy hArder! 💀💀💀` or `Thats the flag: CSCG{}` and a long series of
diffrent emojis. If we run the program it prints
````
Usage: ./eVMoji <code.bin>
Segmentation fault (core dumped)
````
and if we supply the code.bin as an argument we get
````
Welcome to eVMoji 😎
🤝 me the 🏳️
````
then it waits for input and if we enter some junk it responds
````
tRy hArder! 💀💀💀
````
Using the file command we can also find that the binary is stripped so reversing will be a bit harder.

## Reversing (a lot)
As a debuger/decomplier i again used ghidra because it is free and has some nice decompilation

**This challange took we quite a while to reverse and its not that simple. Thats why i will not explain how i discoverd every litter thing , but descibe what every function does with the knowlege of how the hole challange work in mind.**

### Setup/ Main function
We can find the main function using the entry function and rename it. Main opens the code.bin file wich is supplied in the second argument.
Then it allocates 3 region, the first 2 of size 0x400 and the third of size 0x10000. The start of the file is loaded into one of the size 0x400 regions and the emojis are loaded into the 0x10000 size section. The the file is closed and we enter the function that contaions the main loop.

### Generell
After Completing i can tell you, that the challenge is a about a emulator/interpreter that runs the emoji code. The main loop that is called from main loops 


