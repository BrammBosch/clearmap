import json
import sys


def create_file_process(pathClearMap):

    with open(pathClearMap + "ClearMap/Scripts/work_dir/savedSettings.txt", "r") as outputFile:
        data = json.load(outputFile)
    if data['fromSettings'] == False:
        finalOutput = config_parameter_build(pathClearMap)
        finalOutput += resampling_operations_build()
        finalOutput += aligment_clearMap()
        finalOutput += detection_clearmap()
        finalOutput += transform_point_coordinates()
        finalOutput += points_intensities()
        finalOutput += heatmap()
        finalOutput += table()

    else:
        finalOutput = config_parameter_import_build(pathClearMap)
        finalOutput += resampling_operations_build()


        if "Manual"in data['alignmentOperation']:
            finalOutput += alignment_manual(pathClearMap)
            temp = transform_point_coordinates_manual()
            #finalOutput += "exec(open('" + pathClearMap + "ClearMap/Scripts/work_dir/parameter_file.py').read())\n"


        elif "Machine" in data['alignmentOperation']:
            finalOutput += alignment_machineLearning()
            temp = transform_point_coordinates()
        else:
            finalOutput += aligment_clearMap()
            temp = transform_point_coordinates()

        if "arivis" in data['celDetection']:
            finalOutput += detection_arivis()

        elif "Import" in data['celDetection']:
            finalOutput += detection_import()

        else:
            finalOutput += detection_clearmap()

        finalOutput += temp

        if data['table'] == True or data['heatmap'] == True:
            finalOutput += points_intensities()

        if data['heatmap'] == True:
            finalOutput += heatmap()

        if data['table'] == True:
            finalOutput += table()



    processFile = open(pathClearMap + "ClearMap/Scripts/work_dir/process_template.py", "w+")

    processFile.write(finalOutput)


def config_parameter_build(pathClearMap):
    fileConfigAndParameter = "exec(open('" + pathClearMap + "docs/conf.py').read())\nimport ClearMap\n"
    fileConfigAndParameter += "exec(open('" + pathClearMap + "ClearMap/Scripts/work_dir/parameter_file.py').read())\n"
    return fileConfigAndParameter

def config_parameter_import_build(pathClearMap):
    fileConfigAndParameter = "exec(open('" + pathClearMap + "docs/conf.py').read())\nimport ClearMap\n"
    fileConfigAndParameter += """from ClearMap.alignmentOptions.machineLearning import machineLearning
from ClearMap.alignmentOptions.manualAlignment import manual
from ClearMap.celDetectionOptions.arivisPipeline import arivis
from ClearMap.celDetectionOptions.importOwnFiles import importOwn
"""
    fileConfigAndParameter += "exec(open('" + pathClearMap + "ClearMap/Scripts/work_dir/parameter_file.py').read())\n"
    return fileConfigAndParameter


def resampling_operations_build():
    resamplingOperations = "resampleData(**CorrectionResamplingParameterCfos);\n"
    resamplingOperations += "resampleData(**CorrectionResamplingParameterAutoFluo);\n"
    resamplingOperations += "resampleData(**RegistrationResamplingParameter);\n"

    return resamplingOperations


def aligment_clearMap():
    alignment = "resultDirectory  = alignData(**CorrectionAlignmentParameter);\n"
    alignment += "resultDirectory  = alignData(**RegistrationAlignmentParameter);\n"
    return alignment


def alignment_manual(pathClearMap):
    alignment = 'manual("' + pathClearMap + '")\n'
    alignment += "resampleData(**RegistrationResamplingParameter);\n"
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

def detection_arivis():
    detection = "arivis()\n"
    return detection

def detection_import():
    detection = "importOwn()\n"
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
    heatmapText = """points = io.readPoints(TransformedCellsFile)
intensities = io.readPoints(FilteredCellsFile[1])
vox = voxelize(points, AtlasFile, **voxelizeParameter);
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