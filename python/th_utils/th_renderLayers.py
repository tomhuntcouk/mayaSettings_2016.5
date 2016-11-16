import pymel.core as pm
import os

def create( renderLayer = 'defaultRenderLayer' ) :

	passes = [ 
	    ( 'ao', 'AO' ),
	    ( 'colour', 'DIFRAW' ),
	    ( 'diffuse', 'DIFFNS' ),
	    ( 'irradience', 'DIRIRR' ),
	    ( 'indirect', 'INDIRR' ),
	    ( 'matte', 'MATTE' ),
	    ( 'refraction', 'REFR' ),
	    ( 'reflection', 'REFL' ),
	    ( 'shadow', 'SHDRAW' ),
	    ( 'specular', 'SPECNS' ),
	    # ( 'opacity', 'OPACTY' )
	]

	translist = [ 'colour', 'diffuse', 'irradience', 'indirect' ]

	rl = pm.PyNode( renderLayer )

	for p in passes :
		rpname = '%s_PASS' % ( p[0] )
		try :
			rp = pm.PyNode( rpname )
		except :
			rp = pm.rendering.shadingNode( 'renderPass', asRendering=True, name=rpname )
	    
		pm.rendering.setRenderPassType( rp, type=p[1] )

		if( p[0] in translist ) :
			rp.useTransparency = 1
			rp.transparentAttenuation = 1
	    
		try :
			pm.general.connectAttr( rl.renderPass, rp.owner, nextAvailable=True )	        
		except :
			print rp

	if( 'ao' in [ p[0] for p in passes ] ) :
		print 'Turning on Anbient Occlusion'

			
def reference_lightcam_rig() :

	lightcampath = 'xrefs/pepper_lightcam/dog_lightscamera.ma'
	projectpath = pm.Workspace().getPath()
	fullpath = os.path.join( projectpath, lightcampath )

	for r in pm.listReferences() :
		filepathwithoutprojectpath = str(r).replace( projectpath, '' )
		if lightcampath in filepathwithoutprojectpath :
			print 'Lightcam rig already loaded: %s' % ( r.refNode )
			return False

	print 'Referencing lightcam rig from %s' % ( fullpath )

	try :
		pm.createReference(
			fullpath,
			groupReference=True,
			groupName='lightcam',
			namespace='dog_lightscamera'
		)
		return True
	except :
		pm.err( 'Could not reference file %s. Do you have your project set correctly?' % ( fullpath ) )
		return False

			
def set_render_settings() :
	
	print 'Setting up render'
	pm.renderSettings( camera='dog_lightscamera:camera2' )


