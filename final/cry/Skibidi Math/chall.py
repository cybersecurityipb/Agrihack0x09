from fractions import Fraction
from Crypto.Util.number import getPrime, bytes_to_long
from secret import X, Y, s

with open('flag.txt', 'r') as flag:
    flag  = flag.read()
m = bytes_to_long(flag.encode())
p, q = getPrime(512), getPrime(512)
while(p > q):
    p, q = q, p
n, p_q = p*q, p-q

c = pow(m, 0x20002, n)
assert p_q.bit_length() > 500
assert Fraction(1, p+1) - Fraction(1, q) == Fraction(X + Y, s + Y)

with open('enc.txt', 'w') as enc:
    enc.write(f'n = {n}\n')
    enc.write(f'X = {X}\n')
    enc.write(f'Y = {Y}\n')
    enc.write(f'c = {c}\n')