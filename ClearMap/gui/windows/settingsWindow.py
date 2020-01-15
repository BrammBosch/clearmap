import tkinter as tk
import json
from tkinter import messagebox


from ClearMap.gui.tools.callFile import call_file
from ClearMap.gui.tools.createFiles import create_files
from ClearMap.gui.tools.killProgram import kill
from ClearMap.gui.windows.export import export


def create_settings_window(nextButton,root,pathClearMap):
    """
    This function is called after the user has choosen which parts of the clearmap pipeline to run.
    It creates a tkinter window where the user has to input settings matching his data.
    If the files in the work dir where imported the program automatically fills in the previous settings.
    These can be overruled at any time.
    If the user doesn't input any settings the program gives a warning and uses standard settings so the pipeline can
    continue.
    Opening this step locks the next button on the previous screen so multiple threads won't interfere with the data.
    :return:
    """
    nextButton['state'] = 'disabled'

    settingsWindow = tk.Toplevel(root)
    settingsWindow.title("Settings")

    with open(pathClearMap + "ClearMap/Scripts/work_dir/savedSettings.txt", "r") as outputFile:
        data = json.load(outputFile)

    varFilter = tk.StringVar(settingsWindow)
    filterMean = "uniform averaging filter"
    filterGaussian = "Gaussian filter"
    filterLog = "Laplacian of Gaussian filter (LoG)"
    filterDog = "Difference of Gaussians filter (DoG)"
    filterSphere = "Sphere filter"
    filterDisk = "Disk filter"
    filterNone = "None"

    choicesFilter = {filterMean, filterGaussian, filterLog, filterDog, filterSphere, filterDisk, filterNone}


    if data['fromImport']:
        if data['filterOption'] == filterMean:
            varFilter.set(filterMean)
        elif data['filterOption'] == filterGaussian:
            varFilter.set(filterGaussian)
        elif data['filterOption'] == filterLog:
            varFilter.set(filterLog)
        elif data['filterOption'] == filterDog:
            varFilter.set(filterDog)
        elif data['filterOption'] == filterSphere:
            varFilter.set(filterSphere)
        elif data['filterOption'] == filterDisk:
            varFilter.set(filterDisk)
        elif data['filterOption'] == filterNone:
            varFilter.set(filterNone)
    else:
        varFilter.set(filterMean)


    popupMenuFilter = tk.OptionMenu(settingsWindow, varFilter, *choicesFilter)


    textX = tk.Entry(settingsWindow, width=10)
    textY = tk.Entry(settingsWindow, width=10)
    textZ = tk.Entry(settingsWindow, width=10)

    textXAtlas = tk.Entry(settingsWindow, width=10)
    textYAtlas = tk.Entry(settingsWindow, width=10)
    textZAtlas = tk.Entry(settingsWindow, width=10)

    textBackgroundRemovalX = tk.Entry(settingsWindow, width=10)
    textBackgroundRemovalY = tk.Entry(settingsWindow, width=10)



    if data['fromImport']:
        textX.insert(0, data['realX'])
        textY.insert(0, data['realY'])
        textZ.insert(0, data['realZ'])
        textXAtlas.insert(0, data['atlasX'])
        textYAtlas.insert(0, data['atlasY'])
        textZAtlas.insert(0, data['atlasZ'])
        textBackgroundRemovalX.insert(0, data['backgroundRemY'])
        textBackgroundRemovalY.insert(0, data['backgroundRemX'])

    #tk.Label(settingsWindow, text="X").grid(row=1, column=1, padx=4, pady=4, sticky='ew')
    #tk.Label(settingsWindow, text="Y").grid(row=1, column=2, padx=4, pady=4, sticky='ew')
    #tk.Label(settingsWindow, text="Z").grid(row=1, column=3, padx=4, pady=4, sticky='ew')

    textX.grid(row=2, column=1)
    textY.grid(row=2, column=2)
    textZ.grid(row=2, column=3)

    tk.Label(settingsWindow, text="Axis resolution in μm/px (X, Y, Z) = ").grid(row=2, column=0, padx=4, pady=4, sticky='ew')

    textXAtlas.grid(row=3, column=1)
    textYAtlas.grid(row=3, column=2)
    textZAtlas.grid(row=3, column=3)

    tk.Label(settingsWindow, text="Atlas resolution in μm/px (X, Y, Z) = ").grid(row=3, column=0, padx=4, pady=4,
                                                                       sticky='ew')



    textBackgroundRemovalX.grid(row=5,column=1)
    textBackgroundRemovalY.grid(row=5,column=2)


    tk.Label(settingsWindow, text="Height and width of the cicle matrix used for the background removal (None will disable filter) = ").grid(
        row=5, column=0, padx=4, pady=4, sticky='ew')

    tk.Label(settingsWindow,
             text="Choose an filter option ot perform on the images = ").grid(
        row=6, column=0, padx=4, pady=4, sticky='ew')

    popupMenuFilter.grid(row=6, column=1)


    def settings_quit():
        """
        This function is called when the user quits the settings window.
        It enables the use of the button on the previous window and passes a kill parameter to the local settings file.
        This is done so the pipeline isn't able to run on accident without settings freezing the GUI and crashing later
        in the program. It also looks for if a toplevel above this window was opened and closes it so any
        windows which should be inaccessible are not staying open.
        :return:
        """
        settingsWindow.destroy()  # close the popup
        nextButton['state'] = 'normal'
        kill(pathClearMap)

        listToplevel = []
        for widget in root.winfo_children():
            if isinstance(widget, tk.Toplevel):
                listToplevel.append(widget)
        if len(listToplevel) != 1:
            listToplevel[-1].destroy()

    def save():
        """
        This function takes alle the settings selected by the users and writes them to a local json file.
        It also checks whether the entered settings are valid.
        :return:
        """
        with open(pathClearMap + "ClearMap/Scripts/work_dir/savedSettings.txt") as json_file:
            dataSettings = json.load(json_file)
        realX = textX.get()
        realY = textY.get()
        realZ = textZ.get()
        atlasX = textXAtlas.get()
        atlasY = textYAtlas.get()
        atlasZ = textZAtlas.get()
        backgroundRemovalX = textBackgroundRemovalX.get()
        backgroundRemovalY = textBackgroundRemovalY.get()


        run = True
        if atlasX != "" or atlasY != "" or atlasZ != "":
            atlasX = atlasX.replace(",", ".").replace(" ", "")
            atlasY = atlasY.replace(",", ".").replace(" ", "")
            atlasZ = atlasZ.replace(",", ".").replace(" ", "")

            try:
                float(atlasX) / 2
            except ValueError:
                messagebox.showinfo("ERROR", "Please enter a valid number for the X value of the atlas")
                run = False
            try:
                float(atlasY) / 2
            except ValueError:
                messagebox.showinfo("ERROR", "Please enter a valid number for the Y value of the atlas")
                run = False
            try:
                float(atlasZ) / 2
            except ValueError:
                messagebox.showinfo("ERROR", "Please enter a valid number for the Z value of the atlas")
                run = False
        else:
            messagebox.showinfo("ERROR",
                                "Please enter values for the atlas resolution in the axes. If you don't the standard "
                                "values X= 25, Y= 25, Z = 25 will be used")
            textXAtlas.insert(0, "25")
            textYAtlas.insert(0, "25")
            textZAtlas.insert(0, "25")
            atlasX = "25"
            atlasY = "25"
            atlasZ = "25"
            run = False

        if realX != "" or realY != "" or realZ != "":
            realX = realX.replace(",", ".")
            realY = realY.replace(",", ".")
            realZ = realZ.replace(",", ".")

            try:
                float(realX) / 2
            except ValueError:
                messagebox.showinfo("ERROR", "Please enter a valid number for the X value of the resolution")
                run = False
            try:
                float(realY) / 2
            except ValueError:
                messagebox.showinfo("ERROR", "Please enter a valid number for the Y value of the resolution")
                run = False
            try:
                float(realZ) / 2
            except ValueError:
                messagebox.showinfo("ERROR", "Please enter a valid number for the Z value of the resolution")
                run = False
        else:
            messagebox.showinfo("ERROR",
                                "Please enter values for the resolution in the axes. If you don't the standard values "
                                "X= 4.0625, Y= 4.0625, Z = 3 will be used")
            textX.insert(0, "4.0625")
            textY.insert(0, "4.0625")
            textZ.insert(0, "3")
            realX = "4.0625"
            realY = "4.0625"
            realZ = "3"
            run = False

        if backgroundRemovalY != "" or backgroundRemovalX != "":

            try:
                float(realX) / 2
            except ValueError:
                messagebox.showinfo("ERROR", "Please enter a valid number for the X value of the matrix")
                run = False
            try:
                float(realY) / 2
            except ValueError:
                messagebox.showinfo("ERROR", "Please enter a valid number for the Y value of the matrix")
                run = False
        else:
            messagebox.showinfo("ERROR",
                                "Please enter values for the size of the matrix. Else standard values 7 by 7 will be used")
            textBackgroundRemovalX.insert(0, "7")
            textBackgroundRemovalY.insert(0, "7")
            realX = "7"
            realY = "7"
            run = False


        dataSettings['filterOption'] = varFilter.get()
        dataSettings['backgroundRemX'] = backgroundRemovalX
        dataSettings['backgroundRemY'] = backgroundRemovalY
        dataSettings['realX'] = realX
        dataSettings['realY'] = realY
        dataSettings['realZ'] = realZ
        dataSettings['atlasX'] = atlasX
        dataSettings['atlasY'] = atlasY
        dataSettings['atlasZ'] = atlasZ


        if not run:
            dataSettings['kill'] = True
        else:
            dataSettings['kill'] = False

        with open(pathClearMap + "ClearMap/Scripts/work_dir/savedSettings.txt", "w") as outputFileSettings:
            json.dump(dataSettings, outputFileSettings)

        create_files(pathClearMap)
        saveStatus.set("Settings saved")

    saveStatus = tk.StringVar(settingsWindow)
    saveStatus.set("")
    tk.Label(settingsWindow, textvariable=saveStatus).grid(row=0, column=0, padx=4, pady=4, sticky='ew')

    runButton = tk.Button(settingsWindow, text="Implement changes and run clearmap",
                          command=lambda: [save(), create_files(pathClearMap), call_file(root,pathClearMap)])
    runButton.grid(column=4, padx=4, pady=4, sticky='ew')
    runExportButton = tk.Button(settingsWindow, text="save changes and export settings",
                                command=lambda: [save(), create_files(pathClearMap), export(pathClearMap)])
    runExportButton.grid(column=4, padx=4, pady=4, sticky='ew')
    settingsWindow.protocol("WM_DELETE_WINDOW", settings_quit)

