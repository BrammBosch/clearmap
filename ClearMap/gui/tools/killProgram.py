import json


def kill(pathClearMap):
    """
    When this function is called the function loads the local json file where the settings are saved.
    It then changes the kill parameter to True so the main pipeline is never ran
    :param pathClearMap:The path to where the gui is located
    :return:
    """
    with open(pathClearMap + "ClearMap/Scripts/work_dir/savedSettings.txt") as json_file:
        data = json.load(json_file)
    data['kill'] = True
    with open(pathClearMap + "ClearMap/Scripts/work_dir/savedSettings.txt", "w") as outputFile:
        json.dump(data, outputFile)