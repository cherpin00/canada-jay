import os
import subprocess
import argparse
import logging
import shutil

def run(cmd):
    subprocess.call(cmd.split())
    # subprocess.Popen(cmd.split())

def get_args(parser):
    parser.add_argument("-d", "--drives", nargs="+", required=True, help="list of relitive paths to split your data to") #nargs="+" takes 1 or more arguments
    parser.add_argument("-f", "--file", default="test", help="input file to split")
    args = parser.parse_args()
    return args

def main():
    args = get_args(argparse.ArgumentParser())
    drives = args.drives

    numParts = len(drives)
    fileName = args.file
    fileSize = os.path.getsize(fileName)

    partSize = fileSize//numParts
    if (fileSize % numParts > 0):
        partSize += 1

    tmpFolder = "temp"
    if not os.path.exists(tmpFolder):
        os.mkdir(tmpFolder)
    prefix = "split"
    run(f"split -b {partSize} {fileName} {os.path.join(tmpFolder, prefix)}-")

    count = 0
    for obj in os.scandir(tmpFolder):
        if obj.is_file():
            if not os.path.exists(drives[count]):
                os.mkdir(drives[count])
            shutil.move(obj.path, drives[count])
            print(obj.path)
            count+=1

    os.rmdir(tmpFolder)

if __name__ == "__main__":
    main()