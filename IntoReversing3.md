# Reversing 3
## General information
After unzipping the provided files, we get a binary and a dummy flag file. To get more information about the binary we can run the file commandline tool.

```
timo@ubuntu:~/CSCG/intro_rev3$ file rev3
rev3: ELF 64-bit LSB shared object, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 3.2.0, BuildID[sha1]=7fc813b97129ba8e754158292465a8e3dca5b05e, not stripped
```

This tells us that rev3 is ELF 64-bit executable. The binary is also not stripped, this makes debugging it a lot easier.

## Reversing with Ghidra
Ghidra is a free decompiler, which we can use to take a closer look a the executable. We analyze the file with all the default settings and open the main function.
After renaming some of the variables we get the following decompilation:

```
int main(void)

{
  int cmpResult;
  ssize_t lenReadBytes;
  long in_FS_OFFSET;
  int counter;
  byte readBuf [40];
  long stack_canary;
  
  stack_canary = *(long *)(in_FS_OFFSET + 0x28);
  initialize_flag();
  puts("Give me your password: ");
  lenReadBytes = read(0,readBuf,0x1f);
  readBuf[(int)lenReadBytes + -1] = 0;
  counter = 0;
  while (counter < (int)lenReadBytes + -1) {
    readBuf[counter] = readBuf[counter] ^ (char)counter + 10U;
    readBuf[counter] = readBuf[counter] - 2;
    counter = counter + 1;
  }
  cmpResult = strcmp((char *)readBuf,"lp`7a<qLw\x1ekHopt(f-f*,o}V\x0f\x15J");
  if (cmpResult == 0) {
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

Like in reversing 2 we have a loop going over the bytes in the password, but now we xor it with the position if the byte + 10. After this process
our password has to be ```` lp`7a<qLw\x1ekHopt(f-f*,o}V\x0f\x15J ```` (notice the `\x` encoded bytes here).

## Decoding the password
To reverse this algorithm we first have to add 2 back to every byte and the xor it with the position + 10. We use a python script to easily do
that, wich you can find in the additional files. As a password we get `dyn4m1c_k3y_gen3r4t10n_y34h`.

We connect to the server and sumit the password with `nc hax1.allesctf.net 9602`. The Server gives us the flag `CSCG{pass_1_g3ts_a_x0r_p4ss_2_g3ts_a_x0r_EVERYBODY_GETS_A_X0R}`.

## Preventing the attack
On way to make this application more secure, is to not store the password in plain text, but as a hash. Then the user supplied password is hashed using the same algorithm and they both are compared.
Also the attacker shouldn't have a way to extract the hash from the server. In theory this would make a password check secure, as long the password is not easy to brute force.
