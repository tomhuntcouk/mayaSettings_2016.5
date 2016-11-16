import os
import subprocess
import sys
import pymel.core as pm

class Path:
    ''' '''

    def __init__(self, *args, **kwargs):
      ''' '''
        
    @classmethod
    def getSceneName(cls, *args, **kwargs):
      ''' '''
      scenePath = pm.sceneName()
      sceneName = os.path.basename(scenePath).split('.')[0]
      return sceneName

    @classmethod
    def repath(cls, filePath='', newPath='', *args, **kwargs):
      """ replace the entire path to a file """
      if newPath != '':
        fileName = os.path.basename(filePath)
        returnPath = os.path.normpath(os.path.join(newPath, fileName))
        return returnPath
      else:
        return filePath

    @classmethod
    def getSettingsPath(cls, *args, **kwargs):
      """ """
      currentLocation = os.path.dirname(__file__)
      settingsPath = os.path.normpath(os.path.join(currentLocation, '..', '..', 'settings'))

      return settingsPath

    @classmethod
    def getMelPath(cls, *args, **kwargs):
      """ """
      currentLocation = os.path.dirname(__file__)
      melPath = os.path.normpath(os.path.join(currentLocation, '..', 'mel'))

      return melPath

    @classmethod
    def getSrcPath(cls, *args, **kwargs):
      """ """
      currentLocation = os.path.dirname(__file__)
      srcPath = os.path.normpath(os.path.join(currentLocation, '..'))

      return srcPath

    @classmethod
    def browsePathTextField(cls, textField, filter, caption, *args, **kwargs):
      ''' '''
      path = pm.textField(textField, query=True, text=True)
      path = pm.fileDialog2(ds=1, caption=caption, dir=path, fileFilter=filter, fileMode=3)
      if path:
        pm.textField(textField, edit=True, text=path[0])

      return path

    @classmethod
    def openFilePath(cls, path, *args, **kwargs):
      ''' open a file or path '''
      path = os.path.normpath(path)
      if os.path.exists(path):
        try:
          if sys.platform.startswith('darwin'):
            subprocess.call(('open', path))
          elif os.name == 'nt':
            os.startfile(path)
          elif os.name == 'posix':
            subprocess.call(('xdg-open', path))
        except:
          pm.warning('some problem opening the file or path')