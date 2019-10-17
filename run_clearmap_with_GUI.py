__author__ = "Bram Bosch"

import mmap
import re
import os
import tkinter as tk
import tkinter.ttk as ttk
from tkfilebrowser import askopendirname

maindir = os.path.abspath(__file__)
maindir = maindir.replace("run_clearmap_with_GUI.py", "")
with open(maindir + "ClearMap/Settings.py", 'r+') as settingsFileRead:
    data = mmap.mmap(settingsFileRead.fileno(), 0)
    try:
        settingsMatchElastix = re.search(b'(?<=ElastixPath = ")([^"]+)', data)
        firstSetupElastix = os.path.isdir(settingsMatchElastix.group(0))

    except AttributeError:
        firstSetupElastix = False
    try:
        settingsMatchSave = re.search(b'(?<=saveSettings = ")([^"]+)', data)
        firstSetupSave = os.path.isdir(settingsMatchSave.group(0))
    except AttributeError:
        firstSetupSave = False


def searchElastix():
    """
    This function opens a dir chooser which asks the user to select the folder where elastix is installed
    :return:
    """
    elastixPath = askopendirname(parent=rootFirstSetup, title="Select the elastix folder")
    settingsFileRead = open(maindir + "ClearMap/Settings.py").read()
    if os.path.isdir(re.search(r'(?<=saveSettings = ")([^"]+)', settingsFileRead).group(0)) and elastixPath != "":
        quitButton['state'] = 'normal'
    settingsFileRead = re.sub('("mark")\nElastix.*', '"mark"\nElastixPath = "' + elastixPath + '";', settingsFileRead)
    settingsFileWrite = open(maindir + "ClearMap/Settings.py", "w")
    settingsFileWrite.write(settingsFileRead)


def searchIlastik():
    """
    This function opens a dir chooser which asks the user to select the folder where Ilastik is installed
    :return:
    """
    ilastikPath = askopendirname(parent=rootFirstSetup, title="Select the ilastik folder")
    settingsFileRead = open(maindir + "ClearMap/Settings.py").read()
    settingsFileRead = re.sub('("mark")\nIlastik.*', '"mark"\nIlastikPath = "' + ilastikPath + '";', settingsFileRead)

    settingsFileWrite = open(maindir + "ClearMap/Settings.py", "w")
    settingsFileWrite.write(settingsFileRead)


def saveLocation():
    savePath = askopendirname(parent=rootFirstSetup, title="Select the save location folder")
    settingsFileRead = open(maindir + "ClearMap/Settings.py").read()
    if os.path.isdir(re.search(r'(?<=ElastixPath = ")([^"]+)', settingsFileRead).group(0)) and savePath != "":
        quitButton['state'] = 'normal'
    settingsFileRead = re.sub('saveSettings.*', 'saveSettings = "' + savePath + '";', settingsFileRead)

    settingsFileWrite = open(maindir + "ClearMap/Settings.py", "w")
    settingsFileWrite.write(settingsFileRead)


"""
If firstSetup is true a tkinter gui is called which lets the user give the path to their installation of elastix and
Ilastik. The path to elastix is obligated. The path to Ilastik is not necessary.
"""
if not firstSetupElastix or not firstSetupSave:
    rootFirstSetup = tk.Tk()
    rootFirstSetup.title("Clearmap")
    style = ttk.Style(rootFirstSetup)
    style.theme_use("clam")
    tk.Label(rootFirstSetup, text="It looks like this is your first time running this program").grid(padx=4, pady=4,
                                                                                                     sticky='ew')
    tk.Label(rootFirstSetup, text="Please refer to the requirements file for all the downloads").grid(padx=4, pady=4,
                                                                                                      sticky='ew')
    tk.Label(rootFirstSetup, text="The path to where elastix is located is mandatory").grid(padx=4, pady=4, sticky='ew')
    tk.Label(rootFirstSetup, text="A save location is also mandatory").grid(padx=4, pady=4, sticky='ew')

    tk.Label(rootFirstSetup, text="The path to ilastik can be left empty if you dont want to use it").grid(padx=4,
                                                                                                           pady=4,
                                                                                                           sticky='ew')

    pathElastixButton = tk.Button(rootFirstSetup, text="Search elastix", command=searchElastix)
    pathElastixButton.grid(padx=4, pady=4, sticky='ew')

    pathIlastikButton = tk.Button(rootFirstSetup, text="Search Ilastik", command=searchIlastik)
    pathIlastikButton.grid(padx=4, pady=4, sticky='ew')

    pathSave = tk.Button(rootFirstSetup, text="Set a location for the saved files", command=saveLocation)
    pathSave.grid(padx=4, pady=4, sticky='ew')

    quitButton = tk.Button(rootFirstSetup, state=tk.DISABLED, text="Run clearmap", command=rootFirstSetup.destroy)
    quitButton.grid(padx=4, pady=4, sticky='ew')

    rootFirstSetup.mainloop()

from ClearMap.gui.tkinter_gui import run_gui

run_gui()
