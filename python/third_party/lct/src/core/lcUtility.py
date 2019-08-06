import os
import re
import pymel.core as pm

from lct.src.core.lcPath import Path as path

class Utility:

  def __init__(self, *args, **kwargs):
    """ Initialize class and variables """

  @classmethod
  def addFramePadding(cls, frame, pad='0000', *args, **kwargs):
    '''
      returns a string
      adds frame padding if neccessary
    '''

    padLen = len(pad)
    frameLen = len(str(frame) )

    if frameLen > padLen:
      return str(frame)

    else:
      paddedFrame = '{0}{1}'.format(pad,frame)
      min = abs(padLen-len(paddedFrame))
      paddedFrame = paddedFrame[min:len(paddedFrame)+1]

      return str(paddedFrame)

  @classmethod
  def centerPvt(cls, sel, *args, **kwargs):
    ''' center geometry pivot (scale, rotate, translate) to 0,0,0 '''
    for obj in sel:
      pm.move(obj.rotatePivot, [0,0,0])
      pm.move(obj.scalePivot, [0,0,0])

  @classmethod
  def reloadTextures(cls, *args, **kwargs):
    ''' reloads all texture files in a scene '''
    sel = pm.ls(typ='file')
    for tex in sel:
      path = pm.getAttr(tex+'.fileTextureName')
      if path != '':
        pm.setAttr(tex+'.fileTextureName',path)

  @classmethod
  def filterByToken(cls, list, token='', *args, **kwargs):
    ''' filter a list based on a suffix token '''
    filtered = []
    for obj in list:
      buffer1 = obj.split('_') #split obj names up around underscore character
      for elem in buffer1:
        elem = elem.rstrip('0123456789') #removes numbers from the end of the token so Occlude1 becomes Occlude
        token = token.rstrip('0123456789')
        if elem.capitalize() == token.capitalize(): # compares token and obj's - .capitalize() turns testABC into Testabc
          filtered.append(obj)

    return filtered

  @classmethod
  def setTransformVisibility(cls, list, visibility, *args, **kwargs):
    ''' set visibility of any transforms in list'''
    for item in list:
      if item.nodeType() == 'transform':
        pm.setAttr(item+'.visibility', visibility)

    return list

  @classmethod
  def buildPublishList(cls, inline, *args, **kwargs):
    ''' build a list of the scripts that are published and some relevent commands '''
    moduleBase = 'lct.src'
    data = []

    srcPath = path.getSrcPath()

    for subDir in os.listdir(srcPath):
      full = os.path.normpath(os.path.join(srcPath, subDir))
      if os.path.isdir(full):
        if os.path.exists(os.path.normpath(os.path.normpath(os.path.join(full, subDir+'.py'))) ):
          file = open(os.path.normpath(os.path.join(full, subDir+'.py')) )
          first = file.readline()[:-2]# ????

          if first.split(' = ')[0] == 'publish':
            publish = first.split(' = ')[1]
            annotation = file.readline()[:-2].split(' = ')[1].split('"')[1]
            prefix = file.readline()[:-2].split(' = ')[1].split("'")[1]            
            if inline: #if you need to preserve the command as a single line when printing or writing to a file
              runCommand = 'import '+moduleBase+'.'+subDir+'.'+subDir+' as '+prefix+'\\nreload('+prefix+')\\n'+prefix+'.'+subDir+'UI()'
            else:
              runCommand = 'import '+moduleBase+'.'+subDir+'.'+subDir+' as '+prefix+'\nreload('+prefix+')\n'+prefix+'.'+subDir+'UI()'
            set = [subDir, prefix, annotation, publish, runCommand]
            #print 'set: {0}'.format(set)
            data.append(set)

    return data

class Plugin:

  def __init__(self):
    """ """

  @classmethod
  def reloadPlugin(cls, plugin='', autoload=False, *args, **kwargs):
    """ reloads a plugin by name and sets it to autoload if necessary """
    if not pm.pluginInfo(plugin, query=True, loaded=True) and not plugin == '':
      try:
        pm.loadPlugin(plugin)
        pm.pluginInfo(plugin, edit=True, autoload=autoload)
      except:
        pm.warning('Something went wrong, does this plugin - {0} - exist?'.format(plugin))

class Camera:

  def __init__(self):
    """ """

  @classmethod
  def toggleBackground(cls, *args, **kwargs):
    """ toggle maya's viewport background between solid color and gradient """
    if pm.displayPref(query=True, displayGradient=True):
      pm.displayPref(displayGradient=False)
    else:
      pm.displayPref(displayGradient=True)
