# Cyrpto 2
## Setup
This challage is very similar to Intro to Crypto 1. Again we get a public key in PEM format and a encrypted message.

## The Attack
If we look at the number of the public key we get:
````
timo@ubuntu:~/CSCG/Crypto/crypt2$ openssl rsa -pubin -in pubkey.pem -text -noout
RSA Public-Key: (2047 bit)
Modulus:
    57:c8:8f:1c:9b:9e:d4:7d:84:4f:87:b2:9f:44:79:
    6e:17:ce:47:c2:fe:24:cc:1a:b7:e3:44:32:b3:35:
    21:24:63:d2:39:9d:07:47:11:80:05:72:ea:68:12:
    e2:90:12:02:bc:5f:19:0c:cb:49:66:d5:70:90:4a:
    41:69:7a:63:64:48:8a:e1:40:b1:b6:35:7f:c6:a6:
    b4:ac:cd:51:7a:74:03:bb:c9:96:df:d0:72:89:5f:
    6a:9a:1e:a8:f2:a6:da:b6:9d:a1:55:75:17:7f:4c:
    ef:1a:db:90:82:5b:bd:4f:ec:50:01:aa:c0:1a:70:
    e8:a1:0e:10:13:34:71:39:32:be:47:d1:a0:9d:70:
    d3:11:57:fe:26:e5:53:77:4f:8d:9e:50:20:98:47:
    2b:ca:87:07:93:1e:2b:c9:cb:92:aa:c9:44:51:be:
    6f:1e:55:8b:93:a8:68:5c:e9:84:f4:84:0a:fa:f8:
    d2:a8:ad:0d:46:54:54:62:a9:18:15:1a:50:de:a1:
    a2:8f:4d:f1:e5:e6:99:b0:05:2d:a5:23:05:9e:b2:
    1d:56:b6:7c:91:e5:6a:b7:5f:35:bc:9f:64:9b:ea:
    76:a1:36:b1:70:d3:a6:76:f5:14:b9:c8:95:5e:af:
    78:a9:0b:ad:d5:48:5b:ba:7f:12:17:8b:1f:8f:ef:
    ef
Exponent: 65537 (0x10001)
````
They look similar to crypto 1, but if we try to bruteforce a factor of the Modulo N we don't find a small result and the script takes a lot of time.
So is the Modulus used secure? Obviously not but this time we need to use a bit more complicated approtch to find the factors quickly.

If we search for attacks on RSA we can learn about the `Fermat factoring algorithm`. It can quickly factor a product of 2 primes, even if they
are large, as long as they are about the same size.

You can find a detalied explonation of the methode (here)[https://www.nku.edu/~christensen/Mathematical%20attack%20on%20RSA.pdf] under `Fermat factoring algorithm`.
It used the property that you can write the difference of 2 squares as 2 factors.

````
x^2 - y^2 = (x - y) * (x + y)
````
So if we can express N as the diffrence of 2 squares we can find the prime factors. We use python to test values for y^2 until y is a an integer.
Then we can calculate q and p and thereby d. If we decrypt the message and turn it into text we get `CSCG{Ok,_next_time_I_choose_p_and_q_random...}`.
