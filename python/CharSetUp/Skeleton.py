####################################################
#
# Character UI Setup for character Rigging tools
# Creator = Leo Michalek
# Created 18.08.2016
#
#
####################################################

import maya.cmds as cmds
import MASTER
import Rigging
import Rigging_IK

Skeleton_ONOFF = True

def Suffix():
    SuffixList = ["RigJNT","JNT"]
    return SuffixList


def Label_GetSide(Node,RigSides= None):
    if RigSides == None:
        RigSides = Rigging.Sides()
    NodeSide = None
    Value = 3
    
    for Side in RigSides:
        print Side
        if(Node.startswith(Side + "_")) :
            NodeSide = Side
           
            if RigSides[0] == Side: # Left Side
                Value = 1
            if RigSides[1] == Side: # Right Side
                Value = 2


    return [NodeSide,Value]

def JointLabeling(JNT,Label,SideAttrValue):
    cmds.setAttr(JNT + ".side",SideAttrValue)
    cmds.setAttr(JNT + ".type",18)
    cmds.setAttr(JNT + ".otherType",Label,type="string")



def UpdateJointLabel(SideLoc = 0,CheckBox=False,Hierarchy=False,InputSides=None,InputRemoveList=None):
    Locations       = ["Prefix","Infix","Suffix"]
    RigSuffixList   = Suffix()
    TempSides       = Rigging.Sides()
    RemoveList      = []
    SideList        = []


    for List in RigSuffixList:
        RemoveList.append(["Suffix",List])
    
    if InputRemoveList != None:
        for RL in InputRemoveList:
            RemoveList.append(RL)
         
    

    if InputSides != None:
        Value = 1 # right side
        for S in InputSides:
            if S == InputSides[0]: #should be == to left side
                Value = 2 # left side
            SideList.append(S)    
    #print "SideList2"
    #print SideList

    cmds.select(hi=Hierarchy)
    Sel     = cmds.ls(sl=True,type="joint")

    for Node in Sel:
        SideInfo = Label_GetSide(Node,InputSides)
        Side = SideInfo[0]
        Value = SideInfo[1]
        Label           = Node
        Temp            = ""
        #i = 1
        #getside info
        if not Side == None:
            Label   = Label.replace(Side + "_", "")
        #print "Label 1 "    
        #print Label
            #i+= 1
        #print "----------------"
        #print "Info"
        #print Node
        
        #print Side
 
        for List in RemoveList:
            Remove = List[1]
            #print "Remove"
            #print Remove
            #Label   = Label.replace("_" + Remove + "_", "_")
            #print Label
            Label   = Label.replace("_" + Remove, "")
            #print Label
            #Label   = Label.replace(Remove + "_", "")
            #print Label
            Label   = Label.replace(Remove, "")
            #print Label
        #print "Node :", Node,"Label :", Label, "Side :", SideNumb
        JointLabeling(Node,Label,Value)
        

def ScaleCompensate(Hiarchy=False,OnOff=1):
    if Hiarchy :
        cmds.select(hi=True)
    Sel = cmds.ls( sl=True,type="joint" )
    
    for S in Sel:
        cmds.setAttr(S + ".segmentScaleCompensate", OnOff)

def JointOrient_ToggleDisplay():
    #toggle display on Channel box for JointOrient for easy adjusting. 
    Sel = cmds.ls( sl=True )
    Axis = ["X","Y","Z"]
    On = cmds.getAttr(str(Sel[0]) + ".jointOrient" + Axis[0],k=True)
    for S in Sel:
        for A in Axis:
            cmds.setAttr( S + ".jointOrient" + A,k=(not On))

def LocalAxis_ToggleDisplay():
    #toggle display on Channel box for JointOrient for easy adjusting. 
    Sel = cmds.ls( sl=True )
    On = cmds.getAttr(str(Sel[0]) + ".displayLocalAxis")
    print (str(Sel[0]) + ".displayLocalAxis")
    print On
    for S in Sel:
        print S
        print (not On)
        cmds.setAttr( S + ".displayLocalAxis",(not On))


def CountJoints():
    cmds.select(hi=True)
    Sel = cmds.ls( sl=True,type="joint" )
    print len(Sel)
    return Sel

def SidesForMirroring(Name):
    Sides = [None]
    if(Name.startswith( "L_")):
        Sides = ["L_","R_"]
    if(Name.startswith( "R_")):
        Sides = ["R_","L_"]
    return Sides

def MirrorJoints():
    Sel = cmds.ls( sl=True,type="joint" )
    print Sel
    for S in Sel:
        Sides = SidesForMirroring(S)
        print Sides
        if(len(Sides)>1):
            cmds.mirrorJoint(S,mirrorYZ=True,mirrorBehavior=True,searchReplace=Sides)

def Joint_FreezeTransforms(Node=None,Trans=True,Rot=True,Sc=True):
    if Node == None:
        Node = cmds.ls(sl=True,type="joint")
    cmds.makeIdentity(Node,apply=True,t=Trans,r=Rot,s=Sc,n=False,pn=True)
    
def ZeroRotations(KeepOrientation,JNTS = None,WorldOrient=False,ScaleReset = False):
    
    
    #get list of joints in selection chain
    Axis = ["x","y","z"]
    if(JNTS == None):
        cmds.select(hi=True)
        JNTS = cmds.ls(sl=True,type="joint")
    #store parent of each joint
    if(KeepOrientation):
        Joint_FreezeTransforms(JNTS,True,True,ScaleReset)
    else:
        Parents = []
        for Jnt in JNTS:
            if(cmds.objExists(Jnt)):
                CParent = cmds.listRelatives( Jnt, p=True )
                Parents.append([Jnt,CParent])
                #if(not KeepOrientation):
                if (CParent != None):
                    print CParent
                    cmds.parent(Jnt,w=True)
                #remove rotations now that nothing is parented
        #cmds.select("kdkdkdkddk")
        for Jnt in JNTS:
            if(cmds.objExists(Jnt)):
                TEmp = cmds.createNode( 'transform', n=(Jnt + "_TEMP"))
                CParent = cmds.listRelatives( Jnt, p=True )
                cmds.parent(Jnt,TEmp)
                for A in Axis:
                    Attr = 0
                    cmds.setAttr(Jnt + ".r" + A,0)
                    if(ScaleReset):
                        cmds.setAttr(Jnt + ".s" + A,1)
                cmds.parent(Jnt,w=True)
                cmds.delete(TEmp)
          
        #reparent. 
        #if(not KeepOrientation): 
        for P in Parents:
            if(P[1] != None):
                if(cmds.listRelatives( P[0], p=True ) != P[1]):
                    cmds.parent(P[0],P[1])
    


def Connect_JNTS(Sel=None,Sel_Hierarchy=True):
    import re
    Driver = "_RigJNT"
    Driven = "_JNT"
    Extras = "RIG_EXTRAS"
    Parent = "JNT_Constraints"
    Sub    = "Sub"
    if(Sel_Hierarchy):
        cmds.select(hi=True)
    if Sel  == None:
        Sel = cmds.ls(sl=True,type="joint")
    if(str(Sel) == "[]"):
        print "nothing Selected.. Please Select top of Joint chain"   
    else:
        #if Parent nodes do not exists create them. 
        if Sel_Hierarchy:
            if(cmds.objExists(Parent)):
                cmds.delete(Parent)
        if(cmds.objExists(Extras) == False):
            cmds.createNode( 'transform', n=Parent)
        else:
            if(cmds.objExists(Parent) == False):
                cmds.createNode( 'transform', n=Parent,p=Extras)
        #now make connections.. and palce constraints in constraint node.
        for S in Sel:
            Prefix = re.sub(Driver, '', S)
            Prefix = re.sub(Driven, '', Prefix)
            Prefix2 = re.sub(Sub,'',Prefix)
            print Prefix
            print Prefix2
            NDriver = Prefix + Driver
            NDriven = Prefix + Driven
            NDriver_NoSub = Prefix2 + Driver
            RigJointExists = False
            if(cmds.objExists(NDriver)):
                RigJointExists = True
                NDriver = NDriver
            elif(cmds.objExists(NDriver_NoSub)):
                RigJointExists = True
                NDriver = NDriver_NoSub
            if(RigJointExists):
                Point   = cmds.pointConstraint(NDriver,NDriven)
                Orient  = cmds.orientConstraint(NDriver,NDriven)
                Scale   = cmds.scaleConstraint(NDriver,NDriven)
                for Constraint in [Point,Orient,Scale]:
                    cmds.parent(Constraint,Parent)
                #match Joint Orient's 
                JOrients = ["X","Y","Z"]
                for JO in JOrients:
                    Value = cmds.getAttr(NDriver + "." + "jointOrient" + JO)
                    cmds.setAttr(NDriven + "." + "jointOrient" + JO, Value)
            else:
                print (NDriver + " does not exists...")
                print ("Skipping connecting... : " + NDriven)

def PlaceJNT():
    
    Sel = cmds.ls(sl=True)
    Suffix = "PlaceJNT"
    for S in Sel:
        PlaceJNT = S + "_" + Suffix
        if(cmds.objExists(PlaceJNT) == False):
            cmds.createNode( 'transform', n=PlaceJNT)
            cmds.matchTransform(PlaceJNT,S,pos=True)
            cmds.parent(S,PlaceJNT)

def CreateIGJNTS():
    print "Create IG JNTS... "
    Sel = cmds.ls(sl=True)
    print Sel
    IG_SGRP = "IG_JNTS"
    NewJNTS = cmds.duplicate(Sel[0],rc=True)
    cmds.select(hi=True)
    IG_JNTS = cmds.ls(sl=True)
    NewJNTS = [IJ.replace("RigJNT","JNT") for IJ in NewJNTS]
    NewJNTS = [IJ.replace("JNT1","JNT") for IJ in NewJNTS]
    print NewJNTS
    print Sel
    [cmds.rename(IG_JNTS[i],NewJNTS[i]) for i in range(len(IG_JNTS))] 
    cmds.parent(NewJNTS[0],IG_SGRP)

def RemoveEndJNTS(Suffix):
    cmds.select(hi=True)
    Sel = cmds.ls(sl=True)
    for S in Sel:
      if (("End_" + Suffix) in S):
        cmds.delete(S)
        print "Deleted...->" + S
        
def ShowSkeleton(SkeletonTypeList,Status = None):
    for Type in SkeletonTypeList:
        Skeleton = Type + "_JNTS"
        if(cmds.objExists(Skeleton)):
            if (Status == None):
                Status = not cmds.getAttr(Skeleton + ".v")
            cmds.setAttr(Skeleton + ".v",Status)
            



########################################################
#
#
#                   Joint Helper Setup.. 
#
#
########################################################


def applyMaterial(Nodes,Color,ShaderName):
    shd = cmds.shadingNode('lambert', name="%s_lambert" % ShaderName, asShader=True)
    shdSG = cmds.sets(name='%sSG' % shd, empty=True, renderable=True, noSurfaceShader=True)
    cmds.connectAttr('%s.outColor' % shd, '%s.surfaceShader' % shdSG)
    cmds.setAttr('{0}.color'.format(shd), Color[0], Color[1], Color[2], type='double3')

    for node in Nodes:
        if cmds.objExists(node):
            cmds.sets(node, e=True, forceElement=shdSG)


def JointAxisHelper():
    
    Name        = "Template"
    Suffix      = "JNTHelper"
    Node        = Name + "_" + Suffix
    GRP         = Node + "_" + "GRP"
    RigTemplate = "Rig_" + Name
    SkelTemplate = "SkeletonTemplate"
    if (not cmds.objExists(GRP) or not cmds.objExists(Node) ):
        cmds.createNode('transform', n=RigTemplate)
        cmds.createNode('transform', n=GRP,parent= RigTemplate)
        cmds.setAttr(GRP + ".v",0)
        Mesh1 = cmds.polyCube(h=2,w=2,d=2)[0]
        
        Mesh2 = cmds.polyCube(h=.2,w=10,sd=2,sw=3)[0]
     
        List = [2,6,10,14,18,22]
        cmds.select(cl=True)
        for x in List:
            #print x
            vert = str(Mesh2) + ".vtx[" + str(x) + "]"
            #print vert
            cmds.select(vert,add=True)
        cmds.move(3.5,x=True,absolute=True)
        cmds.scale(1,1,3,r=True,ocp=True)
        List = [1,5,9,13,17,21]
        cmds.select(cl=True)
        for x in List:
            #print x
            vert = str(Mesh2) + ".vtx[" + str(x) + "]"
            #print vert
            cmds.select(vert,add=True)
        cmds.move(3.5,x=True,absolute=True)
        List = [3,7,11,15,19,23]
        cmds.select(cl=True)
        for x in List:
            #print x
            vert = str(Mesh2) + ".vtx[" + str(x) + "]"
            #print vert
            cmds.select(vert,add=True)
        #cmds.move(3.5,x=True,absolute=True)
        cmds.scale(1.5,0,0,r=True,ocp=True)
        cmds.select(Mesh2,r=True)
        cmds.move(5,x=True)
        cmds.move(0,0,0,Mesh2 + ".scalePivot",Mesh2 + ".rotatePivot",rpr=True)
        cmds.makeIdentity( apply=True, t=1, r=1, s=1, n=2 )
        TempMesh = cmds.duplicate(rr=True)[0]
        cmds.rotate(90,0,0,r=True,ws=True,fo=True)
        cmds.select(cl=True)
        cmds.select(TempMesh,add=True)
        cmds.select(Mesh2,add=True)
        Mesh3 = cmds.polyUnite()[0]
        cmds.DeleteHistory(Mesh3[0])
        
        applyMaterial([Mesh3,Mesh1+".f[4]",Mesh1+".f[5]"],[1,0,0],"Red")
        
        Mesh4 = cmds.duplicate(Mesh3,rr=True)[0]
        cmds.setAttr(Mesh4 + ".rz",90)
        applyMaterial([Mesh4,Mesh1+".f[1]",Mesh1+".f[3]"],[0,1,0],"Green")
        
        Mesh5 = cmds.duplicate(Mesh3,rr=True)[0]
        cmds.setAttr(Mesh5 + ".ry",-90)
        applyMaterial([Mesh5,Mesh1+".f[0]",Mesh1+".f[2]"],[0,0,1],"Blue")

        cmds.polyUnite( Mesh1,Mesh3,Mesh4,Mesh5,n=Node )
        cmds.DeleteHistory(Node)
        cmds.parent(Node,GRP)

    # visual connection... 
    #Pos     = [(0,0,0),(0,0,0)]
    #knots = [ X for  X in range(len(Pos))]
    #cmds.curve(n=CurveName, d=1, p=Pos,k=Knots )  


    return (Node,RigTemplate,SkelTemplate)

#JointAxisHelper()





def JointChain_Setup(JointType=["Spine",3]):
    JointCreateInfo = []
    Trans   = [0,0,0]
    Rot     = [0,0,0]
    LimbNames(Limb)
    if (JointType[0] == "Spine"):
        Name        = JointType[0]
        Distance    = 30
        Trans       = [0,60,0]
        Rot         = [-90,0,90]
        NumbJoints  = JointType[1]
        JointCreateInfo = [Name,NumbJoints,Distance,Trans,Rot]
    if (JointType[0] == "Legs"):
        Name = JointType[0]
        Distance = 30
        Trans       = [25,60,0]
        Rot         = [90,0,-90]
        #LimbList    = 
        NumbJoints = 3 #JointType[1]
        JointCreateInfo = [Name,NumbJoints,Distance,Trans,Rot]
    if (JointType[0] == "Neck"):
        Name = JointType[0]
        Distance = 30
        Trans       = [0,150,0]
        Rot         = [-90,0,90]
        NumbJoints = 1 #JointType[1]
        JointCreateInfo = [Name,NumbJoints,Distance,Trans,Rot]
    if (JointType[0] == "Arms"):
        Name = JointType[0]
        Distance = 30
        Trans       = [30,120,0]
        Rot         = [0,0,0]
        NumbJoints = 3 #JointType[1]
        JointCreateInfo = [Name,NumbJoints,Distance,Trans,Rot]
    if (JointType[0] == "Head"):
        Name = JointType[0]
        Distance = 30
        Trans       = [0,180,0]
        Rot         = [-90,0,90]
        NumbJoints = 1 #JointType[1]
        JointCreateInfo = [Name,NumbJoints,Distance,Trans,Rot]
    if (JointType[0] == "Face"):
        Name = JointType[0]
        Distance = 30
        Trans       = [0,190,20]
        Rot         = [-90,0,90]
        NumbJoints = 1 #JointType[1]
        JointCreateInfo = [Name,NumbJoints,Distance,Trans,Rot]
    if (JointType[0] == "Ears"):
        Name = JointType[0]
        Distance = 30
        Trans       = [20,190,0]
        Rot         = [-90,0,90]
        NumbJoints = 3 # JointType[1]
        JointCreateInfo = [Name,NumbJoints,Distance,Trans,Rot]
    if (JointType[0] == "Hair"):
        Name = JointType[0]
        Distance = 30
        Trans       = [0,150,-20]
        Rot         = [-90,0,90]
        NumbJoints = 4 #JointType[1]
        JointCreateInfo = [Name,NumbJoints,Distance,Trans,Rot]
    if (JointType[0] == "Tail"):
        Name = JointType[0]
        Distance = 30
        Trans       = [0,60,20]
        Rot         = [0,90,0]
        NumbJoints = 3 #JointType[1]
        JointCreateInfo = [Name,NumbJoints,Distance,Trans,Rot]      
    return JointCreateInfo
        

def JointChain_Create(JointType=["Spine",3]):
    JointHelperTemplate = JointAxisHelper()
    SkelTemplate        = JointHelperTemplate[2]
    JointHelperTemplate = JointHelperTemplate[0]
    JointCreateInfo     = JointChain_Setup(JointType)
    print "JointInfo... ",JointCreateInfo
    Name                = JointCreateInfo[0]
    NumJoints           = JointCreateInfo[1]
    Distance            = JointCreateInfo[2]
    Trans               = JointCreateInfo[3]
    Rot                 = JointCreateInfo[4]
    JointHelperBase     = ""
    Parent              = ""
    for i in range(0,JointCreateInfo[1]):
        JointName = Name + str(i) + "_RigJNT"
        JointHelper = Name + str(i) + "_JNTHelper"
        XValue = Distance * i
        
        cmds.duplicate(JointHelperTemplate,rr=True,name=JointHelper)[0]
        
        if i >0:
            cmds.parent(JointHelper,Parent)
            cmds.setAttr(JointHelper + "." + "tx",Distance)
        else:
            cmds.parent(JointHelper,SkelTemplate)
            JointHelperBase =    JointHelper
            #cmds.setAttr(JointHelper + "." + "tx",Distance)
        #cmds.joint(n= JointName,p=(XValue,0,0))
        Parent = JointHelper
    cmds.xform(JointHelperBase,t=Trans,ro=Rot)    
#JointChain_Create()

def SkeletonTemplate_Parts():
    BodyParts = [["Spine",3],["Legs"],["Neck"],["Arms"],["Head"],["Face"],["Ears"],["Hair"],["Tail"],["kdkdkdkdk"]]
    return BodyParts

def JointHelper_To_Joint():
    Suffix = ['JNTHelper','RigJNT']
    SkelTemplate        = JointAxisHelper()[2]
    #get list of Helper nodes
    HelperNodesList = cmds.listRelatives(SkelTemplate,ad=True,type='transform')
    print HelperNodesList
    JointList = []
    for Node in HelperNodesList:
        JointName = Node.replace(Suffix[0], Suffix[1])
        print Node, JointName
        cmds.joint(n= JointName,p=(0,0,0))
        Position = cmds.xform(Node,q=True,t=True,ws=True,a=True)
        Rotation = cmds.xform(Node,q=True,ro=True,ws=True,a=True)
        cmds.xform(JointName,t=Position,a=True,ws=True)
        cmds.setAttr(JointName + ".jointOrientX", Rotation[0])
        cmds.setAttr(JointName + ".jointOrientY", Rotation[1])
        cmds.setAttr(JointName + ".jointOrientZ", Rotation[2])
        cmds.select(cl=True)
        Parent = cmds.listRelatives(Node,parent=True)[0]
        print Parent
        Parent = Parent.replace(Suffix[0], Suffix[1])
        JointList.append([JointName,Parent])
    for Joint in JointList:
        if Joint[1]== SkelTemplate:
            cmds.parent(Joint[0],w=True)
        else:
            cmds.parent(Joint[0],Joint[1])
    print JointList

    #save Name and Parent of Helper nodes
    # Create, Name and place Actual Joint in Helper nodes and zero out. 
    # Unparent All Joints
    # Parent Joints to Helper Joint Parents. 


def CheckSide(Joint):
    RigSides = Rigging.Sides()
    OppositeSide = ""
    JointSide       = ""
    Mirror = False
    HasSide = None
    for Side in RigSides:
        if(Joint.startswith(Side + "_")) :
            JointSide = Side
            HasSide = True
        else:
            OppositeSide = Side
    if(HasSide):
        if(not cmds.listRelatives(Joint,p=True)[0].startswith(JointSide + "_")):
            MirrorJoint = Joint.replace(JointSide + "_", OppositeSide + "_")
            print MirrorJoint
            if(not cmds.objExists(MirrorJoint)):
                Mirror = True

    return (Mirror,[JointSide + "_",OppositeSide + "_"])

def Skeleton_MirrorFromRoot(TopNode = None,Force = True):
    if TopNode == None:
        TopNode = cmds.ls(sl=True,type='joint')
    List = cmds.listRelatives(TopNode,ad=True,type='joint')
    RigSides = Rigging.Sides()
    NewSide = False
    MirrorList = []
    for Joint in List:
        Mirror = SkelCheckSide(Joint)
        if Mirror[0] == False:
            cmds.mirrorJoint(Joint,mirrorYZ=True,mirrorBehavior=True,searchReplace=Mirror[1])
   
   
   
#------------------------------------------             
# create Joints from selected nodes..    
#------------------------------------------    


def CreateJoints(List):
    Suffix= "_RigJNT"
    cmds.select(cl=True)
    for L in List:
        print L
        NewParent = cmds.listRelatives(L,p=True)
        print NewParent
       
        cmds.joint(n=L + Suffix)
        if NewParent is not None:
            NewParent = str(NewParent[0]) + Suffix
            
            CurrentParent = cmds.listRelatives(L+Suffix,p=True)
            CurrentParent = str(CurrentParent[0])
            print NewParent
            print CurrentParent
            if NewParent != CurrentParent:
                cmds.parent(L+Suffix,NewParent) 
        cmds.select(L,add=True)
        cmds.MatchTransform(L + Suffix,L)
        cmds.select(L + Suffix)

     
     
def CreateSkeleton_SelectionList():
    Sel = cmds.ls(sl=True)
    cmds.select(cl=True)
    for S in Sel:
        cmds.select(S)
        cmds.select(hi=True)
        List = cmds.ls(sl=True)
        CreateJoints(List)
    

