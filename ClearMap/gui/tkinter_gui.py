import json
import os
import tkinter as tk
import tkinter.ttk as ttk

from ClearMap.gui.tools.clearFolder import clear_folder
from ClearMap.gui.tools.killProgram import kill
from ClearMap.gui.windows.importer import importer
from ClearMap.gui.windows.runWindow import create_run_window
from ClearMap.gui.windows.chooseDirs import choose_dirs
from ClearMap.gui.tools.usePresets import use_presets

__author__ = "Bram Bosch"

"""
This is the main gui function, from here all other functions can be called.
"""
root = tk.Tk()

root.title("Clearmap")
style = ttk.Style(root)
style.theme_use("clam")

pathToGui = os.path.abspath(__file__)
pathClearMap = pathToGui.replace("ClearMap/gui/tkinter_gui.py", "")
settingsFileRead = open(pathClearMap + "ClearMap/Settings.py").read()

presetButton = tk.Button(root, text="Use preset folder",
                         command=lambda: [use_presets(pathClearMap, runButtonMain, textVar)])
manualButton = tk.Button(root, text="Choose each folder",
                         command=lambda: [choose_dirs(root, pathClearMap, runButtonMain)])
importButton = tk.Button(root, text="import scripts with saved settings",
                         command=lambda: [importer(root, pathClearMap, runButtonMain, textVar)])
runButtonMain = tk.Button(root, text="Next", state=tk.DISABLED, command=lambda: [
    create_run_window(root, pathClearMap, runButtonMain, importButton, presetButton, manualButton)])
presetButton.grid(row=1, column=0, padx=4, pady=4, sticky='ew')
manualButton.grid(row=2, column=0, padx=4, pady=4, sticky='ew')
importButton.grid(row=3, column=0, padx=4, pady=4, sticky='ew')
runButtonMain.grid(row=5, column=0, padx=4, pady=4, sticky='ew')

textVar = tk.StringVar(root)
textVar.set("Please choose an action")
tk.Label(root, textvariable=textVar).grid(row=1, column=2, padx=4, pady=4, sticky='ew')


def root_quit():
    """
    This function is called when the use quits the root function. It kills any running toplevels by destroying itself.
    It also set kill to True so the pipeline can't accidentally run.
    :return:
    """
    root.destroy()
    kill(pathClearMap)


def run_gui():
    """
    This function starts by clearing out the work_dir folder and the output folder.
    It then starts the GUI
    :return:
    """

    folder = pathClearMap + "ClearMap/clearmap_preset_folder/output"
    clear_folder(folder)
    # This clears the output folder in the preset.

    folder = pathClearMap + "ClearMap/Scripts/work_dir"
    clear_folder(folder)
    # This empties the work directory before the gui runs

    root.mainloop()


root.protocol("WM_DELETE_WINDOW", root_quit)
