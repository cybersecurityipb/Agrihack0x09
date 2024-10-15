from base64 import b64decode

def rot_n(char, n, start):
    return chr((ord(char) - start - n) % 26 + start)

def decrypt_char(char):
    if char.isdigit(): 
        return str((int(char) - 7) % 10)
    elif char.isupper():  
        return rot_n(char, 13, ord('A'))
    elif char.islower():
        return rot_n(char, 10, ord('a'))
    else:
        return char 

def decrypt_message(message):
    return ''.join(decrypt_char(c) for c in message)

with open('message.enc', 'r') as message_enc:
    message_enc = message_enc.read()

decrypted_message = decrypt_message(message_enc)
decrypted_message = decrypted_message.split()

flag = decrypted_message[5]
while 'agrihack' not in flag:
    flag = b64decode(flag.encode()).decode()

print(flag)



