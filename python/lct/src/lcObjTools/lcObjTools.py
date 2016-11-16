publish = True
annotation = "Export and Import Obj's"
prefix = 'lcObj'

import os
import math
import pymel.core as pm

from lct.src.core.lcUtility import Plugin as plugin
from lct.src.core.lcGeometry import Geometry as geometry
from lct.src.core.lcWindow import lcWindow as lcWindow
from lct.src.core.lcPath import Path as path

import lct.src.core.lcColor as color	
# interface colors
kw = {'hue':0.45, 'saturation':0.5, 'value':0.5}
colorWheel = color.ColorWheel(10, **kw)

basePath = os.path.abspath(os.path.dirname(__file__))+'/'
iconBasePath = os.path.abspath(os.path.dirname(__file__))+"/icons/"

def lcObjToolsUI(dockable=False, *args, **kwargs):
  ''' '''
  global prefix
  ci = 0 #color index iterator
  windowName = 'lcObjTools'
  shelfCommand = 'import lct.src.lcObjTools.lcObjTools as lcObj\nreload(lcObj)\nlcObj.lcObjToolsUI()'
  icon = basePath+'lcObjTools.png'
  winWidth  = 204
  winHeight = 158
  
  mainWindow = lcWindow(windowName=windowName, width=winWidth, height=winHeight, icon=icon, shelfCommand=shelfCommand, annotation=annotation, dockable=dockable, menuBar=True)
  mainWindow.create()

  #
  pm.columnLayout(prefix+'_columLayout_main')

  #
  pm.rowColumnLayout(nc=2, cw=([1,150], [2,50]) )
  pm.textField(prefix+'_textField_export_path', w=150)
  pm.button(prefix+'_button_browse_path', l='Browse', bgc=colorWheel.getColorRGB(ci), annotation='Choose an export directory', w=50, command=lambda *args: path.browsePathTextField(prefix+'_textField_export_path', "Wavefront Obj (*.obj)", 'Obj Export Location') )
  ci+=1
  pm.setParent(prefix+'_columLayout_main')

  #
  pm.checkBox(prefix+'_checkBox_export_indi', l='Export Individual', v=False)
  pm.checkBox(prefix+'_checkBox_use_smooth', l='Use Smooth Preview', v=True)

  #
  pm.rowColumnLayout(nc=2, cw=([1,100], [2,100]) )
  pm.textField(prefix+'_textField_prefix', w=100)
  pm.text(l='   Prefix_', al='left')
  pm.setParent(prefix+'_columLayout_main')

  #
  pm.rowColumnLayout(nc=2, cw=([1,169], [2,31]) )
  pm.columnLayout(w=169)
  pm.button(prefix+'_button_export', l='Export OBJ', bgc=colorWheel.getColorRGB(ci), annotation='Export the selected geometry', w=168, h=30, command=lambda *args: lcObj_exportObjs() )
  ci+=1
  pm.button(prefix+'_button_Import', l='Import Multiple OBJs', bgc=colorWheel.getColorRGB(ci), annotation='Clean import more than one obj', w=168, h=20, command=lambda *args: lcObj_importMultiple() )
  ci+=1
  pm.setParent('..')
  pm.columnLayout(w=31)
  pm.iconTextButton(prefix+'_button_open_folder', style='iconOnly', image=iconBasePath+'folder_30x50.png', annotation='Open the export folder', w=30, h=50, command=lambda *args: path.openFilePath(pm.textField(prefix+'_textField_export_path', query=True, text=True) ) )
  ci+=1
  
  #
  mainWindow.show()
  
  plugin.reloadPlugin(plugin='objExport', autoload=True)

def lcObj_setExportPath(*args, **kwargs):
  ''' browse a folder path and update text field '''
  global prefix
  path = pm.textField(prefix+'_textField_export_path', query=True, text=True)
  filter = "Wavefront Obj (*.obj)"
  path = pm.fileDialog2(ds=1, caption='Obj Export Location', dir=path, fileFilter=filter, fileMode=3)
  if path:
    pm.textField(prefix+'_textField_export_path', edit=True, text=path[0])

def lcObj_exportObjs(*args, **kwargs):
  ''' Export .obj files from selected geometry, either as one combined file or as individual files per object.  Will recognize and convert poly smooth preview to geometry for export '''
  global prefix
  path = pm.textField(prefix+'_textField_export_path', query=True, text=True)
  objPrefix = pm.textField(prefix+'_textField_prefix', query=True, text=True)
  if objPrefix:
    objPrefix+='_'

  if path:

    sel = pm.ls(sl=True)

    if sel:
      sel = geometry.filterForGeometry(sel)
      print sel

      #undo is the easiest way to work on geometry temporarily
      pm.undoInfo(openChunk=True)

      if pm.checkBox(prefix+'_checkBox_use_smooth', query=True, v=True):
        for obj in sel:
          pm.select(obj)
          #find the objects currently displayed as smooth and create converted poly copies
          if pm.displaySmoothness(q=True, polygonObject=True)[0] == 3:
            pm.mel.performSmoothMeshPreviewToPolygon()

      if pm.checkBox(prefix+'_checkBox_export_indi', query=True, v=True):
        #export objects individually
        for obj in sel:
          pm.select(obj)
          name = str(obj)
          exportString = path+'/'+objPrefix+name+'.obj'
          pm.exportSelected(exportString, force=True, options='groups=1;ptgroups=1;materials=0;smoothing=1;normals=1', type='OBJexport', pr=True, es=True)

      else:
        #export as one object
        pm.select(sel)
        name = ''
        while name == '':
          dialog = pm.promptDialog(title='OBJ Name', message='Enter Name:', button=['OK', 'Cancel'], defaultButton='OK', cancelButton='Cancel', dismissString='Cancel')
          if dialog == 'OK':
            name = pm.promptDialog(query=True, text=True)
            if name:
              exportString = path+'/'+objPrefix+name+'.obj'
              pm.exportSelected(exportString, force=True, options='groups=1;ptgroups=1;materials=0;smoothing=1;normals=1', type='OBJexport', pr=True, es=True)
            else:
              pm.warning("You didn't type a name for your obj")
          if dialog == 'Cancel':
            break

      pm.undoInfo(closeChunk=True)
      pm.undo()
      pm.select(clear=True)

  else:
    pm.warning('Did you specify a path?')

def lcObj_importMultiple(*args, **kwargs):
  ''' select multiple .obj's and import them into the scene with best settings '''

  path = pm.textField(prefix+'_textField_export_path', query=True, text=True)
  filter = "Wavefront Obj (*.obj)"
  files = pm.fileDialog2(ds=1, caption="Choose one or more Obj's to import", dir=path, fileFilter=filter, fileMode=4)
  if files:
    for obj in files:
      name = obj.split('/')[-1].split('.')[0]
      importedObj = pm.importFile(obj, type='OBJ', options='mo=0')

# def lcObj_openFolder(*args, **kwargs):
  # ''' select multiple .obj's and import them into the scene with best settings '''

  # folderPath = pm.textField(prefix+'_textField_export_path', query=True, text=True)
  # path.openTextureList(pm.textField(prefix+'_textField_export_path', query=True, text=True) )



