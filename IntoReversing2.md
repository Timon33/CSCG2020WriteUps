# Reversing 2
## General information
After unzipping the provided files, we get a binary and a dummy flag file. To get more information about the binary we can run the file commandline tool.

```
timo@ubuntu:~/CSCG/intro_rev2$ file rev2
rev2: ELF 64-bit LSB shared object, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 3.2.0, BuildID[sha1]=6f10fffe1293cf3b8e79f2d2b7b27fa4cfd9b1b9, not stripped
```

This tells us that rev2 is ELF 64-bit executable. The binary is also not stripped, this makes debugging it a lot easier.

## Reversing with Ghidra
Ghidra is a free decompiler, which we can use to take a closer look a the executable. We analyze the file with all the default settings and open the main function.
After renaming some of the variables we get the following decompilation:

```
int main(void)

{
  int compareResult;
  ssize_t lenReadBytes;
  long in_FS_OFFSET;
  int counter;
  char readBuf [40];
  long stack_canary;
  
  stack_canary = *(long *)(in_FS_OFFSET + 0x28);
  initialize_flag();
  puts("Give me your password: ");
  lenReadBytes = read(0,readBuf,0x1f);
  readBuf[(int)lenReadBytes + -1] = '\0';
  counter = 0;
  while (counter < (int)lenReadBytes + -1) {
    readBuf[counter] = readBuf[counter] + -0x77;
    counter = counter + 1;
  }
  compareResult = strcmp(readBuf,&encodedPassword);
  if (compareResult == 0) {
    puts("Thats the right password!");
    printf("Flag: %s",flagBuffer);
  }
  else {
    puts("Thats not the password!");
  }
  if (stack_canary != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return 0;
}
```
This setup is very similar to reversing 1, however instead of a constant string the password is encoded in a while loop
and the compared to some constant bytes. If we display the bytes in ghidra after changing the data to be displayed as a array we can
see the following output:

```
           00100ab0 [0]            FCh, FDh, EAh, C0h
           00100ab4 [4]            BAh, ECh, E8h, FDh
           00100ab8 [8]            FBh, BDh, F7h, BEh
           00100abc [12]           EFh, B9h, FBh, F6h
           00100ac0 [16]           BDh, C0h, BAh, B9h
           00100ac4 [20]           F7h, E8h, F2h, FDh
           00100ac8 [24]           E8h, F2h, FCh, 00h

```

If we look back at the decompliation of main we can see that here

```
readBuf[counter] = readBuf[counter] + -0x77;
```

0x77 is subtracted from evey byte in the password. If we want to find the password we have to add 0x77 to every byte in the array
accounting for potantial buffer overflows.

## Decoding the password
We can use a very simple python script to decode the password and print it. We store the encoded bytes in an array and add 0x77 to every
number in it. Then we and it with 0xff so it say in the range of a byte. We can print the result as a bytearray and get `sta71c_tr4n5f0rm4710n_it_isw`
(You can find the full script at additional files). 

We connect to the server and sumit the password with `nc hax1.allesctf.net 9601`. The Server gives us the flag `CSCG{1s_th4t_wh4t_they_c4ll_on3way_transf0rmati0n?}`.

## Preventing the attack
On way to make this application more secure, is to not store the password in plain text, but as a hash. Then the user supplied password is hashed using the same algorithm and they both are compared.
Also the attacker shouldn't have a way to extract the hash from the server. In theory this would make a password check secure, as long the password is not easy to brute force.
