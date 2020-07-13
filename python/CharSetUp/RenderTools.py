import maya.cmds as cmds
import maya.mel as mel



def RenderSettings(Rsettings = [1,1,1,1]):
    #Get render ViewPort2.0 settings... 
    Attributes = ["motionBlurEnable","ssaoEnable","lineAAEnable","multiSampleEnable"]
    Settings   =  []
    i = 0
    for Attr in Attributes:
        Settings.append(cmds.getAttr("hardwareRenderingGlobals." + Attr))
        cmds.setAttr("hardwareRenderingGlobals." + Attr, Rsettings[i])
        i = i + 1
    return Settings

def Render_PlayBlast():
	viewPanels    = cmds.getPanel(type="modelPanel")
	print viewPanels
	visiblePanels = cmds.getPanel(visiblePanels=True)
	print visiblePanels
	renderPanels  = list( set(viewPanels) & set(visiblePanels) ) 
	print renderPanels


	Scene     = cmds.file(q=True,sn=True,shn=True)
	SceneFull = cmds.file(q=True,sn=True)
	Directory = cmds.file(q=True,sn=True).strip(Scene) + "PlayBlast/"
	FileName  = Scene.split(".")[0] 

	print Scene
	print SceneFull
	print Directory
	print FileName

	#Settings = RenderSettings()



	for panel in renderPanels:
		cmds.setFocus(panel)
		panelName = cmds.panel(panel, q=True, label=True).split(" ")[0]
		Camera = cmds.modelPanel( panel, q=True, camera=True )
		renderPath = Directory + FileName + "_" + Camera + ".mov"
		cmds.playblast( fmt="qt",f=renderPath,fo=True,sqt=0,cc=True,v=False,orn=True,os=True,fp=4,p=100,c="jpeg",quality=100,wh=(1280,720))
		print renderPath
		

def fixThePerspCamera():
    perCam = 'persp'
    cmds.camera(perCam,e=True,sc=False)
    cmds.delete(perCam)
    newCam = cmds.camera()
    cmds.rename(newCam[0] ,'persp')
    cmds.camera('persp',e=True,sc=True)

