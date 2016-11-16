import pymel.core as pm
from tempfile import mkstemp
from shutil import move
import os
from os import remove, close

from lct.src.core.lcPath import Path as path
from lct.src.core.lcUtility import Utility as utility

class Shelf:

  def __init__(self):
    """ """

  @classmethod
  def makeShelfButton(cls, name, command, icon, annotation='', *args, **kwargs):
      """ """
      currentShelf = pm.mel.eval('tabLayout -q -st $gShelfTopLevel;')

      buttonArray = pm.shelfLayout(currentShelf, query=True, childArray=True)
      if buttonArray:
        for item in buttonArray:
          label = pm.shelfButton(item, query=True, label=True)
          if label == name:
            pm.deleteUI(item)

      pm.setParent(currentShelf)

      pm.shelfButton(label=name, annotation=annotation, image1=icon, command=command)

  @classmethod
  def makeLctShelf(cls, *args, **kwargs):
      """ """
      src = path.getSrcPath()
      mel = path.getMelPath()
      shelf = os.path.normpath(os.path.join(mel, 'shelf_LCT.mel'))

      file = open(shelf, 'w+')
      opening = 'global proc shelf_LCT () {\n    global string $gBuffStr;\n    global string $gBuffStr0;\n    global string $gBuffStr1;\n\n'
      closing = '\n}'

      file.write(opening)

      initShelfIcon = os.path.normpath(os.path.join(src, 'icons', 'shelf.png'))
      initShelfLabel = 'Init Shelf'
      initShelfAnno = 'Initialize LCT Shelf'
      initShelfCommand = 'from lct.src.core.lcShelf import Shelf as shelf\nshelf.makeLctShelf()'

      file.write(closing)

      file.close()

      if not pm.layout('LCT', ex=True):
        if os.name == 'nt':
            shelf = shelf.replace('\\','/')
        pm.mel.loadNewShelf(shelf)
        pm.shelfButton(label=initShelfLabel, annotation=initShelfAnno, image1=initShelfIcon, command=initShelfCommand)
      else:
        pm.mel.eval('shelfTabLayout -edit -selectTab "LCT" $gShelfTopLevel;')
        
      list = utility.buildPublishList(inline=False)
      for item in list:
        if item[3] == 'True':
          label = item[0]
          annotation = item[2]
          icon = os.path.normpath(os.path.join(src, label, item[0]+'.png'))
          runCommand = item[4]

          cls.makeShelfButton(label, runCommand, icon, annotation)