publish = True
annotation = "Create image planes and add movement controls"
prefix = 'lcMIP'

import pymel.core as pm
import os
import math

from lct.src.core.lcWindow import lcWindow as lcWindow

import lct.src.core.lcColor as color

# interface colors
kw = {'hue':0.2, 'saturation':0.5, 'value':0.5}
colorWheel = color.ColorWheel(15, **kw)

basePath = os.path.abspath(os.path.dirname(__file__))+'/'
iconBasePath = os.path.abspath(os.path.dirname(__file__))+"/icons/"

defaultString = 'Unconnected Image Planes'

def lcMoveImagePlaneUI(dockable=False, *args, **kwargs):
  ''' '''
  ci = 0 #color index iterator
  windowName = 'lcMoveImagePlane'
  shelfCommand = 'import lct.src.lcMoveImagePlane.lcMoveImagePlane as lcMIP\nreload(lcMIP)\nlcMIP.lcMoveImagePlaneUI()'
  icon = basePath+'lcMoveImagePlane.png'
  winWidth  = 204
  winHeight = 103
  
  mainWindow = lcWindow(windowName=windowName, width=winWidth, height=winHeight, icon=icon, shelfCommand=shelfCommand, annotation=annotation, dockable=dockable, menuBar=True)
  mainWindow.create()

  #
  pm.columnLayout(prefix+'_columLayout_main')
  
  #
  pm.rowColumnLayout(nc=3, cw=([1,66], [2,66], [3,66] ) )
  pm.button(l='Front', bgc=colorWheel.getColorRGB(ci), w=66, h=25, annotation='Create an image plane for the front camera', command=lambda *args: mip_make_image_plane('front', imageListDropdown) )
  ci+=1
  pm.button(l='Side', bgc=colorWheel.getColorRGB(ci), w=66, h=25, annotation='Create an image plane for the side camera', command=lambda *args: mip_make_image_plane('side', imageListDropdown) )
  ci+=1
  pm.button(l='Top', bgc=colorWheel.getColorRGB(ci), w=66, h=25, annotation='Create an image plane for the top camera', command=lambda *args: mip_make_image_plane('top', imageListDropdown) )
  ci+=1
  pm.setParent(prefix+'_columLayout_main')
  
  #
  pm.rowColumnLayout(nc=2, cw=([1,25], [2,175]) )
  pm.iconTextButton(w=25, h=25, style='iconOnly', image=iconBasePath+'reloadList.png', annotation='Reload the image planes list', command=lambda *args: mip_populate_image_list(imageListDropdown) )
  imageListDropdown = pm.optionMenu(prefix+'_optionMenu_image_plane_list', w=175, h=25, annotation='List of orthographic image planes' )
  pm.setParent(prefix+'_columLayout_main')
  
  #
  pm.button(l='Make Image Plane Move Control', bgc=colorWheel.getColorRGB(ci), w=200, h=25, annotation='Create control curve for image plane from drop down list', command=lambda *args: mip_make_ctrl(imageListDropdown) )
  ci+=1
  
  #
  mainWindow.show()
  
  mip_populate_image_list(imageListDropdown)
  
def mip_populate_image_list(imageListDropdown, *args, **kwargs):
  ''' '''
  global defaultString
  imageListDropdown.clear()
  imageListDropdown.addItems([defaultString])

  sel = pm.ls(type='imagePlane')
  
  for IP in sel:
    #maya 2013+ made changes to image planes
    IPlist = str(IP).split('>')
    if len(IPlist) > 1:
      IP = IPlist[1]
    
    print 'imagePlane: {0}'.format(IP)
    #clean up expressions
    expressions = pm.connectionInfo(IP+'.displayMode', sourceFromDestination=True)
    if expressions:
      expName = expressions.split('.')[0]
      expInput = pm.connectionInfo(expName+'.input[0]', sourceFromDestination=True)
      if not expInput:
        pm.delete(expName)
        
    #add unconnected image planes to list    
    connections = pm.connectionInfo(IP+'.message', destinationFromSource=True)
    for item in connections:
      allowedCams = ['front', 'side', 'top']
      print 'item: {0}'.format(item)
      for cam in allowedCams:
        if item.split('Shape.')[0] == cam:
          activeConn = pm.connectionInfo(IP+'.displayMode', sourceFromDestination=True)
          print 'activeConn: {0}'.format(activeConn)
          if not activeConn:
            imageListDropdown.addItems([IP])
                  
def mip_make_ctrl(imageListDropdown, *args, **kwargs):
  ''' '''
  chosen = imageListDropdown.getValue()
  if chosen != defaultString:
    mip_move_image_plane(chosen)
    mip_populate_image_list(imageListDropdown)
  
def mip_move_image_plane(imagePlane = '', *args, **kwargs):
  if imagePlane:
    
    connections = pm.connectionInfo(imagePlane+'.message', destinationFromSource=True)    
    cam = 'none'
    
    for item in connections:
      if item.split('Shape.')[0] == 'front':
        cam = 'front'
      if item.split('Shape.')[0] == 'side':
        cam = 'side'
      if item.split('Shape.')[0] == 'top':
        cam = 'top'
        
    if cam != 'none':
      curve = pm.curve(per=True, d=1, p=[(0.5,0,0.5), (0.5,0,-0.5), (-0.5,0,-0.5), (-0.5,0,0.5), (0.5,0,0.5)], k=[0,1,2,3,4])
      if cam == 'front':
        curve.setRotation((90,0,0))
      if cam == 'top':
        curve.setRotation((0,0,0))
      if cam == 'side':
        curve.setRotation((90,90,0))
      
      pm.setAttr(curve+'.rx', lock=True, keyable=False, channelBox=False)
      pm.setAttr(curve+'.ry', lock=True, keyable=False, channelBox=False)
      pm.setAttr(curve+'.rz', lock=True, keyable=False, channelBox=False)
      pm.setAttr(curve+'.sy', lock=True, keyable=False, channelBox=False)
    
      filename = pm.getAttr(imagePlane+'.imageName').split('/')[-1].split('.')[0]
    
      pm.rename(curve, 'Mover_'+filename)
         
      pm.expression(name=imagePlane+'_expression', s='{0}.displayMode = {1}.visibility * 3'.format(imagePlane, curve))
      
      ratio = 1.0
      coverageX = float(pm.getAttr(imagePlane+'.coverageX'))
      coverageY = float(pm.getAttr(imagePlane+'.coverageY'))
      size = 1.0
      sizeW = float(pm.getAttr(imagePlane+'.width'))
      sizeH = float(pm.getAttr(imagePlane+'.height'))
      if sizeW>sizeH:
        size = sizeW
      else:
        size = sizeH
      
      if coverageX > coverageY:
        ratio = coverageX/coverageY
        x = size
        z = size/ratio
        curve.setScale((x,1,z))
        pm.select(curve.cv[0:3])
        pm.scale(1.2,1+(.2/ratio),1)
      else:
        ratio = coverageY/coverageX
        x = size/ratio
        z = size
        curve.setScale((x,1,z))
        pm.select(curve.cv[0:3])
        pm.scale(1+(.2/ratio),1.2,1)
            
      if pm.mel.getApplicationVersionAsFloat() > 2012:
        pm.connectAttr(curve.translate, imagePlane+'.imageCenter')
      else:
        pm.connectAttr(curve.translate, imagePlane+'.center')
      pm.connectAttr(curve.scaleX, imagePlane+'.width')
      pm.connectAttr(curve.scaleZ, imagePlane+'.height')
      
      pm.select(curve, replace=True)
    else:
      pm.warning('not using the front, side or top camera !!!')

def mip_make_image_plane(camera, imageListDropdown, *args, **kwargs):
  ''' '''
  pm.mel.importImagePlane([camera+'Shape'])
  mip_populate_image_list(imageListDropdown)