
"""
tom.hunt@king.com

Script to combine the skinclusters of a combine mesh into one skincluster
Useful for when you want to paint weights on seperate meshes and want a tidy scene afterwards.


LIMITATIONS

	currently looks through ALL skinClusters in the scene rather than just the ones associated with the mesh
	due to the way the polyUnite node works finding the skinClusters for the combined mesh is quite tricky

	UPDATE :
	look at the way reduce_influences() gets the skinCluster
	we can use that

"""

import sys, os
import pickle
import maya.OpenMaya as OpenMaya
import pymel.core as pm


userhome = os.path.expanduser( '~' )

logdir = os.path.join( userhome, 'skinClusterMerge_logs' )
if( not os.path.exists( logdir ) ) :
	os.makedirs( logdir )

weightsloc = '%s/weightfile' % (logdir)
skinjointsloc = '%s/skinjointsfile' % (logdir)
vlogloc = '%s/vlog.txt' % (logdir)

def main( new=False ) :
	sel = pm.ls( sl=True )
	if( len( sel ) != 1 ) :
		pm.error( 'Please select ONE mesh transform' )

	mesh = sel[0]
	if( mesh.type() != 'transform' ) :
		pm.error( 'Please select a MESH TRANSFORM' )
	
	# meshverts = list( mesh.vtx )
	# remainingverts = list( mesh.vtx )
	skinclusters = pm.ls( type='skinCluster' )

	# print len( remainingverts ), len( meshverts )	
	
	if( len( skinclusters ) < 2 ) :
		pm.error( 'The selected mesh (%s) only has one skinCluster' % mesh )

	vertexweights = {}
	skinjoints = []

	# initialise the status bar
	pbar = pm.language.Mel.eval( '$tmp = $gMainProgressBar' )
	pm.progressBar( pbar, edit=True, beginProgress=True, isInterruptable=True,
					status='"Merging skinClusters..."',
					maxValue=len( skinclusters )
	)	

	# iterate through skinClusters to get the weights associated with each vertex
	# these vertices will be associated with the pre-polyUnite'd meshes
	# then compare the position of each vertex in the cluster with the position of each vertex in the united mesh
	# if they are equivilent, store their influences and weights for later

	if( new ) :
		
		open( vlogloc, 'w+' ).close()		

		for s, skincluster in enumerate( skinclusters ) :
			
			vlog = open( vlogloc, 'a' )
			vlog.write( '%s : %s/%s \n' % ( str( skincluster ), s, len( skinclusters ) ) )
			vlog.close()

			weightedInfluences = skincluster.getWeightedInfluence()
			for j, joint in enumerate( weightedInfluences ) :
				
				vlog = open( vlogloc, 'a' )
				vlog.write( '	%s : %s/%s \n' % ( str( joint ), j, len( weightedInfluences ) ) )
				vlog.close()

				skinjoints.append( joint )
				influenceset, weights = skincluster.getPointsAffectedByInfluence( joint )

				for i, vertex in enumerate( influenceset[0] ) :

					if( pm.progressBar( pbar, query=True, isCancelled=True ) ) :
						pm.progressBar( pbar, edit=True, endProgress=True )
						return

					p1 = vertex.getPosition( 'world' )

					closestPointOnMeshNode = pm.nodetypes.ClosestPointOnMesh()
					mesh.getShape().worldMesh >> closestPointOnMeshNode.inMesh
					closestPointOnMeshNode.inPosition.set( p1 )
					idx = closestPointOnMeshNode.closestVertexIndex.get()
					pm.delete( closestPointOnMeshNode )

					meshvertex = mesh.vtx[ idx ]

					if( not meshvertex in vertexweights.keys() ) :
						vertexweights[ meshvertex ] = []

					vertexweights[ meshvertex ].append( [ joint, weights[i] ] )


			pm.progressBar( pbar, edit=True, step=s )

		vlog.close()
		
		weightsfile = open( weightsloc, 'w+' )
		pickle.dump( vertexweights, weightsfile )
		weightsfile.close()

		skinjointsfile = open( skinjointsloc, 'w+' )
		pickle.dump( skinjoints, skinjointsfile )
		skinjointsfile.close()


	# now we'll rebind the mesh and apply the weights saved from earlier

	if( not new ) :
		vertexweights = pickle.load( open( weightsloc ) )
		skinjoints = pickle.load( open( skinjointsloc ) )


	pm.progressBar( pbar, edit=True, beginProgress=True, isInterruptable=True,
					status='"Reskinning..."',
					maxValue=len( vertexweights )
	)

	pm.delete( mesh, ch=True )
	pm.select( skinjoints )
	pm.select( mesh, add=True )
	newskin = pm.animation.skinCluster( toSelectedBones=True )
	
	for i, vertex in enumerate( vertexweights ) :
		jointweights = vertexweights.get( vertex )
		for jointweight in jointweights :
			pm.animation.skinPercent( newskin, vertex, tv=( str(jointweight[0]), float(jointweight[1]) ) )

		pm.progressBar( pbar, edit=True, step=i )

	pm.progressBar( pbar, edit=True, endProgress=True )


	print 'Completed combining skins on %s' % mesh
	return True


def _get_vert_weight_dict() :
	sel = pm.ls( sl=True )
	if( len( sel ) != 1 ) :
		pm.error( 'Please select ONE mesh transform' )

	mesh = sel[0]
	if( mesh.type() != 'transform' ) :
		pm.error( 'Please select a MESH TRANSFORM' )

	# get the skincluster
	skinclusters = []
	for node in pm.listHistory( mesh ) :
		if( type( node ) == pm.nodetypes.SkinCluster ) :
			skinclusters.append( node )

	vertweightdict = {}

	for skincluster in skinclusters :
		for joint in skincluster.getWeightedInfluence() :
			verts, weights = skincluster.getPointsAffectedByInfluence( joint )
			for i, vert in enumerate( verts[0] ) :
				weight = weights[i]
				
				if( not vert in vertweightdict.keys() ) :
					vertweightdict[ vert ] = []

				vertweightdict[ vert ].append( ( joint, weight ) )

	return vertweightdict, skinclusters


def select_influences( _maxinfluences=2 ) :
	vertweightdict = _get_vert_weight_dict()[0]

	pm.select( None )

	for vert, weightlist in vertweightdict.iteritems() :		
		if( len( weightlist ) > 2 ) :
			print vert, len(weightlist)
			pm.select( vert, add=True )


def reduce_influences( _maxinfluences=2 ) :
	vertweightdict, skinclusters = _get_vert_weight_dict()

	# ONLY WORKS WITH ONE SKINCLUSTER ATM - TOO LAZY TO FIX RIGHT NOW


	skincluster = skinclusters[0]

	c = len( vertweightdict )
	for vert, weightlist in vertweightdict.iteritems() :
		
		print c

		weightlist = sorted( weightlist, key=lambda x: x[1] )[::-1]
		
		keepweightlist = []
		for i in range( _maxinfluences ) :
			if( len( weightlist ) > 0  ) :
				keepweightlist.append( weightlist.pop( 0 ) )
		
		
		if( len( weightlist ) > 0 ) :
			shareweight = sum( zip( *weightlist )[1] ) / _maxinfluences

			for i in range(len(keepweightlist)) :
				weight = keepweightlist[i]
				keepweightlist[i] = ( weight[0], weight[1] + shareweight)

		pm.animation.skinPercent( skincluster, vert, tv=keepweightlist )

		c -= 1



			