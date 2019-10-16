import json
import sys

import numpy as np
from tkfilebrowser import askopenfilename
import csv


def arivis_cel_detection(importCelWindow, pathClearMap):
    try:
        cellsDir = askopenfilename(parent=importCelWindow, title="Select the csv file with the detected cells")
        print(cellsDir)
        f = open(cellsDir, 'r')
        reader = csv.reader(f)
        headers = next(reader, None)
        print(headers)

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

        for count, item in enumerate(xValues):

            cellsList.append([xValues[count], yValues[count], zValues[count]])
        np.save(pathClearMap + "ClearMap/clearmap_preset_folder/output/cells.npy", np.array(cellsList))


    except Exception as e:
        with open(pathClearMap + "ClearMap/Scripts/work_dir/savedSettings.txt") as json_file:
            data = json.load(json_file)
        data['kill'] = True
        with open(pathClearMap + "ClearMap/Scripts/work_dir/savedSettings.txt", "w") as outputFile:
            json.dump(data, outputFile)
