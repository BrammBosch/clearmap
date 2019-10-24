import tkinter as tk

from ClearMap.gui.tools.arivisCelDetection import cel_detection
from ClearMap.gui.tools.killProgram import kill


def import_cell(root, pathClearMap):
    """
    This is the window from where the user can import their own cell detection
    :param root: root is the mainloop where import_cell creates a toplevel from
    :param pathClearMap: The path to the gui
    :return:
    """
    importCellWindow = tk.Toplevel(root)
    importCellWindow.title("Clearmap")

    tk.Label(importCellWindow, text="""
     Please choose a csv file which contains the x y and z coordinates of the detect cells. Or choose an exported
     arivis file.
     """).grid(padx=4, pady=4, sticky='ew')
    findCellFile = tk.Button(importCellWindow, text="Search for the landmarks file",
                                    command=lambda: [cel_detection(importCellWindow, pathClearMap),
                                                     importCellWindow.destroy()])
    findCellFile.grid(padx=4, pady=4, sticky='ew')

    def cel_window_quit():
        """
        If the window is closed this function is called which sets the kill parameter to True and stops the pipeline
        béfore it can run.
        :return:
        """
        kill(pathClearMap)

        importCellWindow.destroy()

    importCellWindow.protocol("WM_DELETE_WINDOW", cel_window_quit)

    importCellWindow.wait_window(importCellWindow)
