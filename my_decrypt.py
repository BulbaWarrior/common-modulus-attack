import rsa
import sys
from base64 import b64decode
from mod_ops.exponentiation import exp_mod
from gmpy2 import invert

class extended_euclidean:
    def __init__(self, n1, n2):

        
        self.r0 = max((n1, n2))
        self.r1 = min((n1, n2))
        self.swapped = (self.r0 != n1)
        self.s0 = 1
        self.s1 = 0
        self.t0 = 0
        self.t1 = 1

        self.fit()

    def fit(self):
        while self.r1 != 0:
            q = self.r0 // self.r1
            r2 = self.r0 - (q * self.r1) 
            s2 = self.s0 - (q * self.s1)
            t2 = self.t0 - (q * self.t1)

            self.r0 = self.r1
            self.r1 = r2

            self.s0 = self.s1
            self.s1 = s2
            
            self.t0 = self.t1
            self.t1 = t2

    def get_coeff(self):
        if self.swapped:
            return (self.t0, self.s0)
        else:
            return (self.s0, self.t0)
        


class RSAModule:
    def __init__(self, e1, e2, N):
        self.e1 = e1
        self.e2 = e2
        self.N = N
        ecl = extended_euclidean(e1, e2)
        if ecl.r0 != 1:
            print("warning! exponents are not coprime")
        self.a, self.b = ecl.get_coeff()

        

    def decrypt(self, c1, c2):
        if self.a < 0:
            c1 = int(invert(c1, self.N))
            a = -self.a
            b = self.b
        else:
            c2 = int(invert(c2, self.N))
            a = self.a
            b = -self.b
            
        c1 = exp_mod(c1, a, self.N)
        c2 = exp_mod(c2, b, self.N)

        return c1*c2 % self.N

key1_name = 'pubkey1.pem'
key2_name = 'pubkey2.pem'

message1_name = 'message1'
message2_name = 'message2'

with open(key1_name, 'rb') as key1_f:
    key1 = rsa.PublicKey.load_pkcs1(key1_f.read())

with open(key2_name, 'rb') as key2_f:
    key2 = rsa.PublicKey.load_pkcs1(key2_f.read())

if key1.n != key2.n:
    print('different modulus of public keys')
    exit(1)

rsa = RSAModule(key1.e, key2.e, key1.n)

with open(message1_name) as f:
    ciphertext1 = b64decode(f.read())

with open(message2_name) as f:
    ciphertext2 = b64decode(f.read())

c1 = int.from_bytes(ciphertext1, 'big')
c2 = int.from_bytes(ciphertext2, 'big')

m = rsa.decrypt(c1, c2)
plaintext = m.to_bytes(1024//8, 'big')
print(plaintext.decode())

