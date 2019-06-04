import pymel.all as pm
import os
from glob import glob

def __create_shelf_frame( shelf_file, shelf_name, layout ) :
	shelf_function = os.path.basename( shelf_file ).replace( '.mel', '' )	
	shelf_frame = pm.frameLayout( label=shelf_name, collapsable=True, p=layout )			
	shelf_layout = pm.gridLayout( ag=True, nc=8 )
	if( 'Script found' in pm.mel.whatIs( shelf_file) ) :
		pm.mel.eval( 'source "%s"' % ( shelf_file ) )
		if( 'Mel procedure found' in pm.mel.whatIs( shelf_function ) ) :
			pm.mel.eval( '%s()' % ( shelf_function ) )
		else :
			pm.warning('Could not find shelf function : %s' % (shelf_function))
	else :
			pm.warning('Could not find shelf file : %s' % (shelf_file))
	
	return shelf_frame

def __load_shelves( layout ) :
	print 'Loading shelves'
	children = layout.getChildArray()
	if children :
		for child in children :
			pm.deleteUI( child )

	shelf_frames = []
	shelves_paths = pm.internalVar( userShelfDir=True )
	shelves_paths = shelves_paths.split(':')
	shelves = []
	for shelves_path in shelves_paths :
		shelves = glob( shelves_path + '/shelf*.mel' )
		shelves.extend(shelves)

	print shelves_path
	print shelves
	for i in range( 1, len( shelves ) + 1 ) :
		# shelf_file = shelves[i-1]
		# shelf_name = os.path.basename(shelves[i-1]).replace( 'shelf_', '' )	

		shelf_file = pm.Env.optionVars.get( 'shelfFile%s' % i )	
		shelf_file = os.path.join( shelves_path, '%s.mel' % shelf_file )
		if( os.path.isfile( shelf_file ) ) :
			shelf_name = pm.Env.optionVars.get( 'shelfName%s' % i )
			shelf_frames.append( __create_shelf_frame( shelf_file, shelf_name, layout ) )
		
	layout.redistribute( *[0] * len( shelf_frames ) )
	for shelf_frame in shelf_frames :
		shelf_frame.setCollapse( True )

	return shelf_frames


def create( layout ) :
	print 'Creating shelves'
	container = pm.verticalLayout( p=layout )
	scroll_layout = pm.scrollLayout( p=container )
	top_layout = pm.verticalLayout( p=scroll_layout )
	bottom_layout = pm.verticalLayout( p=container )

	shelf_frames = __load_shelves( top_layout )
	pm.button(
		label='Refresh Shelves', 
		c=lambda x : __load_shelves( top_layout ),
		p=bottom_layout
	)
	pm.button(
		label='Edit Shelves',
		c=lambda x : pm.mel.eval( 'ShelfPreferencesWindow' ), 
		p=bottom_layout
	)	

	bottom_layout.redistribute()
	container.redistribute( 12, 1 )





	


