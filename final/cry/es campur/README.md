# es campur

## Description
es campur > es teler

## Attachment
chall.py
nc -l [port]

## Flag
agrihack{35_c4mpur_3n4k_b4ng3t_cuy_9hvq91hd2nqp9h}

## Proof of Concept
1. cari c dan n yang benar dengan cara brutforce
2. buat ciphertext baru dengan mengalikan ciphertext lama dengan 2^e mod n
3. setelah mendapat semua decrypted text, kalikan dengan 2^-1 mod n lalu di mod n untuk mendapat m
4. hapus 10 angka pertama dari m karena string m sudah di padding dengan 32 bit random integer
5. cari xor1 dan xor2 yang benar dengan cara bruteforce
6. m ^ xor1 untuk mendapat iv, m ^ xor2 untuk mendapat key
7. cari enc yang benar dengan brutefoce bersama key dan iv
8. lalu tinggal decrypt dengan aes cbc
