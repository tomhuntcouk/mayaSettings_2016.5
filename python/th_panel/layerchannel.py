import pymel.all as pm

global TH_LC_GRID

def create( layout ) :
	print 'Creating ChannelBox and Layer Editor'			
	pm.runtime.DisplayLayerEditorWindow()	
	pm.refresh(f=True)

	container = pm.verticalLayout( 'th_layerchannel', p=layout )
	qt_container = container.asQtObject()
	layerchannelui = pm.PyUI( 'MainChannelsLayersLayout' )	
	qt_layerchannelui = layerchannelui.asQtObject()
	
	if( not qt_layerchannelui ) :
		layerchannelui = pm.PyUI( 'MainChannelsLayersLayout' ).parent()
		qt_layerchannelui = layerchannelui.asQtObject()
	
	qt_layerchannelui.setParent( qt_container )

	container.redistribute(0)
	pm.mel.eval('setChannelsLayersVisible( 0 )')	
	return container

def cleanup() :
	try :
		layerchannelui = pm.PyUI( 'MainChannelsLayersLayout' )	
		qt_layerchannelui = layerchannelui.asQtObject()
		c = pm.FormLayout( 'th_layerchannel' )
		if( layerchannelui.parent() == c ) :		
			qt_layerchannelui.setParent(None)	
	except :
		print 'Could not cleanup layer channel box'