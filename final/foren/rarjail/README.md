# rarjail

## Description
semua yang bidangnya foren pasti tau cara ngebrute force password itu gimana, tapi yang ini nggak bisa cuy passwordnya beda.
Mungkin yang didalemnya bisa, tapi caranya gimana ya ngeluarinnya?

## Attachment
jail.rar

## Flag
agrihack{1_c4n_3sc4p3_3v3ry_j4il_1n_th3_w0rld}

## Proof of Concept
1. cari 12 bytes terakhir rar pertama(ada ditengah-tengah)
2. 12 bytes setelah itu punya rar kedua, tinggal tambahin headernya
3. bruteforce passwordnya pake rockyou.txt
