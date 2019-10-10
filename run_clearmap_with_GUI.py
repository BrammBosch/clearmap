__author__ = "Bram Bosch"
import os
import tkinter as tk
import tkinter.ttk as ttk
from ClearMap.gui.tkinter_gui import run_gui
from tkfilebrowser import askopendirname

maindir = os.path.abspath(__file__)
maindir = maindir.replace("run_clearmap_with_GUI.py", "")
settingsFileRead = open(maindir + "ClearMap/Settings.py").read()
firstSetup = settingsFileRead.__contains__(
    "placeholderElastix")  # Check if placeholderElastix is in the settings.py file


def searchElastix():
    """
    This function opens a dir chooser which asks the user to select the folder where elastix is installed
    :return:
    """
    elastixPath = askopendirname(parent=root, title="Select the elastix folder")
    settingsFileRead = open(maindir + "ClearMap/Settings.py").read()
    settingsFileRead = settingsFileRead.replace("placeholderElastix", elastixPath)
    settingsFileWrite = open(maindir + "ClearMap/Settings.py", "w")
    settingsFileWrite.write(settingsFileRead)
    quitButton['state'] = 'normal'


def searchIlastik():
    """
    This function opens a dir chooser which asks the user to select the folder where Ilastik is installed
    :return:
    """
    ilastikPath = askopendirname(parent=root, title="Select the ilastik folder")
    settingsFileRead = open(maindir + "ClearMap/Settings.py").read()
    settingsFileRead = settingsFileRead.replace("placeholderIlastik", ilastikPath)
    settingsFileWrite = open(maindir + "ClearMap/Settings.py", "w")
    settingsFileWrite.write(settingsFileRead)


"""
If firstSetup is true a tkinter gui is called which lets the user give the path to their installation of elastix and
Ilastik. The path to elastix is obligated. The path to Ilastik is not necessary.
.
"""
if firstSetup:
    root = tk.Tk()
    root.title("Clearmap")
    style = ttk.Style(root)
    style.theme_use("clam")
    tk.Label(root, text="It looks like this is your first time running this program").grid(padx=4, pady=4, sticky='ew')
    tk.Label(root, text="Please refer to the requirements file for all the downloads").grid(padx=4, pady=4, sticky='ew')
    tk.Label(root, text="The path to where elastix is located is mandatory").grid(padx=4, pady=4, sticky='ew')
    tk.Label(root, text="The path to ilastik can be left empty if you dont want to use it").grid(padx=4, pady=4,
                                                                                                 sticky='ew')

    pathElastixButton = tk.Button(root, text="Search elastix", command=searchElastix)
    pathElastixButton.grid(padx=4, pady=4, sticky='ew')

    pathIlastikButton = tk.Button(root, text="Search Ilastik", command=searchIlastik)
    pathIlastikButton.grid(padx=4, pady=4, sticky='ew')

    quitButton = tk.Button(root, state=tk.DISABLED, text="Run clearmap", command=root.destroy)
    quitButton.grid(padx=4, pady=4, sticky='ew')

    root.mainloop()

run_gui()
