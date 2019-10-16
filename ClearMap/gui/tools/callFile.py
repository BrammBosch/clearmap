import json
from distutils.dir_util import copy_tree
from tkinter import messagebox

from tkfilebrowser import askopendirname

from ClearMap.gui.tools.importCells import import_cell
from ClearMap.gui.windows.manualAlign import manual


def call_file(root,pathClearMap):
    """
    This is the last function that is called, it runs the process_template file which starts clearmap.
    It also checks if it should kill the program before it begins by looking at the kill parameter in the
    saved settings file.
    :return:
    """

    with open(pathClearMap + "ClearMap/Scripts/work_dir/savedSettings.txt") as json_file:
        dataLoaded = json.load(json_file)
    if not dataLoaded['kill']:
        if "Import" in dataLoaded['cellDetection']:
            import_cell(root, pathClearMap)
        if "Manual" in dataLoaded['alignmentOperation']:
            manual(root, pathClearMap)


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

    #textVar.set("Done with the current operation")
    if not dataLoaded['kill']:
        if dataLoaded['baseDir'] == pathClearMap + "ClearMap/clearmap_preset_folder/output":
            try:
                if messagebox.askyesno("Finished", "Succesfully ran clearmap with the selected settings,"
                                                   "would you like to save the output?"):

                    saveLocation = askopendirname(parent=root, title="Select a folder to save the output")
                    if saveLocation == "":
                        raise FileNotFoundError
                    else:
                        saveLocation = str(saveLocation) + "/results"
                        print(saveLocation)
                        copy_tree(pathClearMap + "ClearMap/clearmap_preset_folder/output", saveLocation)
                        messagebox.showinfo("Finished", "Everything has been saved succesfully")

            except FileNotFoundError:
                pass
        else:
            messagebox.askyesno("Finished", "Succesfully ran clearmap with the selected settings")
