"""

Creates subfolders for an asset within a Maya project

Installation
____________

Paste this code snippet into your Maya Script Editor

import imp, os
import pymel.core as pm
path = os.path.join( pm.system.Workspace.getPath(), "scripts/createFolders.py" )
cf = imp.load_source( "cf", path )
cf.main()

In the Script Editor select File->Save Script to Shelf
Enter a suitable name (e.g. Create Folders)


How to use
__________

Make sure your Maya Project is set to your game's Maya folder
Click the Create Folders shelf button
Enter the name of your asset e.g. pepper_dog
Select which folders you would like to create a subfolder in
Click 'Create Folders'

"""


import os, sys
import pymel.core as pm

def main() :

	ws = pm.system.Workspace.getPath()
	
	if( pm.windows.window( 'w_th_createFolders', q=True, exists=True ) ) :
		pm.deleteUI( 'w_th_createFolders' )	

	win = pm.windows.window( 'w_th_createFolders', title='Asset Folders' )
	l = pm.windows.verticalLayout()

	assname = pm.windows.textField( text='Asset name' )

	checkboxes = []
	for f in os.listdir( ws ) :		
		if( os.path.isdir( os.path.join( ws, f ) ) ) :
			if( f[0] != '.' ) :
				checkboxes.append( pm.windows.checkBox( label=f ) )

	pm.windows.button( label='Create Folders', c=lambda *args : createFolders( assname, checkboxes, ws )  )

	l.redistribute()
	win.show()


def createFolders( assname, checkboxes, ws ) :

	name = assname.getText()
	if( name == 'Asset name' or name == '' ) :
		pm.error( 'Please choose an asset name' )

	total = 0;
	success = 0
	for checkbox in checkboxes :
		if( checkbox.getValue() ) :
			total += 1
			folder = os.path.join( ws, checkbox.getLabel() )

			if( os.path.exists( folder ) ) :
				try :
					os.mkdir( os.path.join( folder, name ) )
					success += 1
				except OSError :
					pm.warning( 'Could not create %s/%s. It may already exist' % ( folder, name ) )
			else :
				pm.warning( folder + ' does not exist. skipping...' )

	print 'Sucessfully created %s out of %s folders' % ( success, total )


if __name__ == '__main__':
	main()
