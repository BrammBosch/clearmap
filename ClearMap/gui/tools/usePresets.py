import glob
import json
import os
import re
from tkinter import messagebox


def use_presets(pathClearMap, runButtonMain, textVar):
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
    run = True

    try:
        os.chdir(pathAtlas)
    except FileNotFoundError:
        messagebox.showinfo("ERROR", "The atlas folder doesn't seem to exist")
        run = False

    try:
        os.chdir(pathBaseDirectory)
    except FileNotFoundError:
        os.mkdir(pathBaseDirectory)

    try:
        os.chdir(pathAutoFluo)
    except FileNotFoundError:
        messagebox.showinfo("ERROR", "The auto fluo folder doesn't seem to exist")
        run = False
    for file in glob.glob("*.tif"):
        fileAutoFluo = file
        break

    try:
        os.chdir(pathProtein)

    except FileNotFoundError:
        messagebox.showinfo("ERROR", "The protein folder doesn't seem to exist")
        run = False
    for file in glob.glob("*.tif"):
        fileProtein = file
        break

    try:
        fileProtein = re.sub(r'Z[0-9]{4}', 'Z\\\\d{4}', fileProtein)
        fileAutoFluo = re.sub(r'Z[0-9]{4}', 'Z\\\\d{4}', fileAutoFluo)
        # These 2 lines search for a file format where the image stack is made up out of separate images where each
        # has a Z number which corresponds to the Z plane. If this Z number isn't present the program assumes the stack
        # is saved in a single file.
    except Exception as e:
        pass
    if run:
        try:
            pathAutoFluo += "/" + fileAutoFluo
        except UnboundLocalError:
            messagebox.showinfo("ERROR", "The auto fluo folder doesn't contain any tif images")
            run = False
        try:
            pathProtein += "/" + fileProtein
        except UnboundLocalError:
            messagebox.showinfo("ERROR", "The protein folder doesn't contain any tif images")
            run = False

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
    if run:
        runButtonMain['state'] = 'normal'
