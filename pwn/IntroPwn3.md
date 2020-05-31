# Intro Pwn 3
## General information
This challange is again very similar to Pwn 2. The diffrence there is now there is now more WIN function. Well it is still in the source
code but it does not call `/bin/sh` anymore so it is usless. Instead we have to call a function like system with `/bin/sh`

## The Exploit
After sending the previous password we change the buffer overflow to instead of sending the address of the WIN function, send the
address of the system function together with a poniter to the `/bin/sh` string.

Running the IntroPwn3.py script with python 2 drops you into a shell on the server from wich you can cat the flag `CSCG{VOLDEMORT_DID_NOTHING_WRONG}`.
