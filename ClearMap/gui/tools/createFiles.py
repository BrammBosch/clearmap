from ClearMap.gui.tools.createParameter import create_file_parameter
from ClearMap.gui.tools.createProcess import create_file_process


def create_files(pathClearMap):
    """
    This function calls 2 different functions which create the parameter and the process template file.
    They are saved in the work_dir and removed and rewritten on start up and on every change.
    :return:
    """
    create_file_parameter(pathClearMap)
    create_file_process(pathClearMap)
