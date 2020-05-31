# revers algorithm
def decrypt(cyper):
    res = []
    for i, e in enumerate(cyper):
        res.append(((e + 2) ^ (i + 0xa)))

    return res

# encrypted string in the binary
cyper = b"lp`7a<qLw\x1ekHopt(f-f*,o}V\x0f\x15J"

psswd = decrypt(cyper)

print(bytearray(psswd).decode())
