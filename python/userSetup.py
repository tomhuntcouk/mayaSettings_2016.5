import pymel.all as pm

def delayed_setup() :
	import th_panel	
	th_panel.ui.create()

pm.mayautils.executeDeferred( delayed_setup )
