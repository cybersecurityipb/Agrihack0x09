from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad


enc = bytes.fromhex('1531775fe7f14327b81e12b4e7209c9747eec1f0fac37efb99f5bd30a8ace5095a1697ec618a083f66098ddb8cdab69e8d39f4d6c56b214618041ea9b6e08a31472e4cfd52b1c8aa6c5114f5944b5201')
key = b'kuncirahasiadansangatpenting4321'

def decrypt(msg, key):
	cipher = AES.new(key, AES.MODE_ECB)
	plaintext = cipher.decrypt(msg)
	plaintext = unpad(plaintext, 16)
	return plaintext

print("Flag:", decrypt(enc, key))