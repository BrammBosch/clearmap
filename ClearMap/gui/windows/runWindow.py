import json
import tkinter as tk

from ClearMap.gui.windows.customRunOptions import custom_run_options


def create_run_window(root, pathClearMap, runButtonMain, importButton, presetButton, manualButton):
    """
    This function is called after the user has specified where the files are and lets the user
    choose which parts of the pipeline they want to run how they want to execute them.
    :return:


    """
    runWindow = tk.Toplevel(root)
    runWindow.title("Options")

    with open(pathClearMap + "ClearMap/Scripts/work_dir/savedSettings.txt") as json_file:
        data = json.load(json_file)

    varCellDetection = tk.StringVar(runWindow)
    varAlignmentData = tk.StringVar(runWindow)
    internalClearmapDetectionChoice = 'Internal clearmap cell detection'
    importChoice = 'Import your own cell detection'
    # arivisChoice = 'Use arivis'
    internalClearmapAlignChoice = 'Internal clearmap alignment'
    manualChoice = "Manual using imageJ"
    machineLearningChoice = "Machine learning"

    choicesCellDetection = {internalClearmapDetectionChoice, importChoice}
    choicesAlignmentOperation = {internalClearmapAlignChoice, manualChoice, machineLearningChoice}

    if data['fromImport']:
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
        """
        This function is called when the user quits the run options window.
        It enables the use of the button on the previous window and passes a kill parameter to the local settings file.
        This is done so the pipeline isn't able to run on accident without settings freezing the GUI and crashing later
        in the program. It also looks for if a toplevel above this window was opened and closes it so any
        windows which should be inaccessible are not staying open.
        :return:
        """
        runWindow.destroy()  # close the popup
        runButtonMain['state'] = 'normal'
        importButton['state'] = 'normal'
        presetButton['state'] = 'normal'
        manualButton['state'] = 'normal'
        with open(pathClearMap + "ClearMap/Scripts/work_dir/savedSettings.txt") as outputFileRunSettingsKill:
            dataKillRunSettings = json.load(outputFileRunSettingsKill)
        dataKillRunSettings['kill'] = True
        with open(pathClearMap + "ClearMap/Scripts/work_dir/savedSettings.txt", "w") as outputFile:
            json.dump(dataKillRunSettings, outputFile)
        for widget in root.winfo_children():
            if isinstance(widget, tk.Toplevel):
                widget.destroy()

    def saveSettings():
        """
        saveSettings saves the data from the checkboxes and the dropdown menus and writes this data to the local
        json file.
        :return:
        """
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
    importButton['state'] = 'disabled'
    presetButton['state'] = 'disabled'
    manualButton['state'] = 'disabled'

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

    nextButton = tk.Button(runWindow, text="Next",
                           command=lambda: [saveSettings(), custom_run_options(nextButton, pathClearMap, root)])

    nextButton.grid(column=2, padx=4, pady=4, sticky='ew')
    runWindow.protocol("WM_DELETE_WINDOW", run_quit)
