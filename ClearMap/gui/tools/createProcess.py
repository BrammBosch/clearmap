__author__ = "Bram Bosch"
import json


def create_file_process(pathClearMap):
    """
    This the main function called when creating a process file.
    It starts by reading the settings from the json file.
    The process file template is then constructed by looking at the saved settings and deciding which of the settings
    to add to the file. The process function can easily be expanded by adding more functions to the finalOutput var.


    :param pathClearMap: The path to the clearmap folders, unique for each computer.
    :return:
    """

    with open(pathClearMap + "ClearMap/Scripts/work_dir/savedSettings.txt", "r") as outputFile:
        data = json.load(outputFile)


    finalOutput = config_parameter_import(pathClearMap)

    if data['resampleBox']:
        finalOutput += resampling_operations()
    temp = transform_point_coordinates()

    if data['alignmentBox']:
        if "Manual"in data['alignmentOperation']:
            finalOutput += alignment_manual()
            temp = transform_point_coordinates_manual()

        elif "Machine" in data['alignmentOperation']:
            finalOutput += alignment_machineLearning()
        else:
            finalOutput += aligment_clearMap()
    if data['cellDetectionBox']:
        if "clearmap" in data['cellDetection']:
            finalOutput += detection_clearmap()
        else:
            finalOutput += detection_manual()
    if data['tableBox'] or data['heatmapBox']:
        finalOutput += temp
        finalOutput += points_intensities()


    if data['heatmapBox'] == True:
        finalOutput += heatmap()

    if data['tableBox'] == True:
        finalOutput += table()



    processFile = open(pathClearMap + "ClearMap/Scripts/work_dir/process_template.py", "w+")

    processFile.write(finalOutput)



def config_parameter_import(pathClearMap):
    fileConfigAndParameter = "exec(open('" + pathClearMap + "docs/conf.py').read())\nimport ClearMap\n"
    fileConfigAndParameter += "exec(open('" + pathClearMap + "ClearMap/Scripts/work_dir/parameter_file.py').read())\n"

    return fileConfigAndParameter


def resampling_operations():
    resamplingOperations = "resampleData(**CorrectionResamplingParameterCfos);\n"
    resamplingOperations += "resampleData(**CorrectionResamplingParameterAutoFluo);\n"
    resamplingOperations += "resampleData(**RegistrationResamplingParameter);\n"

    return resamplingOperations


def aligment_clearMap():
    alignment = 'resultDirectory  = alignData(**CorrectionAlignmentParameter);\n'
    alignment += 'resultDirectory  = alignData(**RegistrationAlignmentParameter);\n'
    return alignment


def alignment_manual():
    alignment = "resampleData(**RegistrationResamplingParameter);\n"
    alignment += "resultDirectory  = alignData(**RegistrationAlignmentParameter);\n"
    return alignment


def alignment_machineLearning():
    alignment = "machineLearning()\n"
    return alignment

def detection_clearmap():
    detection = 'detectCells(**ImageProcessingParameter);\n'
    detection += 'points, intensities = io.readPoints(ImageProcessingParameter["sink"]);\n'
    detection += 'points, intensities = thresholdPoints(points, intensities, threshold = (20, 900), row = (3,3));\n'
    detection += 'io.writePoints(FilteredCellsFile, (points, intensities));\n'
    return detection

def detection_manual():
    #detection = 'points, intensities = io.readPoints(ImageProcessingParameter["sink"]);\n'
    detection = 'points, intensities = thresholdPoints(points, intensities, threshold = (20, 900), row = (3,3));\n'
    detection += 'io.writePoints(FilteredCellsFile, (points, intensities));\n'
    return detection

def transform_point_coordinates():
    transform = """points = io.readPoints(CorrectionResamplingPointsParameter["pointSource"]);
points = resamplePoints(**CorrectionResamplingPointsParameter);
points = transformPoints(points, transformDirectory = CorrectionAlignmentParameter["resultDirectory"], indices = False, resultDirectory = None);
CorrectionResamplingPointsInverseParameter["pointSource"] = points;
points = resamplePointsInverse(**CorrectionResamplingPointsInverseParameter);
RegistrationResamplingPointParameter["pointSource"] = points;
points = resamplePoints(**RegistrationResamplingPointParameter);
points = transformPoints(points, transformDirectory = RegistrationAlignmentParameter["resultDirectory"], indices = False, resultDirectory = None);
io.writePoints(TransformedCellsFile, points);   
"""
    return transform

def transform_point_coordinates_manual():
    transform = """points = io.readPoints(CorrectionResamplingPointsParameter["pointSource"]);
points = resamplePoints(**CorrectionResamplingPointsParameter);
CorrectionResamplingPointsInverseParameter["pointSource"] = points;
points = resamplePointsInverse(**CorrectionResamplingPointsInverseParameter);
RegistrationResamplingPointParameter["pointSource"] = points;
points = resamplePoints(**RegistrationResamplingPointParameter);
points = transformPoints(points, transformDirectory = RegistrationAlignmentParameter["resultDirectory"], indices = False, resultDirectory = None);
io.writePoints(TransformedCellsFile, points);   
"""
    return transform


def points_intensities():
    pointsAndIntensities = "points = io.readPoints(TransformedCellsFile)\n"
    pointsAndIntensities += "intensities = io.readPoints(FilteredCellsFile[1])\n"
    return pointsAndIntensities

def heatmap():
    heatmapText = """vox = voxelize(points, AtlasFile, **voxelizeParameter);
if not isinstance(vox, str):
    io.writeData(os.path.join(BaseDirectory, 'cells_heatmap.tif'), vox.astype('int32'));
voxelizeParameter["weights"] = intensities[:,0].astype(float);
vox = voxelize(points, AtlasFile, **voxelizeParameter);
if not isinstance(vox, str):
    io.writeData(os.path.join(BaseDirectory, 'cells_heatmap_weighted.tif'), vox.astype('int32'));
"""
    return heatmapText

def table():
    tableText = """ids, counts = countPointsInRegions(points, labeledImage = AnnotationFile, intensities = intensities, intensityRow = 0);
table = numpy.zeros(ids.shape, dtype=[('id','int64'),('counts','f8'),('name', 'a256')])
table["id"] = ids;
table["counts"] = counts;
table["name"] = labelToName(ids);
io.writeTable(os.path.join(BaseDirectory, 'Annotated_counts_intensities.csv'), table);
ids, counts = countPointsInRegions(points, labeledImage = AnnotationFile, intensities = None);
table = numpy.zeros(ids.shape, dtype=[('id','int64'),('counts','f8'),('name', 'a256')])
table["id"] = ids;
table["counts"] = counts;
table["name"] = labelToName(ids);
io.writeTable(os.path.join(BaseDirectory, 'Annotated_counts.csv'), table);
"""
    return tableText