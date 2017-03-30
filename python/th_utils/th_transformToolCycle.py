# import pymel.all as pm
# global moveToolMode, rotateToolMode, scaleToolMode

# rotateToolMode = None
# scaleToolMode = None

# MAX_MOVE = 3
# pm.mel.eval( 'buildTranslateMM' )
# mm = pm.manipMoveContext( 'Move', q=True, mode=True )
# if( moveToolMode is not None ) :
# 	mm = (mm + 1) % MAX_MOVE
# moveToolMode = mm
# pm.manipMoveContext( 'Move', e=True, mode=mm )


import pymel.all as pm

validIndexes = {
	'Move' : [ 0, 1, 2, 3 ],
	'Rotate' : [ 0, 1, 2 ],
	'Scale' : [ 0, 1, 2, 3 ],
}

def cycle( tool ) :
	tool = tool.capitalize()
	getCmd = "pm.manip%sContext( '%s', q=True, mode=True )" % ( tool, tool )
	currentIndex = eval(getCmd)
	
	indexList = sorted(validIndexes[tool])
	nextIndex = 0	
	for i, index in enumerate( indexList ) :				
		if( index == currentIndex ) :			
			nextIndex = indexList[ (i+1) % len(indexList) ]
			break
		elif( index > currentIndex ) :
			nextIndex = index
			break
	
	setCmd = "pm.manip%sContext( '%s', e=True, mode=%s )" % ( tool, tool, nextIndex )
	eval(setCmd)
	pm.displayInfo( '%s Tool : %s' % ( tool, nextIndex ) )
