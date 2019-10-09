import glob
import json
import os
import re
import shutil
import sys
import tkinter as tk
import tkinter.ttk as ttk


from tkinter import simpledialog, messagebox

from tkfilebrowser import askopendirname, askopenfilename

from ClearMap.Scripts.Templates.split_CSV import write_landmarks_to_files
from ClearMap.gui.create_parameter import create_file_parameter
from ClearMap.gui.create_process import create_file_process

root = tk.Tk()


root.title("Clearmap")
style = ttk.Style(root)
style.theme_use("clam")

pathToGui = os.path.abspath(__file__)
pathClearMap = pathToGui.replace("ClearMap/gui/tkinter_gui.py", "")



def choose_dirs():
    """
    This function lets the user choose their own directories where all the files will be found.
    It saved all relevant data in the local json file
    :return:
    """

    try:
        data = {}


        autoFluoDir = askopendirname(parent=root, title="Select auto fluo folder")
        if autoFluoDir == "":
            raise FileNotFoundError
        proteinDir = askopendirname(parent=root, title="Select protein folder")
        if proteinDir == "":
            raise FileNotFoundError
        atlasDir = askopendirname(parent=root, title="Select atlas folder")
        if atlasDir == "":
            raise FileNotFoundError
        baseDir = askopendirname(parent=root, title="Select output folder")
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
            fileProtein = re.sub(r'Z[0-9]{4}}', 'Z\d{4}', fileProtein)
            fileAutoFluo = re.sub(r'Z[0-9]{4}', 'Z\d{4}', fileAutoFluo)
        except:
            pass
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
        messagebox.showinfo("ERROR", "whoops")
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


def use_presets():
    """
    This function uses the 4 standard folders where the user can paste all their data
    :return:
    """
    data = {}

    pathAutoFluo = pathClearMap + "ClearMap/clearmap_preset_folder/auto_fluo"
    pathProtein = pathClearMap + "ClearMap/clearmap_preset_folder/protein"
    pathAtlas = pathClearMap + "ClearMap/clearmap_preset_folder/atlas"
    pathBaseDirectory = pathClearMap + "ClearMap/clearmap_preset_folder/output"
    text_var.set("Used preset folders")

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
        fileProtein = re.sub(r'(Z)[0-9][0-9][0-9][0-9]', 'Z\d{4}', fileProtein)
        fileAutoFluo = re.sub(r'(Z)[0-9][0-9][0-9][0-9]', 'Z\d{4}', fileAutoFluo)
    except:
        pass
    pathAutoFluo += "/" + fileAutoFluo
    pathProtein += "/" + fileProtein

    data['autoFluoDir'] = pathAutoFluo
    data['proteinDir'] = pathProtein
    data['atlasDir'] = pathAtlas
    data['baseDir'] = pathBaseDirectory
    data['fromImport'] = False

    with open(pathClearMap + "ClearMap/Scripts/work_dir/savedSettings.txt", "w+") as outputFile:
        json.dump(data, outputFile)

    runButtonMain['state'] = 'normal'


def create_files():
    """
    This function call 2 different functions which create the parameter and the process template file.
    They are saved in the work_dir and deleten en rewritten on start up and every change.
    :return:
    """
    create_file_parameter(pathClearMap)
    create_file_process(pathClearMap)


def export():
    """
    This function prompts the user for a name and creates a folder in the /Scripts/exports directory
    with that name in which the parameter and process file are stored.
    :return:
    """
    try:
        nameFolder = simpledialog.askstring(title="Export scripts", prompt="Name these settings:")

        os.mkdir(pathClearMap + "ClearMap/Scripts/exports/" + nameFolder)
        shutil.copy(pathClearMap + "ClearMap/Scripts/work_dir/parameter_file.py",
                    pathClearMap + "ClearMap/Scripts/exports/" + nameFolder)
        shutil.copy(pathClearMap + "ClearMap/Scripts/work_dir/process_template.py",
                    pathClearMap + "ClearMap/Scripts/exports/" + nameFolder)
        shutil.copy(pathClearMap + "ClearMap/Scripts/work_dir/savedSettings.txt",
                    pathClearMap + "ClearMap/Scripts/exports/" + nameFolder)
    except FileExistsError:
        messagebox.showinfo("ERROR", "A save under this name already exists")


def importer():
    """
    The importer function copies the parameter and process file to the work_dir directory.
    It starts looking in the exports folder but if any files were copied it is also possible to point it to another
    directory
    :return:
    """

    scriptsFolder = askopendirname(parent=root, title="Select scripts",
                                   initialdir=pathClearMap + "ClearMap/Scripts/exports/")
    nameFolder = scriptsFolder.replace(pathClearMap + "ClearMap/Scripts/exports/", "")
    shutil.copy(scriptsFolder + "/parameter_file.py", pathClearMap + "ClearMap/Scripts/work_dir/")
    shutil.copy(scriptsFolder + "/process_template.py", pathClearMap + "ClearMap/Scripts/work_dir/")
    shutil.copy(scriptsFolder + "/savedSettings.txt", pathClearMap + "ClearMap/Scripts/work_dir/")

    runButtonMain['state'] = 'normal'
    text_var.set("Imported folder " + nameFolder)
    with open(pathClearMap + "ClearMap/Scripts/work_dir/savedSettings.txt", "r") as outputFile:
        data = json.load(outputFile)
    data['fromImport'] = True

    with open(pathClearMap + "ClearMap/Scripts/work_dir/savedSettings.txt", "w+") as outputFile:
        json.dump(data, outputFile)


def create_settings_window(nextButton):
    """
    This function creates a second window for the gui where all the setting options are visualised.
    Any options chosen will be automatically written into the files in the work_dir
    :return:
    """
    nextButton['state'] = 'disabled'

    settingsWindow = tk.Toplevel(root)
    settingsWindow.title("Settings")

    with open(pathClearMap + "ClearMap/Scripts/work_dir/savedSettings.txt", "r") as outputFile:
        data = json.load(outputFile)

    # Dictionary with options for the drop down options

    textX = tk.Entry(settingsWindow, width=10)
    textY = tk.Entry(settingsWindow, width=10)
    textZ = tk.Entry(settingsWindow, width=10)

    textXAtlas = tk.Entry(settingsWindow, width=10)
    textYAtlas = tk.Entry(settingsWindow, width=10)
    textZAtlas = tk.Entry(settingsWindow, width=10)

    if data['fromImport'] == True:
        textX.insert(0, data['realX'])
        textY.insert(0, data['realY'])
        textZ.insert(0, data['realZ'])
        textXAtlas.insert(0, data['atlasX'])
        textYAtlas.insert(0, data['atlasY'])
        textZAtlas.insert(0, data['atlasZ'])

    tk.Label(settingsWindow, text="X").grid(row=1, column=1, padx=4, pady=4, sticky='ew')
    tk.Label(settingsWindow, text="Y").grid(row=1, column=2, padx=4, pady=4, sticky='ew')
    tk.Label(settingsWindow, text="Z").grid(row=1, column=3, padx=4, pady=4, sticky='ew')

    textX.grid(row=2, column=1)
    textY.grid(row=2, column=2)
    textZ.grid(row=2, column=3)

    tk.Label(settingsWindow, text="axis resolution in μm/px = ").grid(row=2, column=0, padx=4, pady=4, sticky='ew')

    textXAtlas.grid(row=3, column=1)
    textYAtlas.grid(row=3, column=2)
    textZAtlas.grid(row=3, column=3)

    tk.Label(settingsWindow, text="Atlas resolution in μm/px = ").grid(row=3, column=0, padx=4, pady=4,
                                                                       sticky='ew')

    def settings_quit():
        settingsWindow.destroy()  # close the popup
        nextButton['state'] = 'normal'
        with open(pathClearMap + "ClearMap/Scripts/work_dir/savedSettings.txt") as json_file:
            data = json.load(json_file)
        data['kill'] = True
        with open(pathClearMap + "ClearMap/Scripts/work_dir/savedSettings.txt", "w") as outputFile:
            json.dump(data, outputFile)
        listToplevel = []
        for widget in root.winfo_children():
            if isinstance(widget, tk.Toplevel):
                listToplevel.append(widget)
        if len(listToplevel) != 1:
            listToplevel[-1].destroy()

    def save():
        """
        This function takes alle the settings selected by the users and writes them to a local json fikle
        :return:
        """
        realX = textX.get()
        realY = textY.get()
        realZ = textZ.get()
        atlasX = textXAtlas.get()
        atlasY = textYAtlas.get()
        atlasZ = textZAtlas.get()

        if atlasX != "" or atlasY != "" or atlasZ != "":
            atlasX = atlasX.replace(",", ".").replace(" ", "")
            atlasY = atlasY.replace(",", ".").replace(" ", "")
            atlasZ = atlasZ.replace(",", ".").replace(" ", "")

            try:
                float(atlasX) / 2
            except ValueError:
                messagebox.showinfo("ERROR", "Please enter a valid number for the X value")
            try:
                float(atlasY) / 2
            except ValueError:
                messagebox.showinfo("ERROR", "Please enter a valid number for the Y value")
            try:
                float(atlasZ) / 2
            except ValueError:
                messagebox.showinfo("ERROR", "Please enter a valid number for the Z value")
        else:
            messagebox.showinfo("ERROR",
                                "Please enter values for the resolution in the axes. If you don't the standard values X= 25, Y= 25, Z = 25 will be used")
            textXAtlas.insert(0, "25")
            textYAtlas.insert(0, "25")
            textZAtlas.insert(0, "25")
            atlasX = "25"
            atlasY = "25"
            atlasZ = "25"

        if realX != "" or realY != "" or realZ != "":
            realX = realX.replace(",", ".")
            realY = realY.replace(",", ".")
            realZ = realZ.replace(",", ".")

            try:
                float(realX) / 2
            except ValueError:
                messagebox.showinfo("ERROR", "Please enter a valid number for the X value")
            try:
                float(realY) / 2
            except ValueError:
                messagebox.showinfo("ERROR", "Please enter a valid number for the Y value")
            try:
                float(realZ) / 2
            except ValueError:
                messagebox.showinfo("ERROR", "Please enter a valid number for the Z value")
        else:
            messagebox.showinfo("ERROR",
                                "Please enter values for the resolution in the axes. If you don't the standard values X= 4.0625, Y= 4.0625, Z = 3 will be used")
            textX.insert(0, "4.0625")
            textY.insert(0, "4.0625")
            textZ.insert(0, "3")
            realX = "4.0625"
            realY = "4.0625"
            realZ = "3"

        with open(pathClearMap + "ClearMap/Scripts/work_dir/savedSettings.txt") as json_file:
            data = json.load(json_file)

        data['realX'] = realX
        data['realY'] = realY
        data['realZ'] = realZ
        data['atlasX'] = atlasX
        data['atlasY'] = atlasY
        data['atlasZ'] = atlasZ
        data['kill'] = False

        with open(pathClearMap + "ClearMap/Scripts/work_dir/savedSettings.txt", "w") as outputFile:
            json.dump(data, outputFile)

        create_files()
        saveStatus.set("Settings saved")


    saveStatus = tk.StringVar(settingsWindow)
    saveStatus.set("")
    tk.Label(settingsWindow, textvariable=saveStatus).grid(row=0, column=0, padx=4, pady=4, sticky='ew')

    runButton = tk.Button(settingsWindow, text="Implement changes and run clearmap",
                          command=lambda: [save(), create_files(), call_file()])
    runButton.grid(column=4, padx=4, pady=4, sticky='ew')
    runExportButton = tk.Button(settingsWindow, text="save changes and export settings",
                                command=lambda: [save(), create_files(), export()])
    runExportButton.grid(column=4, padx=4, pady=4, sticky='ew')
    settingsWindow.protocol("WM_DELETE_WINDOW", settings_quit)


def create_run_window():
    runWindow = tk.Toplevel(root)
    runWindow.title("Options")

    with open(pathClearMap + "ClearMap/Scripts/work_dir/savedSettings.txt") as json_file:
        data = json.load(json_file)

    varCellDetection = tk.StringVar(runWindow)
    varAlignmentData = tk.StringVar(runWindow)
    internalClearmapDetectionChoice = 'Internal clearmap cell detection'
    importChoice = 'Import your own cell detection'
    #arivisChoice = 'Use arivis'
    internalClearmapAlignChoice = 'Internal clearmap alignment'
    manualChoice = "Manual using imageJ"
    machineLearningChoice = "Machine learning"

    choicesCellDetection = {internalClearmapDetectionChoice, importChoice}
    choicesAlignmentOperation = {internalClearmapAlignChoice, manualChoice, machineLearningChoice}

    if data['fromImport'] == True:
        if data['alignmentOperation'] == internalClearmapAlignChoice:
            varAlignmentData.set(internalClearmapAlignChoice)
        elif data['alignmentOperation'] == manualChoice:
            varAlignmentData.set(manualChoice)
        elif data['alignmentOperation'] == machineLearningChoice:
            varAlignmentData.set(machineLearningChoice)
        if data['cellDetection'] == internalClearmapDetectionChoice:
            varCellDetection.set(internalClearmapDetectionChoice)
        elif data['cellDetection'] == importChoice:
            varCellDetection.set(importChoice)

    else:
        varAlignmentData.set(internalClearmapAlignChoice)
        varCellDetection.set(internalClearmapDetectionChoice)

    popupMenuCelDetection = tk.OptionMenu(runWindow, varCellDetection, *choicesCellDetection)
    popupMenuAlignmentOperation = tk.OptionMenu(runWindow, varAlignmentData, *choicesAlignmentOperation)

    tableBox = tk.BooleanVar()
    heatmapBox = tk.BooleanVar()
    cellDetectionBox = tk.BooleanVar()
    alignmentBox = tk.BooleanVar()
    resampleBox = tk.BooleanVar()

    if data['fromImport']:

        if data['tableBox']:
            tableBox.set(True)
        if data['heatmapBox']:
            heatmapBox.set(True)
        if data['resampleBox']:
            resampleBox.set(True)
        if data['cellDetectionBox']:
            cellDetectionBox.set(True)
        if data['alignmentBox']:
            alignmentBox.set(True)


    else:
        tableBox.set(True)
        heatmapBox.set(True)
        cellDetectionBox.set(True)
        alignmentBox.set(True)
        resampleBox.set(True)

    def run_quit():
        runWindow.destroy()  # close the popup
        runButtonMain['state'] = 'normal'
        with open(pathClearMap + "ClearMap/Scripts/work_dir/savedSettings.txt") as json_file:
            data = json.load(json_file)
        data['kill'] = True
        with open(pathClearMap + "ClearMap/Scripts/work_dir/savedSettings.txt", "w") as outputFile:
            json.dump(data, outputFile)
        for widget in root.winfo_children():
            if isinstance(widget, tk.Toplevel):
                widget.destroy()

    def saveSettings():
        data['tableBox'] = tableBox.get()
        data['heatmapBox'] = heatmapBox.get()
        data['cellDetectionBox'] = cellDetectionBox.get()
        data['alignmentBox'] = alignmentBox.get()
        data['resampleBox'] = resampleBox.get()
        data['alignmentOperation'] = varAlignmentData.get()
        data['cellDetection'] = varCellDetection.get()

        with open(pathClearMap + "ClearMap/Scripts/work_dir/savedSettings.txt", "w") as outputFile:
            json.dump(data, outputFile)

    runButtonMain['state'] = 'disabled'

    checkResample = tk.Checkbutton(runWindow, var=resampleBox)
    checkResample.grid(row=1, column=2)

    checkCelDetection = tk.Checkbutton(runWindow, var=cellDetectionBox)
    checkCelDetection.grid(row=2, column=2)

    checkAlignment = tk.Checkbutton(runWindow, var=alignmentBox)
    checkAlignment.grid(row=3, column=2)

    checkTable = tk.Checkbutton(runWindow, var=tableBox)
    checkTable.grid(row=4, column=2)

    checkHeat = tk.Checkbutton(runWindow, var=heatmapBox)
    checkHeat.grid(row=5, column=2)

    tk.Label(runWindow, text="Choose which parts of the pipeline you want to run").grid(row=0, column=2)

    resampleLabel = tk.Label(runWindow, text="Resample the files")
    resampleLabel.grid(row=1, column=0)

    detectLabel = tk.Label(runWindow, text="Choose a way to detect cells")
    detectLabel.grid(row=2, column=0)

    popupMenuCelDetection.grid(row=2, column=1)

    alignmentLabel = tk.Label(runWindow, text="Choose a way to the alignment operations")
    alignmentLabel.grid(row=3, column=0)
    popupMenuAlignmentOperation.grid(row=3, column=1)

    tableLabel = tk.Label(runWindow, text="Generate a table")
    tableLabel.grid(row=4, column=1)

    heatmapLabel = tk.Label(runWindow, text="generate a heatmap")
    heatmapLabel.grid(row=5, column=1)

    nextButton = tk.Button(runWindow, text="Next", command=lambda: [saveSettings(), create_settings_window(nextButton)])

    nextButton.grid(column=2, padx=4, pady=4, sticky='ew')
    runWindow.protocol("WM_DELETE_WINDOW", run_quit)


def manual():
    manualWindow = tk.Toplevel(root)
    manualWindow.title("Clearmap")

    tk.Label(manualWindow, text="""Open the "autofluo_resampled.tif file and the "template_25.tif" file in ImageJ. 
Go to Plugins -> Big Data Viewer -> Bigwarp. Open template_25 first, then autofluo_resampled. 
In both images, hit Shift + A to flip both to coronal view. 
Scroll around and match the files as closely as possible 
(left click + pull around to tilt your plane of view in 3d. Ctrl + Y to reset to starter view.)
Landmark procedure: 
    click on one of the windows to make sure you are active in the right window. 
    Press Space bar to activate the landmark mode. 
    Click on one of the landmarks. 
    click the other window, re-activate landmark mode by pressing space bar(twice, if need be)
    Mark the same landmark. 
    Repeat until approx. 50-100 landmarks are marked. 
Go to the landmarks window -> File -> Export landmarks. """).grid(padx=4, pady=4, sticky='ew')
    findLandmarksButton = tk.Button(manualWindow, text="Search for the landmarks file",
                                    command=lambda: [findLandmarks(manualWindow, pathClearMap), manualWindow.destroy()])
    findLandmarksButton.grid(padx=4, pady=4, sticky='ew')

    def manual_quit():
        with open(pathClearMap + "ClearMap/Scripts/work_dir/savedSettings.txt") as json_file:
            data = json.load(json_file)
        data['kill'] = True
        with open(pathClearMap + "ClearMap/Scripts/work_dir/savedSettings.txt", "w") as outputFile:
            json.dump(data, outputFile)

        manualWindow.destroy()

    manualWindow.protocol("WM_DELETE_WINDOW", manual_quit)

    manualWindow.wait_window(manualWindow)


def findLandmarks(rootMA, pathClearMap):
    landmarksDir = askopenfilename(parent=rootMA, title="Select landmarks file")
    pathOutput = pathClearMap + "ClearMap/clearmap_preset_folder/output/landmarks.csv"
    try:
        shutil.copyfile(landmarksDir, pathOutput)
        write_landmarks_to_files(pathClearMap)
    except FileNotFoundError:
        with open(pathClearMap + "ClearMap/Scripts/work_dir/savedSettings.txt") as json_file:
            data = json.load(json_file)
        data['kill'] = True
        with open(pathClearMap + "ClearMap/Scripts/work_dir/savedSettings.txt", "w") as outputFile:
            json.dump(data, outputFile)


def call_file():
    text_var.set("Starting")

    with open(pathClearMap + "ClearMap/Scripts/work_dir/savedSettings.txt") as json_file:
        dataLoaded = json.load(json_file)
    if "Manual" in dataLoaded['alignmentOperation']:
        manual()
    with open(pathClearMap + "ClearMap/Scripts/work_dir/savedSettings.txt") as json_file:
        dataLoaded = json.load(json_file)
    if dataLoaded['kill']:
        print("kill")
        with open(pathClearMap + 'ClearMap/Scripts/work_dir/process_template.py', 'r') as file:
            file = file.read()
        output = "sys.exit()\n" + file
        processFile = open(pathClearMap + "ClearMap/Scripts/work_dir/process_template.py", "w+")

        processFile.write(output)

        exec(open(pathClearMap + "ClearMap/Scripts/work_dir/process_template.py").read())
    else:

        exec(open(pathClearMap + "ClearMap/Scripts/work_dir/process_template.py").read())

        """
        proc = subprocess.Popen(['sudo', pathClearMap + "ClearMap/Scripts/work_dir/process_template.py"], shell=False)
        proc.communicate()
      
        p = Popen(['sudo',pathClearMap + "ClearMap/Scripts/work_dir/process_template.py"])
        poll = p.poll()
        while poll == None:
            poll = p.poll()
            time.sleep(5)
            print("yes")
    """
    text_var.set("Done with the current operation")
    messagebox.showinfo("Finished", "Succesfully ran clearmap with the selected settings")


def clear_folder(folder):
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(e)


presetButton = tk.Button(root, text="Use preset folder", command=use_presets)
manualButton = tk.Button(root, text="Choose each folder", command=choose_dirs)
importButton = tk.Button(root, text="import scripts with saved settings", command=importer)
runButtonMain = tk.Button(root, text="Next", state=tk.DISABLED, command=create_run_window)
presetButton.grid(row=1, column=0, padx=4, pady=4, sticky='ew')
manualButton.grid(row=2, column=0, padx=4, pady=4, sticky='ew')
importButton.grid(row=3, column=0, padx=4, pady=4, sticky='ew')
runButtonMain.grid(row=5, column=0, padx=4, pady=4, sticky='ew')

text_var = tk.StringVar(root)
text_var.set("Please choose an action")
tk.Label(root, textvariable=text_var).grid(row=1, column=2, padx=4, pady=4, sticky='ew')


def run_gui():
    """
    This function starts by clearing out the work_dir folder and the output folder.
    It then starts the GUI
    :return:
    """
    try:
        folder = pathClearMap + "ClearMap/clearmap_preset_folder/output"
        # clear_folder(folder)
        # This clears the output folder in the preset.

        folder = pathClearMap + "ClearMap/Scripts/work_dir"
        clear_folder(folder)
        # This empties the work directory before the gui runs
    except:
        pass
    root.mainloop()


class sameFolderProteinAutoFluo(Exception):
    pass


class sameFolderAtlas(Exception):
    pass
