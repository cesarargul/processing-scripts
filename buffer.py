#Definition of inputs and outputs
#==================================
##[cesarag]=group
##input=vector
##output=output vector
##buffer=number 10

#Algorithm body 1111111111
#==================================
from qgis.core import *
from PyQt4.QtCore import *
from processing.core.VectorWriter import VectorWriter
from shapely.geometry import Polygon
from shapely.wkb import loads, dumps
from shapely.ops import cascaded_union

# "input" contains the location of the selected layer.
# We get the actual object,
layer = processing.getobject(input)
provider = layer.dataProvider()
fields = provider.fields()


inFeat = QgsFeature()
outFeat = QgsFeature()
inGeom = QgsGeometry()
nElement = 0
writer = VectorWriter(output, None, fields, provider.geometryType(), layer.crs() )

feats = processing.getfeatures(layer)
nFeat = len(feats)
for inFeat in feats:
    progress.setPercentage(int((100 * nElement)/nFeat))
    inGeom = inFeat.geometry()

    pol = loads(inGeom.asWkb())
    buff = pol.buffer(buffer)
    outGeom = QgsGeometry()
    outGeom.fromWkb(dumps(buff))
    
    outFeat.setGeometry(outGeom)
    outFeat.setAttributes(inFeat.attributes())
    writer.addFeature(outFeat)
    nElement+=nElement

del writer