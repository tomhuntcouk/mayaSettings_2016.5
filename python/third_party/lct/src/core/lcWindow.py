import webbrowser
import pymel.core as pm
from lct.src.core.lcShelf import Shelf as shelf

class lcWindow:
  
  def __init__(self, windowName, width, height, icon, shelfCommand, annotation = ' ', dockable=False, menuBar=False, mnb=False, mxb=False, s=False, rtf=False, startArea='right', allowedAreas='all', floating=False, *args, **kwargs):
    """ Initialize class and variables """
    self.windowName = windowName
    self.dockName = windowName+'Dock'
    self.width = width
    self.height = height
    self.icon = icon
    self.shelfCommand = shelfCommand
    self.annotation = annotation
    self.dockable = dockable
    self.menuBar = menuBar
    self.mnb = mnb
    self.mxb = mxb
    self.sizeable = s
    self.rtf = rtf
    self.startArea = startArea
    self.allowedAreas = allowedAreas
    self.floating = floating
    self.mainWindow = ''

  def create(self, *args, **kwargs):
    ''' '''
    if pm.control(self.windowName, exists = True):
      pm.deleteUI(self.windowName)
    if pm.control(self.dockName, exists = True):
      pm.deleteUI(self.dockName)
      
    if self.dockable:
      self.mainWindow = pm.window(self.windowName, t=self.windowName, menuBar=self.menuBar)
    else:
      self.mainWindow = pm.window(self.windowName, t=self.windowName, widthHeight=[self.width, self.height], menuBar=self.menuBar, rtf=self.rtf, mnb=self.mnb, mxb=self.mxb, s=self.sizeable)
    
    if self.menuBar:
      pm.menu(l='Help', helpMenu=True)
      pm.menuItem(l='blog.leocov.com', command=lambda *args: webbrowser.open('http://blog.leocov.com', new=2) )
      pm.menu(l='Tools')
      pm.menuItem(l='Make Shelf Icon', command=lambda *args: shelf.makeShelfButton(self.windowName, self.shelfCommand, self.icon, self.annotation) )
        
  def show(self, *args, **kwargs):
    ''' '''
    if self.dockable:
      mainDock = pm.dockControl(self.dockName, label=self.windowName, area=self.startArea, content=self.mainWindow, allowedArea=self.allowedAreas, floating=self.floating, w=self.width, h=self.height)
    else:
      self.mainWindow.show()
