import sys
import os
import argparse
import logging
import shutil
import glob

from utils import encrypt, decrypt, my_split, run, concat_files, slugify

g_driveRoot = "canada_jay_root"

def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--drives", nargs="+", required=True, help="list of relitive paths to split your data to") #nargs="+" takes 1 or more arguments
    parser.add_argument("-f", "--files", nargs="+", default=["test"], help="input file to split")
    parser.add_argument("-j", "--join", action="store_true", help="Join the specified files using drives specified.")
    return parser

def split(drives, files, prefix="split"): #TODO: Add option to pass in folders instead of just files
    tmpFolder = "temp"
    for file in files:
        if not os.path.exists(file):
            logging.error(f"File {file} does not exists.  Skipping")
            continue
        try:
            encrypt(file)
            numParts = len(drives)
            fileSize = os.path.getsize(file)
            partSize = fileSize//numParts
            if (fileSize % numParts > 0):
                partSize += 1

            if not os.path.exists(tmpFolder):
                os.mkdir(tmpFolder)
            my_split(file, partSize, f"{os.path.join(tmpFolder, prefix)}-{slugify(file)}-") #Come up with why for there to not be duplicate files
            # run(f"split -b {partSize} {file} {os.path.join(tmpFolder, prefix)}-{file}-")

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
    return True

def join(drives, files, prefix="split"):
    tempFolder = "temp"
    slugified_files = [slugify(f) for f in files]

    if not os.path.exists(tempFolder): #TODO: Do error handling.  If anything in here fails we should not remove the files in the drives.  To do this first do a copy check to make sure they are there and then delete them
        os.mkdir(tempFolder)

    for folder in drives:
        folder = os.path.join(folder, g_driveRoot)
        for file in glob.glob(os.path.join(folder, f"{prefix}-*")):
            name = file.split(os.path.sep)[-1]
            if name.split("-")[1] in slugified_files: #TODO: Think about forcing them to pass in a set to make this o(1) look up time.
                destination = os.path.join(tempFolder, name)
                logging.debug(f"moving {file} to {destination}")
                shutil.move(file, destination) #TODO: Add feature to copy or move
    
    for current_file in files:
        toJoin = glob.glob(os.path.join(tempFolder, f"*{slugify(current_file)}*"))
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
    return True


def main():
    logging.getLogger().setLevel(logging.DEBUG)
    parser = get_parser()
    if len(sys.argv) == 1:
        args = parser.parse_args("-d google_drive one_drive -f /mnt/c/temp/test.txt -j".split(" "))
        # args = parser.parse_args("-d google_drive one_drive -f test.txt".split(" "))
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
TODO: Add the drives that the file was split with in the name or somewhere else
TODO: Test duplicate slugify file names

Test cases:
No root directory in 1 of drives
No root directory in all of drives
Input file does not exists
Drives does not exist
Cannot read or write to Drive
"""