# SSS

## Deskripsi
"Note that the mapping is injective... according to `@yqroo`, this is the easiest challenge, definitely worth a try!"

## Attachment
- [source.py](source.py)
- [enc.txt](enc.txt)

## Proof of Concept
- Jelas terjadi pemetaan injektif antara printable ASCII dengan hasil hash nya, maka bisa di recover dengan membuat dictionary.
- Diperoleh challenge Tahap 2, yakni XOR
- Perhatikan bahwa kita bisa bruteforce n1 dan n2
- Analisis grey_v1 dan grey_v2 dalam level bit, akan diperoleh bahwa fungsinya bisa di reverse
Berikut [solver1](solve1.py) dan [solver2](solve2.py)
