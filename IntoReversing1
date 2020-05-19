# Reversing 1
## General information
After unzipping the provided files, we get a binary and a dummy flag file. To get more information about the binary we can run the file commandline tool.

```
root@5e8781bc73e4:/pwd/intro_rev1# file rev1
rev1: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 3.2.0, 
BuildID[sha1]=c26549fbcc84a4199635818d97bd48b69eea5fb2, not stripped
```

This tells us that rev1 is ELF 64-bit executable. The binary is also not stripped, this makes debugging it a lot easier.

## Reversing with Ghidra
Ghidra is a free decompiler, which we can use to take a closer look a the executable. We analyze the file with all the default settings and open the main function.
After renaming some of the variables we get the following decompilation:

```
int main(void)

{
  int compare_result;
  ssize_t password_len;
  long in_FS_OFFSET;
  char password_buffer [40];
  long stack_canary;
  
  stack_canary = *(long *)(in_FS_OFFSET + 0x28);
  initialize_flag();
  puts("Give me your password: ");
  password_len = read(0,password_buffer,0x1f);
  password_buffer[(int)password_len + -1] = '\0';
  compare_result = strcmp(password_buffer,"y0u_5h3ll_p455");
  if (compare_result == 0) {
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
We need the `strcmp` to return 0, in order to print the flag. `strcmp` returns 0 if both strings are identical, so the `password_buffer` also needs to be `"y0u_5h3ll_p455"`. This is your password.

## Getting the flag 
To get the flag from the server we connect to the given address and port using netcat and enter the password after we are prompted to do so.

```
root@5e8781bc73e4:/pwd/intro_rev1# nc hax1.allesctf.net 9600
Give me your password: 
y0u_5h3ll_p455
Thats the right password!
Flag: CSCG{ez_pz_reversing_squ33zy}root@5e8781bc73e4:/pwd/intro_rev1# 
```
We get the flag  `CSCG{ez_pz_reversing_squ33zy}` and submit it.

## Preventing the attack
On way to make this application more secure, is to not store the password in plain text, but as a hash. Then the user supplied password is hashed using the same algorithm and they both are compared.
Also the attacker shouldn't have a way to extract the hash from the server. In theory this would make a password check secure, as long the password is not easy to brute force.
