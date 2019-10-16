import glob
import json
import os
import re
import sys
import tkinter as tk
from tkinter import messagebox, filedialog
from ClearMap.errors.customExceptions import *


def choose_dirs(root,pathClearMap,runButtonMain):
    """
    This function lets the user choose their own directories where all the files will be found.
    It saved all relevant data in the local json file.
    Using regex the program checks if file is part of a tif stack where the sequence is labeled by a Z
    followed by a 4 digit number
    :return:
    """

    try:
        data = {}

        autoFluoDir = filedialog.askdirectory(parent=root, title="Select auto fluo folder")
        if autoFluoDir == "":
            raise FileNotFoundError
        proteinDir = filedialog.askdirectory(parent=root, title="Select protein folder")
        if proteinDir == "":
            raise FileNotFoundError
        atlasDir = filedialog.askdirectory(parent=root, title="Select atlas folder")
        if atlasDir == "":
            raise FileNotFoundError
        baseDir = filedialog.askdirectory(parent=root, title="Select output folder")
        if baseDir == "":
            raise FileNotFoundError

        if autoFluoDir == proteinDir:
            raise sameFolderProteinAutoFluo

        if autoFluoDir == atlasDir or proteinDir == atlasDir:
            raise sameFolderAtlas

        try:
            os.chdir(proteinDir)

        except FileNotFoundError:
            messagebox.showinfo("ERROR", "The protein folder doesn't seem to exist")
            sys.exit()
        for file in glob.glob("*.tif"):
            fileProtein = file
            break

        try:
            os.chdir(autoFluoDir)
        except FileNotFoundError:
            messagebox.showinfo("ERROR", "The auto fluo folder doesn't seem to exist")
            sys.exit()

        for file in glob.glob("*.tif"):
            fileAutoFluo = file
            break

        try:
            fileProtein = re.sub(r'Z[0-9]{4}', 'Z\\\\d{4}', fileProtein)
            fileAutoFluo = re.sub(r'Z[0-9]{4}', 'Z\\\\d{4}', fileAutoFluo)
        except Exception as e:
            print(e)
        print(fileProtein)
        print(fileAutoFluo)
        autoFluoDir += "/" + fileAutoFluo
        proteinDir += "/" + fileProtein
        data['autoFluoDir'] = autoFluoDir
        data['proteinDir'] = proteinDir
        data['atlasDir'] = atlasDir
        data['baseDir'] = baseDir
        data['fromImport'] = False

        with open(pathClearMap + "ClearMap/Scripts/work_dir/savedSettings.txt", "w+") as outputFile:
            json.dump(data, outputFile)

        runButtonMain['state'] = 'normal'
    except FileNotFoundError:
        pass
    except tk.TclError:
        pattern = re.compile("(!filebrowser)[2-5]")
        for widget in root.winfo_children():
            if pattern.match(widget.winfo_name()):
                widget.destroy()
    except UnboundLocalError:
        messagebox.showinfo("ERROR", "No tiff files were found in the auto fluo or protein directories ")
    except sameFolderProteinAutoFluo:
        messagebox.showinfo("ERROR", "The autofluo folder and the protein folder seem to be same")
    except sameFolderAtlas:
        messagebox.showinfo("ERROR", "The autofluo folder or the protein folder seem to be same as the atlas folder")
