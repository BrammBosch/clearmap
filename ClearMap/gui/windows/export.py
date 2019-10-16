import os
import shutil
from tkinter import simpledialog, messagebox


def export(pathClearMap):
    """
    This function prompts the user for a name and creates a folder in the /Scripts/exports directory
    with that name in which the parameter, process and settings files are stored.
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
    except TypeError:
        pass