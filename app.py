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
from command_line.cjay import split, join

eel.init('web')
root = tk.Tk()
root.wm_attributes('-topmost', 1)
db = TinyDB('db.json')
User = Query()

files = {}
drives = {}
    
@eel.expose
def load_db():
    results_files = db.search(where('type') == 'file')
    results_drives = db.search(where('type') == 'drive')
    for result_file in results_files:
        load_file(result_file)
    for result_drive in results_drives:
        load_drive(result_drive)

@eel.expose
def load_file(result):
    eel.add_content(result['name'], "file_saved", "files_saved", "p", result.doc_id)
    return result['name']

@eel.expose
def load_drive(result):
    drives[result.doc_id] = result['name']
    eel.add_content(result['name'], "drive", "drives", "p", result.doc_id)
    return result['name']

@eel.expose
def get_file_path(id):
    obj = db.get(doc_id=int(id))
    drives_list = [x.replace("/", os.path.sep) for x in drives.values()]
    db.remove(doc_ids=[int(id)])
    join(drives_list, [obj["name"]])

@eel.expose
def pythonFunction(file_count):
    root.withdraw()
    file_path = filedialog.askopenfilename()
    files[file_count] = file_path
    eel.inner_element_file_change(file_path) 
    eel.add_filename_change(file_path)
    return file_path

@eel.expose
def drive_addition(drive_count):
    root.withdraw()
    file_path = filedialog.askdirectory()
    id = db.insert({'type': 'drive', 'name' : file_path})
    drives[drive_count] = file_path
    eel.add_content(file_path, "drive", "drives", "p", id) 
    return file_path

@eel.expose
def split_function_call():
    files_list = [x.replace("/", os.path.sep) for x in files.values()]
    drives_list = [x.replace("/", os.path.sep) for x in drives.values()]
    eel.remove_to_split()
    if split(drives_list, files_list):
        for value in files.values():
            if not db.contains(Query().fragment({'type': 'file', 'name': value})):
                id = db.insert({'type': 'file', 'name' : value})
                eel.add_content(value, "file_saved", "files_saved", "p", id)
    files.clear()


eel.start('index.html')