import pymel.all as pm

def create( layout ) :
	print 'Creating Script Editor'
	container = pm.paneLayout( configuration='horizontal2', p=layout )
	top_layout = pm.verticalLayout( p=container )
	bottom_layout = pm.verticalLayout( p=container )
	
	cmdreporter = pm.cmdScrollFieldReporter( p=top_layout )
	cmdexecuter = pm.cmdScrollFieldExecuter( sourceType='python', sln=True, bgc=(0.2,0.2,0.2), p=bottom_layout )
	
	top_layout.redistribute()
	bottom_layout.redistribute()

	return container