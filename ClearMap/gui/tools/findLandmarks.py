import json
import shutil
from ClearMap.gui.tools.splitCSV import write_landmarks_to_files
from tkfilebrowser import askopenfilename


def findLandmarks(manualWindow, pathClearMap):
    """
    This function is called when the user has to select where the landmarks.csv file is located.
    :param rootMA: This the window where the select landmarks button is called from.
    :param pathClearMap: The path to where the entire program is saved.
    :return:
    """
    landmarksDir = askopenfilename(parent=manualWindow, title="Select landmarks file")
    print(landmarksDir)
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
