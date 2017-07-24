import pymel.all as pm
import time
import sys

"""
import th_utils.th_splitMeshesByMaterial as sbm
reload(sbm)
sbm.splitSelection()
"""

DEBUG=False

OUTPUT_GRP_NAME = "__th_splitMeshesByMaterialOutput__"
TIMER = [None] * 20

def __st( id ) :
	TIMER[id] = time.clock()

def __et( id, msg='EndTimer' ) :
	if( DEBUG ) :
		print '%s : %.2f' % ( msg, time.clock() - TIMER[id] )


def getMeshesRecursivelyFromSelection() :
	sel = pm.ls(sl=True)
	workingList = []
	for item in sel :
	    meshes = item.listRelatives(ad=True, ni=True,type=pm.nodetypes.Mesh)
	    meshes = [ mesh for mesh in meshes if mesh.isVisible() ]
	    workingList.extend(meshes)
	return workingList, sel



def splitByMaterials( mesh, outputGrp ) :	

	materials = mesh.listConnections(type=pm.nodetypes.ShadingEngine)
	print mesh.name()
	materials = list(set(materials))
	
	for material in materials :
		# print '----- ' + material.name()
		__st(1)

		faces = material.members( flatten=True )

		outmesh = None

		for facelist in faces :
			
			if( type( facelist ) is pm.Mesh ) :
				facelist = facelist.f[:]

			shape = facelist.node()		
			if( shape == mesh ) :
					
				__st(6)

				duplicate = facelist.node().getTransform().duplicate()[0]
				if( duplicate is None ) :
					pm.warning( "%s could not be duplicated" % mesh.name() )
					continue
				duplicate.setParent(outputGrp)

								
				dupfacelist = facelist.indices()				
				dupallfaces = duplicate.f[:].indices()
				deletefacelist = duplicate.f[facelist.indices()]

				__et(6, 'initTime')

				__st(2)
				# deletefacelist = [ duplicate.f[face] for face in dupallfaces if face not in dupfacelist ]
				pm.select(deletefacelist)
				pm.runtime.InvertSelection()
				# deletefacelist = pm.ls(sl=True, fl=True)
				__et(2, 'obtainFaceListTime')
				
				__st(3)
				pm.delete()
				__et(3, 'deleteFaceTime')
				# pm.filterExpand(dupfacelist, sm=34)


				__st(4)
				# pm.mel.select( duplicate.f[:] )
				# pm.hyperShade(assign=material)				
				pm.sets( material, fe=duplicate.f[:]  )					
				__et(4, 'assignMaterialTime')

				outmesh = duplicate
		

		__st(5)
		try:
			outmeshGrp = pm.PyNode( '%s|%s' % ( OUTPUT_GRP_NAME, material.name() + '_split' ) )
		except (pm.MayaNodeError) :
			outmeshGrp = pm.group(name=material.name() + '_split', parent=pm.PyNode(OUTPUT_GRP_NAME), empty=True)

		outmesh.setParent(outmeshGrp)
		__et(5, 'tidyUpTime')


		__et( 1, material.name() + ' done' )

		# break


def mergeGroup( group ) :
	p = group.getParent()
	n = group.name().replace( '_split', '_G' )
	if( len( group.getChildren() ) < 2 ) :
		combinedmesh = group.getChildren()[0]
	else :
		combinedmesh = pm.polyUnite(group, ch=False)[0]

	combinedmesh.setParent(p)
	combinedmesh.rename( n )
	
	pm.delete(group)	
	



def splitSelection() :

	__st(0)
	workingList, sel = getMeshesRecursivelyFromSelection()

	gMainProgressBar = pm.PyUI(pm.mel.eval( '$tmp = $gMainProgressBar' ))
	gMainProgressBar.setMaxValue( len(workingList) )

	if( len(workingList) > 0 ) :
		try :
			outputGrp = pm.PyNode(OUTPUT_GRP_NAME)
		except (pm.MayaNodeError) :
			outputGrp = pm.group(name=OUTPUT_GRP_NAME, world=True, empty=True)						

		outputContents = outputGrp.getChildren()
		for child in outputContents :
			pm.delete(child)

		
		pm.uitypes.ProgressBar.beginProgress(
			gMainProgressBar,
			status="Splitting meshes..."
		)
		gMainProgressBar.step(0)
		pm.refresh()


		for mesh in workingList :
			splitByMaterials(mesh, outputGrp)
			gMainProgressBar.step(1)
			pm.refresh()

		materialGroups = outputGrp.getChildren()
		for group in materialGroups :
			mergeGroup(group)
			
	else :
		pm.warning( 'No meshes found in selection' )

	gMainProgressBar.endProgress()

	# pm.select(sel)
	pm.select(outputGrp)

	print 'Splitting mesh by material COMPLETE'

	__et(0, 'Total')




