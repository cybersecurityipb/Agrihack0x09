from base64  import b64decode, b64encode

flag = 'agrihack{yah4h4!!!__dukun_ialah_ultimate_skill}'
for i in range(5):
    flag = b64encode(flag.encode()).decode()

print(flag)

def rot_n(char, n, start):
    """Helper function to rotate a character by n positions"""
    return chr((ord(char) - start - n) % 26 + start)

def decrypt_char(char):
    """Decrypt individual character based on its type"""
    if char.isdigit():  # Number: ROT7
        return str((int(char) - 7) % 10)
    elif char.isupper():  # Uppercase: ROT13
        return rot_n(char, 13, ord('A'))
    elif char.islower():  # Lowercase: ROT10
        return rot_n(char, 10, ord('a'))
    else:
        return char  # Non-alphanumeric characters remain the same

def decrypt_message(message):
    """Decrypt entire message"""
    return ''.join(decrypt_char(c) for c in message)

# Your encrypted message
encrypted_message = "Nzooukr uke xku ukx pvkq!!! IwzTLJRiEKvJlTrGLunyl8IaFw6MIvWLGvMXGu8LDvrKk8MbLIHhEIMblSrsluWRIGW1IwDhJxECIwrGHvMIoSnJHudIZJEVIJdJH9WKoUOIk9D7GGSMoSndnR6FZSzWIJ87k8ITJuMKluWJGHMgGSzRExAtZKOTJuH8H9WbFvvJERMfMQWTEu8LHwhGFRWrJIEXk77hIunFIThEIIDgBD== Qomyno ukx sxs too!!!"

# Decrypt the message
decrypted_message = decrypt_message(encrypted_message)
print(decrypted_message)
