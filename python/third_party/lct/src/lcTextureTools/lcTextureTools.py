publish = True
annotation = "Global Texture Node Controls"
prefix = 'lcTxT'

import os
import math
import pymel.core as pm

from lct.src.core.lcWindow import lcWindow as lcWindow
from lct.src.core.lcTexture import Texture as texture
from lct.src.core.lcPath import Path as path
from lct.src.core.lcShelf import Shelf as shelf

import lct.src.core.lcColor as color
# interface colors
kw = {'hue':1, 'saturation':0.5, 'value':0.5}
colorWheel = color.ColorWheel(30, **kw)

basePath = os.path.abspath(os.path.dirname(__file__))+'/'
iconBasePath = os.path.abspath(os.path.dirname(__file__))+"/icons/"

def lcTextureToolsUI(dockable=False, *args, **kwargs):
  ''' '''
  ci = 0 #color index iterator
  windowName = 'lcTextureTools'
  shelfCommand = 'import lct.src.lcTextureTools.lcTextureTools as lcTxT\nreload(lcTxT)\nlcTxT.lcTextureToolsUI()'
  icon = basePath+'lcTextureTools.png'
  winWidth  = 204
  winHeight = 174

  mainWindow = lcWindow(windowName=windowName, width=winWidth, height=winHeight, icon=icon, shelfCommand=shelfCommand, annotation=annotation, dockable=dockable, menuBar=True)
  mainWindow.create()

  #
  pm.columnLayout(prefix+'_columLayout_main')

  #
  pm.rowColumnLayout(nc=1, cw=([1,201]) )
  pm.iconTextButton(w=200, h=25, style='iconOnly', image=iconBasePath+'renameNodes.png', annotation='Renames all file nodes based on the attached file name with a tx_ suffix', command=lambda *args: texture.renameAllTextureNodes() )
  pm.setParent('..')
  pm.separator(style='in', h=5)

  #
  pm.rowColumnLayout(nc=2, cw=([1,100], [2,100]) )
  pm.rowColumnLayout(nc=2, cw=([1,75], [2,25]) )
  pm.iconTextButton(w=100, h=25, style='iconOnly', image=iconBasePath+'reloadAll.png', annotation='Reloads all the file texture nodes', command=lambda *args: texture.reloadTextures() )
  pm.iconTextButton(w=25, h=25, style='iconOnly', image=iconBasePath+'addToShelf.png', highlightImage=iconBasePath+'addToShelf_over.png', annotation='Add to Shelf', command=lambda *args: shelf.makeShelfButton('Reload Textures', 'from lct.src.core.lcTexture import Texture as texture\ntexture().reloadTextures()', iconBasePath+'reloadAllTextures.png', 'Reload All Textures') )
  pm.setParent('..')
  pm.rowColumnLayout(nc=2, cw=([1,75], [2,25]) )
  pm.iconTextButton(w=100, h=25, style='iconOnly', image=iconBasePath+'reloadChanged.png', annotation='Reloads only the changed file texture nodes based on timestamp', command=lambda *args: texture().reloadChangedTextures() )
  pm.iconTextButton(w=25, h=25, style='iconOnly', image=iconBasePath+'addToShelf.png', highlightImage=iconBasePath+'addToShelf_over.png', annotation='Add to Shelf', command=lambda *args: shelf.makeShelfButton('Reload Changed Textures', 'from lct.src.core.lcTexture import Texture as texture\ntexture().reloadChangedTextures()', iconBasePath+'reloadChangedTextures.png', 'Reload Changed Textures') )
  pm.setParent('..')
  pm.setParent(prefix+'_columLayout_main')
  pm.separator(style='in', h=5)

  #
  pm.rowColumnLayout(nc=2, cw=([1,150], [2,50]) )
  pm.textField(prefix+'_textField_new_path', w=150)
  pm.button(prefix+'_button_browse_path', l='Browse', bgc=colorWheel.getColorRGB(ci), annotation='Choose a new directory', w=50, command=lambda *args: path.browsePathTextField(prefix+'_textField_new_path', '', 'Browse New Texture Directory') )
  ci+=1
  pm.setParent(prefix+'_columLayout_main')

  #
  pm.rowColumnLayout(nc=2, cw=([1,100], [2,100]) )
  pm.iconTextButton(w=100, h=25, style='iconOnly', image=iconBasePath+'pathAll.png', annotation='Repath all file texture nodes', command=lambda *args: lcTxT_repath_all() )
  pm.iconTextButton(w=100, h=25, style='iconOnly', image=iconBasePath+'pathSelected.png', annotation='Repath selected file texture nodes', command=lambda *args: lcTxT_repath_selected() )
  pm.setParent(prefix+'_columLayout_main')
  pm.separator(style='in', h=5)

  #
  pm.rowColumnLayout(nc=2, cw=([1,100], [2,100]) )
  pm.iconTextButton(w=100, h=25, style='iconOnly', image=iconBasePath+'openAll.png', annotation='Open all file texture nodes in default associated program', command=lambda *args: lcTxT_open_all() )
  pm.iconTextButton(w=100, h=25, style='iconOnly', image=iconBasePath+'openSelected.png', annotation='Open selected file texture nodes in default associated program', command=lambda *args: lcTxT_open_selected() )
  pm.setParent(prefix+'_columLayout_main')
  pm.separator(style='in', h=5)

  #
  mainWindow.show()

def lcTxT_repath_all(*args, **kwargs):
  ''' '''
  textures = pm.ls(type='file')
  if textures:
    newPath = pm.textField(prefix+'_textField_new_path', query=True, text=True)
    if newPath:
      texture.repathTextures(textures, newPath)

def lcTxT_repath_selected(*args, **kwargs):
  ''' '''
  textures = pm.ls(sl=True)
  textures = texture.filterForTextures(textures)
  if textures:
    newPath = pm.textField(prefix+'_textField_new_path', query=True, text=True)
    if newPath:
      texture.repathTextures(textures, newPath)

def lcTxT_open_all(*args, **kwargs):
  ''' '''
  textures = pm.ls(type='file')
  if textures:
    texture.openTextureList(textures)

def lcTxT_open_selected(*args, **kwargs):
  ''' '''
  textures = pm.ls(sl=True)
  textures = texture.filterForTextures(textures)
  if textures:
    texture.openTextureList(textures)