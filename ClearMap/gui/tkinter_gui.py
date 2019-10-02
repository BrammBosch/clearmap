import glob, os
import multiprocessing
import re
import shutil
import subprocess
import sys
import threading
import tkinter
import json
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import simpledialog, messagebox
from tkfilebrowser import askopendirname

from ClearMap.gui.create_parameter import create_file_parameter
from ClearMap.gui.create_process import create_file_process

root = tk.Tk()
root.title("Clearmap")
style = ttk.Style(root)
style.theme_use("clam")

pathToGui = os.path.abspath(__file__)
pathClearMap = pathToGui.replace("ClearMap/gui/tkinter_gui.py", "")
#sys.stdout = open(pathClearMap + "ClearMap/myprog.log", "w+")

def choose_dirs():
    """
    This function lets the user choose their own directories where all the files will be found.
    It saved all relevant data in the local json file
    :return:
    """

    try:
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
            fileProtein = re.sub(r'(Z)[0-9][0-9][0-9][0-9]', 'Z\d{4}', fileProtein)
            fileAutoFluo = re.sub(r'(Z)[0-9][0-9][0-9][0-9]', 'Z\d{4}', fileAutoFluo)
        except:
            pass
        autoFluoDir += "/" + fileAutoFluo
        proteinDir += "/" + fileProtein


        data = {}
        data['autoFluoDir'] = autoFluoDir
        data['proteinDir'] = proteinDir
        data['atlasDir'] = atlasDir
        data['baseDir'] = baseDir
        data['fromSettings'] = False

        with open(pathClearMap + "ClearMap/Scripts/work_dir/savedSettings.txt", "w+") as outputFile:
            json.dump(data, outputFile)

        create_files()
        runButton['state'] = 'normal'
        exportButton['state'] = 'normal'
        settingsButton['state'] = 'normal'
    except FileNotFoundError:
        pass
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
    data = {}

    data['autoFluoDir'] = pathAutoFluo
    data['proteinDir'] = pathProtein
    data['atlasDir'] = pathAtlas
    data['baseDir'] = pathBaseDirectory
    data['fromSettings'] = False

    with open(pathClearMap + "ClearMap/Scripts/work_dir/savedSettings.txt", "w+") as outputFile:
        json.dump(data, outputFile)
    create_files()
    runButton['state'] = 'normal'
    exportButton['state'] = 'normal'
    settingsButton['state'] = 'normal'


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

    runButton['state'] = 'normal'
    exportButton['state'] = 'normal'
    settingsButton['state'] = 'normal'
    text_var.set("Imported folder " + nameFolder)
    create_files()


def create_settings_window():
    """
    This function creates a second window for the gui where all the setting options are visualised.
    Any options chosen will be automatically written into the files in the work_dir
    :return:
    """
    window = tk.Toplevel(root)
    window.title("Settings")
    varCelDetection = tk.StringVar(window)
    varAlignmentData = tk.StringVar(window)

    with open(pathClearMap + "ClearMap/Scripts/work_dir/savedSettings.txt", "r") as outputFile:
        data = json.load(outputFile)

    # Dictionary with options for the drop down options
    internalClearmapDetectionChoice = 'Internal clearmap cel detection'
    importChoice = 'Import your own cel detection'
    arivisChoice = 'Use arivis'
    internalClearmapAlignChoice = 'Internal clearmap alignment'
    manualChoice = "Manual using imageJ"
    machineLearningChoice = "Machine learning"

    choicesCelDetection = {internalClearmapDetectionChoice, importChoice, arivisChoice}
    choicesAlignmentOperation = {internalClearmapAlignChoice, manualChoice, machineLearningChoice}

    if data['fromSettings'] == True:
        if data['alignmentOperation'] == internalClearmapAlignChoice:
            varAlignmentData.set(internalClearmapAlignChoice)
        if data['alignmentOperation'] == manualChoice:
            varAlignmentData.set(manualChoice)
        if data['alignmentOperation'] == machineLearningChoice:
            varAlignmentData.set(machineLearningChoice)
        if data['celDetection'] == internalClearmapDetectionChoice:
            varCelDetection.set(internalClearmapDetectionChoice)
        if data['celDetection'] == importChoice:
            varCelDetection.set(importChoice)
        if data['celDetection'] == arivisChoice:
            varCelDetection.set(arivisChoice)
    else:
        varAlignmentData.set(internalClearmapAlignChoice)
        varCelDetection.set(internalClearmapDetectionChoice)

    popupMenuCelDetection = tk.OptionMenu(window, varCelDetection, *choicesCelDetection)
    popupMenuAlignmentOperation = tk.OptionMenu(window, varAlignmentData, *choicesAlignmentOperation)

    tk.Label(window, text="Choose a way to detect cells").grid(row=1, column=1)
    popupMenuCelDetection.grid(row=2, column=1)
    tk.Label(window, text="Choose a way to the alignment operations").grid(row=3, column=1)
    popupMenuAlignmentOperation.grid(row=4, column=1)

    table = tk.BooleanVar()
    heatmap = tk.BooleanVar()

    if data['fromSettings'] == True:

        if data['table'] == True:
            table.set(True)
        if data['heatmap'] == True:
            heatmap.set(True)
    else:
        table.set(True)
        heatmap.set(True)
    checkTable = tk.Checkbutton(window, text="Generate a table", var=table)
    checkTable.grid(row=5, column=1)

    checkHeat = tk.Checkbutton(window, text="Generate a heatmap", var=heatmap)
    checkHeat.grid(row=6, column=1)

    textX = tk.Entry(window, width=10)
    textY = tk.Entry(window, width=10)
    textZ = tk.Entry(window, width=10)

    textXAtlas = tk.Entry(window, width=10)
    textYAtlas = tk.Entry(window, width=10)
    textZAtlas = tk.Entry(window, width=10)

    if data['fromSettings'] == True:
        textX.insert(0, data['realX'])
        textY.insert(0, data['realY'])
        textZ.insert(0, data['realZ'])
        textXAtlas.insert(0, data['atlasX'])
        textYAtlas.insert(0, data['atlasY'])
        textZAtlas.insert(0, data['atlasZ'])

    textX.grid(row=7, column=1)
    textY.grid(row=8, column=1)
    textZ.grid(row=9, column=1)

    tk.Label(window, text="X axis resolution in μm/px = ").grid(row=7, column=0, padx=4, pady=4, sticky='ew')
    tk.Label(window, text="Y axis resolution in μm/px = ").grid(row=8, column=0, padx=4, pady=4, sticky='ew')
    tk.Label(window, text="Z axis resolution in μm/px = ").grid(row=9, column=0, padx=4, pady=4, sticky='ew')

    textXAtlas.grid(row=10, column=1)
    textYAtlas.grid(row=11, column=1)
    textZAtlas.grid(row=12, column=1)

    tk.Label(window, text="Atlas X axis resolution in μm/px = ").grid(row=10, column=0, padx=4, pady=4, sticky='ew')
    tk.Label(window, text="Atlas Y axis resolution in μm/px = ").grid(row=11, column=0, padx=4, pady=4, sticky='ew')
    tk.Label(window, text="Atlas Z axis resolution in μm/px = ").grid(row=12, column=0, padx=4, pady=4, sticky='ew')

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
            realX = realX.replace(",", ".").replace(" ", "")
            realY = realY.replace(",", ".").replace(" ", "")
            realZ = realZ.replace(",", ".").replace(" ", "")

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

        data['fromSettings'] = True
        data['realX'] = realX
        data['realY'] = realY
        data['realZ'] = realZ
        data['atlasX'] = atlasX
        data['atlasY'] = atlasY
        data['atlasZ'] = atlasZ
        data['table'] = table.get()
        data['heatmap'] = heatmap.get()
        data['alignmentOperation'] = varAlignmentData.get()
        data['celDetection'] = varCelDetection.get()

        with open(pathClearMap + "ClearMap/Scripts/work_dir/savedSettings.txt", "w") as outputFile:
            json.dump(data, outputFile)

        create_files()
        saveStatus.set("Settings saved")

    saveStatus = tk.StringVar(window)
    saveStatus.set("")
    tk.Label(window, textvariable=saveStatus).grid(row=0, column=0, padx=4, pady=4, sticky='ew')

    saveButton = tk.Button(window, text="Implement changes", command=save)
    saveButton.grid(column=1, padx=4, pady=4, sticky='ew')

    quitButton = tk.Button(window, text="Quit", command=window.destroy)
    quitButton.grid(column=2, padx=4, pady=4, sticky='ew')


def call_file():
    """
    def tee_pipe(pipe, f1, f2):
        for line in pipe:
            f1.write(line)
            f2.write(line)

    proc = subprocess.Popen(['sudo', pathClearMap + 'ClearMap/Scripts/work_dir/process_template.py'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)

    # Open the output files for stdout/err in unbuffered mode.
    out_file = open(pathClearMap + "ClearMap/myprog.log", "wb", 0)
    err_file = open(pathClearMap + "ClearMap/myprog2.log", "wb", 0)

    stdout = sys.stdout
    stderr = sys.stderr

    # On Python3 these are wrapped with BufferedTextIO objects that we don't
    # want.
    if sys.version_info[0] >= 3:
        stdout = stdout.buffer
        stderr = stderr.buffer

    # Start threads to duplicate the pipes.
    out_thread = threading.Thread(target=tee_pipe,
                                  args=(proc.stdout, out_file, stdout))
    err_thread = threading.Thread(target=tee_pipe,
                                  args=(proc.stderr, err_file, stderr))

    out_thread.start()
    err_thread.start()

    # Wait for the command to finish.
    proc.wait()

    # Join the pipe threads.
    out_thread.join()
    err_thread.join()

    #sys.stdout = open(pathClearMap + "ClearMap/myprog.log", "a")
    #subprocess.call(['ls','-l'], stdout=f)
    #subprocess.call(['sudo', pathClearMap + 'ClearMap/Scripts/work_dir/process_template.py'], stdout=f)

    """    
    try:
        exec(open(pathClearMap + "ClearMap/Scripts/work_dir/process_template.py").read())
    except Exception as e:
        print(e)

    text_var.set("Done with the current operation")



presetButton = tk.Button(root, text="Use preset folder", command=use_presets)
manualButton = tk.Button(root, text="Choose each folder", command=choose_dirs)
quitButton = tk.Button(root, text="Quit", command=lambda: [root.destroy, sys.exit()])
exportButton = tk.Button(root, text="Export scripts with current settings", state=tk.DISABLED, command=export)
importButton = tk.Button(root, text="import scripts with saved settings", command=importer)
runButton = tk.Button(root, text="Run", state=tk.DISABLED, command=call_file)
settingsButton = tk.Button(root, text="Settings", state=tk.DISABLED, command=create_settings_window)
presetButton.grid(row=1, column=0, padx=4, pady=4, sticky='ew')
manualButton.grid(row=2, column=0, padx=4, pady=4, sticky='ew')
quitButton.grid(row=5, column=2, padx=4, pady=4, sticky='ew')
exportButton.grid(row=3, column=1, padx=4, pady=4, sticky='ew')
importButton.grid(row=3, column=0, padx=4, pady=4, sticky='ew')
runButton.grid(row=5, column=0, padx=4, pady=4, sticky='ew')
settingsButton.grid(row=4, column=0, padx=4, pady=4, sticky='ew')

text_var = tk.StringVar(root)
text_var.set("Please choose an action")
tk.Label(root, textvariable=text_var).grid(row=1, column=2, padx=4, pady=4, sticky='ew')


def run_gui():
    """
    This function starts by clearing out the work_dir folder.
    It then starts the GUI
    :return:
    """
    folder = pathClearMap + "ClearMap/clearmap_preset_folder/output"
    try:  # This clears the output folder in the preset.
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(e)

        folder = pathClearMap + "ClearMap/Scripts/work_dir"
        # This empties the work directory before the gui runs
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(e)
    except:
        pass
    root.mainloop()

class sameFolderProteinAutoFluo(Exception):
    pass
class sameFolderAtlas(Exception):
    pass