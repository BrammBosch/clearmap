import os, numpy, math
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
BaseDirectory ="/home/bram/Desktop/Jaar_3/donders/ClearMap_3/ClearMap/clearmap_preset_folder/output"
cFosFile = os.path.join(BaseDirectory,"/home/bram/Desktop/Jaar_3/donders/ClearMap_3/ClearMap/clearmap_preset_folder/protein/cfos-substack.tif");
AutofluoFile = os.path.join(BaseDirectory,"/home/bram/Desktop/Jaar_3/donders/ClearMap_3/ClearMap/clearmap_preset_folder/auto_fluo/template_25.tif");
cFosFileRange = {'x': all, 'y': all, 'z': all};
FinalOrientation = (1, 2, 3);
OriginalResolution = (4.0625, 4.0625, 3)
AtlasResolution = (25, 25, 25)
PathReg ="/home/bram/Desktop/Jaar_3/donders/ClearMap_3/ClearMap/clearmap_preset_folder/atlas"
AtlasFile = os.path.join(PathReg, 'template_25.tif');
AnnotationFile = os.path.join(PathReg, 'annotation_25_full_color.tif');
ResamplingParameter = {"processes": int(12)
}
ImageProcessingMethod = "SpotDetection";
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
