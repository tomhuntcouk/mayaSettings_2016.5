import pymel.all as pm
import shelves, scripteditor, layerchannel, outliner, renaming

class Widgets( dict ) :
	def __init__( self ) :
		dict.__init__( self )

	# def __getitem__( key ) :
	# 	return self[ key ]


TH_P_DOCK = 'th_panel_dock'
TH_P_WIN = 'th_panel_window'
global TH_P_WIDGETS


def init() :
	global TH_P_WIDGETS	
	try : 
		TH_P_WIDGETS
		del( TH_P_WIDGETS )
	except : pass
	TH_P_WIDGETS = Widgets()


def create() :
	global TH_P_WIDGETS
	init()

	layerchannel.cleanup()	

	if( pm.dockControl( TH_P_DOCK, exists=True ) ) :
		pm.deleteUI( TH_P_DOCK )
	if( pm.window( TH_P_WIN, exists=True ) ) :
		pm.deleteUI( TH_P_WIN )

	TH_P_WIDGETS[ 'window' ] = pm.window( TH_P_WIN )
	TH_P_WIDGETS[ 'main' ] = pm.paneLayout( configuration='vertical3', staticWidthPane=1 )	
	TH_P_WIDGETS[ 'tabs' ] = pm.tabLayout( p=TH_P_WIDGETS[ 'main' ], width=274, height=100 )
	TH_P_WIDGETS[ 'column1' ] = pm.verticalLayout( p=TH_P_WIDGETS[ 'main' ], height=100 )
	TH_P_WIDGETS[ 'column2' ] = pm.verticalLayout( p=TH_P_WIDGETS[ 'main' ] )	
	
	# tabs ##########################################################################################
	
	# shelves
	TH_P_WIDGETS[ 'tab_shelves' ] = pm.verticalLayout( p=TH_P_WIDGETS['tabs'] )	
	TH_P_WIDGETS[ 'tabs' ].setTabLabel( ( TH_P_WIDGETS[ 'tab_shelves' ], 'Shelves' ) )
	shelves.create( TH_P_WIDGETS[ 'tab_shelves' ] )
	TH_P_WIDGETS[ 'tab_shelves' ].redistribute()

	# renaming
	TH_P_WIDGETS[ 'tab_renaming' ] = pm.verticalLayout( p=TH_P_WIDGETS['tabs'] )
	renaming.create( TH_P_WIDGETS[ 'tab_renaming' ] )
	TH_P_WIDGETS[ 'tabs' ].setTabLabel( ( TH_P_WIDGETS[ 'tab_renaming' ], 'Renaming' ) )
	TH_P_WIDGETS[ 'tab_renaming' ].redistribute()

	# script editor
	TH_P_WIDGETS[ 'tab_scripteditor' ] = pm.verticalLayout( p=TH_P_WIDGETS['tabs'] )		
	TH_P_WIDGETS[ 'tabs' ].setTabLabel( ( TH_P_WIDGETS[ 'tab_scripteditor' ], 'Script Editor' ) )
	scripteditor.create( TH_P_WIDGETS[ 'tab_scripteditor' ] )
	TH_P_WIDGETS[ 'tab_scripteditor' ].redistribute()

	"""

	# column1 ##########################################################################################

	# layer editor / channel box
	TH_P_WIDGETS[ 'channellayer' ] = pm.verticalLayout( p=TH_P_WIDGETS[ 'column1' ] )		
	layerchannel.create( TH_P_WIDGETS[ 'channellayer' ] )		
	TH_P_WIDGETS[ 'channellayer' ].redistribute()
	

	# column2 ##########################################################################################

	# outliner
	TH_P_WIDGETS[ 'outliner' ] = pm.verticalLayout( p=TH_P_WIDGETS[ 'column2' ] )	
	outliner.create( TH_P_WIDGETS[ 'outliner' ] )	
	TH_P_WIDGETS[ 'outliner' ].redistribute()

	TH_P_WIDGETS[ 'tabs' ].setSelectTabIndex( 1 )
	TH_P_WIDGETS[ 'column1' ].redistribute()
	TH_P_WIDGETS[ 'column2' ].redistribute()	
	"""

	TH_P_WIDGETS[ 'dock_panel' ] = pm.dockControl(
		TH_P_DOCK, label='th_panel', 
		area='right', allowedArea=[ 'left', 'right' ], sizeable=True, w=540,
		content=TH_P_WIDGETS[ 'window' ]
	)




