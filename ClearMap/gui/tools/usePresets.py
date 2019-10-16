import glob
import json
import os
import re
import sys
from tkinter import messagebox


def use_presets(pathClearMap,runButtonMain,textVar):
    """
    This function uses the 4 standard folders where the user can paste all their data so they don't have to search for
    it each time. Using regex the program checks if file is part of a tif stack where the sequence is labeled by a Z f
    ollowed by a 4 digit number. The standard paths are then stored in a local json file.
    :return:
    """
    data = {}

    pathAutoFluo = pathClearMap + "ClearMap/clearmap_preset_folder/auto_fluo"
    pathProtein = pathClearMap + "ClearMap/clearmap_preset_folder/protein"
    pathAtlas = pathClearMap + "ClearMap/clearmap_preset_folder/atlas"
    pathBaseDirectory = pathClearMap + "ClearMap/clearmap_preset_folder/output"
    textVar.set("Used preset folders")

    try:
        os.chdir(pathProtein)

    except FileNotFoundError:
        messagebox.showinfo("ERROR", "The protein folder doesn't seem to exist")
        sys.exit()
    for file in glob.glob("*.tif"):
        fileProtein = file
        break

    try:
        os.chdir(pathAutoFluo)
    except FileNotFoundError:
        messagebox.showinfo("ERROR", "The auto fluo folder doesn't seem to exist")
        sys.exit()
    for file in glob.glob("*.tif"):
        fileAutoFluo = file
        break

    try:
        fileProtein = re.sub(r'Z[0-9]{4}', 'Z\\\\d{4}', fileProtein)
        fileAutoFluo = re.sub(r'Z[0-9]{4}', 'Z\\\\d{4}', fileAutoFluo)
    except:
        pass
    pathAutoFluo += "/" + fileAutoFluo
    pathProtein += "/" + fileProtein

    data['autoFluoDir'] = pathAutoFluo
    data['proteinDir'] = pathProtein
    data['atlasDir'] = pathAtlas
    data['baseDir'] = pathBaseDirectory
    data['fromImport'] = False
    try:
        with open(pathClearMap + "ClearMap/Scripts/work_dir/savedSettings.txt", "w+") as outputFile:
            json.dump(data, outputFile)
    except FileNotFoundError:
        os.mkdir(pathClearMap + "ClearMap/Scripts/work_dir")
        with open(pathClearMap + "ClearMap/Scripts/work_dir/savedSettings.txt", "w+") as outputFile:
            json.dump(data, outputFile)
    runButtonMain['state'] = 'normal'