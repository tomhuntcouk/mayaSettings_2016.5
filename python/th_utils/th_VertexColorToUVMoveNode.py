import pymel.all as pm
from collections import Counter

# example
# v.Create( sel[0], pm.datatypes.Color.red, sel[1],  'leftEye', 0.2 )
def Create( obj, targetColor, control, attr, offset ) :
	shape = obj.getShape()
	name = obj.name()
	if( type(shape) == pm.Mesh ) :
		outVerts = []
		verts = shape.vtx[:]				
		for i, vert in enumerate(verts) :			
			if( vert.getColor() == targetColor ) :
				outVerts.append(vert)


		# this needs rewriting
		# what shells does this vert eblong to?
		# out of teh verts we have, which shell contains the most?
		uvShellsList = shape.getUvShellsIds()[0]
		uvList = []
		outUvShellList = []
		for vert in outVerts :
			uvs = vert.getUVIndices()
			for uv in uvs :
				uvList.append(uv)
				outUvShellList.append(uvShellsList[uv])
		
		outUvList = []
		mostCommonShell = Counter(outUvShellList).most_common(1)[0][0]		
		for i, uvshell in enumerate(outUvShellList) :
			if( uvshell == mostCommonShell ) :
				outUvList.append(shape.map[uvList[i]])

		# print outUvList


		

		# return

		if( len(outVerts) > 0 ) :
			moveUV = pm.polyMoveUV( outUvList )[0]
			moveUV.rename('%s_%s_moveUV' % ( name, attr ))

			crv = pm.AnimCurveTU(name='%s_%s_animCurveTU' % ( name, attr ) )
			pm.setKeyframe(crv, t=0.0, v=0.0, itt='linear', ott='linear')
			pm.setKeyframe(crv, t=20.0, v=-offset * 20, itt='linear', ott='linear')

			control.attr(attr) >> crv.input
			crv.output >> moveUV.translateV

			return moveUV

		else :
			pm.warning( 'No verts found with color %s' % ( targetColor ) )

	else :
		pm.warning('The target must be a mesh')


def ConnectToAttr( src, trgt, attr ) :
	moveUVs = src.getShape().history(type='polyMoveUV')
	try :
		attr = pm.PyNode(trgt).attr(attr).getChildren()
	except :
		attr = [ pm.PyNode(trgt).attr(attr) ]

	if( len(moveUVs) > len(attr) ) :
		pm.warning( 'There are more polyMoveUV nodes that attrs to connect to %s:%s' % ( len(moveUVs), len(attr) )  )
	else :
		for i, moveUV in enumerate(moveUVs)	:
			moveUV.translateV >> attr[i]

