publish = True
annotation = "Quickly edit the basic Camera attributes"
prefix = 'lcCam'

import os
import math
import pymel.core as pm

from lct.src.core.lcWindow import lcWindow as lcWindow
from lct.src.core.lcUtility import Camera as camera
from lct.src.core.lcShelf import Shelf as shelf

import lct.src.core.lcColor as color	
# interface colors
kw = {'hue':0.45, 'saturation':0.5, 'value':0.5}
colorWheel = color.ColorWheel(10, **kw)

basePath = os.path.abspath(os.path.dirname(__file__))+'/'
iconBasePath = os.path.abspath(os.path.dirname(__file__))+"/icons/"

def lcCameraToolsUI(dockable=False, *args, **kwargs):
  ''' '''
  ci = 0 #color index iterator
  windowName = 'lcCameraTools'
  shelfCommand = 'import lct.src.lcCameraTools.lcCameraTools as lcCam\nreload(lcCam)\nlcCam.lcCameraToolsUI()'
  icon = basePath+'lcCameraTools.png'
  winWidth  = 204
  winHeight = 209
  
  mainWindow = lcWindow(windowName=windowName, width=winWidth, height=winHeight, icon=icon, shelfCommand=shelfCommand, annotation=annotation, dockable=dockable, menuBar=True)
  mainWindow.create()
  pm.menu(l='Options', helpMenu=True)
  pm.menuItem(l='Reset Gradient Colors', command=lambda *args: cam_set_default_colors() )

  #
  pm.columnLayout(prefix+'_columLayout_main')
  
  #
  pm.rowColumnLayout(nc=2, cw=([1,50], [2,150]) )
  pm.text(l='Edit:', al='right')
  cameraListDropdown = pm.optionMenu(prefix+'_optionMenu_camera_list', bgc=colorWheel.getColorRGB(ci), w=150, h=25 )
  ci+=1
  cameraListDropdown.changeCommand(lambda *args: cam_get_cam_attrs(cameraListDropdown) )
  pm.setParent(prefix+'_columLayout_main')
  
  #  
  pm.rowColumnLayout(nc=2, cw=([1,125], [2,75]) )
  pm.text(l='Focal Length:', al='right')
  pm.floatField(prefix+'_floatField_focal_length', min=0.0, v=0.0, pre=1, w=75, changeCommand=lambda *args: cam_set_cam_attrs(cameraListDropdown), receiveFocusCommand=lambda *args: cam_set_cam_attrs(cameraListDropdown) )
  pm.text(l='Near Clip Plane:', al='right')
  pm.floatField(prefix+'_floatField_near_clip_plane', min=0.0, v=0.0, pre=4, w=75, changeCommand=lambda *args: cam_set_cam_attrs(cameraListDropdown), receiveFocusCommand=lambda *args: cam_set_cam_attrs(cameraListDropdown) )
  pm.text(l='Far Clip Plane:', al='right')
  pm.floatField(prefix+'_floatField_far_clip_plane', min=0.0, v=0.0, pre=0, w=75, changeCommand=lambda *args: cam_set_cam_attrs(cameraListDropdown), receiveFocusCommand=lambda *args: cam_set_cam_attrs(cameraListDropdown) )
  pm.text(l='Overscan:', al='right')
  pm.floatField(prefix+'_floatField_overscan', min=0.0, v=0.0, pre=3, w=75, changeCommand=lambda *args: cam_set_cam_attrs(cameraListDropdown), receiveFocusCommand=lambda *args: cam_set_cam_attrs(cameraListDropdown) )
  pm.text(l='Background Color:', al='right')
  pm.colorSliderGrp(prefix+'_colorSliderGrp_background_color', cw1=50, rgb=(0.0,0.0,0.0), changeCommand=lambda *args: cam_set_cam_attrs(cameraListDropdown) )
  pm.text(l='Gradient Top:', al='right')
  pm.colorSliderGrp(prefix+'_colorSliderGrp_gradient_top', cw1=50, rgb=(0.54,0.62,0.70), changeCommand=lambda *args: cam_set_cam_attrs(cameraListDropdown) )
  pm.text(l='Gradient Bottom:', al='right')
  pm.colorSliderGrp(prefix+'_colorSliderGrp_gradient_bottom', cw1=50, rgb=(0.1,0.1,0.1), changeCommand=lambda *args: cam_set_cam_attrs(cameraListDropdown) )
  pm.setParent(prefix+'_columLayout_main')
  
  #
  pm.rowColumnLayout(nc=2, cw=([1,175], [2,25]) )
  pm.button(prefix+'_button_toggle_bkgd', l='Toggle Background', bgc=colorWheel.getColorRGB(ci), w=200, h=25, annotation='Toggle between flat color and gradient background', command=lambda *args: camera.toggleBackground() )
  ci+=1
  pm.iconTextButton(w=25, h=25, style='iconOnly', image=iconBasePath+'addToShelf.png', highlightImage=iconBasePath+'addToShelf_over.png', annotation='Add to Shelf', command=lambda *args: shelf.makeShelfButton('Toggle Camera Background', 'from lct.src.core.lcUtility import Camera as camera\ncamera.toggleBackground()', iconBasePath+'toggleBackground.png', "Toggle Camera's Viewport Background") )

  #
  mainWindow.show()
  
  cam_populate_camera_list(cameraListDropdown)  
  cam_get_cam_attrs(cameraListDropdown)

def cam_populate_camera_list(cameraListDropdown, *args, **kwargs):
  ''' '''
  cameraListDropdown.clear()
  
  cameras = pm.ls(type='camera')
  for cam in cameras:
    cameraListDropdown.addItems([cam])

  numItems = cameraListDropdown.getNumberOfItems()
  perspIndex = -1
  for index in range(numItems):
    index = index+1
    cameraListDropdown.setSelect(index)
    currentCam = cameraListDropdown.getValue()
    if currentCam == 'perspShape':
      perspIndex = index
    
  cameraListDropdown.setSelect(perspIndex) #make the default selection the persp camera
  
def cam_get_cam_attrs(cameraListDropdown, *args, **kwargs):
  ''' '''
  camera = cameraListDropdown.getValue()  
  focalLength = pm.getAttr(camera+'.focalLength')
  nearClip = pm.getAttr(camera+'.nearClipPlane')
  farClip = pm.getAttr(camera+'.farClipPlane')
  overscan = pm.getAttr(camera+'.overscan')
  bkgdColor = pm.displayRGBColor('background', query=True)
  topColor = pm.displayRGBColor('backgroundTop', query=True)
  bottomColor = pm.displayRGBColor('backgroundBottom', query=True)
  
  pm.floatField(prefix+'_floatField_focal_length', edit=True, value=focalLength)
  pm.floatField(prefix+'_floatField_near_clip_plane', edit=True, value=nearClip)
  pm.floatField(prefix+'_floatField_far_clip_plane', edit=True, value=farClip)
  pm.floatField(prefix+'_floatField_overscan', edit=True, value=overscan)
  pm.colorSliderGrp(prefix+'_colorSliderGrp_background_color', edit=True, rgb=bkgdColor )
  pm.colorSliderGrp(prefix+'_colorSliderGrp_gradient_top', edit=True, rgb=topColor )
  pm.colorSliderGrp(prefix+'_colorSliderGrp_gradient_bottom', edit=True, rgb=bottomColor )
  
def cam_set_cam_attrs(cameraListDropdown, *args, **kwargs):
  ''' '''
  camera = cameraListDropdown.getValue()
  focalLength = pm.floatField(prefix+'_floatField_focal_length', query=True, value=True)
  nearClip = pm.floatField(prefix+'_floatField_near_clip_plane', query=True, value=True)
  farClip = pm.floatField(prefix+'_floatField_far_clip_plane', query=True, value=True)
  overscan = pm.floatField(prefix+'_floatField_overscan', query=True, value=True)
  bkgdColor = pm.colorSliderGrp(prefix+'_colorSliderGrp_background_color', query=True, rgb=True )
  topColor = pm.colorSliderGrp(prefix+'_colorSliderGrp_gradient_top', query=True, rgb=True )
  bottomColor = pm.colorSliderGrp(prefix+'_colorSliderGrp_gradient_bottom', query=True, rgb=True )
  
  pm.setAttr(camera+'.focalLength', focalLength)
  pm.setAttr(camera+'.nearClipPlane', nearClip)
  pm.setAttr(camera+'.farClipPlane', farClip)
  pm.setAttr(camera+'.overscan', overscan)
  pm.displayRGBColor('background', bkgdColor[0], bkgdColor[1], bkgdColor[2])
  pm.displayRGBColor('backgroundTop', topColor[0], topColor[1], topColor[2])
  pm.displayRGBColor('backgroundBottom', bottomColor[0], bottomColor[1], bottomColor[2])
  
def cam_set_default_colors(*args, **kwargs):
  ''' '''  
  pm.displayRGBColor('background', 0.0, 0.0, 0.0)
  pm.displayRGBColor('backgroundTop', 0.54, 0.62, 0.70)
  pm.displayRGBColor('backgroundBottom', 0.1, 0.1, 0.1)
  
  bkgdColor = pm.displayRGBColor('background', query=True)
  topColor = pm.displayRGBColor('backgroundTop', query=True)
  bottomColor = pm.displayRGBColor('backgroundBottom', query=True)
  
  pm.colorSliderGrp(prefix+'_colorSliderGrp_background_color', edit=True, rgb=bkgdColor )
  pm.colorSliderGrp(prefix+'_colorSliderGrp_gradient_top', edit=True, rgb=topColor )
  pm.colorSliderGrp(prefix+'_colorSliderGrp_gradient_bottom', edit=True, rgb=bottomColor )
  