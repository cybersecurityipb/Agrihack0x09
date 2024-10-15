from Crypto.Cipher import AES
from Crypto.Util.Padding import pad


flag = b'[REDACTED]'
key = b'kuncirahasiadansangatpenting4321'

def encrypt(msg, key):
	cipher = AES.new(key, AES.MODE_ECB)
	ciphertext = cipher.encrypt(pad(msg, 16))
	return ciphertext.hex()

print("ciphertext =", encrypt(flag, key))

'ciphertext = 1531775fe7f14327b81e12b4e7209c9747eec1f0fac37efb99f5bd30a8ace5095a1697ec618a083f66098ddb8cdab69e8d39f4d6c56b214618041ea9b6e08a31472e4cfd52b1c8aa6c5114f5944b5201'