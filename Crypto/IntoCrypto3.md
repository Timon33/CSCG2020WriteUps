# Crypto 3
## Setup
This time we get get a intercepted-messages.txt containing 3 encrypted messages for the US, RUS and GER goverment. We also get
3 public PEM keys, one for each goverment.

## The Attack
A idea would be to compute the gcd of the diffrent moduli and if they are greater then one we know a prime factor, but sadly the all have
no gcd > 1.

However if we use openssl to look at the numbers of the public keys we will notice they all use the public exponent e = 3. We also know that
they probaly all contain the same plain text message. This allows attack as descript (here)[https://www.johndcook.com/blog/2019/03/06/rsa-exponent-3/].

If we solve the system
````
x = c1 mod N1
x = c2 mod N2
x = c3 mod N3
````
using the given messages as cs and the moduli as Ns, we can solve for x. The cuberoot of x is then the decrypted message.

If we implement the math in python using the Chinese Remainder Theorem function from the sympy module, we get the string `'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACSCG{ch1nes3_g0vernm3nt_h4s_n0_pr0blem_w1th_c0ron4}`
as the decrypted message.
