import os
import ClearMap.Settings as settings
filename = os.path.join(settings.ClearMapPath, 'Test/Data/ImageAnalysis/cfos-substack.tif');
import ClearMap.Visualization.Plot as plt
import ClearMap.IO as io
data = io.readData(filename, z = (0,26));
import ClearMap.ImageProcessing.BackgroundRemoval as bgr
dataBGR = bgr.removeBackground(data.astype('float'), size=(3,3), verbose = True);
from ClearMap.ImageProcessing.Filter.DoGFilter import filterDoG
dataDoG = filterDoG(dataBGR, size=(8,8,4), verbose = True);
from ClearMap.ImageProcessing.MaximaDetection import findExtendedMaxima
dataMax = findExtendedMaxima(dataDoG, hMax = None, verbose = True, threshold = 10);
from ClearMap.ImageProcessing.MaximaDetection import findCenterOfMaxima
cells = findCenterOfMaxima(data, dataMax);
from ClearMap.ImageProcessing.CellSizeDetection import detectCellShape
dataShape = detectCellShape(dataDoG, cells, threshold = 15);
from ClearMap.ImageProcessing.CellSizeDetection import findCellSize, findCellIntensity
cellSizes = findCellSize(dataShape, maxLabel = cells.shape[0]);
cellIntensities = findCellIntensity(dataBGR, dataShape,  maxLabel = cells.shape[0]);
import matplotlib.pyplot as mpl
mpl.figure()
mpl.plot(cellSizes, cellIntensities, '.')
mpl.xlabel('cell size [voxel]')
mpl.ylabel('cell intensity [au]')