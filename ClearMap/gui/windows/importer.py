import json
import shutil

from tkfilebrowser import askopendirname


def importer(root,pathClearMap,runButtonMain,textVar):
    """
    The importer function copies the parameter, process and settings files to the work_dir directory.
    It starts looking in the exports folder but if any files were copied it is also possible to point it to another
    directory
    :return: If a file is part of a tif stack where the sequence is labeled by a Z followed by a 4 digit number this is
    found using regex and the code is adjusted to fit these images.
    """
    try:
        scriptsFolder = askopendirname(parent=root, title="Select scripts",
                                       initialdir=pathClearMap + "ClearMap/Scripts/exports/")
        nameFolder = scriptsFolder.replace(pathClearMap + "ClearMap/Scripts/exports/", "")
        shutil.copy(scriptsFolder + "/parameter_file.py", pathClearMap + "ClearMap/Scripts/work_dir/")
        shutil.copy(scriptsFolder + "/process_template.py", pathClearMap + "ClearMap/Scripts/work_dir/")
        shutil.copy(scriptsFolder + "/savedSettings.txt", pathClearMap + "ClearMap/Scripts/work_dir/")

        runButtonMain['state'] = 'normal'
        textVar.set("Imported folder " + nameFolder)
        with open(pathClearMap + "ClearMap/Scripts/work_dir/savedSettings.txt", "r") as outputFile:
            data = json.load(outputFile)
        data['fromImport'] = True

        with open(pathClearMap + "ClearMap/Scripts/work_dir/savedSettings.txt", "w+") as outputFile:
            json.dump(data, outputFile)
    except FileNotFoundError:
        pass