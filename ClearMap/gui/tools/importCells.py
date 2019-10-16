import json
import tkinter as tk

from ClearMap.gui.tools.arivisCelDetection import arivis_cel_detection


def import_cell(root, pathClearMap):
    importCellWindow = tk.Toplevel(root)
    importCellWindow.title("Clearmap")

    tk.Label(importCellWindow, text="""
     
     """).grid(padx=4, pady=4, sticky='ew')
    findCellFile = tk.Button(importCellWindow, text="Search for the landmarks file",
                                    command=lambda: [arivis_cel_detection(importCellWindow, pathClearMap),
                                                     importCellWindow.destroy()])
    findCellFile.grid(padx=4, pady=4, sticky='ew')

    def cel_window_quit():
        """
        If the window is closed this function is called which sets the kill parameter to True which stops the pipeline
        béfore it can run.
        :return:
        """
        with open(pathClearMap + "ClearMap/Scripts/work_dir/savedSettings.txt") as json_file:
            data = json.load(json_file)
        data['kill'] = True
        with open(pathClearMap + "ClearMap/Scripts/work_dir/savedSettings.txt", "w") as outputFile:
            json.dump(data, outputFile)

        importCellWindow.destroy()

    importCellWindow.protocol("WM_DELETE_WINDOW", cel_window_quit)

    importCellWindow.wait_window(importCellWindow)
