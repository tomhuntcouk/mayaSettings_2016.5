import pymel.all as pm
import re

def create( layout ) :
	container = pm.verticalLayout( p=layout )
	top_layout = pm.columnLayout( p=container, adj=True )
	# top_layout = pm.verticalLayout( bgc=(1,0,0), p=container )		
	bottom_layout = pm.scrollLayout( p=container, cr=True )	
	bottom_horiz = pm.horizontalLayout( p=bottom_layout )

	left = pm.frameLayout( label='Old Name', mh=4, mw=4, p=bottom_horiz )
	right = pm.frameLayout( label='New Name', mh=4, mw=4, p=bottom_horiz )		
	list_left = pm.columnLayout( 'th_rename_preview_left', p=left, rs=4 )
	list_right = pm.columnLayout( 'th_rename_preview_right', p=right, rs=4 )
	
	bottom_horiz.redistribute()
	
	# regex
	rename_frame = pm.frameLayout( label='Regex', mh=4, mw=4, p=top_layout )
	rename_layout = pm.columnLayout( p=rename_frame, adj=True, rs=4 )
	
	rename_search = pm.textField( 'th_rename_search', pht='Search', p=rename_layout,
		cc=lambda *args : __update_rename_preview()
	)
	rename_replace = pm.textField( 'th_rename_replace', pht='Replace/Rename', p=rename_layout,
		cc=lambda *args : __update_rename_preview()
	)

	renumber_layout = pm.rowLayout( p=rename_layout, nc=2, adj=True )
	rename_from = pm.textField( 'th_rename_from', pht='Renumber From', p=renumber_layout,
		cc=lambda *args : __update_rename_preview()
	)
	rename_by = pm.textField( 'th_rename_by', pht='Renumber By', p=renumber_layout,
		cc=lambda *args : __update_rename_preview()
	)

	rename_prefix = pm.textField( 'th_rename_prefix', pht='Prefix', p=rename_layout,
		cc=lambda *args : __update_rename_preview()
	)
	rename_suffix = pm.textField( 'th_rename_suffix', pht='Suffix', p=rename_layout,
		cc=lambda *args : __update_rename_preview()
	)
	
	

	pm.button( 
		label='Rename', 
		p=rename_layout,
		c=lambda *args : __rename_from_ui()
	)

	# setup a script job to update preview grids
	pm.scriptJob( 
		p=container,
		e=(		
		'SelectionChanged',
		lambda *args : __populate_preview_grids( list_left, list_right )
	) )

	__populate_preview_grids( list_left, list_right )
	container.redistribute( 1, 3 )



def __populate_preview_grids( list_left, list_right ) :	
	list_left.clear()
	list_right.clear()
	for obj in pm.ls( sl=True ):
		pm.text( label=obj.name(), align='left', p=list_left )
		pm.text( label=obj.name(), align='left', p=list_right )


def __update_rename_preview() :	
	preview_left = pm.ColumnLayout( 'th_rename_preview_left' )
	preview_right = pm.ColumnLayout( 'th_rename_preview_right' )
	old = []
	for item in preview_left.getChildArray() :
		old.append( pm.Text( item ).getLabel()  )
	new = __rename_list_from_textfields( *old )
	preview_right.clear()
	for name in new : pm.text( label=name, align='left', p=preview_right )


def __rename_list_from_textfields( *args ) :	
	# preview = pm.PyUI( 'th_rename_preview_right' )	
	search = pm.TextField( 'th_rename_search' ).getText()
	replace = pm.TextField( 'th_rename_replace' ).getText()
	prefix = pm.TextField( 'th_rename_prefix' ).getText()
	suffix = pm.TextField( 'th_rename_suffix' ).getText()
	fr = pm.TextField( 'th_rename_from' ).getText()
	by = pm.TextField( 'th_rename_by' ).getText()

	ret = []
	for i, name in enumerate(args) :
		if( search and replace ) : name = re.sub( search, replace, name )
		else : 
			if( replace ) : name = replace
		if( prefix ) : name = prefix + name
		if( fr and by ) : name = name.rstrip('0123456789') + str( int(fr) + i * int(by) )
		if( suffix ) : name = name + suffix
		ret.append( name )
		print '+',name
	return ret


def __rename_from_ui() :	
	# rename_replace( pm.ls( sl=True ), searchfield.getText(), replacefield.getText() )
	sel = pm.ls( sl=True )
	new = __rename_list_from_textfields( *[i.name() for i in sel] )
	for name, obj in zip( new, sel ) :
		obj.rename( name )
	pm.select(sel)

def rename( objs ) :	
	for obj in objs :
		obj.rename( re.sub( search, replace, obj.name() ) )

