import pymel.all as pm
import xml.etree.cElementTree as et
import th_skinClusterMerge
import os, re

global THU_MFT_LOCATOR_MATERIAL_NAME, THU_MFT_ANGLE_TOLERANCE
global THU_MFT_LOCATOR_ATTR, THU_MFT_LOCATORGROUP_ATTR, THU_MFT_SPRITE_ATTR
THU_MFT_LOCATOR_MATERIAL_NAME = 'thu_mft_loc_MAT'
THU_MFT_ANGLE_TOLERANCE = 10
THU_MFT_LOCATOR_ATTR = 'thu_mft_locator'
THU_MFT_LOCATORGROUP_ATTR = 'thu_mft_locator_group'
THU_MFT_SPRITE_ATTR = 'thu_mft_sprite'

def __get_filename_noext( filename ) :
	return filename.split( '.' )[0]

def __get_shading_group_from_material( material ) :
	print material.connections( )


###################################################################################################


def create_locator( name ) :
	pm.select( None )
	global THU_MFT_LOCATOR_MATERIAL_NAME, THU_MFT_LOCATOR_ATTR
	try : material = pm.PyNode( THU_MFT_LOCATOR_MATERIAL_NAME )
	except : material = pm.createSurfaceShader( 'lambert', name=THU_MFT_LOCATOR_MATERIAL_NAME )[0]
	material.color.set( ( 1, 0, 0 ) )
	material.transparency.set( ( 0.8, 0.8, 0.8 ) )

	loc_name = '%s_%s' % ( name, THU_MFT_LOCATOR_ATTR )
	try : 
		locator_trans = pm.PyNode( loc_name )
	except :
		locator_trans = pm.polyPlane(
			name=loc_name,
			sw=1, sh=1
		)[0]
		pm.sets( material.shadingGroups()[0], edit=True, forceElement=locator_trans )

	if( not locator_trans.hasAttr( THU_MFT_LOCATOR_ATTR ) ) :
		locator_trans.addAttr( THU_MFT_LOCATOR_ATTR, dt='string' )
	locator_trans.setAttr( THU_MFT_LOCATOR_ATTR, name )

	return locator_trans


def create_material( xml_path, suppress_warnings=True ) :
	pm.select( None )
	if( suppress_warnings ) :
		pm.scriptEditorInfo( edit=True, suppressWarings=True )

	tree = et.parse( xml_path )
	root_keys = tree.getroot().keys()
	if( not 'imagePath' in root_keys ) :
		pm.error( 'The XML file does not appear to be a Texture Packer XML' )
	texture_file = tree.getroot().get( 'imagePath' )
	texture_path = os.path.join( os.path.dirname( xml_path ), texture_file );
	
	material_name = __get_filename_noext( texture_file ) + '_MAT'
	try : material = pm.PyNode( material_name )
	except : material = pm.createSurfaceShader( 'lambert', name=material_name )[0]
	try : material_file = material.connections( type='file' )[0]
	except : material_file = pm.File( name=__get_filename_noext( texture_file ) + '_FILE' )
	try : material_file.outColor >> material.color
	except : pass
	try : material_file.outTransparency >> material.transparency
	except : pass
	material_file.fileTextureName.set( texture_path )

	if( suppress_warnings ) :
		pm.scriptEditorInfo( edit=True, suppressWarings=False )

	return material


def create_mesh( xml_path, name, locator=None ) :
	pm.select( None )
	tree = et.parse( xml_path )
	root_keys = tree.getroot().keys()
	if( not 'imagePath' in root_keys ) :
		pm.error( 'The XML file does not appear to be a Texture Packer XML' )
	texture_size = ( tree.getroot().get( 'width' ), tree.getroot().get( 'height' ) )

	sprite = tree.find( ".//*[@n='%s']" % ( name ) )
	material = create_material( xml_path )

	if( not len( material.shadingGroups() ) ) :
		pm.error( 'Material %s is not connected to a Shading Group. Aborting.' )

	plane_name = __get_filename_noext( name ) + '_G'
	if( locator ) :
		plane_name = '%s_%s' % ( locator.name(), plane_name )
	
	try : 
		plane_trans = pm.PyNode( plane_name )		
	except :
		# v = pm.datatypes.Vector( float(sprite.get('w')) / 100.0, float(sprite.get('h')) / 100.0 )
		# v = v.normal()
		w_scale = float(sprite.get('w')) / 100.0
		h_scale = float(sprite.get('h')) / 100.0
		w_h = w_scale / h_scale
		h_w = h_scale / w_scale
		if( w_h > h_w ) :
			wp = 1.0 / w_h
			# print wp
			w_scale = 1.0
			h_scale = 1.0 / w_h
			# print 'w_h', w_scale, h_scale
		else :
			hp = 1.0 / h_w
			# print hp
			h_scale = 1.0
			w_scale = 1.0 / h_w
			# print w_h, h_w
			# print 'h_w', w_scale, h_scale
		plane_trans = pm.polyPlane(
			name=plane_name,
			sw=1, sh=1,			
			w=w_scale, h=h_scale
		)[0]
	plane_shape = plane_trans.getShape()

	if( not plane_trans.hasAttr( THU_MFT_SPRITE_ATTR ) ) :
		plane_trans.addAttr( THU_MFT_SPRITE_ATTR, dt='string' )
	plane_trans.setAttr( THU_MFT_SPRITE_ATTR, name.replace( '.png', '' ) )

	pm.sets( material.shadingGroups()[0], edit=True, forceElement=plane_trans )

	sx = ( float( sprite.get( 'x' ) ) / float( texture_size[0] ) )
	sy = 1 - ( float( sprite.get( 'y' ) ) / float( texture_size[1] ) )
	sw = ( float( sprite.get( 'w' ) ) / float( texture_size[0] ) )
	sh = ( float( sprite.get( 'h' ) ) / float( texture_size[1] ) )

	uv_positions = (
		( sx, sy - sh ),		
		( sx + sw, sy - sh ),
		( sx, sy ),
		( sx + sw, sy )
	)

	for uv, uv_position in zip( plane_shape.uvs, uv_positions ) :
		pm.polyEditUV( uv, r=False, u=uv_position[0], v=uv_position[1] )

	if( locator ) :
		# print locator
		plane_trans.setParent( locator )
		plane_trans.setTranslation( ( 0, 0, 0 ) )
		plane_trans.setRotation( ( 0, 0, 0 ) )
		plane_trans.setScale( ( 1, 1, 1 ) )		
		locator_bounds = locator.getBoundingBox()
		plane_bounds = plane_trans.getBoundingBox()
		if( plane_bounds.width() > plane_bounds.height() ) :
			pass
		else :
			s = locator_bounds.height() / plane_bounds.height()
			# plane_trans.setScale( (s, s, s) )
			
		

	pm.select( plane_trans )
	return plane_trans


###################################################################################################


def __get_next_edges( edge, prev_edge, reverse=False ) :
	edge_vector = ( edge.getPoint(0, space='world') - edge.getPoint(1, space='world') ).normal()	
	try : prev_edge_vector = ( prev_edge.getPoint(0, space='world') - prev_edge.getPoint(1, space='world') ).normal()	
	except : prev_edge_vector = None

	next_edges = []
	viable_planar_edges = []
	viable_normal_edges = []
	# viable_ortho_edges = []

	normals = [ f.getNormal() for f in edge.connectedFaces() ]
	normal = reduce( lambda x, y : x + y, normals ) / len( normals )
	connectedEdges = edge.connectedEdges()
	if( not reverse ) :
		connectedEdges = list(connectedEdges)[::-1]

	for connected_edge in  connectedEdges :
		connected_edge_vector = ( connected_edge.getPoint(0) - connected_edge.getPoint(1) ).normal()		

		# if edges are planar, the edge is viable
		angle = pm.degrees( edge_vector.angle( connected_edge_vector ) )				
		if( abs( 180.0 - angle ) <= THU_MFT_ANGLE_TOLERANCE or abs( 0.0 - angle ) <= THU_MFT_ANGLE_TOLERANCE ) :
			viable_planar_edges.append( connected_edge )
			continue

		# if edge and normal and planar, the edge is vaiable
		angle = pm.degrees( connected_edge_vector.angle( normal ) )		
		if( abs( 180.0 - angle ) <= THU_MFT_ANGLE_TOLERANCE or abs( 0.0 - angle ) <= THU_MFT_ANGLE_TOLERANCE ) :
			viable_normal_edges.append( connected_edge )
			continue		

		# if edge is in the opposite direction as prev_edge, it may be viable
		if( prev_edge_vector ) :			
			dot = connected_edge_vector.dot( prev_edge_vector )
			# print dot, prev_edge, connected_edge
			if( abs( -1.0 - dot ) <= 0.01 or abs( 1.0 - dot ) <= 0.01 ) :
				if( connected_edge is not prev_edge ) :				
					viable_normal_edges.append( connected_edge )

		# # if edges are orthogonal relative to upvector, the edge is viable
		# angle = pm.degrees( connected_edge_vector.angle( up_edge_cross ) )
		# if( abs( 180.0 - angle ) <= THU_MFT_ANGLE_TOLERANCE or abs( 0.0 - angle ) <= THU_MFT_ANGLE_TOLERANCE ) :
		# 	# next_edges.append( connected_edge )
		# 	viable_ortho_edges.append( connected_edge )
		# 	continue		

		
	if( len( viable_planar_edges ) ) : next_edges = viable_planar_edges
	else : next_edges = viable_normal_edges

	if( prev_edge ) :
		if( prev_edge in next_edges ) :
			next_edges.pop( next_edges.index( prev_edge ) )

	if( len( next_edges ) ) : 
		return next_edges[0]
	elif( len( viable_normal_edges ) ) :
		return viable_normal_edges[0]
	else : return None


def __get_edge_loop( edge, edgeloop=[], prev_edge=None ) :	
	next_edge = __get_next_edges( edge, prev_edge )
	# edgeloop.append( edge )
	if( next_edge ) :		
		if( next_edge not in edgeloop ) :
			# print next_edge
			edgeloop.append( next_edge )
			__get_edge_loop( next_edge, edgeloop, edge )
	return edgeloop


def __create_curve_from_edge( edge ) :
	edgeloop = __get_edge_loop( edge, [], None )
	edgeloop.insert(0, edge )
	edge_curves = []
	for edgeloop_edge in edgeloop :
		edge_curves.append( pm.curve(
			# name=n,
			degree=1,
			ws=True,
			point=[ v.getPosition() for v in edgeloop_edge.connectedVertices() ]
		) )	

	pm.select(None)
	if( len( edge_curves ) > 1 ) :
		merged_curve = pm.attachCurve( edge_curves[:-1], method=1, keepMultipleKnots=False, ch=False )[0]
		edge_curves.pop( edge_curves.index(merged_curve) )
		# closed_curve = pm.closeCurve( merged_curve )[0]
		closed_curve = merged_curve
		# pm.delete( merged_curve )
	else :
		closed_curve = None
	pm.delete( edge_curves )		
	return closed_curve, edgeloop



def create_curves_from_mesh( mesh ) :	
	global THU_MFT_ANGLE_TOLERANCE

	try :
		edges = mesh.edges
	except :
		pm.error( 'Could not get edges from %s' % ( mesh ) )

	edge_curve_group_name = mesh.name().split( ':' )[-1] + '_edgeCurve_GRP'
	try : edge_curve_group = pm.PyNode( edge_curve_group_name )
	except : edge_curve_group = pm.group( name=edge_curve_group_name, world=True, empty=True )

	converted_edges = []
	for c, edge in enumerate( edges ) :
		if( edge not in converted_edges ) :
			print 'Processing edge %s of %s' % ( c, len(edges) )		
			merged_curve, edgeloop = __create_curve_from_edge( edge )
			pm.select( None )
			converted_edges.extend( edgeloop )
			# print merged_curve
			if( merged_curve ) :
				merged_curve.setParent( edge_curve_group )

	return edge_curve_group

def vert_on_rect_edge( vert, rect ) :
	vp = vert.getPosition( )
	mn = rect.min()
	mx = rect.max()
	onedge = False
	for axis in range( 0, 3 ) :
		if( vp[axis] == mn[axis] ) : onedge = True
		if( vp[axis] == mx[axis] ) : onedge = True	
	return onedge


def delete_vertex( mesh ) :
	# print mesh
	pm.select(None)
	for v in mesh.getShape().vtx :
		d = True
		if( vert_on_rect_edge( v, mesh.getBoundingBox() ) ) :
			d = False
		try :			
			if( len( v.connectedEdges() ) > 2 ) :
				d = False
		except : 
			d = False
		
		if(d) :
			# print v
			pm.delete(v)
	
	pm.polyMergeVertex( mesh, d=0.001, am=1 )	
	
	# faces = [f for f in mesh.f]

	# for i in range(len(faces)) :
	# 	try : f = faces[i]
	# 	except : break

	# 	if( f.isZeroArea() ) :
	# 		# print f
	# 		pm.delete(f)			
	# 		delete_vertex(mesh)
	# 		break

	pm.delete( mesh, ch=True )
	return mesh



def project_curves_onto_mesh( mesh, curves_grp, direction ) :
	# projected_curves = []	
	mesh = mesh
	old_meshes = []
	for i, curve in enumerate( curves_grp.getChildren( ) ) :		
		try :
			if( not type(curve.getShape()) is pm.NurbsCurve ) :				
				continue
		except :			
			continue				

		while True :
			nv = len(mesh.vtx)
			mesh = delete_vertex(mesh)
			if( len(mesh.vtx) == nv ) : break

		projected_curves = pm.polyProjectCurve( mesh, curve, direction=direction )[0]
		pm.delete( projected_curves.getChildren()[1:] )
		projected_curve = projected_curves.getChildren()[0]		

		split_mesh = pm.polySplit( mesh, detachEdges=0, projectedCurve=projected_curve )
		# print projected_curve
		split_mesh = split_mesh[0]

		pm.delete( split_mesh, ch=True )
		old_meshes.append( mesh )	

		mesh = split_mesh			

		if( projected_curves ) :
			pm.delete( projected_curves )

		# if( i == 10 ) : return

	for old_mesh in old_meshes :
		try : pm.delete( old_mesh )
		except : 
			pm.warning( 'Could not delete %s' % (old_mesh) )
	

	pm.polyTriangulate( mesh )
	# pm.polyQuad( mesh )
	# -ver 1 -trm 0 -p 50 -vct 0 -tct 0 -shp 0.5326 -keepBorder 1 -keepMapBorder 1 -keepColorBorder 1 -keepFaceGroupBorder 1 -keepHardEdge 1 -keepCreaseEdge 1 -keepBorderWeight 0.5 -keepMapBorderWeight 0.5 -keepColorBorderWeight 0.5 -keepFaceGroupBorderWeight 0.5 -keepHardEdgeWeight 0.5 -keepCreaseEdgeWeight 0.5 -useVirtualSymmetry 0 -symmetryTolerance 0.01 -sx 0 -sy 1 -sz 0 -sw 0 -preserveTopology 1 -keepQuadsWeight 1 -vertexMapName "" -replaceOriginal 1 -cachingReduce 1 -ch 1
	# pm.polyReduce( mesh, ver=True, trm=False, p=50, replaceOriginal=True, kb=True, kbw=1.0, kmb=True, kmw=1.0, kfb=True, kfw=1.0, kqw=1.0 )
	pm.polySoftEdge( mesh, a=180, ch=True )
	pm.delete( mesh, ch=True )


def point_in_rect_bb( point, bb ) :
	# print point, bb.min(), bb.max()
	if( point[0] > bb.min()[0] and point[0] < bb.max()[0] ) :
		if( point[1] > bb.min()[1] and point[1] < bb.max()[1] ) :
			return True
	return False



def project_curves_onto_mesh2( mesh, source_mesh, direction ) :
	# duplicate sources_mesh
	dup_source_mesh = pm.duplicate( source_mesh )[0]
	dup_source_mesh.setParent(None)

	# create curve around mesh	
	edge_curves = []
	for edge in mesh.getShape().e :
		edge_curves.append( pm.curve(
			# name=n,
			degree=1,
			ws=True,
			point=[ v.getPosition(space='world') for v in edge.connectedVertices() ]
		) )
	merged_curve = pm.attachCurve( edge_curves, method=1, keepMultipleKnots=False, ch=False )[0]
	merged_curve = pm.duplicate( merged_curve )
	pm.delete( edge_curves )

	# project curve onto dup_source_mesh	
	projected_curves = projected_curves = pm.polyProjectCurve( dup_source_mesh, merged_curve, direction=direction )[0]
	# pm.delete( projected_curves.getChildren()[1:] )
	projected_curve = projected_curves.getChildren()[0]

	split_mesh = pm.polySplit( dup_source_mesh, detachEdges=0, projectedCurve=projected_curve )	
	split_mesh = split_mesh[0]	

	# delete faces not within mesh bounds
	# faces_to_delete = []
	pm.select(None)
	for face in split_mesh.f :
		face_center = ( 0.0, 0.0, 0.0 )
		for v in face.connectedVertices() :
			face_center += v.getPosition( space='world' )
		face_center /= len( face.connectedVertices() )		

		if( point_in_rect_bb( face_center, mesh.getBoundingBox( space='world' ) ) ) :
			# faces_to_delete.append( face )
			dot = face.getNormal( space='world' ).dot( mesh.f[0].getNormal( space='world' ) )
			if( dot > 0.0 )	 :
				pm.select(face, add=True)
		
	# for face in faces_to_delete :		
	# 	dot = face.getNormal( space='world' ).dot( mesh.f[0].getNormal( space='world' ) )
	# 	if( dot > 0.0 )	 :
	# 		pm.select(face, add=True)

	pm.runtime.InvertSelection()
	pm.delete()

	# transfer UVs from mesh to dup_source_mesh
	pm.transferAttributes( mesh, split_mesh, transferUVs=2 )

	# assign mesh material to dup_source_mesh


	# rename dup_source_mesh to mesh
	pm.delete( split_mesh, ch=True )
	n = mesh.name()
	p = mesh.getParent()
	pm.delete( mesh )
	split_mesh.rename( n )

	for attr in split_mesh.listAttr() :		
		if attr.isLocked() : attr.setLocked(False)


	# cleanup

	pm.delete( projected_curves )
	pm.delete( merged_curve )
	pm.delete( dup_source_mesh )

	# split_mesh.centerPivots( True )
	# t = split_mesh.getPivots( worldSpace=1 )[0]
	# split_mesh.setTranslation((-t[0], -t[1], -t[2]), space='world')		
	# pm.makeIdentity( split_mesh, apply=True )
	# split_mesh.setParent( p )
	# split_mesh.setTranslation( ( 0,0,0 ) )
	# pm.makeIdentity( split_mesh, apply=True )

	# position bodge
	split_mesh.setTranslation( ( 0, 0, 1 ), space='world' )
	split_mesh.setParent( p )

	pm.polyTriangulate( split_mesh )

	if( not split_mesh.hasAttr( THU_MFT_SPRITE_ATTR ) ) :
		split_mesh.addAttr( THU_MFT_SPRITE_ATTR, dt='string' )
	split_mesh.setAttr( THU_MFT_SPRITE_ATTR, split_mesh.name().replace( '.png', '' ) )



###################################################################################################

def __get_by_attr( attr, typ=None ) :
	ret = []
	sel = pm.ls( '*.%s' % ( attr ), o=True )
	for obj in sel :		
		if( typ ) :
			if( re.match( typ, obj.name() ) ) :
				ret.append( obj )
		else :
			ret.append( obj )
	# pm.flushUndo()
	return ret

def get_sprites( typ=None ) :
	return __get_by_attr( THU_MFT_SPRITE_ATTR, typ )

def get_locators( typ=None ) :
	return __get_by_attr( THU_MFT_LOCATOR_ATTR, typ )


###################################################################################################


def __red_or_black( suit ) :
	if( suit in [ 'Hearts', 'Diamonds' ] ) : return 'R'
	elif( suit in [ 'Clubs', 'Spades' ] ) : return 'B'
	else : return None 

def get_card_sprites( rank, suit ) :
	sprites = []
	# get rank
	sprites.extend( get_sprites( 'rank.+%s%s' % ( __red_or_black( suit ), rank ) ) )
	# get suit
	sprites.extend( get_sprites( 'suit.+%s' % ( suit ) ) )	
	# get numbers/face
	if( int(rank) < 11 ) :
		# number		
		sprites.extend( get_sprites( 'number_%s.+%s' % ( rank, suit ) ) )
	elif( int(rank) == 14 ) :
		# ace			
		sprites.extend( get_sprites( 'face.+%s%s' % ( suit[0], rank ) ) )
	else :		
		# face
		sprites.extend( get_sprites( 'royalty.+%s%s' % ( suit[0], rank ) ) )

	return sprites


def create_card_locators() :
	locators = {}
	rank_locators = [ 'rank_top', 'rank_bottom' ]
	suit_locators = [ 'suit_top', 'suit_bottom' ]
	face_locators = [ 'face' ]
	number_locators = range( 2, 11 )

	locators[ 'rank_locators' ] = []
	for rank_locator in rank_locators :
		locators[ 'rank_locators' ].append( create_locator( rank_locator ) )
	locators[ 'suit_locators' ] = []
	for suit_locator in suit_locators :
		locators[ 'suit_locators' ].append( create_locator( suit_locator ) )
	locators[ 'face_locators' ] = []
	for face_locator in face_locators :
		locators[ 'face_locators' ].append( create_locator( face_locator ) )

	locators[ 'number_locators' ] = []	
	for number in number_locators :
		g_name = 'number_%s_GRP' % ( number )
		try : g = pm.PyNode( g_name )
		except : g = pm.group( name=g_name, empty=True, world=True )
		locators[ 'number_locators' ].append( g )		
		for n in range( number ) :			
			l = create_locator( 'number_%s_%s' % ( number, n ) )
			l.setParent( g )

	for key, item in locators.items() :
		g_name = '%s_GRP' % ( key )
		try : g = pm.PyNode( g_name )
		except : g = pm.group( name=g_name, empty=True, world=True )		
		for i in item : i.setParent(g)

	return locators


def create_ranks( xml_file, mesh_curves_grp, project=False ) :
	colours = [ 'B', 'R' ]
	ranks = range( 2, 15 )	
	# ranks = range( 11, 12 )	
	total = len( colours ) * len( ranks )
	i = 0
	for locator in get_locators( 'rank' ) :
		print 'Processing rank'
		for colour in colours :
			for rank in ranks :
				print locator, colour, rank

				sprite = '%s%s.png' % ( colour, rank )
				sprite_mesh = create_mesh(
					xml_file,
					sprite,
					locator
				)
				if( project ) :
					# project_curves_onto_mesh( sprite_mesh, mesh_curves_grp, ( 0, 0, 1 ) )	
					project_curves_onto_mesh2( sprite_mesh, mesh_curves_grp, ( 0, 0, 1 ) )					


def create_suits( xml_file, mesh_curves_grp, project=False ) :	
	suits = [ 'Hearts', 'Spades', 'Diamonds', 'Clubs' ]	
	for locator in get_locators( 'suit' ) :
		for suit in suits :			
			print locator, suit
			sprite = '%s.png' % ( suit )
			sprite_mesh = create_mesh(
				xml_file,
				sprite,
				locator
			)
			if( project ) :
				# project_curves_onto_mesh( sprite_mesh, mesh_curves_grp, ( 0, 0, 1 ) )		
				project_curves_onto_mesh2( sprite_mesh, mesh_curves_grp, ( 0, 0, 1 ) )		


def create_numbers( xml_file, mesh_curves_grp, project=False ) :
	suits = [ 'Hearts', 'Spades', 'Diamonds', 'Clubs' ]
	numbers = range( 2, 11 )
	for number in numbers :
		for locator in get_locators( 'number_%s' % ( number ) ) :
			for suit in suits :
				print locator, suit, number
				sprite = '%s.png' % ( suit )
				sprite_mesh = create_mesh(
					xml_file,
					sprite,
					locator
				)
				if( project ) :
					# project_curves_onto_mesh( sprite_mesh, mesh_curves_grp, ( 0, 0, 1 ) )		
					project_curves_onto_mesh2( sprite_mesh, mesh_curves_grp, ( 0, 0, 1 ) )		


def create_faces( xml_file, mesh_curves_grp, project=False ) :	
	suits = [ 'D', 'S', 'H', 'C' ]
	faces = range( 14, 15 )
	for locator in get_locators( 'face' ) :
		for suit in suits :
			for face in faces :
				print locator, suit, face				
				sprite = '%s%s.png' % ( suit, face )				
				sprite_mesh = create_mesh(
					xml_file,
					sprite,
					locator
				)				
				if( project ) :
					# project_curves_onto_mesh( sprite_mesh, mesh_curves_grp, ( 0, 0, 1 ) )
					project_curves_onto_mesh2( sprite_mesh, mesh_curves_grp, ( 0, 0, 1 ) )	


def create_royalty( xml_file, mesh_curves_grp, project=False ) :	
	suits = [ 'D', 'S', 'H', 'C' ]
	faces = range( 11, 14 )
	for locator in get_locators( 'royalty' ) :
		for suit in suits :
			for face in faces :				
				print locator, suit, face
				sprite = '%s%s.png' % ( suit, face )				
				sprite_mesh = create_mesh(
					xml_file,
					sprite,
					locator
				)				
				if( project ) :
					# project_curves_onto_mesh( sprite_mesh, mesh_curves_grp, ( 0, 0, 1 ) )
					project_curves_onto_mesh2( sprite_mesh, mesh_curves_grp, ( 0, 0, 1 ) )					


def merge_cards( start, end, suit ) :
	cards = []
	# suits = [ 'Hearts', 'Diamonds', 'Clubs', 'Spades' ]
	ranks = range( start, end )

	total_cards = len( ranks )
	i = 0
	# for suit in suits :
	try : suit_group = pm.PyNode( '%s_cards_GRP' % ( suit ) )
	except : suit_group = pm.group( name='%s_cards_GRP' % ( suit ), empty=True, world=True )
	for rank in ranks :
		print 'Processing card %s of %s' % ( i, total_cards )
		# print rank, suit
		# print get_card_sprites( rank, suit )
		# return
		card_sprites = pm.duplicate( get_card_sprites( rank, suit ) )	
		for card_sprite in card_sprites : card_sprite.setParent(None)
		card = pm.polyUnite( card_sprites, mergeUVSets=1, ch=True )[0]		
		pm.delete( card, ch=True )
		for cs in card_sprites :
			try : pm.delete( cs )
			except : pass
		card.rename( '%s_%s_G' % ( suit, rank ) )
		card.setParent( suit_group )
		cards.append( card )
		# pm.flushUndo()
		i += 1
	return cards


def bind_card( source_mesh, target_mesh, combine=True ) :

	hasskin = True
	try :
		source_skin_cluster = pm.PyNode( pm.mel.eval( 'findRelatedSkinCluster %s' % ( source_mesh ) ) )
		joints = source_skin_cluster.getWeightedInfluence()	
	except :
		hasskin = False
			
	if( combine ) :
		p = target_mesh.getParent()
		dup_source_mesh = source_mesh.duplicate()[0]
		dup_target_mesh = target_mesh.duplicate()[0]
				
		bind_mesh = pm.polyUnite( dup_source_mesh, dup_target_mesh )[0]
		bind_mesh.rename( target_mesh.name() )
		pm.delete( bind_mesh, ch=True )
		try :
			pm.delete( dup_source_mesh )
		except : pass
	else :
		bind_mesh = target_mesh

	if hasskin :
		target_skin_cluster = pm.skinCluster( bind_mesh, joints )	
		pm.copySkinWeights( source_mesh, bind_mesh, ia='oneToOne', sa='closestPoint' )

		pm.select( bind_mesh )
		th_skinClusterMerge.reduce_influences()
	pm.select(None)



