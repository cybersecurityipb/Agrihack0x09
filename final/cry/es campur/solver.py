import re
from pwn import *
import libnum
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import binascii

host = '34.50.87.57'
port = 9002

# Mencoba membuka koneksi
io = remote(host, port)
print("Koneksi berhasil ke server.")

# Mengirim pilihan menu dan menerima respons awal
io.recvuntil(b'Pilih menu (1-6): ')
io.sendline(b'5')

# Menerima data awal sampai semua elemen diterima
response = io.recvuntil(b'Selesai').decode().strip()
list_res = response.split()
list_res.pop()

# Membagi list ke dalam beberapa bagian sesuai kebutuhan
c_list = list_res[:100]
n_list = list_res[100:200]
xor1_list = list_res[200:300]
xor2_list = list_res[300:400]
enc_list = list_res[400:500]
key_list = list_res[500:550]
iv_list = list_res[550:]

io.sendline(b'<')
io.recvuntil(b'Pilih menu (1-6): ')
io.sendline(b'4')
io.recvline()

c_real = []
n_real = []
for c in c_list:
    for n in n_list:
        io.sendline(f"{c} {n}".encode())
        jawab = io.recv(timeout=3).decode()
        if "Benar" in jawab:
            match = re.search(r"Benar\((\d+)\)", jawab)
            if match:
                i = int(match.group(1))
                while len(c_real) <= i:
                    c_real.append(None)
                    n_real.append(None)
                c_real[i] = int(c)
                n_real[i] = int(n)
            else:
                pass
        else:
            pass


io.sendline(b'<')
io.recvuntil(b'Pilih menu (1-6): ')
io.sendline(b'3')
io.recvline()

for idx, (c, n) in enumerate(zip(c_real, n_real)):
    ct = int(c) * pow(2, 65537, int(n))
    pesan = f"{idx} {ct}"
    io.sendline(pesan.encode())

full_response = b''
while True:
    try:
        part = io.recv(timeout=1)
        if not part:
            break
        full_response += part
    except EOFError:
        break

response_lines = full_response.decode().splitlines()


m_real = []
for idx, (line, modulus) in enumerate(zip(response_lines, n_list)):
    if "Pesan didekripsi:" in line:
        respons = line.replace("Pesan didekripsi: ", "").strip()
        ct_div = int(respons) * libnum.invmod(2, int(modulus)) % int(modulus)
        str_div = str(ct_div)
        m = str_div[10:] 
        m_real.append(int(m))

io.sendline(b'<')
io.recvuntil(b'Pilih menu (1-6): ')
io.sendline(b'2')
io.recvline()

xor1_real = []
xor2_real = []
for xor1 in xor1_list:
    for xor2 in xor2_list:
        io.sendline(f"{xor1} {xor2}".encode())
        jawab = io.recv(timeout=3).decode()
        if "Benar" in jawab:
            match = re.search(r"Benar\((\d+)\)", jawab)
            if match:
                i = int(match.group(1))
                while len(xor1_real) <= i:
                    xor1_real.append(None)
                    xor2_real.append(None)
                xor1_real[i] = int(xor1)
                xor2_real[i] = int(xor2)
            else:
                pass
        else:
            pass


key_real = []
iv_real = []
for m, sor1, sor2 in zip(m_real, xor1_real, xor2_real):
    s1 = int(m) ^ sor2
    s2 = int(m) ^ sor1
    k1 = f"{s1:x}"
    k2 = f"{s2:x}"

    key = k1  
    iv = k2  

    if len(k1) % 2 != 0:
        key = '0' + k1  
    if len(k2) % 2 != 0:
        iv = '0' + k2  

    key_real.append(key)
    iv_real.append(iv)

io.sendline(b'<')
io.recvuntil(b'Pilih menu (1-6): ')
io.sendline(b'1')
io.recvline()


enc_real = []
for enc in enc_list:
    for key, iv in zip(key_real, iv_real):
        io.sendline(f"{enc} {key} {iv}".encode())
        balas = io.recv(timeout=3).decode()
        if "Benar" in balas:
            pasangan = re.search(r"Benar\((\d+)\)", balas)
            if pasangan:
                j = int(pasangan.group(1))
                while len(enc_real) <= j:
                    enc_real.append(None)
                enc_real[j] = enc
            else:
                pass
        else:
            pass


flag_list = []
for enc, key, iv in zip(enc_real, key_real, iv_real):
    if enc is None or key is None or iv is None:
        continue
    a = binascii.unhexlify(enc)
    b = binascii.unhexlify(key)
    c = binascii.unhexlify(iv)
    
    cipher = AES.new(b, AES.MODE_CBC, c)
    plaintext = cipher.decrypt(a)
    plaintext = unpad(plaintext, AES.block_size)
    message = plaintext.decode('utf-8')
    flag_list.append(message)

flag = ''.join(flag_list)
print(flag)

io.close()
