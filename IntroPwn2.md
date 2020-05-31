# Intro Pwn 2
## General information
This challage is the same as challange 1 with the twist that the stack canary is enabled. We also have to send the first flag to the server
befor we can start the exploit. 

## The Exploit
We can use almost the same script as in Pwn 1. We cange it to send the password befor the format string and the overflow and we also
get the cannary and the old value of rbp from the stack so we can can use it in our overflow to not overwrite the old values.

The script gives us a shell on the server and we cat the flag `CSCG{NOW_GET_VOLDEMORT}`.
