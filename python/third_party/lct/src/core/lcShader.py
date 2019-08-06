from lct.src.core.lcPath import Path as path
from lct.src.core.lcGeometry import Geometry as geometry
from lct.src.core.lcUtility import Plugin as plugin

import pymel.core as pm
import os


class Shader():
  """
    make and work with shaders in general

  """
  def __init__(self, *args, **kwargs):
    """ """

  @classmethod
  def assignShader (cls, shader, objs, *args, **kwargs):
    ''' assign the shader to the list '''
    shadingGroup = pm.connectionInfo(shader.outColor, dfs=True)
    try:
      shadingGroup = shadingGroup[0].split('.')[0]
    except:
      pm.warning('This Shader has no Shading Group')

    if objs:
      for obj in objs:
        pm.select(obj, r=True)
        pm.sets(shadingGroup, edit=True, forceElement=True)
      pm.select(clear=True)

class CGFX():
  """
    make and work with cgfx shaders

  """
  def __init__(self, *args, **kwargs):
    """ """

  @classmethod
  def toggleLinear(cls,toggle, *args, **kwargs):
    """ switch all cgfx shaders to linear shading mode """
    cgfx=pm.ls(exactType='cgfxShader')
    for obj in cgfx:
      pm.setAttr(obj.linear, toggle)# will error if this attr '.linear' is not available

  @classmethod
  def switchToTechnique(cls,technique, *args, **kwargs):
    """ switch all cgfx shaders to the specified technique """
    cgfx=pm.ls(exactType='cgfxShader')
    for obj in cgfx:
      pm.setAttr(obj.technique, technique, type='string')# will error if this attr '.technique' is not available

  @classmethod
  def getAllShaders(cls, *args, **kwargs):
    """ return a list of all the cgfx shaders in the scene """
    return pm.ls(type='cgfxShader')

  @classmethod
  def connectVector(cls, plug, src, *args, **kwargs):
    """ runs the connectVector method from this mel script cgfxShader_util.mel; installed with Maya """
    pm.mel.cgfxShader_connectVector(plug, src)

  @classmethod
  def revertToLambert(cls, shader, textureSampler='.diffuseMapSampler', *args, **kwargs):
    """ create lambert copies of all the cgfx shaders and connect the diffuse texture """
    if pm.getAttr(shader+'.shader'):
      diffuseTexNode = pm.connectionInfo(shader+textureSampler, sourceFromDestination=True)
      lambert = pm.shadingNode('lambert', asShader=True, name='L_'+shader )
      lambertSG = pm.sets(renderable=True, noSurfaceShader=True, empty=True, name='L_'+shader+'SG' )
      pm.connectAttr(lambert+'.outColor', lambertSG+'.surfaceShader', force=True)
      if diffuseTexNode:
        pm.connectAttr(diffuseTexNode, lambert+'.color', force=True)

      pm.hyperShade(objects=shader)
      pm.sets(lambertSG, edit=True, forceElement=True)
      pm.select(clear=True)

  @classmethod
  def reloadShader(cls, shader, *args, **kwargs):
    """ reload the cgfx shader file """
    cgfxFile = pm.getAttr(shader+'.shader')
    if cgfxFile:
      pm.cgfxShader(shader, edit=True, fx=cgfxFile)

  @classmethod
  def repathShader(cls, shader, newPath, *args, **kwargs):
    """ reload the shader from a new path """
    cgfxFile = pm.getAttr(shader+'.shader')
    if cgfxFile:
      pm.cgfxShader(shader, edit=True, fx=path.repath(cgfxFile, newPath) )

  @classmethod
  def createShader(cls, name, path, *args, **kwargs):
    """
      'name' is the name you want to give the shader
      'path' is the filepath with .cgfx file

    """
    plugin.reloadPlugin('cgfxShader', True)

    shaderCGFX = pm.shadingNode('cgfxShader', asShader=True, name=name+'_CGFX_01' )
    SG = pm.sets(renderable=True, noSurfaceShader=True, empty=True, name=(shaderCGFX+'_SG') )
    pm.connectAttr(shaderCGFX.outColor, SG.surfaceShader, force=True)

    pm.cgfxShader(shaderCGFX, edit=True, fx=path) #this will fail if the cgfxShader plugin is not loaded

    return shaderCGFX

  @classmethod
  def createShaderLambert(cls, name, path, *args, **kwargs):
    """
      name is the name you want to give the shader
      path is the filepath with .cgfx file

    """
    plugin.reloadPlugin('cgfxShader', True)

    shaderBase = pm.shadingNode('lambert', asShader=True, name=name+'_01')
    shaderBase.color.set(0.5, 0.0, 1.0)
    shaderCGFX = pm.shadingNode('cgfxShader', asShader=True, name=name+'_CGFX_01' )
    SG = pm.sets(renderable=True, noSurfaceShader=True, empty=True, name=(shaderBase+'_SG') )
    pm.connectAttr(shaderBase.outColor, SG.surfaceShader, force=True)
    pm.connectAttr(shaderCGFX.outColor, shaderBase.hardwareShader, force=True)

    pm.cgfxShader(shaderCGFX, edit=True, fx=path) #this will fail if the cgfxShader plugin is not loaded

    return shaderBase

  @classmethod
  def buildShaderList(cls, sourcePath, *args, **kwargs):
    """
      return a list of all the cgfx files from a directory by name type
      ex. dir has:
            lcWalkable_2.1.cgfx
            lcComicShader_1.5.cgfx
            lcLiveShader_4.4.cgfx
          return:
            [lcWalkable, lcComicShader, lcLiveShader]

    """
    shaderFiles = [shaderFile for shaderFile in os.listdir(sourcePath) if shaderFile.lower().endswith(".cgfx")]
    shaderList = []

    for fileName in shaderFiles:
      fileName = fileName.split('_')
      baseName = fileName[0]
      if baseName not in shaderList:
        shaderList.append(baseName)

    return shaderList

  @classmethod
  def getLatestVersion(cls, sourcePath, baseName, *args, **kwargs):
    """
      if there are multiple versions of the same shader file, pick the highest version number
      ex. lcLiveShader_4.6.cgfx

    """
    shaderFiles = [shaderFile for shaderFile in os.listdir(sourcePath) if shaderFile.lower().endswith(".cgfx")]

    oldest = 00
    age = -1
    latest = ''

    for fname in shaderFiles:
      if baseName in fname:
        splitName = fname.split('_')
        version = splitName[1].split('.')
        age = version[0]+version[1]
        if age > oldest:
          oldest = age
          latest = splitName[0]+'_'+version[0]+'.'+version[1]+'.cgfx'
    return latest

class HLSL:
  """ """

  def __init__(self, *args, **kwargs):
    """ """

  @classmethod
  def getAllShaders(cls, *args, **kwargs):
    """ return a list of all the hlsl shaders in the scene """
    return pm.ls(type='hlslShader')

  @classmethod
  def reloadShader(cls, shader, *args, **kwargs):
    """ reload the shader """
    hlslFile = shader.shader.get()
    shader.shader.set(hlslFile)
    print '# hlslShader :  \"{0}\" loaded effect \"{1}\" #'.format(shader, hlslFile)

  @classmethod
  def createShader(cls, name, path, *args, **kwargs):
    """
      name is the name you want to give the shader
      path is the filepath with .fx file

    """
    plugin.reloadPlugin('hlslShader', True)

    shaderHLSL = pm.shadingNode('hlslShader', asShader=True, name=name+'_HLSL_01' )
    SG = pm.sets(renderable=True, noSurfaceShader=True, empty=True, name=(shaderHLSL+'_SG') )
    pm.connectAttr(shaderHLSL.outColor, SG.surfaceShader, force=True)
    shaderHLSL.shader.set(path)
    print '# hlslShader :  \"{0}\" loaded effect \"{1}\" #'.format(shaderHLSL, path)

    return shaderHLSL

  @classmethod
  def createShaderLambert(cls, name, path, *args, **kwargs):
    """
      name is the name you want to give the shader
      path is the filepath with .fx file

    """
    plugin.reloadPlugin('hlslShader', True)

    shaderBase = pm.shadingNode('lambert', asShader=True, name=name+'_01')
    shaderBase.color.set(0.0, 0.5, 1.0)
    shaderHLSL = pm.shadingNode('hlslShader', asShader=True, name=name+'_HLSL_01' )
    SG = pm.sets(renderable=True, noSurfaceShader=True, empty=True, name=(shaderBase+'_SG') )
    pm.connectAttr(shaderBase.outColor, SG.surfaceShader, force=True)
    pm.connectAttr(shaderHLSL.outColor, shaderBase.hardwareShader, force=True)
    shaderHLSL.shader.set(path)
    print '# hlslShader :  \"{0}\" loaded effect \"{1}\" #'.format(shaderHLSL, path)

    return shaderBase