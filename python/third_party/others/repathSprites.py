import os, sys
import pymel.all as pm

BASE_PATH = '/Volumes/SSD/Work/FarmHeroes/FarmHeroes_art/Game/live-ops/pet'
DIR_PATH = 'pet_cropsie_strawberry-assets'
REPLACE_PATH = 'pet_cropsie_carrot-assets/%s'


sel = pm.ls(type=pm.nodetypes.File)

for f in sel :
    path = f.fileTextureName.get()
    dirpath = os.path.join( BASE_PATH, DIR_PATH )
    if( dirpath in path ) :
        filename = os.path.basename(path)
        
        newpath = os.path.join( BASE_PATH, REPLACE_PATH % ( filename ) )
        
        if( os.path.exists( newpath ) ) :
            f.fileTextureName.set( newpath )
        else :
            print 'Could not find file %s' % ( newpath )
            
        