import pymel.all as pm
from farm_map import importSprites

sel = pm.ls( sl=True )
for obj in sel :
    importSprites.shift_depth( obj, 0.1)