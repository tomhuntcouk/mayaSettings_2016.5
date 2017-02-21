import pymel.all as pm

def CreateScaleRig(name) :
    outgrp = pm.group(name='%s_squashRig_GRP' % (name), empty=True )    
    outloc = pm.spaceLocator(name='%s_squashOut_LOC' % (name) )
    outloc.setParent(outgrp)
    aims = []
    inattrs = []
    pm.cycleCheck(e=False)
    for axis in [ 'X', 'Y', 'Z' ] :
        loc = pm.spaceLocator(name='%s_squashIn%s_LOC' % (name, axis))
        grp = pm.group(name='%s_squashLoc%s_GRP' % (name, axis), empty=True)
        loc.setParent(grp)
        grp.setAttr( 'translate%s' % (axis), 1 )        
        pm.pointConstraint(loc, outloc, mo=False)        
        aims.append( pm.aimConstraint(outloc, grp) )
        grp.setParent(outgrp)
        inattrs.append(loc.translateX)
    for aim in aims :
        pm.delete(aim)
    pm.cycleCheck(e=True)
    return {
        'group' : outgrp,
        'inattrs' : inattrs,
        'outattrs' : outloc.translate
    }
        
def ConnectThroughRig( src, attr, root, rigObject ) :
    name = src.name()    
    grp = pm.group(name='%s_squash_GRP' % (name), empty=True, parent=src.getParent())
    grp.setTranslation( src.getTranslation(space='world'), space='world' )

    for child in src.getChildren(type=pm.Transform) :
        child.setParent(grp)

    md = pm.MultiplyDivide(name='%s_squashInvert_MD' % ( name ) )
    md.input1.set(-1,-1,-1)
    for i, axis in enumerate(['X', 'Y', 'Z']) :
        src.attr('%s%s' % (attr,axis)) >> md.attr('input2%s'%axis)
        md.attr('output%s'%axis) >> rigObject['inattrs'][i]

    md = pm.MultiplyDivide(name='%s_squashScaleOffset_MD' % ( name ) )
    rigObject['outattrs'] >> md.input1
    md.input2.set(3,3,3)
    md.output >> grp.scale


    pm.pointConstraint( src, grp, mo=False )
    pm.orientConstraint( src, grp, mo=False )

    return {
        'control' : src,
        'root' : root,
        'rig' : rigObject['group']
    }


def __group(name, parent) :
    try :
        grp = pm.PyNode('%s|%s' % (parent, name))
        # if( len(grp.getChildren(type=pm.Shape)) > 0 ) :
        #     return None
        # else :
        #     return grp
    except :
        grp = pm.group(name=name, parent=parent, empty=True)
    return grp


def Tidy( connectionObjectList ) :    

    for i, connectionObject in enumerate( connectionObjectList ) :
        controlgrp = __group('controls_GRP', connectionObject['root'] )

        if i == 0 :
            connectionObject['control'].setParent( controlgrp )
        else :
            connectionObject['control'].setParent( connectionObjectList[i-1]['control'] )

        riggrp = __group('rig_GRP', connectionObject['root'])
        connectionObject['rig'].setParent(riggrp)
        riggrp.hide()

        return {
            'controlgrp' : controlgrp,
            'riggrp' : riggrp
        }



def Create( sourceList ) :

    connectionObjectList = []

    for cntrl in sourceList :
        src = cntrl[0]
        attr = cntrl[1]
        root = cntrl[2]

        rigObject = CreateScaleRig(src.name())
        connectionObject = ConnectThroughRig( src, attr, root, rigObject )
        connectionObjectList.append(connectionObject)

    return Tidy( connectionObjectList )

