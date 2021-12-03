import random
from datetime import datetime
import sys
from time import sleep
import os
from tinydb import TinyDB, Query, where

import eel

import tkinter as tk
from tkinter import filedialog

sys.path.insert(0, './command_line')
from command_line.cjay import split

eel.init('web')
root = tk.Tk()
root.wm_attributes('-topmost', 1)
db = TinyDB('db.json')
User = Query()

files = {}
drives = {}
    
@eel.expose
def load_db():
    results = db.search(where('type') == 'file')
    file_names = [r['name'] for r in results]

    results = db.search(where('type') == 'drive')
    drives = [r['name'] for r in results]

    for name0 in file_names:
        load_file(name0,0)
    for name1 in drives:
        load_drive(name1,0)
    print(file_names)


@eel.expose
def pythonFunction(file_count):
    print(file_count)
    root.withdraw()
    file_path = filedialog.askopenfilename()
    db.insert({'type': 'file', 'name' : file_path})
    print(db.all())
    files[file_count] = file_path
    eel.inner_element_file_change(file_path) 
    eel.add_filename_change(file_path)
    return file_path

@eel.expose
def load_file(name, file_count):
    eel.add_para_file(name, "files_saved") 
    print(name)
    return name

@eel.expose
def load_drive(name, drive_count):
    drives[drive_count] = name
    drives[drive_count] = name
    print("drive here")
    eel.add_para(name, "drives") 
    return name

@eel.expose
def drive_addition(drive_count):
    print(drive_count)
    root.withdraw()
    file_path = filedialog.askdirectory()
    db.insert({'type': 'drive', 'name' : file_path})
    print(db.all())
    drives[drive_count] = file_path
    eel.add_para(file_path, "drives") 
    return file_path

@eel.expose
def split_function_call():
    print(files)
    print(drives)

    files_list = [x.replace("/", os.path.sep) for x in files.values()]
    drives_list = [x.replace("/", os.path.sep) for x in drives.values()]
    print(db.all())
    split(drives_list, files_list)


eel.start('index.html')