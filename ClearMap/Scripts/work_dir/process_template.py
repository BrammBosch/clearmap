exec(open('/home/bram/Desktop/Jaar_3/donders/ClearMap_3/docs/conf.py').read())
import ClearMap
from ClearMap.alignmentOptions.machineLearning import machineLearning
from ClearMap.alignmentOptions.manualAlignment import manual
from ClearMap.celDetectionOptions.arivisPipeline import arivis
from ClearMap.celDetectionOptions.importOwnFiles import importOwn
exec(open('/home/bram/Desktop/Jaar_3/donders/ClearMap_3/ClearMap/Scripts/work_dir/parameter_file.py').read())
resampleData(**CorrectionResamplingParameterCfos);
resampleData(**CorrectionResamplingParameterAutoFluo);
resampleData(**RegistrationResamplingParameter);
resultDirectory  = alignData(**CorrectionAlignmentParameter);
resultDirectory  = alignData(**RegistrationAlignmentParameter);
arivis()
points = io.readPoints(CorrectionResamplingPointsParameter["pointSource"]);
points = resamplePoints(**CorrectionResamplingPointsParameter);
points = transformPoints(points, transformDirectory = CorrectionAlignmentParameter["resultDirectory"], indices = False, resultDirectory = None);
CorrectionResamplingPointsInverseParameter["pointSource"] = points;
points = resamplePointsInverse(**CorrectionResamplingPointsInverseParameter);
RegistrationResamplingPointParameter["pointSource"] = points;
points = resamplePoints(**RegistrationResamplingPointParameter);
points = transformPoints(points, transformDirectory = RegistrationAlignmentParameter["resultDirectory"], indices = False, resultDirectory = None);
io.writePoints(TransformedCellsFile, points);   
points = io.readPoints(TransformedCellsFile)
intensities = io.readPoints(FilteredCellsFile[1])
points = io.readPoints(TransformedCellsFile)
intensities = io.readPoints(FilteredCellsFile[1])
vox = voxelize(points, AtlasFile, **voxelizeParameter);
if not isinstance(vox, str):
    io.writeData(os.path.join(BaseDirectory, 'cells_heatmap.tif'), vox.astype('int32'));
voxelizeParameter["weights"] = intensities[:,0].astype(float);
vox = voxelize(points, AtlasFile, **voxelizeParameter);
if not isinstance(vox, str):
    io.writeData(os.path.join(BaseDirectory, 'cells_heatmap_weighted.tif'), vox.astype('int32'));
ids, counts = countPointsInRegions(points, labeledImage = AnnotationFile, intensities = intensities, intensityRow = 0);
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
