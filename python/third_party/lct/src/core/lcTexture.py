import os
import subprocess
import sys
import pymel.core as pm
import xml.dom.minidom
from xml.dom.minidom import Document

from lct.src.core.lcPath import Path as path

class Texture:

  def __init__(self, *args, **kwargs):
    """ Initialize class and variables """
    self.settingsPath = path.getSettingsPath()+'/'
  
  @classmethod
  def filterForTextures(cls, textureList, *args, **kwargs):
    ''' filter a list for only file texture nodes '''
    newList = []
    if textureList:
      #
      for item in textureList:
        type = pm.nodeType(item)
        if type == 'file':
          newList.append(item)
    return newList
    
  @classmethod
  def renameAllTextureNodes(cls, *args, **kwargs):
    """ rename texture nodes based on the name of linked file """
    textures = pm.ls(exactType='file')
    for tex in textures:
      if tex.fileTextureName.get() != "":
        path = tex.fileTextureName.get()
        fileName = 'tx_'+os.path.split(path)[1].split('.')[0]
        pm.rename(tex, fileName)
  
  @classmethod
  def repathTextures(cls, texList, newPath, *args, **kwargs):
    ''' repath the textures in a given list '''
    if texList:
      for tex in texList:
        oldPath = pm.getAttr(tex+'.fileTextureName')
        fixedPath = path.repath(oldPath , newPath)
        pm.setAttr(tex+'.fileTextureName', fixedPath)
  
  @classmethod
  def reloadTextures(cls, *args, **kwargs):
    ''' reloads all texture files in a scene '''
    sel = pm.ls(typ='file')
    for tex in sel:
      path = pm.getAttr(tex+'.fileTextureName')
      if os.path.exists(path):
        pm.setAttr(tex+'.fileTextureName',path)
    pm.refresh()
        
  @classmethod
  def reloadTexture(cls, texNode, *args, **kwargs):
    ''' reloads a single texture node '''
    path = pm.getAttr(texNode+'.fileTextureName')
    if os.path.exists(path):
      pm.setAttr(texNode+'.fileTextureName',path)
    pm.refresh()
    
  @classmethod
  def reloadTextureList(cls, texList, *args, **kwargs):
    ''' reloads a list of texture nodes '''
    for item in texList:
      path = pm.getAttr(item+'.fileTextureName')
      if os.path.exists(path):
        pm.setAttr(item+'.fileTextureName',path)
    pm.refresh()
  
  @classmethod
  def openTextureList(cls, texList, *args, **kwargs): 
    ''' open a list of file nodes in default program ie. photoshop '''
    for item in texList:
      texPath = pm.getAttr(item+'.fileTextureName')
      path.openFilePath(texPath)
  
  def saveTextureList(self, *args, **kwargs):
    ''' write an xml file with a list of the scenes textures and timestamps '''
    fileNodes = pm.ls(type='file')
    sceneName = path.getSceneName()
    xmlFileName = sceneName+'_textureList'
    
    doc = Document()
    textureList = doc.createElement('textureList')
    textureList.setAttribute('sceneName', sceneName)
    doc.appendChild(textureList)
    
    for node in fileNodes:
      fileTextureName = pm.getAttr(node+'.fileTextureName')
      if os.path.isfile(fileTextureName):
        time = os.path.getmtime(fileTextureName)
        
        textureNode = doc.createElement('textureNode')
        textureNode.setAttribute('nodeName', node)
        textureList.appendChild(textureNode)
        
        texturePath = doc.createElement('path')
        texturePath.appendChild(doc.createTextNode(fileTextureName) )
        textureNode.appendChild(texturePath)
        
        textureTime = doc.createElement('time')   
        textureTime.appendChild(doc.createTextNode(str(time) ) )
        textureNode.appendChild(textureTime)
      
    f = open(self.settingsPath+xmlFileName+'.xml', 'w+')
    #f.write(doc.toprettyxml(indent='    ') ) #This is super slow !!!!!
    doc.writexml(f)
    f.close()
  
  def reloadChangedTextures(self, *args, **kwargs):
    ''' '''
    fileNodes = pm.ls(type='file')
    sceneName = path.getSceneName()
    xmlFileName = sceneName+'_textureList'
    
    if os.path.exists(self.settingsPath+xmlFileName+'.xml'):
      textureList = xml.dom.minidom.parse(self.settingsPath+xmlFileName+'.xml')

      for node in fileNodes:    
        fileTextureName = pm.getAttr(node+'.fileTextureName')
          
        for nodeStored in textureList.getElementsByTagName('textureNode'):
          nodeNameStored = nodeStored.getAttribute('nodeName')
          if node == nodeNameStored:
            time = os.path.getmtime(fileTextureName)
            
            timeList = nodeStored.getElementsByTagName('time')
            timeNode = timeList[0]
            timeChild = timeNode.firstChild
            timeStored= timeChild.data
            
            if str(time) != timeStored:
              self.reloadTexture(node)         
        
      self.saveTextureList()
    else:
      self.saveTextureList()
      self.reloadTextures()

# ###############################################      
class TextureEditor:
  """
    Methods to get and set info related to the UV Editor and objects linked to it
    
  """
  def __init__ (self, *args, **kwargs):
    """ set some initial values """
    self.uvTextureView = pm.getPanel(scriptType='polyTexturePlacementPanel') #specifies the UV Texture Editor, there is only one
  
  def getTextureTiling(self, *args, **kwargs):     
    '''
      return format is [U min, V min, U max, V max]
      return the sizing matrix for the UV Editor's image tiling
      
    '''
    currentSize = pm.textureWindow(self.uvTextureView[0],q=True,imageTileRange=True)
    return currentSize
  
  def setTextureTiling(self, resizeMatrix, *args, **kwargs):
    '''
      input and return format is [U min, V min, U max, V max]
      Resizes the range the texture image is tiled in the UV Editor
    
    '''
    currentSize = pm.textureWindow(self.uvTextureView[0],q=True,imageTileRange=True)
    newSize = [currentSize[0]+resizeMatrix[0],currentSize[1]+resizeMatrix[1],currentSize[2]+resizeMatrix[2],currentSize[3]+resizeMatrix[3]] #add the matrices together
    pm.textureWindow(self.uvTextureView[0],e=True,imageTileRange=list(newSize))
    return newSize
    
  def getTextureDimensions(self, *args, **kwargs):
    '''
      returns the dimensions of the currently displayed texture in the UV Editor
      If there is no texture loaded returns a default [1,1]
    
    '''
    textureDimensions = [1,1]
    numImages = pm.textureWindow(self.uvTextureView[0],q=True, ni=True)
    if numImages>0:
      currentTextureImage = pm.textureWindow(self.uvTextureView[0],q=True, imageNumber=True)
      imageList = pm.textureWindow(self.uvTextureView[0],q=True, imageNames=True)
      currentTextureString = imageList[currentTextureImage].split('|')
      currentTextureNode = currentTextureString[len(currentTextureString)-1].strip()
      if pm.nodeType(currentTextureNode)=='file':
        textureDimensions = pm.getAttr(currentTextureNode+'.outSize')        
    return textureDimensions
    
  def uvSnapshot(self, name, xr, yr, aa, *args, **kwargs):
    ''' takes a snapshot image from the UV Editor in TGA format '''
    pm.uvSnapshot(name=name,xr=xr,yr=yr,overwrite=True,aa=aa,fileFormat='tga')
    
  def getTextureList(self, *args, **kwargs):
    '''
      returns a list of file texture nodes currently loaded in the UV Editor
      list items are formatted: [texture number, texture node]
      texture number is the index associated with the texture in the UV Editor
      texture node is the name of the maya file texture node
      SHADING GROUPS ARE EXCLUDED FROM THIS LIST
      
    '''
    texList = []
    numImages = pm.textureWindow(self.uvTextureView[0],q=True, ni=True)
    if numImages>0:
      imageList = pm.textureWindow(self.uvTextureView[0],q=True, imageNames=True)

      for i in range(0,numImages):
        shadString = imageList[i].split('|')
        shadNode   = shadString[len(shadString)-1].strip()
        if pm.nodeType(shadNode)=='file':
          texList.append([i,shadNode])
      
    return texList