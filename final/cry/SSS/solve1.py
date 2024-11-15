import ast, hashlib

with open('enc.txt', 'r') as f:
    encrypted_message = ast.literal_eval(f.read())

methods = ['md5', 'sha256', 'sha3_256', 'sha3_512', 'sha3_384', 'sha1', 'sha384', 'sha3_224', 'sha512', 'sha224']

def encrypt(x, method): return hashlib.new(method, x.encode()).hexdigest()

sha512_ = [hashlib.sha512(str(i).encode()).hexdigest() for i in range(130)]
final_encrypted = [encrypt(sha512_[i % 130], methods[i // 130]) for i in range(1300)]
hashed_dict = dict(zip(final_encrypted, range(1300)))
message_ = [chr(i - 20) if i - 20 > 0 else chr(110 + i) for i in [hashed_dict[i] % 130 for i in encrypted_message]]

with open("nomor2", "w") as f:
    f.write("".join(message_))
