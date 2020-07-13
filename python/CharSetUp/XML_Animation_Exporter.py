################################################
# Maya pyMel script                            #
# Export animation to XML 0.1                  #
#                                              #
# Exports animation data from current selected #
# object to an XML file of choice              #
################################################

from pymel.core import *

import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMaya as OpenMaya
import maya.OpenMayaAnim as OpenMayaAnim
import pymel.core as pm
# For debugging
# import pydevd
# pydevd.settrace()
# pydevd.settrace(stdoutToServer=True, stderrToServer=True, suspend=False)

# scriptTable command calls MEL procedures internally so we have to specify these in MEL
mel.eval( 'global proc string getCellMel( int $row, int $column ) { return python( "cvxporter.getCell( " + $row + ", " + $column + ")" ); }' )
mel.eval( 'global proc cellChangedMel( int $row, int $column, string $value ) { python( "cvxporter.cellChanged( " + $row + ", " + $column + ", \\\"" + $value + "\\\" )" ); }' )

# startDirectory = cmds.workspace( query=True, rootDirectory=True )

def main_XML_Anim_Export():
    # Selected objects
    selected = ls(sl=True)
    
    error = 0
    
    # Check for first selected object
    try:
        s = selected[0] 
    except IndexError:
        print "ERROR: No object selected for animation data export"
        error = 1
    
    if error == 0:
        fileName = fileDialog2(fileFilter="XML Files (*.xml);;All Files (*.*)", caption='Output to animation file')
        try:
            file = open( fileName[0], 'w' )
        except TypeError:
            print "ERROR: No file chosen, aborting"
            error = 1
    if error == 0:
        # Let's get some animation data!
        
        
        animationFrameRate = pm.mel.currentTimeUnitToFPS()
        startTime = OpenMayaAnim.MAnimControl.minTime().value()
        endTime = OpenMayaAnim.MAnimControl.maxTime().value()
        print "FrameRate:", animationFrameRate
        #animCurves = cmds.keyframe(q=True,n=True,sl=True)
        ##timeSelKey = cmds.keyframe(animCurves[0],q=True,sl=True)
        gPlayBackSlider = mel.eval("string $temp=$gPlayBackSlider")
        
        FrameRange = cmds.timeControl(gPlayBackSlider, q=True,rangeArray=True)
        print "FrameRange:", FrameRange
        print len(FrameRange)
        if((FrameRange[1] - FrameRange[0]) > 2):
            startTime = FrameRange[0]
            endTime  = FrameRange[1]-1
        
        print "Start:", startTime
        print "End  :", endTime
        
        
        
        
        print "Collecting animation data from frame "+str(startTime)+" to "+str(endTime)+" ..."
        
        # Translations, x y z
        lastTx = 0.0
        lastTy = 0.0
        lastTz = 0.0
        curTx = 0.0
        curTy = 0.0
        curTz = 0.0
        # Rotation, x y z
        lastRx = 0.0
        lastRy = 0.0
        lastRz = 0.0
        curRx = 0.0
        curRy = 0.0
        curRz = 0.0
        # Scale, x y z
        lastSx = 0.0
        lastSy = 0.0
        lastSz = 0.0
        curSx = 0.0
        curSy = 0.0
        curSz = 0.0
        
        write = 0
        
        for k in range(1, 4):
            for j in range( int(startTime), int(endTime) + 1 ):
                cmds.progressWindow( edit=True, step=1 )
                # Set current frame
                OpenMayaAnim.MAnimControl.setCurrentTime( OpenMaya.MTime( j, OpenMaya.MTime.uiUnit() ) )
                
                ###############
                ## Translate ##
                ###############
                
                if k == 1:
                    curTx = s.tx.get()
                    curTy = s.ty.get()
                    curTz = s.tz.get()
                    if j != int(startTime) and j != int(endTime): # time is first or last, always set keyframe
                        if curTx != lastTx or curTy != lastTy or curTz != lastTz:
                            write = 1
                            lastTx = curTx
                            lastTy = curTy
                            lastTz = curTz
                    else:
                        write = 1
                    if write == 1:
                        file.write( '\t\t<Translation time="%.3f" x="%.3f" y="%.3f" z="%.3f"/>\n' % (float(j-int(startTime))/animationFrameRate, (curTx), -(curTy), (curTz)))
                write = 0
                
                ###############
                ##  Rotate   ##
                ###############
                
                if k == 2:
                    curRx = s.rx.get()
                    curRy = s.ry.get()
                    curRz = s.rz.get()
                    if j != int(startTime) and j != int(endTime): # time is first or last, always set keyframe
                        if curRx != lastRx or curRy != lastRy or curRz != lastRz:
                            write = 1
                            lastRx = curRx
                            lastRy = curRy
                            lastRz = curRz
                    else:
                        write = 1
                    if write == 1:
                        file.write( '\t\t<Rotation time="%.3f" x="%.3f" y="%.3f" z="%.3f"/>\n' % (float(j-int(startTime))/animationFrameRate, (curRx), (curRy), -(curRz)))
                write = 0
                
                ###############
                ##   Scale   ##
                ###############
                
                if k == 3:
                    curSx = s.sx.get()
                    curSy = s.sy.get()
                    curSz = s.sz.get()
                    if j != int(startTime) and j != int(endTime): # time is first or last, always set keyframe
                        if curSx != lastSx or curSy != lastSy or curSz != lastSz:
                            write = 1
                            lastSx = curSx
                            lastSy = curSy
                            lastSz = curSz
                    else:
                        write = 1
                    if write == 1:
                        file.write( '\t\t<Scale time="%.3f" x="%.3f" y="%.3f" z="%.3f"/>\n' % (float(j-int(startTime))/animationFrameRate, (curSx), (curSy), (curSz)))
                write = 0
                
            file.write( '\n' )
        file.close
        print "Animation data written to '"+fileName[0]+"'"
        
#main()