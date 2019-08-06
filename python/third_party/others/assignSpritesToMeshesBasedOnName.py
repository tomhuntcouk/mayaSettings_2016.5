
import os, sys
import pymel.all as pm


#BASE_PATH = "/Volumes/SSD/Work/FarmHeroes/FarmHeroes_art/Game/core/models/farm_pet_export/pet_cropsie_strawberry-assets/"
BASE_PATH = "/Volumes/SSD/Work/FarmHeroes/FarmHeroes_art/Game/live-ops/pet/pet_cropsie_onion-assets"

sel = pm.ls(selection=True)

# for each mesh
# get name
# create material based on name
# create a file node
# assign texture path to file
# assign material to mesh

for mesh in sel :
    name = mesh.name().encode('ascii')
    spritename = name
    texpath = os.path.join(BASE_PATH, name) + '.png'
    
    # check if the png exists
    if( not os.path.isfile(texpath) ) :
        # check if the opposite side exists (L/R)
        prefix = name[0]
        if( prefix == 'L' ) : prefix = 'R'
        if( prefix == 'R' ) : prefix = 'L'
        
        spritename = prefix + name[1:]
        
        texpath = os.path.join(BASE_PATH, spritename)+ '.png'
        if( not os.path.isfile(texpath) ) :
            pm.warning( "COULD NOT FIND %s (or %s)" % ( name, spritename ) )
            continue
            
            
    # we have found the sprite
    # let's make the material
    
    materialname = spritename + '_MAT'

    try :
        material = pm.PyNode(materialname)
        print 'Found %s' % ( materialname )
    except pm.MayaNodeError :
        material = pm.cmds.shadingNode('lambert', asShader=True, name=materialname)
        material = pm.PyNode(materialname)
        print 'Created %s' % ( materialname )


    # let's create the file node

    filenodes = material.color.listConnections(type='file')
    
    filename = spritename + '_FILE'
    
    if( len(filenodes) == 0) :
        filenode = pm.nodetypes.File(name=filename)
    else :
        filenode = filenodes[0]
    
    filenode.setAttr('fileTextureName', texpath)
    filenode.outColor >> material.color
    filenode.outTransparency >> material.transparency
    material.transparencyR.disconnect()
    material.transparencyG.disconnect()
    material.transparencyB.disconnect()

    # now let's assign the material to the mesh
    
    """
    shadingname = spritename + '_SG'
    shadingGroups = material.listConnections(d=True, type='shadingEngine')
    if( len(shadingGroups) == 0 ) :
        shadingGroup = pm.nodetypes.ShadingEngine(name=shadingname)
    else :
        shadingGroup = shadingGroups[0]
    
    material.outColor >> shadingGroup.surfaceShader
    
    """
    
    #pm.sets(mesh, e=True, forceElement=shadingGroup)    
    #pm.sets(shadingGroup, forceElement=mesh)
    pm.select(mesh)
    pm.hyperShade(assign=material)   
    
        
pm.select(sel)



