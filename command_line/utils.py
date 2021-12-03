from string import ascii_lowercase
import itertools
import subprocess

from cryptography.fernet import Fernet

def run(cmd):
    subprocess.call(cmd.split())
    # subprocess.Popen(cmd.split())

def iter_all_strings():
    for size in itertools.count(1):
        for s in itertools.product(ascii_lowercase, repeat=size):
            yield "".join(s)

def concat_files(outputFile, fileNames):
    with open(outputFile, 'w') as outfile:
        for fname in fileNames:
            with open(fname) as infile:
                for line in infile:
                    outfile.write(line)

def gen_key():
    # key generation
    key = Fernet.generate_key()
  
    # string the key in a file
    with open('filekey.key', 'wb') as filekey: #TODO: Don't hardcode keyfile name
        filekey.write(key)

def get_key():
    filenName = 'filekey.key'
    if not os.path.exists(filenName):
        logging.error(f"Encryption key does not exist please create one useing gen_key()")
        exit(1)

    with open(filenName, 'rb') as filekey:
        key = filekey.read()
    return key

def encrypt(fileName):
    key = get_key()
  
    # using the generated key
    fernet = Fernet(key)
    
    # opening the original file to encrypt
    with open(fileName, 'rb') as file:
        original = file.read()
        
    # encrypting the file
    encrypted = fernet.encrypt(original)
    
    # opening the file in write mode and 
    # writing the encrypted data
    with open(fileName, 'wb') as encrypted_file:
        encrypted_file.write(encrypted)

def decrypt(fileName):
    key = get_key()

    # using the key
    fernet = Fernet(key)
    
    # opening the encrypted file
    with open(fileName, 'rb') as enc_file:
        encrypted = enc_file.read()
    
    # decrypting the file
    decrypted = fernet.decrypt(encrypted)
    
    # opening the file in write mode and
    # writing the decrypted data
    with open(fileName, 'wb') as dec_file:
        dec_file.write(decrypted)