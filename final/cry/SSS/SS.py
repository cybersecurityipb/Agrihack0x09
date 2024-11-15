from Crypto.Util.number import bytes_to_long as b2l

def grey(x, version=2):
    if version == 2:
        return x ^ (x // 2) ^ (x // 4)
    return (2 * x) ^ x ^ (x // 2) ^ (x // 4)

with open('secret.txt', 'rb') as f:
    flag = f.read()
    
n1, n2 = b2l(flag[:len(flag)//2]), b2l(flag[len(flag)//2:])
for _ in range(1000): n1 = grey(n1)
for _ in range(1000): n2 = grey(n2, version=3)

with open('file.txt', 'w') as f:
    f.write(f'ct={n1}{n2}')