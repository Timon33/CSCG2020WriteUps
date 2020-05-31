# Crypto 1
## Setup
The challange provides us with 2 files, message.txt and pubkey.pem. The message file is a large number with is the cypher text that we have
to decrypt using RSA.

We know we are delaying with RSA because the pubkey file is a public RSA key in PEM format. It looks like this:
````
-----BEGIN PUBLIC KEY-----
MIIBITANBgkqhkiG9w0BAQEFAAOCAQ4AMIIBCQKCAQBRz/RtnuMgltbIBsvH3y0d
O+p+ey/E6CbZ/F4YeZkS3KFQspxlwPnmZFM5bOfeYxoPmmdFE4thJbvNGFqhLrCa
ShvYBhGMl6jeBe0L5rRfwcnpk3GS9YvEpcwnZ4A8CyE0KvXLjzSv+xpuwlIMdl2H
UhxoSNvYMYEuzG2Ls9YXM7Drw1LPZNREXJlVcpIvST1xiZWdsjIeG6xZJfpW3Gn2
hY7+66ClqddroZgYcVOSdCTl97aAmKuMEEQrc9FJAnz8N9AwBWM3w+D0IWz0MiOW
dEG2CO7CpkjozoV4lMZlAwwBJFYpJ5s4f829w1thZ3FbVL1VVhgNmvJQS1J6kPrn
AgMBAAE=
-----END PUBLIC KEY-----
````

## Basic RSA
RSA is a asymmetric encryption system that uses public and private keys. The public one is used to encrypt messages and the private to decrypt
them. Normaly it is impossible to get the private key from the public one. This relies on the fact, that it is easy to multiply tow numbers, but hard to factor
a large number to get the tow original values back. RSA is more complicated then that, but if we can factor the number N wich is part of the public key
we can calculate the private key and decrypt the message.

## The Attack
We can use openssl to see the numbers of the public key using the following command:
````
timo@ubuntu:~/CSCG/Crypto/crypt1$ openssl rsa -pubin -in pubkey.pem -text -noout
RSA Public-Key: (2047 bit)
Modulus:
    51:cf:f4:6d:9e:e3:20:96:d6:c8:06:cb:c7:df:2d:
    1d:3b:ea:7e:7b:2f:c4:e8:26:d9:fc:5e:18:79:99:
    12:dc:a1:50:b2:9c:65:c0:f9:e6:64:53:39:6c:e7:
    de:63:1a:0f:9a:67:45:13:8b:61:25:bb:cd:18:5a:
    a1:2e:b0:9a:4a:1b:d8:06:11:8c:97:a8:de:05:ed:
    0b:e6:b4:5f:c1:c9:e9:93:71:92:f5:8b:c4:a5:cc:
    27:67:80:3c:0b:21:34:2a:f5:cb:8f:34:af:fb:1a:
    6e:c2:52:0c:76:5d:87:52:1c:68:48:db:d8:31:81:
    2e:cc:6d:8b:b3:d6:17:33:b0:eb:c3:52:cf:64:d4:
    44:5c:99:55:72:92:2f:49:3d:71:89:95:9d:b2:32:
    1e:1b:ac:59:25:fa:56:dc:69:f6:85:8e:fe:eb:a0:
    a5:a9:d7:6b:a1:98:18:71:53:92:74:24:e5:f7:b6:
    80:98:ab:8c:10:44:2b:73:d1:49:02:7c:fc:37:d0:
    30:05:63:37:c3:e0:f4:21:6c:f4:32:23:96:74:41:
    b6:08:ee:c2:a6:48:e8:ce:85:78:94:c6:65:03:0c:
    01:24:56:29:27:9b:38:7f:cd:bd:c3:5b:61:67:71:
    5b:54:bd:55:56:18:0d:9a:f2:50:4b:52:7a:90:fa:
    e7
Exponent: 65537 (0x10001)
````
We see a large Modulus N and a save Exponent e. So you might think this key is save, but even if the Modulus is large one of the prime factors
might still be small. To test this we can use python and try to divide the modulus by each integer starting at one. If we can divide N by a number
p we have the first factor. To get the secound we take the result of that division and call it q. Using these values we can compute the private exponent
d and decrypt the message. To get the large number that is the reuslt of the decryption into a readable format we use the `long_to_bytes` function from the
`Crypto.Util.number` module.

Running the python script found in additional files we quicky find the small factor `p = 622751` and get the flag `CSCG{factorizing_the_key=pr0f1t}` after decrypting the message.
