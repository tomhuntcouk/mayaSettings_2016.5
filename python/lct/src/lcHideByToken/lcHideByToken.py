publish = True
annotation = "Hide stuff based on a word/token/string"
prefix = 'lcHbT'

import os
import pymel.core as pm

from lct.src.core.lcWindow import lcWindow as lcWindow
from lct.src.core.lcUtility import Utility as utility

import lct.src.core.lcColor as color
# interface colors
kw = {'hue':0.0, 'saturation':0.5, 'value':0.5}
colorWheel = color.ColorWheel(10, **kw)

basePath = os.path.abspath(os.path.dirname(__file__))+'/'

def lcHideByTokenUI(dockable=False, *args, **kwargs):
  ''' '''
  ci = 0 #color index iterator
  windowName = 'lcHideByToken'
  shelfCommand = 'import lct.src.lcHideByToken.lcHideByToken as lcHbT\nreload(lcHbT)\nlcHbT.lcHideByTokenUI()'
  icon = basePath+'lcHideByToken.png'
  winWidth  = 204
  winHeight = 48
  
  mainWindow = lcWindow(windowName=windowName, width=winWidth, height=winHeight, icon=icon, shelfCommand=shelfCommand, annotation=annotation, dockable=dockable, menuBar=True)
  mainWindow.create()

  #
  pm.rowColumnLayout(nc=3, cw=([1,100], [2,50], [3,50]) )
  pm.textField(prefix+'_textField_token', w=100)
  pm.button(prefix+'_button_hide', l='Hide', bgc=colorWheel.getColorRGB(ci), w=50, command=lambda *args: lcHideByTokenButton(vis=0) )
  ci+=1
  pm.button(prefix+'_button_show', l='Show', bgc=colorWheel.getColorRGB(ci), w=50, command=lambda *args: lcHideByTokenButton(vis=1) )
  ci+=1

  #
  mainWindow.show()

def lcHideByTokenButton(vis, *args, **kwargs):
  ''' '''
  queryToken = pm.textField(prefix+'_textField_token',query=True,tx=True)
  meshAndXform = pm.ls(transforms=True) #list all transforms

  filtered = utility.filterByToken(meshAndXform, queryToken)
  utility.setTransformVisibility(filtered, vis)

  pm.refresh(force=True)