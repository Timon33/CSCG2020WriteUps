from Crypto.Util.number import long_to_bytes

n = "51CFF46D9EE32096D6C806CBC7DF2D1D3BEA7E7B2FC4E826D9FC5E18799912DCA150B29C65C0F9E66453396CE7DE631A0F9A6745138B6125BBCD185AA12EB09A4A1BD806118C97A8DE05ED0BE6B45FC1C9E9937192F58BC4A5CC2767803C0B21342AF5CB8F34AFFB1A6EC2520C765D87521C6848DBD831812ECC6D8BB3D61733B0EBC352CF64D4445C995572922F493D7189959DB2321E1BAC5925FA56DC69F6858EFEEBA0A5A9D76BA198187153927424E5F7B68098AB8C10442B73D149027CFC37D030056337C3E0F4216CF43223967441B608EEC2A648E8CE857894C665030C01245629279B387FCDBDC35B6167715B54BD5556180D9AF2504B527A90FAE7"

m =4522827319495133992180681297469132393090864882907734433792485591515487678316653190385712678072377419115291918844825910187405830252000250630794128768175509500175722681252259065645121664124102118609133000959307902964132117526575091336372330412274759536808500083138400040526445476933659309071594237016007983559466411644234655789758508607982884717875864305554594254277210539612940978371460389860098821834289907662354612012313188685915852705277220725621370680631005616548237038578956187747135229995137050892471079696577563496115023198511735672164367020373784482829942657366126399823845155446354953052034645278225359074399

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m

e = 65537
N = int(n, 16)
MAX = 10**7

print("N is: " + str(N))

'''
n = n.split(":")
n.reverse()

for i,b in enumerate(n):
    N += int(b, 16) * (0x100 ** i)
'''

for i in range(2, MAX):
    if N % i == 0:
        print("p is:" + str(i))
        p = i
        break;


q = N // p
print("q is: " + str(q))

pi = (p - 1)*(q - 1)
print("pi is: " + str(pi))
print("e is: " + str(e))

d = modinv(e, pi)

print("d is: " + str(d))

decrypt = pow(m, d, N)

print(long_to_bytes(decrypt))
