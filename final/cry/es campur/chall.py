from Crypto.Cipher import AES
from Crypto.Util.number import *
from Crypto.Util.Padding import pad
from Crypto.Random import *
from math import gcd
from Crypto.Random import get_random_bytes
import random
import string

with open('flag.txt', 'r') as file:
    flag = file.read().strip()
arr = list(flag)

class Encrypt:
    def __init__(self, arr):
        self.arr = arr

    def aes_real(self):
        enc_real = []
        key_real = []
        iv_real = []
        for letter in self.arr:
            key = get_random_bytes(16)
            iv = get_random_bytes(16)
            cipher = AES.new(key, AES.MODE_CBC, iv)
            letter_bytes = letter.encode()
            padded_letter = pad(letter_bytes, AES.block_size)
            ct = cipher.encrypt(padded_letter).hex()
            key_hex = key.hex()
            iv_hex = iv.hex()
            enc_real.append(ct)
            key_real.append(key_hex)
            iv_real.append(iv_hex)
        return enc_real, key_real, iv_real

    def aes_fake(self):
        enc_fake = []
        key_fake = []
        iv_fake = []
        for _ in range(len(self.arr)):
            key = get_random_bytes(16)
            iv = get_random_bytes(16)
            cipher = AES.new(key, AES.MODE_CBC, iv)
            letter_bytes = random.choice(string.punctuation.replace('{', '').replace('}', '')).encode()
            padded_letter = pad(letter_bytes, AES.block_size)
            ct = cipher.encrypt(padded_letter).hex()
            key_hex = key.hex()
            iv_hex = iv.hex()
            enc_fake.append(ct)
            key_fake.append(key_hex)
            iv_fake.append(iv_hex)
        return enc_fake, key_fake, iv_fake

    def xor_real(self, list_a, list_b):
        xor1_real = []
        xor2_real = []
        xor3_real = []
        list_num = [getRandomNBitInteger(512) for _ in range(100 - len(list_a))]
        for a, b, num in zip(list_a, list_b, list_num):
            xor1 = int(a, 16) ^ num
            xor2 = int(b, 16) ^ num
            xor3 = xor1 ^ xor2 ^ num
            xor1_real.append(xor1)
            xor2_real.append(xor2)
            xor3_real.append(xor3)
        return xor1_real, xor2_real, xor3_real

    def xor_fake(self, list_a):
        xor1_fake = []
        xor2_fake = []
        num_campur = [getRandomNBitInteger(512) for _ in range(100 - len(list_a))]
        for num in num_campur:
            xor1 = getRandomInteger(512) ^ getRandomInteger(512) ^ num
            xor2 = getRandomInteger(512) ^ getRandomInteger(512) ^ num
            xor1_fake.append(xor1)
            xor2_fake.append(xor2)
        return xor1_fake, xor2_fake

    def rsa_real(self, list_a):
        c_real = []
        n_real = []
        d_real = []
        e = 2 ** 16 + 1
        for value in list_a:
            while True:
                p = getPrime(512)
                q = getPrime(512)
                n = p * q
                phi = (p - 1) * (q - 1)
                if gcd(e, phi) == 1:
                    break
            d = pow(e, -1, phi)
            m = int(str(getRandomNBitInteger(32)) + str(value))
            c = pow(m, e, n)
            c_real.append(c)
            n_real.append(n)
            d_real.append(d)
        return c_real, n_real, d_real

    def rsa_fake(self, list_a):
        c_fake = []
        n_fake = []
        e = 2 ** 16 + 1
        for value in list_a:
            while True:
                p = getPrime(512)
                q = getPrime(512)
                n = p * q
                phi = (p - 1) * (q - 1)
                if gcd(e, phi) == 1:
                    break
            m = int(str(getRandomNBitInteger(32)) + str(value))
            c = pow(m, e, n)
            c_fake.append(c)
            n_fake.append(n)
        return c_fake, n_fake

    def campur(self, enc_real, key_real, iv_real, enc_fake, key_fake, iv_fake, xor1_real, xor2_real ,xor1_campur, xor2_campur, c_real, n_real ,c_fake, n_fake):
        enc_mix = enc_fake + enc_real
        key_mix = key_fake + key_real
        iv_mix = iv_fake + iv_real
        xor1_mix = xor1_campur + xor1_real
        xor2_mix = xor2_campur + xor2_real
        c_mix = c_fake + c_real
        n_mix = n_fake + n_real
        random.shuffle(enc_mix)
        random.shuffle(key_mix)
        random.shuffle(iv_mix)
        random.shuffle(xor1_mix)
        random.shuffle(xor2_mix)
        random.shuffle(c_mix)
        random.shuffle(n_mix)
        return enc_mix, key_mix, iv_mix, xor1_mix, xor2_mix, c_mix, n_mix

    def process(self):
        enc_real, key_real, iv_real = self.aes_real()
        enc_fake, key_fake, iv_fake = self.aes_fake()
        xor1_real, xor2_real, xor3_real = self.xor_real(key_real, iv_real)
        xor1_fake, xor2_fake = self.xor_fake(key_fake)
        c_real, n_real, d_real = self.rsa_real(xor3_real)
        c_fake, n_fake = self.rsa_fake(xor1_fake)
        enc_mix, key_mix, iv_mix, xor1_mix, xor2_mix, c_mix, n_mix = self.campur(enc_real, key_real, iv_real, enc_fake, key_fake, iv_fake, xor1_real, xor2_real, xor1_fake, xor2_fake, c_real, n_real, c_fake, n_fake)
        return enc_mix, key_mix, iv_mix, xor1_mix, xor2_mix, c_mix, n_mix, enc_real, key_real, iv_real, xor1_real, xor2_real, xor3_real, c_real, n_real, d_real

encrypted = Encrypt(arr)
enc_mix, key_mix, iv_mix, xor1_mix, xor2_mix, c_mix, n_mix, enc_real, key_real, iv_real, xor1_real, xor2_real , xor3_real, c_real, n_real, d_real = encrypted.process()

class Check:
    def __init__(self, enc_mix, key_mix, iv_mix, xor1_mix, xor2_mix, c_mix, n_mix, enc_real, key_real, iv_real, xor1_real, xor2_real, xor3_real, c_real, n_real, d_real):
        self.enc_real = enc_real
        self.key_real = key_real
        self.iv_real = iv_real
        self.xor1_real = xor1_real
        self.xor2_real = xor2_real
        self.xor3_real = xor3_real
        self.c_real = c_real
        self.n_real = n_real
        self.d_real = d_real
        self.enc_mix = enc_mix
        self.key_mix = key_mix
        self.iv_mix = iv_mix
        self.xor1_mix = xor1_mix
        self.xor2_mix = xor2_mix
        self.c_mix = c_mix
        self.n_mix = n_mix

    def check_aes(self):
        print("Masukkan enc, key, dan iv (enc<spasi>key<spasi>iv):")
        while True:
            user_input = input("").split()
            if len(user_input) == 1 and user_input[0] == "<":
                break
            elif len(user_input) != 3:
                print("Input harus 3 nilai (enc, key, iv)")
                continue

            enc_mix, key, iv = user_input
            if enc_mix in self.enc_real and key in self.key_real and iv in self.iv_real:
                idx_enc = self.enc_real.index(enc_mix)
                idx_key = self.key_real.index(key)
                idx_iv = self.iv_real.index(iv)
                if idx_enc == idx_key == idx_iv:
                    print(f"Benar({idx_enc})")
                else:
                    print("Index tidak sama")
            else:
                print("Salah")

    def check_xor(self):
        print("Masukkan xor1 dan xor2 (xor1<spasi>xor2):")
        while True:
            user_input = input("").split()
            if len(user_input) == 1 and user_input[0] == "<":
                break
            elif len(user_input) != 2:
                print("Input harus 2 nilai")
                continue
            
            try:
                xor1 = int(user_input[0])
                xor2 = int(user_input[1])
            except ValueError:
                print("Input harus berupa angka integer")
                continue

            if xor1 in self.xor1_real and xor2 in self.xor2_real:
                idx_xor1 = self.xor1_real.index(xor1)
                idx_xor2 = self.xor2_real.index(xor2)
                if idx_xor1 == idx_xor2:
                    print(f"Benar({idx_xor1})")
                else:
                    print("Index tidak sama.")
            elif xor1 in self.xor1_real or xor2 in self.xor2_real:
                print("Hanya satu XOR yang ditemukan")
            else:
                print("Salah")

    def check_dhc(self):
        print("Masukkan index dan ciphertext c' (i<spasi>c'):")
        while True:
            user_input = input().split()
            if len(user_input) == 1 and user_input[0] == "<":
                break
            elif len(user_input) != 2:
                print("Input harus 2 nilai (index dan ciphertext)")
                continue

            try:
                i = int(user_input[0])
                c = int(user_input[1])
            except ValueError:
                print("Input harus berupa angka integer")
                continue

            if c == self.c_real[i]:
                print("Hacker terdeteksi")
            else:
                d = self.d_real[i]
                n = self.n_real[i]
                decrypted_message = pow(c, d, n)
                print(f"Pesan didekripsi: {decrypted_message}")

    def check_rsa(self):
        print("Masukkan c dan n (c<spasi>n):")
        while True:
            user_input = input().split()
            if len(user_input) == 1 and user_input[0] == "<":
                break
            elif len(user_input) != 2:
                print("Input harus 2 nilai (c dan n)")
                continue
            
            try:
                c = int(user_input[0])
                n = int(user_input[1])
            except ValueError:
                print("Input harus berupa angka integer")
                continue

            if c in self.c_real and n in self.n_real:
                idx_c = self.c_real.index(c)
                idx_n = self.n_real.index(n)
                if idx_c == idx_n:
                    print(f"Benar({idx_c})")
                else:
                    print("Index tidak sama")
            elif c in self.c_real or n in self.n_real:
                print("Hanya satu dari c atau n yang ditemukan")
            else:
                print("Salah")

    def enc_txt(self):
        for c in self.c_mix:
            print(f"{c}")
        for n in self.n_mix:
            print(f"{n}")
        for xor1 in self.xor1_mix:
            print(f"{xor1}")
        for xor2 in self.xor2_mix:
            print(f"{xor2}")
        for enc in self.enc_mix:
            print(f"{enc}")
        for key in self.key_real:
            print(f"{key}")
        for iv in self.iv_real:
            print(f"{iv}")
        print("Selesai")

    def menu_main(self):
        while True:
            print("\nHalo, ada yang bisa dibantu?")
            print("\nMenu:")
            print("1. Cek AES")
            print("2. Cek XOR")
            print("3. Cek DHC")
            print("4. Cek RSA")
            print("5. ENC.txt")
            print("6. Keluar")
            print("Catatan: klik '<' untuk kembali ke menu awal")
            choice = input("Pilih menu (1-6): ")

            if choice == '1':
                self.check_aes()
            elif choice == '2':
                self.check_xor()
            elif choice == '3':
                self.check_dhc()
            elif choice == '4':
                self.check_rsa()
            elif choice == '5':
                self.enc_txt()
            elif choice == '6':
                print("Sampai jumpa kembali")
                break
            else:
                print("Pilihan tidak sesuai")

if __name__ == "__main__":
    check = Check(enc_mix, key_mix, iv_mix, xor1_mix, xor2_mix, c_mix, n_mix, enc_real, key_real, iv_real, xor1_real, xor2_real, xor3_real, c_real, n_real, d_real)
    check.menu_main()
