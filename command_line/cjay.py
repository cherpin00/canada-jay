import sys
import os
import subprocess
import argparse
import logging
import shutil
import itertools
from string import ascii_lowercase
from time import sleep
import glob

from cryptography.fernet import Fernet

g_driveRoot = "canada_jay_root"

def run(cmd):
    subprocess.call(cmd.split())
    # subprocess.Popen(cmd.split())

def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--drives", nargs="+", required=True, help="list of relitive paths to split your data to") #nargs="+" takes 1 or more arguments
    parser.add_argument("-f", "--files", nargs="+", default=["test"], help="input file to split")
    parser.add_argument("-j", "--join", action="store_true", help="Join the specified files using drives specified.")
    return parser

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

def split(drives, files, prefix="split"): #TODO: Add option to pass in folders instead of just files
    for file in files:
        try:
            encrypt(file)
            numParts = len(drives)
            fileSize = os.path.getsize(file)
            partSize = fileSize//numParts
            if (fileSize % numParts > 0):
                partSize += 1

            tmpFolder = "temp"
            if not os.path.exists(tmpFolder):
                os.mkdir(tmpFolder)
            run(f"split -b {partSize} {file} {os.path.join(tmpFolder, prefix)}-{file}-")

            count = 0
            for obj in os.scandir(tmpFolder):
                if obj.is_file():
                    destination = os.path.join(drives[count], g_driveRoot) + os.path.sep
                    destination = os.path.join(destination, os.path.basename(obj.path))
                    if not os.path.exists(os.path.join(drives[count], g_driveRoot)): #TODO: Add option to make drive if not exists.
                        curdir = os.getcwd()
                        try:
                            logging.debug(f"Creating {g_driveRoot} folder in {drives[count]}")
                            os.chdir(drives[count])
                            os.mkdir(g_driveRoot)
                        except Exception as e: #TODO: Don't except all errors here.  Might be okay because we throw it again
                            logging.error(f"Could not create root folder {g_driveRoot} in {drives[count]}.  Please create it manually.")
                            logging.info(f"Could not create root folder {g_driveRoot} in {drives[count]}.  Please create it manually.")
                            shutil.rmtree(tmpFolder) #TODO: Create on cleanup function that we can call so we DRY
                            exit(1)
                        finally:
                            os.chdir(curdir)
                    logging.debug(f"moving {obj.path} to {destination}")
                    try:
                        shutil.move(obj.path, destination)
                    except shutil.Error as e:
                        logging.error(f"Failed moving {obj.path} to {os.path.abspath(destination)}.  Exiting.")
                        logging.error(f"Error message: {e}")
                        exit(1)
                count+=1
        except Exception as e: #TODO: add a status (maybe in a file or database.  So that we can undo the steps if we get an error)
            decrypt(file)
            raise e

        os.remove(file)
    if os.path.exists(tmpFolder):
        os.rmdir(tmpFolder)

def join(drives, files, prefix="split"):
    tempFolder = "temp"

    if not os.path.exists(tempFolder): #TODO: Do error handling.  If anything in here fails we should not remove the files in the drives.  To do this first do a copy check to make sure they are there and then delete them
        os.mkdir(tempFolder)

    for folder in drives:
        folder = os.path.join(folder, g_driveRoot)
        for file in glob.glob(os.path.join(folder, f"{prefix}-*")):
            name = file.split(os.path.sep)[-1]
            if name.split("-")[1] in files:
                destination = os.path.join(tempFolder, name)
                logging.debug(f"moving {file} to {destination}")
                shutil.move(file, destination) #TODO: Add feature to copy or move
    
    for current_file in files:
        toJoin = glob.glob(os.path.join(tempFolder, f"*{current_file}*"))
        if not len(toJoin) > 0:
            logging.warning(f"Cannot find file {current_file}. Skipping.")
            continue
        toJoin.sort()
        logging.debug(f"Concatenating files {toJoin}")
        output_file = current_file
        concat_files(output_file, toJoin) #TODO: allow there to be -'s in the name.  We need to escape them somehow
        decrypt(output_file)
        for f in toJoin: #TODO: Don't do this if the previous stuff fails
            logging.debug(f"Deleting file {f}.")
            os.remove(f)
    if os.path.exists(tempFolder):
        os.rmdir(tempFolder)


def main():
    logging.getLogger().setLevel(logging.DEBUG)
    parser = get_parser()
    if len(sys.argv) == 1:
        args = parser.parse_args("-d google_drive one_drive -f test.txt".split(" "))
    else:
        args = parser.parse_args()

    if args.join:
        join(args.drives, args.files)
    else:
        split(args.drives, args.files)

if __name__ == "__main__":
    main()

"""
TODO: Test run spit twice in a row
TODO: Test run join twice in a row
TODO: Fail correctly.  If we can not make all the splits make sure to make none of them.


Test cases:
No root directory in 1 of drives
No root directory in all of drives
Input file does not exists
Drives does not exist
Cannot read or write to Drive
"""