import numpy as np
from tkfilebrowser import askopenfilename
import csv

from ClearMap.gui.tools.killProgram import kill


def cel_detection(importCelWindow, pathClearMap):
    """
    This function is called when the user chooses to import their own cel detection.
    It opens the file and checks if arivis headers are present. If they aren't the program assumes the csv files first 3
    columns are the x y z coordinates without headers.
    Every time when loading a npy fix imports has to be true because the clearmap program uses a python 2.x way to read
    the numpy arrays and this fixes any header issues that would otherwise occur.
    :param importCelWindow: This is the toplevel from where the chooser is called and is used as parent for the file
    chooser
    :param pathClearMap: This is the path of the gui.
    :return:
    """
    cellsDir = askopenfilename(parent=importCelWindow, title="Select the csv file with the detected cells")

    try:
        f = open(cellsDir, 'r')
        reader = csv.reader(f)
        headers = next(reader, None)
        column = {}
        for h in headers:
            column[h] = []
        for row in reader:
            for h, v in zip(headers, row):
                column[h].append(v)
        f.close()
        if '"X (px), Center of Geometry"' in column and '"Mean, Intensities #1"' in column:
            #if this is true then it is most likely an exported file from arivis. If it isn't but these columns still
            #exist then the outcome should be the same.
            arivis_cel_detection(pathClearMap, column)

        else:
            cel_detection_without_int(pathClearMap, cellsDir)

    except Exception as e:
        print(e)

        kill(pathClearMap)


def arivis_cel_detection(pathClearMap, column):
    """
    This function is called when the chosen cel detection file is an arivis file.

    :param pathClearMap: The path of the gui
    :param column: a dictionary where the keys are the headers of the read csv file, and where the keys are lists of the
    values in each header column.
    :return:
    """
    try:

        xValues = [int(float(x)) for x in column['"X (px), Center of Geometry"']]
        yValues = [int(float(x)) for x in column['"Y (px), Center of Geometry"']]
        zValues = [int(float(x)) for x in column['"Z (px), Center of Geometry"']]

        cellsList = []
        intensList = []
        for count, item in enumerate(xValues):
            intensList.append(["0", "0", column['"Mean, Intensities #1"'][count],
                               column['"VoxelCount, Volume"'][count]])
            cellsList.append([xValues[count], yValues[count], zValues[count]])
        np.save(pathClearMap + "ClearMap/clearmap_preset_folder/output/cells.npy", np.array(cellsList),
                allow_pickle=True, fix_imports=True)
        np.save(pathClearMap + "ClearMap/clearmap_preset_folder/output/intensities.npy", np.array(intensList),
                allow_pickle=True, fix_imports=True)

    except Exception as e:
        print(e)
        kill(pathClearMap)



def cel_detection_without_int(pathClearMap, cellsDir):
    """
    This function is called when the csv file containing cell coordinates is not an arivis file.
    :param pathClearMap: The path to the gui
    :param cellsDir: The path to the chosen file.
    :return:
    """
    f = open(cellsDir, 'r')
    cellsList = []
    for line in f:
        line = line.strip().split(',')
        print(line)
        line = [int(float(x)) for x in line]
        cellsList.append(line)
    np.save(pathClearMap + "ClearMap/clearmap_preset_folder/output/cells.npy", np.array(cellsList),
            allow_pickle=True, fix_imports=True)
    f.close()
