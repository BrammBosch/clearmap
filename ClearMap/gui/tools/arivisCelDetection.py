import json

import numpy as np
from tkfilebrowser import askopenfilename
import csv


def arivis_cel_detection(importCelWindow, pathClearMap):
    try:
        cellsDir = askopenfilename(parent=importCelWindow, title="Select the csv file with the detected cells")
        f = open(cellsDir, 'r')
        reader = csv.reader(f)
        headers = next(reader, None)

        column = {}
        for h in headers:
            column[h] = []
        for row in reader:
            for h, v in zip(headers, row):
                column[h].append(v)

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
        with open(pathClearMap + "ClearMap/Scripts/work_dir/savedSettings.txt") as json_file:
            data = json.load(json_file)
        data['kill'] = True
        with open(pathClearMap + "ClearMap/Scripts/work_dir/savedSettings.txt", "w") as outputFile:
            json.dump(data, outputFile)
