import sys
import os
import pymel.core as pm

class Photoshop():
  """ send files to Photoshop """
  
  def __init__(self):
    """ """
    self.psPath = 'photoshop.exe' #os.environ['PHOTOSHOP']
    
  def openFileNodeTexture(self, fileNode, *args, **kwargs):
    """ open a file node's texture in photoshop """
    self.openTexture(pm.getAttr(fileNode+'.fileTextureName'))
  
  def openTexture(self, fileToOpen, *args, **kwargs):
    """ open a file in photoshop """
    platform = sys.platform
    if platform == 'win32':
      print 'start "" "'+self.psPath+'" "'+os.path.normcase(fileToOpen)+'"'
      os.system('start "" "'+self.psPath+'" "'+os.path.normcase(fileToOpen)+'"')
    else:
      os.startfile(fileToOpen)
      
  def openMesh(self, mesh, *args, **kwargs):
    """ export a mesh as obj and open that file in photoshop """
    self.texture = kwargs.get('texture', False)
    
    sel = pm.ls(sl=True)
    path = pm.workspace(q=True,rd=True)
    fileName = 'lcMtPs_temp.obj'
    exportFile = path+fileName
    
    if texture: pm.exportSelected(exportFile, f=2, pr=0, typ='OBJexport', es=1, op="groups=1;ptgroups=1;materials=1;smoothing=1;normals=1")
    else: pm.exportSelected(exportFile, f=2, pr=0, typ='OBJexport', es=1, op="groups=1;ptgroups=1;materials=0;smoothing=1;normals=1")

    os.system('start "" "photoshop.exe" "'+os.path.normcase(exportFile)+'"')
