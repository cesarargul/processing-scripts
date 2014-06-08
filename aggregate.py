#Definition of inputs and outputs
#==================================
##[cesarag]=group
##input=vector
##output=output vector
##distance=number 20
##type=selection orthogonal; non-orthogonal

#Algorithm body
#==================================
from qgis.core import *
from PyQt4.QtCore import *
from processing.core.VectorWriter import VectorWriter
from shapely.geometry import Polygon
from shapely.wkb import loads, dumps
from shapely.ops import cascaded_union

def buffer(geom, dist):
    if type == 0:
	return geom.buffer(dist, join_style=2, mitre_limit=abs(dist))
    else:
	return geom.buffer(dist)

# "input" contains the location of the selected layer.
# We get the actual object,
layer = processing.getobject(input)
provider = layer.dataProvider()
fields = provider.fields()
buffer_dist = distance / 2


inFeat = QgsFeature()
inGeom = QgsGeometry()
buffered = []

feats = processing.getfeatures(layer)
for inFeat in feats:
    inGeom = inFeat.geometry()
    if not inGeom is None:
	pol = loads(inGeom.asWkb())
	buff = buffer(pol, buffer_dist)
	buffered.append(buff)

union = cascaded_union(buffered)

outFeat = QgsFeature()
writer = VectorWriter(output, None, fields, provider.geometryType(), layer.crs())
for pol in union:
    outGeom = QgsGeometry()
    outGeom.fromWkb(dumps(buffer(pol,-buffer_dist)))
    outFeat.setGeometry(outGeom)
    writer.addFeature(outFeat)
del writer