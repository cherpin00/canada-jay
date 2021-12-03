import random
from datetime import datetime
import sys
from time import sleep
import os
#from tinydb import TinyDB, Query

import eel

import tkinter as tk
from tkinter import filedialog

sys.path.insert(0, './command_line')
from command_line.cjay import split

eel.init('web')
root = tk.Tk()
#db = TinyDB('path/to/db.json')
#User = Query()

files = {}
drives = {}
    
@eel.expose
def pythonFunction(file_count):
    print(file_count)
    root.withdraw()
    file_path = filedialog.askopenfilename()
    #print(file_path)
    files[file_count] = file_path
    eel.inner_element_file_change(file_path) 
    eel.add_filename_change(file_path)
    return file_path

@eel.expose
def drive_addition(drive_count):
    print(drive_count)
    root.withdraw()
    file_path = filedialog.askdirectory()
    drives[drive_count] = file_path
    eel.add_para(file_path, "drives") 
    return file_path

@eel.expose
def split_function_call():
    print(files)
    print(drives)

    files_list = [x.replace("/", os.path.sep) for x in files.values()]
    drives_list = [x.replace("/", os.path.sep) for x in drives.values()]
    split(drives_list, files_list)


eel.start('index.html')