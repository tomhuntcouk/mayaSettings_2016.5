publish = True
annotation = "Bake Textures and Vertex Color with Mental Ray Batch Bake"
prefix = 'lcBake'

import os
import math
import pymel.core as pm
import time

from lct.src.core.lcWindow import lcWindow as lcWindow
from lct.src.core.lcTexture import Texture as texture
from lct.src.core.lcPath import Path as path
from lct.src.core.lcShelf import Shelf as shelf
from lct.src.core.lcUtility import Plugin as plugin
from lct.src.core.lcBake import Bake as bake

import lct.src.core.lcColor as color	
# interface colors
kw = {'hue':0.45, 'saturation':0.5, 'value':0.5}
colorWheel = color.ColorWheel(10, **kw)

basePath = os.path.abspath(os.path.dirname(__file__))+'/'
iconBasePath = os.path.abspath(os.path.dirname(__file__))+"/icons/"

def lcBatchBakeUI(dockable=False, *args, **kwargs):
  ''' '''
  ci = 0 #color index iterator
  windowName = 'lcBatchBake'
  shelfCommand = 'import lct.src.lcBatchBake.lcBatchBake as lcBake\nreload(lcBake)\nlcBake.lcBatchBakeUI()'
  icon = basePath+'lcBatchBake.png'
  winWidth  = 204
  winHeight = 218
  
  mainWindow = lcWindow(windowName=windowName, width=winWidth, height=winHeight, icon=icon, shelfCommand=shelfCommand, annotation=annotation, dockable=dockable, menuBar=True)
  mainWindow.create()
  pm.menu(l='Options', helpMenu=True)
  pm.menuItem(l='Delete All bake sets', command=lambda *args: lcBake_delete_all_bake_sets(bakeSetListDropdown) )

  #
  pm.columnLayout(prefix+'_columLayout_main')
  
  #
  pm.rowColumnLayout(nc=2, cw=([1,100], [2,100]) )
  pm.button(l='Make Texture', bgc=colorWheel.getColorRGB(ci), w=100, h=25, annotation='Create a Texture bake set', command=lambda *args: lcBake_make_new_bake_set(bakeSetListDropdown, 'texture') )
  ci+=1
  pm.button(l='Make Vertex', bgc=colorWheel.getColorRGB(ci), w=100, h=25, annotation='Create a Texture bake set', command=lambda *args: lcBake_make_new_bake_set(bakeSetListDropdown, 'vertex') )
  ci+=1
  pm.setParent(prefix+'_columLayout_main')
  
  #
  pm.rowColumnLayout(nc=3, cw=([1,25], [2,150], [3,25]) )
  pm.iconTextButton(w=25, h=25, style='iconOnly', image=iconBasePath+'reloadList.png', annotation='Reload the bake set list', command=lambda *args: lcBake_populate_bake_set_list(bakeSetListDropdown) )
  bakeSetListDropdown = pm.optionMenu(prefix+'_optionMenu_bake_set_list', w=150, h=25, annotation='List of bake sets' )
  pm.iconTextButton(w=25, h=25, style='iconOnly', image=iconBasePath+'deleteItem.png', annotation='Delete this bake set', command=lambda *args: lcBake_delete_current_bake_set(bakeSetListDropdown) )
  pm.setParent(prefix+'_columLayout_main')
  
  #
  pm.rowColumnLayout(nc=2, cw=([1,100], [2,100] ) )  #nc=3, cw=([1,50], [2,50], [3,100] ) )  
  pm.button(l='+ Add', bgc=colorWheel.getColorRGB(ci), w=100, h=25, annotation='Add geometry to bake set', command=lambda *args: lcBake_add_to_current_bake_set(bakeSetListDropdown) )
  ci+=1
  # pm.button(l='- Rem', bgc=colorWheel.getColorRGB(ci), w=50, h=25, annotation='Remove geometry from bake set', command=lambda *args: lcBake_fake_command() )
  # ci+=1
  pm.button(l='Edit Options', bgc=colorWheel.getColorRGB(ci), w=100, h=25, annotation='Edit the bake set options', command=lambda *args: lcBake_show_bake_set_attrs(bakeSetListDropdown) )
  ci+=1
  pm.setParent(prefix+'_columLayout_main')
  
  #
  pm.rowColumnLayout(nc=2, cw=([1,75], [2,125] ) )  
  pm.text(l='Bake Camera: ', al='right')
  cameraListDropdown = pm.optionMenu(prefix+'_optionMenu_camera_list', w=125, h=25, annotation='List of cameras' )
  pm.text(l='')
  pm.checkBox(prefix+'_checkBox_shadows', w=125, h=25, value=True, label='Shadows and AO?', annotation='Turn on to bake shadows and ambient occlusion' )
  pm.setParent(prefix+'_columLayout_main')
  
  #
  pm.separator(style='none', h=10)
  pm.rowColumnLayout(nc=2, cw=([1,150], [2,50]) )
  pm.textField(prefix+'_textField_texture_path', text='texture output directory', annotation='Output directory path', w=150)
  pm.button(prefix+'_button_browse_path', l='Browse', bgc=colorWheel.getColorRGB(ci), annotation='Choose a directory', w=50, command=lambda *args: path.browsePathTextField(prefix+'_textField_texture_path', '', 'Browse a Directory') )
  ci+=1
  pm.setParent(prefix+'_columLayout_main')
  
  #
  pm.rowColumnLayout(nc=2, cw=([1,150], [2,50]) )
  pm.button(l='Bake It !!', bgc=colorWheel.getColorRGB(ci), w=150, h=25, annotation='Bake to texture or vertex', command=lambda *args: lcBake_convert_lightmap(bakeSetListDropdown, cameraListDropdown) )
  ci+=1
  pm.button(l='Open Dir', bgc=colorWheel.getColorRGB(ci), w=50, h=25, annotation='Open the output directory', command=lambda *args: lcBake_open_lightmap_folder() )
  ci+=1
  
  #
  mainWindow.show()
  
  plugin.reloadPlugin(plugin='Mayatomr', autoload=True)
  
  lcBake_populate_bake_set_list(bakeSetListDropdown)
  lcBake_populate_camera_list(cameraListDropdown)  
    
def lcBake_populate_camera_list(cameraListDropdown, *args, **kwargs):
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
  
def lcBake_populate_bake_set_list(bakeSetListDropdown, *args, **kwargs):
  ''' '''
  bakeSetListDropdown.clear()
  
  textureBakeSets = pm.ls(type='textureBakeSet')
  vertexBakeSets = pm.ls(type='vertexBakeSet')
  bakeSets = textureBakeSets+vertexBakeSets
  for set in bakeSets:
    bakeSetListDropdown.addItems([set])
    
def lcBake_make_new_bake_set(bakeSetListDropdown, type, *args, **kwargs):
  ''' '''
  selectedObjs = pm.ls(selection=True)
  
  newBakeSet = bake.createBakeSet(type=type)  
  bakeSetListDropdown.addItems([newBakeSet])
  numItems = bakeSetListDropdown.getNumberOfItems()
  bakeSetListDropdown.setSelect(numItems)
    
  bake.assignBakeSet(selectedObjs, newBakeSet)

def lcBake_add_to_current_bake_set(bakeSetListDropdown, *args, **kwargs):
  ''' '''
  selectedObjs = pm.ls(selection=True)  
  
  numItems = bakeSetListDropdown.getNumberOfItems()
  if numItems > 0:
    currentBakeSet = bakeSetListDropdown.getValue()
    if currentBakeSet:
      bake.assignBakeSet(selectedObjs, currentBakeSet)
  
def lcBake_delete_current_bake_set(bakeSetListDropdown, *args, **kwargs):
  ''' '''
  numItems = bakeSetListDropdown.getNumberOfItems()
  if numItems > 0:
    currentBakeSet = bakeSetListDropdown.getValue()
    if currentBakeSet:
      pm.delete(currentBakeSet)
  
  lcBake_populate_bake_set_list(bakeSetListDropdown)

def lcBake_show_bake_set_attrs(bakeSetListDropdown, *args, **kwargs):
  ''' '''
  numItems = bakeSetListDropdown.getNumberOfItems()
  if numItems > 0:
    currentBakeSet = bakeSetListDropdown.getValue()
    if currentBakeSet:
      pm.mel.showEditor(currentBakeSet)
      
def lcBake_delete_all_bake_sets(bakeSetListDropdown, *args, **kwargs):
  ''' '''
  textureBakeSets = pm.ls(type='textureBakeSet')
  vertexBakeSets = pm.ls(type='vertexBakeSet')
  bakeSets = textureBakeSets+vertexBakeSets
  
  for item in bakeSets:
    pm.delete(item)
  
  lcBake_populate_bake_set_list(bakeSetListDropdown)
  
def lcBake_convert_lightmap(bakeSetListDropdown, cameraListDropdown, *args, **kwargs):
  ''' '''
  numItems = bakeSetListDropdown.getNumberOfItems()
  if numItems > 0:
    currentBakeSet = bakeSetListDropdown.getValue()
    if currentBakeSet:
      currentCamera = cameraListDropdown.getValue()
      outputDirectory = pm.textField(prefix+'_textField_texture_path', query=True, text=True)      
      if os.path.exists(outputDirectory):
        shadows = pm.checkBox(prefix+'_checkBox_shadows', query=True, value=True)
        
        if pm.control('bakeWindow', exists = True):
          pm.deleteUI('bakeWindow')          
        bakeWindow = pm.window('bakeWindow', t='Batch Bake', widthHeight=[100, 100], rtf=True, mnb=False, mxb=False, s=False)
        pm.columnLayout()
        pm.text(l='')
        pm.text(l='')
        pm.text(l='          Bake In Progress          ')
        pm.text(l='                  ......        ')
        pm.text(l='')
        pm.text(l='')
        bakeWindow.show()
        pm.refresh()
        #pm.pause(seconds=10)
        
        convertString = bake.convertLightmap(currentBakeSet, currentCamera, outputDirectory, shadows)
        
        print('Convert Command: {0}'.format(convertString) )
                
        pm.deleteUI('bakeWindow')    
        
        pm.select(clear=True)
      else:
        pm.warning('Path not found: {0}'.format(outputDirectory) )

def lcBake_open_lightmap_folder(*args, **kwargs):
  ''' '''
  dir = pm.textField(prefix+'_textField_texture_path', query=True, text=True)
  lightmapDir = os.path.normpath(os.path.join(dir, 'lightMap'))
  if os.path.exists(lightmapDir):
    path.openFilePath(lightmapDir)
  elif os.path.exists(dir):
    path.openFilePath(dir)
  else:
    pm.warning('Path not found: {0}'.format(dir) )