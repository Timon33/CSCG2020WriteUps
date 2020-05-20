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
As a debuger/decomplier i again used ghidra because it is free and has some nice decompilation.

**This challange took we quite a while to reverse and its not that simple. Thats why i will not explain how i discoverd every litter thing , but descibe what every function does with the knowlege of how the hole challange work in mind.**

The writeup will be quite long anyways and i dont't want to make it to boring.

### Generell
After completing the challange i found, that the challenge is a about a emulator/interpreter that runs the emoji code. The main loop that is called from main is a big while loop. It gets the next emoji then compares it in a switch case like manner and executes diffrent pices of code depending on the emoji. The emoji program in code.bin implements a password check, where the password is the flag it self. Fist i will explaint how i reversted the program and what the diffrent emojies do, and then how we can find the flag.

### Setup/ Main function
We can find the main function using the entry function and rename it. Main opens the code.bin file wich is supplied in the second argument.
Then it allocates 3 region, the first 2 of size 0x400 and the third of size 0x10000. The start of the file is loaded into one of the size 0x400 regions and the emojis are loaded into the 0x10000 size section. The the file is closed and we enter the function that contaions the main loop. I will call this function runEmojiCode from now on.

### RunEmojiCode Function
The function first calls 2 other functions with the same parameter and then adds the result of the secound to a variable. Later i found that both functions take a pointer to the current emoji (instruction) in the big heap segment allocated in main, the first return the unicode bytes decoded from utf-8 and the second the number of bytes the emoji takes to encode in utf-8. This lenght of bytes is added to a counter variable that keeps track of the current emoji.

Now we enter the large switch case statment (the decomiler show a probably optimized version that uses a lot of if statments, but it's the same), it compares the unicode bytes of the emoji and then executes some code depending on the emoji. The functionality of each emoji also relates to it look (e.g. skull is exit, pen is write...).

### Helper functions
Befor i go into what each emoji does i want to talk about the functions that are frequetly used in the hole program. When you fist open a strip binary it can be very difficult because you have to start somewhere but dont know anything. A good idea is to look at the Xrefs for smaller functions and there parameters and the context they are used in. When i first looked at these function used at the start at the while loop i was confused, because the shift bits all over the place and use a lot of logic operators and loops. Evetually i looked up how emojis are encoded and found the [utf-8](https://en.wikipedia.org/wiki/UTF-8) encoding standart. As you can read on the wiki page it uses the first bits of a byte to determine the lenght and position of the bits that make up the encoded data. These complicated, weird function acctualy just extract these bits and similar things, but look very complicated at first. If the binary was not stript and these function where called something like `long GetUnicodeFromUTF8(char *utf8String)` all of this would of been easier.

### The opcodes
I will now give a short discription of what all of the diffrent emojies do. Once you know this you dont even really need the binary anymore because you can just extract the alogrithm from code.bin. I later used a python script to convert the emoji code to assembly like code to make it more convenient to read.

I will say some instruction push or pop values on/from the stack. The stack refers to one of the in main allocated heap segments because it is used like a stack would be in a binary run a cpu.

#### "Opcode" aruments
You will notice that after many emojis there are allways 6 number emojis. These represend a number that is an argument to the opcode emoji before them. The alogorithem to decode them to one number is:
````
for i in range(3):
  result += numbersFromEmojies[i * 2 + 1] ** numbersFromEmojies[i * 2]
````
where `numbersFromEmojies` is an int array that contains the numbers that the emojies show.

#### Write✏️
This opcode writes a string to stdout. Count of bytes to wite is poped from the stack, then a offset to the string to print is poped. The offset points to the segment that contains the start of the file and the strings like `🤝 me the 🏳️`. The opcode is used to print these messages to the user.
`n = pop()`
`offste = pop()`
`write(stdout, dataSegmentBase + offset, n)`

#### Read📖
This opcode works like write except it reads a number of bytes from stdin and stores them on the same segment the static strings are stored.
`n = pop()`
`offste = pop()`
`read(stdin, dataSegmentBase + offset, n)`


#### Push💪
This opcode pushes the opcode argument that is computed as descripted above onto the stack.

