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

def extract_pols(geom):
    if geom.geom_type=='Polygon':
	return [geom]
    elif geom.geom_type=='GeometryCollection' or geom.geom_type=='MultiPolygon':
	pols=[]
	for subgeom in geom:
	    if subgeom.geom_type=='Polygon':
		pols.append(subgeom)
	return pols
    return []

layer = processing.getobject(input)
provider = layer.dataProvider()
fields = provider.fields()
buffer_dist = distance / 2


inFeat = QgsFeature()
inGeom = QgsGeometry()

outFeat = QgsFeature()
writer = VectorWriter(output, None, fields, provider.geometryType(), layer.crs())

feats = processing.getfeatures(layer)
for inFeat in feats:
    inGeom = inFeat.geometry()
    if not inGeom is None:
	poly = loads(inGeom.asWkb())
	buff = buffer(poly, -buffer_dist)
	buff = buffer(buff, buffer_dist)
	pols = extract_pols(buff)
	for pol in pols:
	    outGeom = QgsGeometry()
	    outGeom.fromWkb(dumps(pol))
	    outFeat.setGeometry(outGeom)
	    writer.addFeature(outFeat)

del writer