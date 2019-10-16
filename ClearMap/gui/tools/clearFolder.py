import os
import shutil


def clear_folder(folder):
    """
    This function clears the entire content of the folder given in the parameter.

    :param folder: The full path to whatever folder needs to be empty
    :return:
    """
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(e)