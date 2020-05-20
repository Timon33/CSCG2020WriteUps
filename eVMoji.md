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
````
n = pop()
offste = pop()
write(stdout, dataSegmentBase + offset, n)
````

#### Read📖
This opcode works like write except it reads a number of bytes from stdin and stores them on the same segment the static strings are stored.
````
n = pop()
offste = pop()
read(stdin, dataSegmentBase + offset, n)
````

#### Push💪
This opcode pushes the opcode argument that is computed as descripted above onto the stack.

#### Load🦾
Similar to push, but the argument is interpreted as an offset from segment the write and read use. This opcode is used to load the bytes stored by read and push them to the stack.

#### Xor🔀
Pops 2 values and pushes the xor reusult of them:
`push(pop() ^ pop())`

#### Or✅
Pops 2 values and ors them pushes the reuslt:
`push(pop() | pop())`

#### Jump🤔
Pops 2 values and compares them, if they are equal jump to the offset in the emoji code given by the argument.

#### Load32🌠
Same as Load but loads 32 bit instead of 8 from the read/write segment. Used to load some constants for the decrypting alogorithm that are stored in binary at the start of the code.bin file.

#### And1➕
Pops a value, ands it with 1 and pushes it back (turining it to a bool value).

#### Shift➡️
Shifts the last stack value as many bits as spezifed in the argument bitwise to the right.

#### Copy‼️
Pushes the last stack value on the stack again.
`push(peek())`

#### Exit💀
Exit the program.

## Extracting the flag
Now that we know what each opcode does, we can write a python script to turn the emojis to assembly like opcodes. The Python script EmojiDecoder.py takes the code.bin and writes a file like:

````
0000 - PUSH	 0090
002E - PUSH	 0017
005C - WRITE
0062 - PUSH	 00A7
0090 - PUSH	 0014
00BE - WRITE
00C4 - PUSH	 0000
00F2 - PUSH	 001B
0120 - READ
0124 - PUSH	 0000
0152 - PUSH	 00F2
0180 - LD08	 0000	(0000)
01AE - XOR
01B2 - PUSH	 009C
01E0 - XOR
01E4 - OR
01E7 - PUSH	 00EA
0215 - LD08	 0001	(0000)
0243 - XOR
0247 - PUSH	 00D9
0275 - XOR
0279 - OR
````

(500+ lines total)

Now we can analyse this. The fist to wirtes print `Welcome to eVMoji 😎` and `🤝 me the 🏳️`. Then we read 0x1b characters, so we now the flag is 27 letters long.

### First part
After that we have the first part of the encoding. First 0 is pushed then we always follow a patter like:
````
PUSH	 val1
LD08	 offset
XOR
PUSH	 val2
XOR
OR
````
At the end we check if the stack value is zero. To achive this our result has to be zero befor the or, and for this to be the case `val2` has to be the same as the xor result of `val1` and `LD08 offset` where offset is always the next byte from our input. Overall this means the input at offset has to `val1 ^ val2`. This happens 23 times so for the first 23 character in the input. Again we can use a python script that xors these values for us and prints them. If we do that we get `n3w_ag3_v1rtu4liz4t1on_`. But here is a part missing, the 4 character to get 27 total...

### Second part
The last for character are checkt in the scound part of the program. You probably can bruteforce them by throwing all possible inputs against the program, but my aproch was to find the algorithm (wich is quite simple to implement in c) and then write a program that performs it quickly. If you can figure out how to revers it that would be even better, but i didn't and the bruteforce only take a few secounds using that approach.

I will not go in such depht this time but the patter is similar. We have a few instruction that are repeated multiple times and then are jump to check if the end result ist correct. If we extract all constants from the code.bin file (and watch out for endianness wich threw me off first) we find the algorithm can be implemented in c like this:

````
void algorithm(unsigned int input)
{	
	unsigned int prev = 0xffffffff;
	unsigned int temp = 0;

	for(int i = 0; i < 32; i++)
	{
		bool x = ((input >> i) & 1) == (prev & 1);

		prev = prev >> 1;

		if(!x)
		{
			prev = prev ^ 0xedb88320;
		}
	}

	if(prev == 0xf40e845e)
	{
		printf("result: %x\n", input);
	}
}
````

The function takes an int wich is made up of the last 4 bytes of the flag and prints if it is a possible solution for the password check. We build and int from all combination of all charakter that could be in the flag and call the function. If we compile bruteforce.c with gcc and the -O3 option for execution speed and run the binary we get the reuslt `3f6c306c` almost instantly. If we convert it back to ASCII and append it to the knowen part of the flag we get `n3w_ag3_v1rtu4liz4t1on_l0l?`.

## Result
If we run the program with the password we get:
````
timo@ubuntu:~/CSCG/eVMoji$ ./eVMoji code.bin 
Welcome to eVMoji 😎
🤝 me the 🏳️
n3w_ag3_v1rtu4liz4t1on_l0l?
Thats the flag: CSCG{n3w_ag3_v1rtu4liz4t1on_l0l?}
````
Thats it, submit it and get the points. 😎😎😎
