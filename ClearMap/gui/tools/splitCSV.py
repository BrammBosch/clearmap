__author__ = "Bram Bosch"
def write_landmarks_to_files(pathClearMap):
    """
    This function opens the landmarks.csv file created by manual aligning points and creates the 2 needed output files.
    In the landmarks.csv file the first 2 lines are discarded and from the remaining 6 lines 2 separate files
    are created.
    The atlas file needs to be converted from microns to pixels so it is multiplied by 0.04

    The 2 output files each start with on the first line the word "point" (no quotation marks)
    On the second line is the amount of points. (3 coordinates per point)
    All the next lines contain 3 columns of coordinates separated by spaces.
    No returns are necessary since everything is exported to the files.
    """
    landmarks_file = open(pathClearMap + "ClearMap/clearmap_preset_folder/output/landmarks.csv")
    fluo = open(pathClearMap + "ClearMap/clearmap_preset_folder/output/autofluo_landmarks.txt", "w+")
    atlas = open(pathClearMap + "ClearMap/clearmap_preset_folder/output/atlas_landmarks.txt", "w+")

    output_fluo = "point \n"
    output_atlas = "point \n"

    output_fluo_temp = ""
    output_atlas_temp = ""

    i = 0
    for line in landmarks_file:
        line = line.split(",")
        output_atlas_temp += str(float(line[2]) * 0.04) + " " + str(float(line[3]) * 0.04) + " " + str(
            float(line[4]) * 0.04) + "\n"
        output_fluo_temp += line[5] + " " + line[6] + " " + line[7]
        i += 1

    output_fluo += str(i) + "\n" + output_fluo_temp

    output_atlas += str(i) + "\n" + output_atlas_temp

    fluo.write(output_fluo)
    atlas.write(output_atlas)

    fluo.close()
    atlas.close()
    landmarks_file.close()
