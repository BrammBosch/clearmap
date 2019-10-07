import json
import multiprocessing


def create_file_parameter(pathClearMap):
    with open(pathClearMap + "ClearMap/Scripts/work_dir/savedSettings.txt", "r") as outputFile:
        data = json.load(outputFile)

    finalOutput = imports_text()
    finalOutput += set_base_dir(data)

    if "Manual" in data['alignmentOperation']:
        finalOutput += set_protein_range_manual()
    else:
        finalOutput += set_protein_range()

    finalOutput += set_final_orientation()
    finalOutput += original_resolution(data)
    finalOutput += atlas_resolution(data)
    finalOutput += path_atlas(data)
    finalOutput += resampling_parameter()
    if "Manual" in data['alignmentOperation']:
        finalOutput += custom_filters_manual()
    else:
        finalOutput += custom_filters()

    processFile = open(pathClearMap + "ClearMap/Scripts/work_dir/parameter_file.py", "w+")

    processFile.write(finalOutput)


def imports_text():
    importsText = """import os, numpy, math
import ClearMap.Settings as settings
import ClearMap.IO as io
from ClearMap.Alignment.Resampling import resampleData;
from ClearMap.Alignment.Elastix import alignData, transformPoints
from ClearMap.ImageProcessing.CellDetection import detectCells
from ClearMap.Alignment.Resampling import resamplePoints, resamplePointsInverse
from ClearMap.Analysis.Label import countPointsInRegions
from ClearMap.Analysis.Voxelization import voxelize
from ClearMap.Analysis.Statistics import thresholdPoints
from ClearMap.Utils.ParameterTools import joinParameter
from ClearMap.Analysis.Label import labelToName
"""
    return importsText


def set_base_dir(data):
    dir = 'BaseDirectory ="' + data['baseDir'] + '"\n'
    dir += 'cFosFile = os.path.join(BaseDirectory,"' + data['proteinDir'] + '");\n'
    dir += 'AutofluoFile = os.path.join(BaseDirectory,"' + data['autoFluoDir'] + '");\n'
    return dir


def csvToNpy():
    conv = """cellspoints = numpy.loadtxt('/home/bram/Desktop/Jaar_3/donders/ClearMap_3/ClearMap/Scripts/Bram/landmarks.csv', delimiter = ",")
numpy.save(os.path.join(BaseDirectory,'cells.npy'), cellspoints)\n"""
    return conv


def set_protein_range():
    proteinRange = "cFosFileRange = {'x': all, 'y': all , 'z': all};\n"
    return proteinRange


def set_protein_range_manual():
    proteinRange = "cFosFileRange = {'x': all, 'y':(180, 2560) , 'z': all};\n"

    return proteinRange


def original_resolution(data):
    originalResolution = "OriginalResolution = (" + data['realX'] + ', ' + data['realY'] + ', ' + data['realZ'] + ')\n'
    return originalResolution


def original_resolution_preset():
    originalResolution = "OriginalResolution = (4.0625,4.0625,3)\n"
    return originalResolution


def set_final_orientation():
    finalOrientation = "FinalOrientation = (1, 2, 3);\n"
    return finalOrientation


def atlas_resolution(data):
    atlasResolution = "AtlasResolution = (" + data['atlasX'] + ', ' + data['atlasY'] + ', ' + data['atlasZ'] + ')\n'
    return atlasResolution


def atlas_resolution_preset():
    atlasResolution = "AtlasResolution = (25,25,25)\n"
    return atlasResolution


def path_atlas(data):
    textPaths = 'PathReg ="' + data['atlasDir'] + '"\n'
    textPaths += """AtlasFile = os.path.join(PathReg, 'template_25.tif');
AnnotationFile = os.path.join(PathReg, 'annotation_25_full_color.tif');\n"""
    return textPaths


def resampling_parameter():
    resamplingParameter = "ResamplingParameter = {"
    resamplingParameter += '"processes": int(' + str(multiprocessing.cpu_count()) + ")\n}\n"
    return resamplingParameter


def custom_filters():
    customFilters = """ImageProcessingMethod = "SpotDetection";
correctIlluminationParameter = {
        "flatfield": None,  
        "background": None,
        "scaling": "Mean",
        "save": None,  
        "verbose": True  
}
removeBackgroundParameter = {
        "size": (7, 7),  
        "save": None, 
        "verbose": True 
}
filterDoGParameter = {
        "size": None,
        "sigma": None,  
        "sigma2": None, 
        "save": None, 
        "verbose": True  
}
findExtendedMaximaParameter = {
        "hMax": None,
        "size": 5,  
        "threshold": 0,
        "save": None,
        "verbose": True 
}
findIntensityParameter = {
        "method": 'Max',
        "size": (3, 3, 3)
}
detectCellShapeParameter = {
        "threshold": 700,
        "save": None, 
        "verbose": True
}
detectSpotsParameter = {
        "correctIlluminationParameter": correctIlluminationParameter,
        "removeBackgroundParameter": removeBackgroundParameter,
        "filterDoGParameter": filterDoGParameter,
        "findExtendedMaximaParameter": findExtendedMaximaParameter,
        "findIntensityParameter": findIntensityParameter,
        "detectCellShapeParameter": detectCellShapeParameter
}
VoxelizationFile = os.path.join(BaseDirectory, 'points_voxelized.tif');
voxelizeParameter = {
        "method": 'Spherical',  # Spherical,'Rectangular, Gaussian'
        "size": (15, 15, 15),
        "weights": None
};
StackProcessingParameter = {
    "processes": 6,
    "chunkSizeMax": 100,
    "chunkSizeMin": 50,
    "chunkOverlap": 32,
    "chunkOptimization": True,
    "chunkOptimizationSize": all,
    "processMethod": "parallel"
};


ResolutionAffineCFosAutoFluo = (16, 16, 16);

CorrectionResamplingParameterCfos = ResamplingParameter.copy();

CorrectionResamplingParameterCfos["source"] = cFosFile;
CorrectionResamplingParameterCfos["sink"] = os.path.join(BaseDirectory, 'cfos_resampled.tif');

CorrectionResamplingParameterCfos["resolutionSource"] = OriginalResolution;
CorrectionResamplingParameterCfos["resolutionSink"] = ResolutionAffineCFosAutoFluo;

CorrectionResamplingParameterCfos["orientation"] = FinalOrientation;

CorrectionResamplingParameterAutoFluo = CorrectionResamplingParameterCfos.copy();
CorrectionResamplingParameterAutoFluo["source"] = AutofluoFile;
CorrectionResamplingParameterAutoFluo["sink"] = os.path.join(BaseDirectory, 'autofluo_for_cfos_resampled.tif');

RegistrationResamplingParameter = CorrectionResamplingParameterAutoFluo.copy();
RegistrationResamplingParameter["sink"] = os.path.join(BaseDirectory, 'autofluo_resampled.tif');
RegistrationResamplingParameter["resolutionSink"] = AtlasResolution;
CorrectionAlignmentParameter = {
    "movingImage": os.path.join(BaseDirectory, 'autofluo_for_cfos_resampled.tif'),
    "fixedImage": os.path.join(BaseDirectory, 'cfos_resampled.tif'),
    "affineParameterFile": os.path.join(PathReg, 'Par0000affine_acquisition.txt'),
    "bSplineParameterFile": None,
    "resultDirectory": os.path.join(BaseDirectory, 'elastix_cfos_to_auto'),
    "movingPoints": None,
    "fixedPoints": None,
};


RegistrationAlignmentParameter = CorrectionAlignmentParameter.copy();

RegistrationAlignmentParameter["resultDirectory"] = os.path.join(BaseDirectory, 'elastix_auto_to_atlas');

RegistrationAlignmentParameter["movingImage"] = AtlasFile;
RegistrationAlignmentParameter["fixedImage"] = os.path.join(BaseDirectory, 'autofluo_resampled.tif');

RegistrationAlignmentParameter["affineParameterFile"] = os.path.join(PathReg, 'Par0000affine.txt');
RegistrationAlignmentParameter["bSplineParameterFile"] = os.path.join(PathReg, 'Par0000bspline.txt');
RegistrationAlignmentParameter["movingPoints"] = os.path.join(BaseDirectory, 'atlas_landmarks.txt');
RegistrationAlignmentParameter["fixedPoints"] = os.path.join(BaseDirectory, 'autofluo_landmarks.txt');

SpotDetectionParameter = {
    "source": cFosFile,
    "sink": (os.path.join(BaseDirectory, 'cells-allpoints.npy'), os.path.join(BaseDirectory, 'intensities-allpoints.npy')),
    "detectSpotsParameter": detectSpotsParameter
};
SpotDetectionParameter = joinParameter(SpotDetectionParameter, cFosFileRange)
ImageProcessingParameter = joinParameter(StackProcessingParameter, SpotDetectionParameter);
FilteredCellsFile = (os.path.join(BaseDirectory, 'cells.npy'), os.path.join(BaseDirectory, 'intensities.npy'));
TransformedCellsFile = os.path.join(BaseDirectory, 'cells_transformed_to_Atlas.npy')
CorrectionResamplingPointsParameter = CorrectionResamplingParameterCfos.copy();
CorrectionResamplingPointsParameter["pointSource"] = os.path.join(BaseDirectory, 'cells.npy');
CorrectionResamplingPointsParameter["dataSizeSource"] = cFosFile;
CorrectionResamplingPointsParameter["pointSink"] = None;
CorrectionResamplingPointsInverseParameter = CorrectionResamplingPointsParameter.copy();
CorrectionResamplingPointsInverseParameter["dataSizeSource"] = cFosFile;
CorrectionResamplingPointsInverseParameter["pointSink"] = None;
RegistrationResamplingPointParameter = RegistrationResamplingParameter.copy();
RegistrationResamplingPointParameter["dataSizeSource"] = cFosFile;
RegistrationResamplingPointParameter["pointSink"] = None;
"""
    return customFilters


def custom_filters_manual():
    customFilters = """ImageProcessingMethod = "SpotDetection";
correctIlluminationParameter = {
        "flatfield": None,  
        "background": None,
        "scaling": "Mean",
        "save": None,  
        "verbose": True  
}
removeBackgroundParameter = {
        "size": (7, 7),  
        "save": None, 
        "verbose": True 
}
filterDoGParameter = {
        "size": None,
        "sigma": None,  
        "sigma2": None, 
        "save": None, 
        "verbose": True  
}
findExtendedMaximaParameter = {
        "hMax": None,
        "size": 5,  
        "threshold": 0,
        "save": None,
        "verbose": True 
}
findIntensityParameter = {
        "method": 'Max',
        "size": (3, 3, 3)
}
detectCellShapeParameter = {
        "threshold": 700,
        "save": None, 
        "verbose": True
}
detectSpotsParameter = {
        "correctIlluminationParameter": correctIlluminationParameter,
        "removeBackgroundParameter": removeBackgroundParameter,
        "filterDoGParameter": filterDoGParameter,
        "findExtendedMaximaParameter": findExtendedMaximaParameter,
        "findIntensityParameter": findIntensityParameter,
        "detectCellShapeParameter": detectCellShapeParameter
}
VoxelizationFile = os.path.join(BaseDirectory, 'points_voxelized.tif');
voxelizeParameter = {
        "method": 'Spherical',  # Spherical,'Rectangular, Gaussian'
        "size": (15, 15, 15),
        "weights": None
};
StackProcessingParameter = {
    "processes": 6,
    "chunkSizeMax": 100,
    "chunkSizeMin": 50,
    "chunkOverlap": 32,
    "chunkOptimization": True,
    "chunkOptimizationSize": all,
    "processMethod": "parallel"
};


ResolutionAffineCFosAutoFluo = (16, 16, 16);

CorrectionResamplingParameterCfos = ResamplingParameter.copy();

CorrectionResamplingParameterCfos["source"] = cFosFile;
CorrectionResamplingParameterCfos["sink"] = os.path.join(BaseDirectory, 'cfos_resampled.tif');

CorrectionResamplingParameterCfos["resolutionSource"] = OriginalResolution;
CorrectionResamplingParameterCfos["resolutionSink"] = ResolutionAffineCFosAutoFluo;

CorrectionResamplingParameterCfos["orientation"] = FinalOrientation;

CorrectionResamplingParameterAutoFluo = CorrectionResamplingParameterCfos.copy();
CorrectionResamplingParameterAutoFluo["source"] = AutofluoFile;
CorrectionResamplingParameterAutoFluo["sink"] = os.path.join(BaseDirectory, 'autofluo_for_cfos_resampled.tif');

RegistrationResamplingParameter = CorrectionResamplingParameterAutoFluo.copy();
RegistrationResamplingParameter["sink"] = os.path.join(BaseDirectory, 'autofluo_resampled.tif');
RegistrationResamplingParameter["resolutionSink"] = AtlasResolution;
CorrectionAlignmentParameter = {
    "movingImage": os.path.join(BaseDirectory, 'autofluo_for_cfos_resampled.tif'),
    "fixedImage": os.path.join(BaseDirectory, 'cfos_resampled.tif'),
    "affineParameterFile": os.path.join(PathReg, 'Par0000affine_acquisition.txt'),
    "bSplineParameterFile": None,
    "resultDirectory": os.path.join(BaseDirectory, 'elastix_cfos_to_auto'),
    "movingPoints": None,
    "fixedPoints": None,
};


RegistrationAlignmentParameter = CorrectionAlignmentParameter.copy();

RegistrationAlignmentParameter["resultDirectory"] = os.path.join(BaseDirectory, 'elastix_auto_to_atlas');

RegistrationAlignmentParameter["movingImage"] = AtlasFile;
RegistrationAlignmentParameter["fixedImage"] = os.path.join(BaseDirectory, 'autofluo_resampled.tif');

RegistrationAlignmentParameter["affineParameterFile"] = os.path.join(PathReg, 'Par0000affine.txt');
RegistrationAlignmentParameter["bSplineParameterFile"] = os.path.join(PathReg, 'Par0000bspline.txt');
RegistrationAlignmentParameter["movingPoints"] = os.path.join(BaseDirectory, 'atlas_landmarks.txt');
RegistrationAlignmentParameter["fixedPoints"] = os.path.join(BaseDirectory, 'autofluo_landmarks.txt');
SpotDetectionParameter = {
    "source": cFosFile,
    "sink": (os.path.join(BaseDirectory, 'cells-allpoints.npy'), os.path.join(BaseDirectory, 'intensities-allpoints.npy')),
    "detectSpotsParameter": detectSpotsParameter
};
SpotDetectionParameter = joinParameter(SpotDetectionParameter, cFosFileRange)
ImageProcessingParameter = joinParameter(StackProcessingParameter, SpotDetectionParameter);
FilteredCellsFile = (os.path.join(BaseDirectory, 'cells.npy'), os.path.join(BaseDirectory, 'intensities.npy'));
TransformedCellsFile = os.path.join(BaseDirectory, 'cells_transformed_to_Atlas.npy')
CorrectionResamplingPointsParameter = CorrectionResamplingParameterCfos.copy();
CorrectionResamplingPointsParameter["pointSource"] = os.path.join(BaseDirectory, 'cells.npy');
CorrectionResamplingPointsParameter["dataSizeSource"] = cFosFile;
CorrectionResamplingPointsParameter["pointSink"] = None;
CorrectionResamplingPointsInverseParameter = CorrectionResamplingPointsParameter.copy();
CorrectionResamplingPointsInverseParameter["dataSizeSource"] = cFosFile;
CorrectionResamplingPointsInverseParameter["pointSink"] = None;
RegistrationResamplingPointParameter = RegistrationResamplingParameter.copy();
RegistrationResamplingPointParameter["dataSizeSource"] = cFosFile;
RegistrationResamplingPointParameter["pointSink"] = None;
"""
    return customFilters
