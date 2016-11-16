import pymel.all as pm

def create( layout ) :
	print 'Creating Outliner'

	container = pm.verticalLayout( 'th_outliner', p=layout )
	pm.windows.outlinerPanel( p=container )
	
	container.redistribute()

	return container

