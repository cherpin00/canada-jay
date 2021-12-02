import os
import subprocess
import argparse
import logging
import shutil
import itertools
from string import ascii_lowercase
from time import sleep
import glob

def run(cmd):
    subprocess.call(cmd.split())
    # subprocess.Popen(cmd.split())

def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--drives", nargs="+", required=True, help="list of relitive paths to split your data to") #nargs="+" takes 1 or more arguments
    parser.add_argument("-f", "--files", nargs="+", default=["test"], help="input file to split")
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

def split(drives, files, prefix="split"):
    for file in files:
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
                if not os.path.exists(drives[count]):
                    os.mkdir(drives[count])
                logging.debug(f"moving {obj.path} to {drives[count]}")
                shutil.move(obj.path, drives[count])
                count+=1
    if os.path.exists(tmpFolder):
        os.rmdir(tmpFolder)

def join(drives, files, prefix="split"):
    tempFolder = "temp"

    if not os.path.exists(tempFolder): #TODO: Do error handling.  If anything in here fails we should not remove the files in the drives.  To do this first do a copy check to make sure they are there and then delete them
        os.mkdir(tempFolder)

    for folder in drives:
        for file in glob.glob(os.path.join(folder, f"{prefix}-*")):
            name = file.split(os.path.sep)[-1]
            if name.split("-")[1] in files:
                destination = os.path.join(tempFolder, name)
                logging.debug(f"moving {file} to {destination}")
                shutil.copy(file, destination) #TODO: Add feature to copy or move
    
    for current_file in files:
        toJoin = glob.glob(os.path.join(tempFolder, f"*{current_file}*"))
        if not len(toJoin) > 0:
            continue
        toJoin.sort()
        logging.debug(f"Concatenating files {toJoin}")
        concat_files(current_file + ".out", toJoin) #TODO: allow there to be -'s in the name.  We need to escape them somehow

    
        

    # if os.path.exists(tempFolder):
        # os.rmdir(tempFolder)


def main():
    logging.getLogger().setLevel(logging.DEBUG)
    parser = get_parser()
    # args = parser.parse_args()
    args = parser.parse_args("-d drive1 drive2 -f test.txt".split(" "))
    # split(args.drives, args.files)
    join(args.drives, args.files)

if __name__ == "__main__":
    main()