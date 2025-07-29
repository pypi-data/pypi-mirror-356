import hashlib
from colorama import Fore, Style

def shift_chiper():
    z=['1','2','3','4','5','6','7','8','9','0','A','B','C','D','E','F','G','H','I',
       'J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','a','b',
       'c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u',
       'v','w','x','y','z','!','@','#','$','%','^','&','*','(',')','-','=','_','+',
       '{','}','[',']',';',':','"','\'',',','.','<','>','/','?','\\','|','`','~',' ']

    print(Fore.CYAN + "Shift Cipher" + Style.RESET_ALL)
    a = input("Enter the text to encrypt: ")
    b = ""
    swift = 9
    for x in range(len(a)):
        temp = z.index(a[x]) + swift
        b = b + z[temp % 95]
    print(Fore.CYAN + "\nPlainText = " + a + Style.RESET_ALL)
    print(Fore.CYAN + "CipherText = " + b + Style.RESET_ALL)

def MD5_hash():
    plaintext = input(Fore.CYAN + "Enter the text to MD5 hash: " + Style.RESET_ALL)
    md5 = hashlib.md5()
    md5.update(plaintext.encode('ascii'))
    print("____________________________________")
    print(Fore.GREEN + "\nCipherText = " + md5.hexdigest() + Style.RESET_ALL)

def SHA1_hash():
    plaintext = input(Fore.CYAN + "Enter the text to SHA1 hash: " + Style.RESET_ALL)
    sha1 = hashlib.sha1()
    sha1.update(plaintext.encode('ascii'))
    print("____________________________________")
    print(Fore.GREEN + "\nCipherText = " + sha1.hexdigest() + Style.RESET_ALL)

def SHA512_hash():
    plaintext = input(Fore.CYAN + "Enter the text to SHA512 hash: " + Style.RESET_ALL)
    sha512 = hashlib.sha512()
    sha512.update(plaintext.encode('ascii'))
    print("____________________________________")
    print(Fore.GREEN + "\nCipherText = " + sha512.hexdigest() + Style.RESET_ALL)

def shake_128_hash():
    plaintext = input("Enter the text to SHAKE128 hash: ")
    shake_128 = hashlib.shake_128()
    shake_128.update(plaintext.encode('ascii'))
    print("____________________________________")
    print(Fore.GREEN + "\nCipherText = " + shake_128.hexdigest(64) + Style.RESET_ALL)

def shake_256_hash():
    plaintext = input(Fore.CYAN + "Enter the text to SHAKE256 hash: " + Style.RESET_ALL)
    shake_256 = hashlib.shake_256()
    shake_256.update(plaintext.encode('ascii'))
    print("____________________________________")
    print(Fore.GREEN + "\nCipherText = " + shake_256.hexdigest(64) + Style.RESET_ALL)

def BLAKE2b_hash():
    plaintext = input(Fore.CYAN + "Enter the text to BLAKE2b hash: " + Style.RESET_ALL)
    blake2b = hashlib.blake2b()
    blake2b.update(plaintext.encode('ascii'))
    print("____________________________________")
    print(Fore.GREEN + "\nCipherText = " + blake2b.hexdigest() + Style.RESET_ALL)

def BLAKE2s_hash():
    plaintext = input(Fore.CYAN + "Enter the text to BLAKE2s hash: " + Style.RESET_ALL)
    blake2s = hashlib.blake2s()
    blake2s.update(plaintext.encode('ascii'))
    print("____________________________________")
    print(Fore.GREEN + "\nCipherText = " + blake2s.hexdigest() + Style.RESET_ALL)

def SHA3_224_hash():
    plaintext = input(Fore.CYAN + "Enter the text to SHA3-224 hash: " + Style.RESET_ALL)
    sha3_224 = hashlib.sha3_224()
    sha3_224.update(plaintext.encode('ascii'))
    print("____________________________________")
    print(Fore.GREEN + "\nCipherText = " + sha3_224.hexdigest() + Style.RESET_ALL)

def SHA3_256_hash():
    plaintext = input(Fore.CYAN + "Enter the text to SHA3-256 hash: " + Style.RESET_ALL)
    sha3_256 = hashlib.sha3_256()
    sha3_256.update(plaintext.encode('ascii'))
    print("____________________________________")
    print(Fore.GREEN + "\nCipherText = " + sha3_256.hexdigest() + Style.RESET_ALL)

def SHA3_384_hash():
    plaintext = input(Fore.CYAN + "Enter the text to SHA3-384 hash: " + Style.RESET_ALL)
    sha3_384 = hashlib.sha3_384()
    sha3_384.update(plaintext.encode('ascii'))
    print("____________________________________")
    print(Fore.GREEN + "\nCipherText = " + sha3_384.hexdigest() + Style.RESET_ALL)

def SHA3_512_hash():
    plaintext = input(Fore.CYAN + "Enter the text to SHA3-512 hash: " + Style.RESET_ALL)
    sha3_512 = hashlib.sha3_512()
    sha3_512.update(plaintext.encode('ascii'))
    print("____________________________________")
    print(Fore.GREEN + "\nCipherText = " + sha3_512.hexdigest() + Style.RESET_ALL)

def PBKDF2_hash():
    import getpass
    from hashlib import pbkdf2_hmac

    password = getpass.getpass(Fore.YELLOW + "Enter the password to PBKDF2 hash: " + Style.RESET_ALL)
    salt = getpass.getpass(Fore.YELLOW + "Enter the salt: " + Style.RESET_ALL)
    iterations = int(input(Fore.YELLOW + "Enter the number of iterations: " + Style.RESET_ALL))

    pbkdf2 = pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), iterations)
    print("____________________________________")
    print(Fore.GREEN + "\nCipherText = " + pbkdf2.hex() + Style.RESET_ALL)

def Argon2_hash():
    from argon2 import PasswordHasher
    from getpass import getpass

    password = getpass("Enter the password to Argon2 hash: ")
    ph = PasswordHasher()
    
    try:
        hash_value = ph.hash(password)
        print("____________________________________")
        print(Fore.GREEN + "\nCipherText = " + hash_value + Style.RESET_ALL)
    except Exception as e:
        print(f"Error hashing password: {e}")   

def AES_Encryption_And_Description():
    from Crypto.Cipher import AES
    from Crypto.Random import get_random_bytes
    from base64 import b64encode, b64decode
    import hashlib
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives import hashes, padding
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import secrets

    # Constants
    KEY_LENGTH = 32       # 256-bit key for AES
    IV_LENGTH = 16        # Block size
    SALT_LENGTH = 16

    def generate_key_with_hashlib(password: str, salt: bytes) -> bytes:
        """
        Derive key using hashlib.sha256 for simple usage (not recommended for production).
        Used here just to apply hashlib meaningfully.
        """
        return hashlib.sha256(password.encode() + salt).digest()

    def generate_key_pbkdf2(password: str, salt: bytes) -> bytes:
        """
        Derive a strong key using PBKDF2 and SHA256 (preferred).
        """
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=KEY_LENGTH,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        return kdf.derive(password.encode())

    def aes_encrypt(plaintext: str, password: str, use_hashlib=False) -> str:
        salt = secrets.token_bytes(SALT_LENGTH)
        iv = get_random_bytes(IV_LENGTH)

        if use_hashlib:
            key = generate_key_with_hashlib(password, salt)
        else:
            key = generate_key_pbkdf2(password, salt)

        # Pad the plaintext
        padder = padding.PKCS7(128).padder()
        padded_text = padder.update(plaintext.encode()) + padder.finalize()

        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(padded_text) + encryptor.finalize()

        # Combine salt + iv + ciphertext
        combined = salt + iv + ciphertext
        return b64encode(combined).decode()

    def aes_decrypt(ciphertext_b64: str, password: str, use_hashlib=False) -> str:
        decoded = b64decode(ciphertext_b64)
        salt = decoded[:SALT_LENGTH]
        iv = decoded[SALT_LENGTH:SALT_LENGTH + IV_LENGTH]
        ciphertext = decoded[SALT_LENGTH + IV_LENGTH:]

        if use_hashlib:
            key = generate_key_with_hashlib(password, salt)
        else:
            key = generate_key_pbkdf2(password, salt)

        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()

        # Remove padding
        unpadder = padding.PKCS7(128).unpadder()
        plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()
        return plaintext.decode()

    # Example usage
    if __name__ == "__main__":
        message = input("Enter your message: ")
        password = input("Enter password: ")
        use_hash = input("Use hashlib instead of PBKDF2? (y/n): ").lower() == 'y'

        print(Fore.RED + "\nEncrypting...")
        encrypted = aes_encrypt(message, password, use_hashlib=use_hash)
        print(f"\nCipherText (base64): {encrypted}")

        print(Fore.RED + "\nDecrypting...")
        decrypted = aes_decrypt(encrypted, password, use_hashlib=use_hash)
        print(f"\nDecrypted message: {decrypted}")

def BLAKE3_hash():
    from hashlib import blake3

    plaintext = input(Fore.CYAN + "Enter the text to BLAKE3 hash: " + Style.RESET_ALL)
    blake3_hash = blake3(plaintext.encode('ascii')).hexdigest()
    print("____________________________________")
    print(Fore.GREEN + "\nCipherText = " + blake3_hash + Style.RESET_ALL)

def Whirlpool_hash():
    from hashlib import new

    plaintext = input(Fore.CYAN + "Enter the text to Whirlpool hash: " + Style.RESET_ALL)
    whirlpool_hash = new('whirlpool', plaintext.encode('ascii')).hexdigest()
    print("____________________________________")
    print(Fore.GREEN + "\nCipherText = " + whirlpool_hash + Style.RESET_ALL)

def Tiger_hash():
    from hashlib import new

    plaintext = input(Fore.CYAN + "Enter the text to Tiger hash: " + Style.RESET_ALL)
    tiger_hash = new('tiger', plaintext.encode('ascii')).hexdigest()
    print("____________________________________")
    print(Fore.GREEN + "\nCipherText = " + tiger_hash + Style.RESET_ALL)

def CRC32_hash():
    import zlib

    plaintext = input(Fore.CYAN + "Enter the text to CRC32 hash: " + Style.RESET_ALL)
    crc32_hash = zlib.crc32(plaintext.encode('ascii'))
    print("____________________________________")
    print(Fore.GREEN + "\nCipherText = " + hex(crc32_hash) + Style.RESET_ALL)

def CRC64_hash():
    import zlib

    plaintext = input(Fore.CYAN + "Enter the text to CRC64 hash: " + Style.RESET_ALL)
    crc64_hash = zlib.crc32(plaintext.encode('ascii'))
    print("____________________________________")
    print(Fore.GREEN + "\nCipherText = " + hex(crc64_hash) + Style.RESET_ALL)

def MurmurHash3_hash():
    from mmh3 import hash

    plaintext = input(Fore.CYAN + "Enter the text to MurmurHash3 hash: " + Style.RESET_ALL)
    murmur_hash = hash(plaintext)
    print("____________________________________")
    print(Fore.GREEN + "\nCipherText = " + hex(murmur_hash) + Style.RESET_ALL)

def NFC_hash():
    from hashlib import new

    plaintext = input(Fore.CYAN + "Enter the text to NFC hash: " + Style.RESET_ALL)
    nfc_hash = new('nfc', plaintext.encode('utf-8')).hexdigest()
    print("____________________________________")
    print(Fore.GREEN + "\nCipherText = " + nfc_hash + Style.RESET_ALL)


                   
