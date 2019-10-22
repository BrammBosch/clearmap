import os
import tkinter as tk
import json
from ClearMap.gui.windows.settingsWindow import create_settings_window


def custom_run_options(nextButton, pathClearMap, root):
    """

    :param nextButton:
    :param pathClearMap:
    :param root:
    :return:
    """
    runOptionsWindow = tk.Toplevel(root)
    runOptionsWindow.title("Error")

    with open(pathClearMap + "ClearMap/Scripts/work_dir/savedSettings.txt") as json_file:
        dataRunOptions = json.load(json_file)
    textVarRun = tk.StringVar(runOptionsWindow)
    textVarRun.set("Please choose an action")
    tk.Label(runOptionsWindow, textvariable=textVarRun).grid(padx=4, pady=4, sticky='ew')
    contButton = tk.Button(runOptionsWindow, text="continue", command=runOptionsWindow.destroy)
    contButton.grid(padx=4, pady=4, sticky='ew')
    if dataRunOptions['tableBox'] and dataRunOptions['heatmapBox'] and dataRunOptions['cellDetectionBox'] and \
            dataRunOptions['alignmentBox'] and dataRunOptions['resampleBox']:
        runOptionsWindow.destroy()
        create_settings_window(nextButton, root, pathClearMap)

    else:
        run = True
        if not dataRunOptions['cellDetectionBox'] and not dataRunOptions['resampleBox'] and dataRunOptions[
            'alignmentBox']:
            if os.path.exists(dataRunOptions['baseDir'] + '/cells.npy') and os.path.exists(
                    dataRunOptions['baseDir'] + '/autofluo_for_cfos_resampled.tif') and os.path.exists(
                dataRunOptions['baseDir'] + '/cfos_resampled.tif'):
                run = True
            else:
                textVarRun.set("""You have chosen to skip the resampling and celdetection but the alignment needs a
                        cells.npy file and the resampled files.
                        Please copy the files to the output folder or go back and select resampling and celdetection """)
                dataRunOptions['kill'] = True
                run = False

        if run and not dataRunOptions['cellDetectionBox'] and dataRunOptions['alignmentBox']:
            if os.path.exists(dataRunOptions['baseDir'] + '/cells.npy'):
                run = True
            else:
                textVarRun.set("""You have chosen to skip the celdetection but the alignment needs a cells.npy file. 
                     Please copy the files to the output folder or go back and select celdetection""")
                dataRunOptions['kill'] = True
                run = False

        if run and not dataRunOptions['resampleBox'] and dataRunOptions['alignmentBox']:

            if os.path.exists(
                    dataRunOptions['baseDir'] + '/autofluo_for_cfos_resampled.tif') and \
                    os.path.exists(dataRunOptions['baseDir'] + '/cfos_resampled.tif'):

                run = True
            else:
                textVarRun.set("""You have chosen to skip the resampling but the alignment needs the resampled tif files. 
                        Please copy the files to the output folder or go back and select resampling""")
                dataRunOptions['kill'] = True
                run = False

        if run and not dataRunOptions['cellDetectionBox'] and dataRunOptions['heatmapBox']:
            if os.path.exists(dataRunOptions['baseDir'] + '/intensities.npy'):
                run = True
            else:
                textVarRun.set("""You have chosen to skip the celdetection but the heatmap creation needs a intensities.npy file.
                        Please copy the files to the output folder or go back and select an alignment option""")
                dataRunOptions['kill'] = True
                run = False

        if run and not dataRunOptions['alignmentBox'] and dataRunOptions['heatmapBox']:
            if os.path.exists(dataRunOptions['baseDir'] + '/cells_transformed_to_Atlas.npy'):
                run = True
            else:
                textVarRun.set("""You have chosen to skip the celdetection but the heatmap creation needs a cells_transformed_to_Atlas.npy file.
                                       Please copy the files to the output folder or go back and select an alignment option""")
                dataRunOptions['kill'] = True
                run = False

        if run and not dataRunOptions['cellDetectionBox'] and dataRunOptions['tableBox']:
            if os.path.exists(dataRunOptions['baseDir'] + '/intensities.npy'):
                run = True
            else:
                textVarRun.set("""You have chosen to skip the celdetection but the table creation needs a intensities.npy file.
                       Please copy the files to the output folder or go back and select an alignment option""")
                dataRunOptions['kill'] = True
                run = False

        if run and not dataRunOptions['alignmentBox'] and dataRunOptions['tableBox']:
            if os.path.exists(dataRunOptions['baseDir'] + '/cells_transformed_to_Atlas.npy'):
                run = True
            else:
                textVarRun.set("""You have chosen to skip the celdetection but the table creation needs a cells_transformed_to_Atlas.npy file.
                                       Please copy the files to the output folder or go back and select an alignment option""")
                dataRunOptions['kill'] = True
                run = False

        with open(pathClearMap + "ClearMap/Scripts/work_dir/savedSettings.txt", "w") as outputFile:
            json.dump(dataRunOptions, outputFile)
        if run:
            runOptionsWindow.destroy()
            create_settings_window(nextButton, root, pathClearMap)
