import glob, os
import multiprocessing
import re
import shutil
import sys
import threading
import tkinter
import tkinter as tk
import tkinter.ttk as ttk
import traceback
from tkinter import simpledialog, messagebox

import psutil
from tkfilebrowser import askopendirname, askopenfilename

from ClearMap.Scripts.Templates.split_CSV import write_landmarks_to_files
def manual(pathClearMap,root):
    rootMA = tk.Tk()

    rootMA.title("Clearmap")
    style = ttk.Style(rootMA)
    style.theme_use("clam")


    tk.Label(rootMA, text="""Open the "autofluo_resampled.tif file and the "template_25.tif" file in ImageJ. 
Go to Plugins -> Big Data Viewer -> Bigwarp. Open template_25 first, then autofluo_resampled. 
In both images, hit Shift + A to flip both to coronal view. 
Scroll around and match the files as closely as possible (left click + pull around to tilt your plane of view in 3d. Ctrl + Y to reset to starter view.)
Landmark procedure: 
    click on one of the windows to make sure you are active in the right window. 
    Press Space bar to activate the landmark mode. 
    Click on one of the landmarks. 
    click the other window, re-activate landmark mode by pressing space bar(twice, if need be)
    Mark the same landmark. 
    Repeat until approx. 50-100 landmarks are marked. 
Go to the landmarks window -> File -> Export landmarks. """).grid(padx=4, pady=4, sticky='ew')
    findLandmarksButton = tk.Button(rootMA, text="Search for the landmarks file", command=lambda :[findLandmarks(rootMA,pathClearMap),rootMA.destroy()])
    findLandmarksButton.grid(padx=4, pady=4, sticky='ew')
    a = True
    try:
        def ask_quit():
            if messagebox.askokcancel("Quit", "Do you want to quit now?"):
                rootMA.destroy()
                root.destroy()
                raise FileNotFoundError
    except FileNotFoundError:
        a = False

    rootMA.protocol("WM_DELETE_WINDOW", ask_quit)
    rootMA.wait_window(rootMA)


    rootMA = tk.Toplevel()
    return a

def findLandmarks(rootMA,pathClearMap):
    landmarksDir = askopenfilename(parent=rootMA, title="Select landmarks file")
    pathOutput = pathClearMap + "ClearMap/clearmap_preset_folder/output/landmarks.csv"
    try:
        shutil.copyfile(landmarksDir,pathOutput)
        write_landmarks_to_files(pathClearMap)
    except FileNotFoundError:
        messagebox.showinfo("ERROR","An error occured while looking for the landmarks file")

