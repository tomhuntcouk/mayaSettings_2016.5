publish = True
annotation = "Retopology Tool"
prefix = 'lcRtB'
  
import os
import math
import pymel.core as pm

from lct.src.core.lcUtility import Utility as utility
from lct.src.core.lcGeometry import Geometry as geometry
from lct.src.core.lcWindow import lcWindow as lcWindow

import lct.src.core.lcColor as color

# interface colors
kw = {'hue':0.74, 'saturation':0.5, 'value':0.5}
colorWheel = color.ColorWheel(10, **kw)

basePath = os.path.abspath(os.path.dirname(__file__))+'/'
iconBasePath = os.path.abspath(os.path.dirname(__file__))+"/icons/"
defaultString = 'Nothing Live . . .'

def lcRetopoBasicUI(dockable=False, *args, **kwargs):
  """ """
  ci = 0 #color index iterator
  windowName = 'lcRetopoBasic'
  shelfCommand = 'import lct.src.lcRetopoBasic.lcRetopoBasic as lcRtB\nreload(lcRtB)\nlcRtB.lcRetopoBasicUI()'
  icon = basePath+'lcRetopoBasic.png'
  winWidth  = 204
  winHeight = 180
  
  mainWindow = lcWindow(windowName=windowName, width=winWidth, height=winHeight, icon=icon, shelfCommand=shelfCommand, annotation=annotation, dockable=dockable, menuBar=True)
  mainWindow.create()

  #
  pm.columnLayout(prefix+'_columLayout_main')

  pm.button(l='Setup for Retopo', bgc=colorWheel.getColorRGB(ci), w=200, h=25, annotation='Setup a high res mesh for retopology', command=lambda *args: rtb_setup_live_mesh(highresListDropdown) )
  ci+=1
  
  #
  pm.rowColumnLayout(nc=3, cw=([1,25], [2,150], [3,25] ) )
  pm.iconTextButton(w=25, h=25, style='iconOnly', image=iconBasePath+'reloadMeshList.png', annotation='Reload the list of high res meshes', command=lambda *args: rtb_highres_list_populate(highresListDropdown) )
  highresListDropdown = pm.optionMenu(prefix+'_optionMenu_highres_list', w=150, h=25, bgc=[0.5,0.5,0.5], annotation='List of high res meshes in the scene' )
  highresListDropdown.changeCommand(lambda *args: rtb_choose_active(highresListDropdown) )
  pm.iconTextButton(w=25, h=25, style='iconOnly', image=iconBasePath+'removeMeshFromList.png', annotation='Remove current high res mesh from the list and return it to a normal state', command=lambda *args: rtb_remove(highresListDropdown) )
  pm.setParent(prefix+'_columLayout_main')

  #
  pm.rowColumnLayout(nc=4, cw=([1,50], [2,100], [3,25], [4,25] ) )
  pm.iconTextStaticLabel(w=50, h=25, style='iconOnly', image=iconBasePath+'meshLayering.png', annotation='Drag slider to change mesh layering' )
  pm.floatSlider(prefix+'_floatSlider_layer_mesh', step=0.01, min=0, max=1, v=0, h=25, dragCommand=lambda *args: rtb_scale_layer_mesh(highresListDropdown) )
  pm.iconTextButton(w=25, h=25, style='iconOnly', image=iconBasePath+'toggleXray.png', annotation='Toggle current high res mesh X-Ray', command=lambda *args: rtb_toggle_xray(highresListDropdown) )
  pm.iconTextButton(w=25, h=25, style='iconOnly', image=iconBasePath+'hideMesh.png', annotation='Hide the high-res mesh', command=lambda *args: rtb_toggle_hide(highresListDropdown) )
  pm.setParent(prefix+'_columLayout_main')

  #
  pm.rowColumnLayout(nc=3, cw=([1,50], [2,100], [3,50] ) )
  pm.iconTextStaticLabel(w=50, h=25, style='iconOnly', image=iconBasePath+'shaderOpacity.png', annotation='Drag slider to change shader transparency' )
  pm.floatSlider(prefix+'_floatSlider_topo_trans', step=0.1, min=0, max=1, v=0.5, h=25, dragCommand=lambda *args: rtb_update_topo_transparency() )
  pm.iconTextButton(w=50, h=25, style='iconOnly', image=iconBasePath+'assignShader.png', annotation='Create and/or assign a semi-transparent shader to selected low res mesh', command=lambda *args: rtb_create_retopo_shader() )
  pm.setParent(prefix+'_columLayout_main')

  #
  pm.separator(style='in', h=5, hr=True) #this doesn't seem to be working right

  pm.rowColumnLayout(nc=2)
  pm.button(l='Relax', bgc=colorWheel.getColorRGB(ci), w=100, h=25, annotation='Relax selected verts and shrink-wrap them to the live mesh', command=lambda *args: rtb_relax_verts(highresListDropdown) )
  ci+=1
  pm.button(l='Shrink-Wrap', bgc=colorWheel.getColorRGB(ci), w=100, h=25, annotation='Shrink-wrap selected verts to the live mesh', command=lambda *args: rtb_shrink_wrap_verts(highresListDropdown) )
  ci+=1
  pm.setParent(prefix+'_columLayout_main')

  #
  pm.progressBar(prefix+'_progress_control', vis=False, w=202)

  #
  mainWindow.show()
  
  rtb_highres_list_populate(highresListDropdown)
  
  #vertex animation cache in viewport 2.0 must be disabled or the mesh will not update properly
  if pm.objExists('hardwareRenderingGlobals'):
    pm.PyNode('hardwareRenderingGlobals').vertexAnimationCache.set(0)

def rtb_setup_live_mesh(highresListDropdown, *args, **kwargs):
  ''' '''
  sel = pm.ls(sl=True)
  geometry.fixNamespaceNames()
  if sel[0] != '':
    root = pm.group(empty=True, name=sel[0]+'_RETOPO')
    live = pm.duplicate(sel[0], name = sel[0]+'_live')[0]
    high = sel[0].rename(sel[0]+'_high')

    pm.makeIdentity([high, live], apply=True, t=1, r=1, s=1, n=0)
    utility.centerPvt([high, live])

    highShape = high.getShape()
    liveShape = live.getShape()

    highShape.overrideEnabled.set(1) #enable display overrides
    highShape.overrideDisplayType.set(2) #set to referenced

    liveShape.overrideEnabled.set(1) #enable display overrides
    liveShape.overrideDisplayType.set(1) #set to template
    liveShape.overrideVisibility.set(0) #set visibility to 0

    pm.select(live)
    pm.makeLive()

    highresListDropdown.addItems([high])
    numItems = highresListDropdown.getNumberOfItems()
    highresListDropdown.setSelect(numItems)

    pm.parent(high, root)
    pm.parent(live, root)

    pm.connectAttr('persp.translate', high.scalePivot)

    rtb_scale_layer_mesh(highresListDropdown)

    rtb_glow(highresListDropdown)

def rtb_remove(highresListDropdown, *args, **kwargs):
  ''' remove item from the list and delete live-mesh and groups '''
  global defaultString
  high = highresListDropdown.getValue()

  if not high == defaultString:
    high = pm.PyNode(high.split("'")[0]) #get rid of unicode crap
    high.rename(high.rstrip('_high'))
    pm.parent(high, world=True)

    high.setScale([1,1,1])
    pm.disconnectAttr('persp.translate', high.scalePivot)

    if pm.displaySurface(high, query=True, xRay=True)[0] == True:
      pm.displaySurface(high, xRay=False)
    if not high.visibility.get():
      high.visibility.set(True)

    highShape = high.getShape()
    highShape.overrideDisplayType.set(0) #sets to normal mode
    highShape.overrideEnabled.set(0) #disable display overrides

    pm.delete(str(high)+'_RETOPO')

  rtb_highres_list_populate(highresListDropdown)

def rtb_create_retopo_shader():
  ''' '''
  try:
    sel = [ obj for obj in pm.ls(sl=True) if obj.getShape() and obj.getShape().nodeType() == 'mesh' ]
  except:
    pm.warning('Please select some geometry')
    return

  shaderName = 'lcRetopo'

  if not pm.objExists(shaderName):
    shader = pm.shadingNode('lambert', asShader=True, name=shaderName )
    SG = shaderName+'SG'
    if not pm.objExists(SG):
      pm.sets(renderable=True, noSurfaceShader=True, empty=True, name=(shader+'SG') )
    pm.connectAttr(shader+'.outColor', SG+'.surfaceShader', force=True)

    shader.color.set(1,0,0)
    shader.transparency.set(0.5,0.5,0.5)

  if sel:
    pm.select(sel, replace=True)  #grab the stored selection
    pm.hyperShade(assign=shaderName)    #assign shader to selection

def rtb_scale_layer_mesh(highresListDropdown, *args, **kwargs):
  ''' '''
  global defaultString
  scale = pm.floatSlider(prefix+'_floatSlider_layer_mesh', query=True, value=True)
  scale = math.pow(scale,2)  #makes the slider a bit progressive, gives a better feel to the scale in the low range
  scale = 1+scale*5  #remaps 0-1 to 1-6

  #iterate over the entire list and adjust scales
  currentItem = highresListDropdown.getSelect()
  numItems = highresListDropdown.getNumberOfItems()

  for item in range(numItems):
    item = item+1
    if item > 1:
      highresListDropdown.setSelect(item)

      high = highresListDropdown.getValue()

      if not high == defaultString:
        high = pm.PyNode(high.split("'")[0]) #get rid of unicode crap        
        high.setScale([scale, scale, scale])

  #return list selection to original
  highresListDropdown.setSelect(currentItem)

  #force a viewport refresh
  pm.refresh()


def rtb_toggle_xray(highresListDropdown, *args, **kwargs):
  ''' '''
  global defaultString
  high = highresListDropdown.getValue()

  if not high == defaultString:
    if pm.displaySurface(high, query=True, xRay=True)[0] == True:
      pm.displaySurface(high, xRay=False)
    else:
      pm.displaySurface(high, xRay=True)
  else:
    pm.warning('Select a mesh from the dropdown list')

def rtb_toggle_hide(highresListDropdown, *args, **kwargs):
  ''' '''
  global defaultString
  high = highresListDropdown.getValue()

  if not high == defaultString:
    high = pm.PyNode(high.split("'")[0]) #get rid of unicode crap
    if high.visibility.get():
      high.visibility.set(False)
    else:
      high.visibility.set(True)
  else:
    pm.warning('Select a mesh from the dropdown list')

def rtb_update_topo_transparency():
  ''' '''
  if pm.objExists('lcRetopo'):
    trans = pm.floatSlider(prefix+'_floatSlider_topo_trans', query=True, value=True)
    pm.setAttr('lcRetopo.transparency', [trans, trans, trans] )

def rtb_choose_active(highresListDropdown, *args, **kwargs):
  ''' '''
  global defaultString
  sel = pm.ls(sl=True)

  pm.select(cl=True)
  pm.makeLive()

  high = highresListDropdown.getValue()
  if not high == defaultString:

    rtb_scale_layer_mesh(highresListDropdown)

    live = pm.PyNode(high.replace('_high', '_live'))
    liveShape = live.getShape()
    pm.select(liveShape, replace=True)
    pm.makeLive()

  pm.select(sel, replace=True)

  rtb_glow(highresListDropdown)

def rtb_highres_list_populate(highresListDropdown, *args, **kwargs):
  ''' '''
  global defaultString
  highresListDropdown.clear()
  highresListDropdown.addItems([defaultString])

  sel = [ obj for obj in  pm.ls(dag=True, transforms=True) if obj.getShape() and obj.getShape().nodeType() == 'mesh' ]
  highres = utility.filterByToken(sel, 'high')

  for mesh in highres:
    highresListDropdown.addItems([mesh])

  rtb_glow(highresListDropdown)

def rtb_relax_verts(highresListDropdown, *args, **kwargs):
  ''' '''
  global defaultString
  high = highresListDropdown.getValue()

  if not high == defaultString:

    pm.undoInfo(openChunk=True)

    live = pm.PyNode(high.replace('_high', '_live'))
    liveShape = live.getShape()
    sel = pm.ls(sl=True)
    if sel:
      verts = geometry.getVertsFromSelection(sel)
      if verts and verts[0].nodeType() == 'mesh':
        try:
          geometry.relaxVerts(verts, liveShape, prefix+'_progress_control')
        except:
          pm.warning('You Should Not See This Error!')
          pm.progressBar(prefix+'_progress_control', edit=True, endProgress=True)
      else:
        pm.warning('No verts to shrink wrap!')
      pm.select(sel, r=True)
      pm.hilite(pm.PyNode(sel[0].split('.')[0]).getParent(), r=True)
      type = geometry.getMeshSelectionType(sel)
      geometry.switchSelectType(type)

      pm.undoInfo(closeChunk=True)

  else:
    pm.warning('Select a mesh from the dropdown list')

def rtb_shrink_wrap_verts(highresListDropdown, *args, **kwargs):
  ''' '''
  global defaultString
  high = highresListDropdown.getValue()

  if not high == defaultString:

    pm.undoInfo(openChunk=True)

    live = pm.PyNode(high.replace('_high', '_live'))
    liveShape = live.getShape()
    sel = pm.ls(sl=True)
    if sel:
      verts = geometry.getVertsFromSelection(sel)
      if verts and verts[0].nodeType() == 'mesh':
        try:
          geometry.shrinkWrap(verts, liveShape, prefix+'_progress_control')
        except:
          pm.warning('You Should Not See This Error!')
          pm.progressBar(prefix+'_progress_control', edit=True, endProgress=True)
      else:
        pm.warning('No verts to shrink wrap!')
      pm.select(sel, r=True)
      pm.hilite(pm.PyNode(sel[0].split('.')[0]).getParent(), r=True)
      type = geometry.getMeshSelectionType(sel)
      geometry.switchSelectType(type)

      pm.undoInfo(closeChunk=True)

  else:
    pm.warning('Select a mesh from the dropdown list')

def rtb_glow(highresListDropdown, *args, **kwargs):
  ''' highlight dropdown list red if nothing is selected '''
  global defaultString
  high = highresListDropdown.getValue()

  if high==defaultString:
    highresListDropdown.setBackgroundColor([1.0,0.4,0.4] )
  else:
    highresListDropdown.setBackgroundColor([0.5,0.5,0.5] )
