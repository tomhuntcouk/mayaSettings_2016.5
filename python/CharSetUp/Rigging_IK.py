
####################################################
#
# Character UI Setup for character Rigging tools
# Creator = Leo Michalek
# Created 18.08.2016
#
#
####################################################

import maya.cmds as cmds
import Curves
import Skeleton
import Rigging
import MASTER
from inspect import currentframe, getframeinfo
ScriptLocation = getframeinfo(currentframe())
Rigging_IK_ONOFF = True

def LimbNames(Limb):
    Spine       = ["COG",["Spine#","Neck#","Head","HeadEnd"],"Hips"]
    Leg         = ["Leg","Knee","Ankle","Foot","Ball","ToeEnd"]
    Arm         = ["Arm","ForeArm","Wrist","Hand","Palm","FingerEnd"]
    Ears        = ["EarBase","Ear#End"]
    Eyes        = [["Eyes",["EyeBase",["Eye","EyePupil"],"EyeLid","EyeLidBottom"]]]
    EyeBrow     = [["EyeBrowBase","EyeBrow#:From CenterOut"]]
    Mouth       = [LipTop,["Jaw",LipBottom,"Chin"]]
    LipTop      = [["LipTopBase","LipTop","MouthCorner"]]
    LipBottom   = [["LipBottomBase","LipBottom:Center & Sides"]]
    Nose        = ["NoseBase",["Nose","Nostril:Side"]]
    Tail        = ["TailBase","Tail#End"]
    Hands       = ["Thumb#",["Fingers","Index#","Middle#","Ring#","Pinky#"]]
    Tools       = ["Tool#:flat"]

def NodeTypes():
    #               0      1        2         3     4     5       6        7
    NodeTypes = ["JNT","RigJNT","IKHandle","CTRL","LOC","GRP","SubGRP","Effector"]

    return NodeTypes

def ExtraAttr():
    Attr =      ["HeelPeel","Ball_Pivot","Ball_Twist","ToePeel","Toe_Pivot","Toe_Twist","ToeTap","ToeWiggle"]
    return Attr


def ReverseFootLimbs(LimbType,GetLimbType = False):
    Limbs = []
    ArmLimbs =     ["Arm","ForeArm","Wrist","Hand","Palm","FingerEnd"]
    LegLimbs =     ["Leg","Knee","Ankle","Foot","Ball","ToeEnd"]
    
    if(LimbType == "Leg"):
        Limbs =  LegLimbs
    if(LimbType == "Arm"):
        Limbs =  ArmLimbs
    if GetLimbType:
        if LimbType in ArmLimbs:
            Limbs = "Arm"
        if LimbType in LegLimbs:
            Limbs = "Leg"

    return Limbs

def Get_LimbPivot(LimbType):
    JointName = "HandPivotEnd"
    if (LimbType == "Leg"):
        JointName = "FootPivotEnd"
    return JointName
    
def JointDirection(StartJoint,EndJoint):

    startJointPos = cmds.xform(StartJoint,q=True,ws=True,t=True)
    endJointPos     = cmds.xform(EndJoint,q=True,ws=True,t=True)
    #Calculate the distance between the points in x, y & z
    xDist = (endJointPos[0] - startJointPos[0])
    yDist = (endJointPos[1] - startJointPos[1])
    zDist = (endJointPos[2] - startJointPos[2])
    # Choose the axis that contains the largest distance
    # X-axis is the default
    axis = 0
    # Y-axis
    if( (abs(yDist) > abs(xDist)) and (abs(yDist) > abs(zDist)) ):
        axis = 1
    # Z-axis
    if( (abs(zDist) > abs(xDist)) and (abs(zDist) > abs(yDist)) ):
        axis = 2

    # get if it's positive direction or negative
    XDir = 0
    if (xDist != 0 ):
        XDir = xDist/abs(xDist)
    YDir = 0
    if (yDist != 0 ):
        YDir = yDist/abs(yDist)
    ZDir = 0
    if (zDist != 0 ):
        ZDir = zDist/abs(zDist)
    PNDir       = [XDir,YDir,ZDir]
    PosNegDir   = PNDir[axis]
    return [PosNegDir,axis]
        

def AddAttr_SetUp(IK_CTRL,ExAttr):
    #********************************    ADD Extra Attributes to IK Controllers   ********************************************************
    # Add the special joint control attributes to the main limb Controllers
    for Attr in ExAttr:
        if (cmds.objExists(IK_CTRL + "." + Attr)):
            cmds.deleteAttr(IK_CTRL,at=Attr)        
        cmds.addAttr(IK_CTRL,ln=Attr,k=1,at="double",dv=0)
    #********************************    END ADD Extra Attributes to IK Controllers   ********************************************************

def IK_Handle_Create(Start_JNT,End_JNT,IKHandleName,IK_Solver = "ikRPsolver"):
    NodeType = NodeTypes()
    IkName = cmds.ikHandle(n=IKHandleName,sj=Start_JNT, ee=End_JNT,solver= IK_Solver)
    effectorName = IkName[0].replace(NodeType[2], NodeType[7])
    cmds.rename( IkName[1],effectorName)
    IkName[1] = effectorName
    MakeAllNoneKeyable = cmds.listAttr(IKHandleName,k=True)
    for MANK in MakeAllNoneKeyable:
        cmds.setAttr(IKHandleName + "." + MANK,k=False,channelBox=True)
    return IkName

def IK_GRPS(GRPName,Children,PositionMatch,Parent,ParentGRP=False):
    ParentGRPName = GRPName
    if(ParentGRP):
        ParentGRPName   = GRPName.replace("GRP","ParentGRP")
        ParentGRPName   = cmds.createNode('transform', n=ParentGRPName)
        GRPName         = cmds.createNode('transform', n=GRPName,p=ParentGRPName)
    else:
        GRPName         = cmds.createNode('transform', n=GRPName)
    if(Parent != None):
        cmds.parent(ParentGRPName,Parent)
    #cmds.setAttr(GRPName + ".rotate",0,0,0)
    cmds.matchTransform(ParentGRPName,PositionMatch)
    if(Children != None):
        cmds.parent(Children,GRPName)   
    return [GRPName,ParentGRPName]
    
def Foot_Direction(Dir,start,End):

    #then set the direction of the Reverse foot setup.
    XYZOrder            = ["X","Y","Z"]
    XYZOrder_ZDir = ["X","Y","Z"]
    XYZOrder_XDir = ["Z","Y","X"]
    if (Dir == 2):
        XYZOrder = XYZOrder_ZDir
    if (Dir == 0):
        XYZOrder = XYZOrder_XDir
    MASTER.PrintCheck(["Return",XYZOrder],Rigging_IK_ONOFF,"")
    return XYZOrder

                
    
def Proxy_ReverseFoot(Side,LimbType,JointChain,IkChain,MainIK_Handle,HeelPeel_GRP,Tap_GRP,PV_CTRL):
    Proxy           = "Proxy_"
    Offset          = "Offset_"
    ProxyJntChain   = []
    Prefix          = Side + "_" + LimbType
    ParentNode      = Prefix + "_" + Proxy  + "GRP"
    TempGRP         = Prefix + "_" + Proxy  + "Temp"
    NewJointChain   = []
    for Jnt in JointChain:
        if(cmds.objExists(Jnt)):
            NewJointChain.append(Jnt)
            ProxyJntChain.append(Proxy + Jnt)
    
    cmds.createNode('transform', n=ParentNode)
    cmds.createNode('transform', n=TempGRP,p=ParentNode)
    #check angle of Ankle/Wrist
    #by creating locators/constraints to get angle
    locators                = [Prefix + "_" + "ReverseFoot_BaseLoc",Prefix + "_" + "ReverseFoot_AngleLoc",Prefix + "_" + "ReverseFoot_AnkleLoc"]
    cmds.createNode('transform', n=locators[0],p=TempGRP)
    cmds.createNode('transform', n=locators[1],p=locators[0])
    cmds.createNode('transform', n=locators[2],p=locators[1])
    
    OffsetChain = []
    #print "start TEst...."
    for i in range(len(NewJointChain)-1,-1,-1):
        #print i
        Jnt = NewJointChain[i]
        if(cmds.objExists(Jnt)):
            OJnt = Offset + Jnt
            OffsetChain.append(OJnt)
            cmds.createNode('transform', n=OJnt)
            cmds.matchTransform(OJnt,Jnt)
            if (i <len(NewJointChain)-1):
                cmds.parent(OJnt,Offset + NewJointChain[i+1])
            else:
                cmds.parent(OJnt,TempGRP)
    
    cmds.matchTransform(locators[0],JointChain[4])
    AimCon      = cmds.aimConstraint(JointChain[3],locators[1],offset=(0,0,0),weight=1,aimVector=(1,0,0),upVector=(0,1,0),worldUpType="vector",worldUpVector=(0,1,0))
    #check direction of locators
    cmds.matchTransform(locators[2],JointChain[3])
    CheckDir = cmds.getAttr(JointChain[4] + "." + "translateX")
    #if(Side == "R"):
    
    #def commentout():  
    if(CheckDir>0):
        TempNum = cmds.getAttr(locators[0] + "." + "rotateY")
        cmds.setAttr(locators[0] + "." + "rotateY", TempNum + 180)
    cmds.matchTransform(locators[2],JointChain[3])
    #check rotation value
    RotValue = cmds.getAttr(locators[1] + "." + "rotateZ")
    #make Adjustment to 45 degrees
    if (abs(RotValue) <45):
        Mult = -1
        cmds.delete(AimCon)
        if (RotValue > 0):
            Mult = 1
        cmds.setAttr(locators[1] + "." + "rotateZ", 45 * Mult)
        
        #set Offset to new position.
        cmds.matchTransform(OffsetChain[2],locators[2],pos=True)
        cmds.parent(OffsetChain[3],w=True)
        cmds.matchTransform(OffsetChain[2],locators[2])
        cmds.parent(OffsetChain[3],OffsetChain[2])
            
        #Create Proxy_Chain. 
        for Jnt in NewJointChain:
            ProxyJnt    = Proxy  + Jnt
            OJnt            = Offset + Jnt
            if(cmds.objExists(OJnt)):
                cmds.joint(n=ProxyJnt)
                cmds.parent(ProxyJnt,OJnt)
                cmds.matchTransform(ProxyJnt,OJnt)
                cmds.setAttr(ProxyJnt + "." + "rotateX", 0)
                cmds.setAttr(ProxyJnt + "." + "rotateY", 0)
                cmds.setAttr(ProxyJnt + "." + "rotateZ", 0)
                cmds.setAttr(ProxyJnt + "." + "jointOrientX", 0)
                cmds.setAttr(ProxyJnt + "." + "jointOrientY", 0)
                cmds.setAttr(ProxyJnt + "." + "jointOrientZ", 0)
                cmds.parent(ProxyJnt,w=True)
        for i in range(len(NewJointChain)):
            Jnt = NewJointChain[i]
            ProxyJnt    = Proxy  + Jnt
            if(Jnt != NewJointChain[0]):
                PJnt = Proxy + NewJointChain[i-1]
                cmds.parent(ProxyJnt,PJnt)
            else:
                cmds.parent(ProxyJnt,ParentNode)
    #print "ProxyJntChain"
    #print ProxyJntChain
    ProxyIKHandle = Proxy + MainIK_Handle
    if (cmds.objExists(ProxyJntChain[0])):
        #print "In.... "
        #create Proxy IKHandles...
        #main (ankle/leg)  Proxy IK Handle
        IK_Handle_Create(ProxyJntChain[0],ProxyJntChain[2],ProxyIKHandle,"ikRPsolver")
        cmds.parent(Proxy + MainIK_Handle,HeelPeel_GRP)
        IK_Handle_Create(ProxyJntChain[2],ProxyJntChain[3],Proxy + IkChain[3],"ikRPsolver")
        #BAll Proxy IK Handle
        cmds.parent(Proxy + IkChain[3],Tap_GRP)
        #Change already parented IKHandles for Proxy to drive. 
        cmds.parentConstraint(ProxyJntChain[2],MainIK_Handle,mo=True,weight=1)
        #add PolevEctor
        cmds.poleVectorConstraint(PV_CTRL,Proxy + MainIK_Handle)
    
    cmds.delete(TempGRP)
    #hide GRP
    cmds.setAttr(ParentNode + "." + "v",0)
    #parent constraint Parent GRP to parent Joint
    #get parent Joint
    ParentJoint = cmds.listRelatives(JointChain[0],p=True)
    cmds.parentConstraint(ParentJoint,ParentNode,mo=True,weight=1)
    return [ParentNode,ProxyJntChain,ProxyIKHandle]

def ResetAttributes(Nodes,Attributes):
    #Zero out rotates of joints
    for Node in Nodes:
        for Attr in Attributes:
            for Axis in ["X","Y","Z"]:
                if cmds.objExists(Node):
                    cmds.setAttr(Node + "." + Attr + Axis, 0)
    
def CreateJNTChain(JointChain,NewJointChain,Parent):
    ShortList = []
    for i in range(len(JointChain)):
        Jnt     = JointChain[i]
        NewJnt  = NewJointChain[i]
        if(cmds.objExists(Jnt)):
            cmds.joint(n=NewJnt)
            cmds.parent(NewJnt,Jnt)
            cmds.matchTransform(NewJnt,Jnt)
            Axis = ["X","Y","Z"]
            Attr = ["jointOrient","rotate"]
            for At in Attr:
                for A in Axis:
                    cmds.setAttr(NewJnt + "." + At + A,0)
            if(i>0):
                if(cmds.objExists(NewJointChain[i-1])):
                    Parent = NewJointChain[i-1]
                else:
                    Parent = NewJointChain[i-2]
            #print "NewJnt ", NewJnt
            #print "Parent ", Parent
            cmds.parent(NewJnt,Parent)
    #Skeleton.ZeroRotations(1,ShortList)
    
                        
def IK_ReverseFoot_SetUp(Side,LimbType,ParentIK_GRPS,IK_CTRL,IncludeFK,CharType,RollFootFix,PVFlip):

    # CREATE THE IK HANDLES FOR REVERSE FOOT & IK limb
    #get Limb names
    Parent          = ParentIK_GRPS[0]
    SubParent       = ParentIK_GRPS[1]
    ExtraLimbAttr   = ExtraAttr()
    Limb            = ReverseFootLimbs(LimbType)
    NodeType        = NodeTypes()
    JointChain      = []
    IKJointChain    = []
    FKJointChain    = []
    IkChain         = []
    JointChainWA    = [] # Joint Chain for Wrist or Ankle
    IKChainWA       = [] # IK's for Wrist or Ankle
    WAJNT           = ""
    MainIK_JNT      = ""
    WAExists        = False
    WA_GRP          = Side + "_" + "WA" + "_" + LimbType + "_"                  + NodeType[5]
    LimbIKJNTGRP    = Side + "_" + "IK" + "_" + LimbType + "_" + NodeType[1]    + NodeType[5]
    
    #more naming convention setup
    for L in Limb:
        JointChain.append(      Side + "_"              + L + "_" + NodeType[1])
        IKJointChain.append(    Side + "_" + "IK" + "_" + L + "_" + NodeType[1])
        IkChain.append(         Side + "_"              + L + "_" + NodeType[2])
        JointChainWA.append(    Side + "_" + "WA" + "_" + L + "_" + NodeType[1])
        IKChainWA.append(       Side + "_" + "WA" + "_" + L + "_" + NodeType[2])
    
    #Create FK IK Chains and groups
    if(IncludeFK):
        cmds.createNode( 'transform', n=LimbIKJNTGRP,p=Parent)
        TempParent = cmds.listRelatives(JointChain[0],p=True)
        CreateJNTChain(JointChain,IKJointChain,TempParent)
        cmds.parentConstraint(TempParent,LimbIKJNTGRP)
        cmds.setAttr(LimbIKJNTGRP + "." + "v",0)
    else:
        IKJointChain = JointChain

    ##for simpler naming of actual IK chain...
    PrintNote = "Names set up for Joint Chains  & IK chains... "
    MASTER.PrintCheck([PrintNote,"JointChain : ",JointChain,"IKJointChain : ",IKJointChain,"FKJointChain : ",FKJointChain,"IkChain : ",IkChain,"JointChainWA : ",JointChainWA,"IKChainWA : ",IKChainWA],Rigging_IK_ONOFF,["*",""])
    
    MainIK_Handle   =   Side + "_"          + LimbType + "_" + NodeType[2]
    WAIK_Handle     = [ Side + "_" + "WA"   + LimbType + "_" + NodeType[2],IkChain[2]]
    
    #Reverse Foot grp names for the IK controllers
    Tap_GRP         = Side + "_" +  Limb[5] + "_"               + NodeType[1] + "_" + "IK" + "Tap"          + "_" + "GRP"
    HeelPeel_GRP    = Side + "_" +  Limb[3] + "_" + "IK" + "_"  + NodeType[3] + "_" + "IK" + "HeelPeel"     + "_" + "GRP"
    Pivot_GRP       = Side + "_" +  Limb[5] + "_"               + NodeType[1] + "_" + "IK" + "Pivot"        + "_" + "GRP"
    HeelPivot_GRP   = Side + "_" +  Limb[3] + "_"               + NodeType[3] + "_" + "IK" + "HeelPivot"    + "_" + "GRP"
    ReverseFoot_GRP = Side + "_" +  Limb[3] + "_"               + NodeType[3]                               + "_" + "GRP"
    
    #PolveVector setup
    PV          = Side + "_" + LimbType + "_" + "PV"
    PV_CTRL     = PV + "_" + NodeType[3]
    PV_GRP      = PV + "_" + NodeType[5]
    PV_SubGRP   = PV + "_" + NodeType[6]
    PVNodes     = [PV,PV_CTRL,PV_GRP,PV_SubGRP]
    # checking if Ankle or Wrist exists.. 
    if(cmds.objExists(IKJointChain[2])):
#       print "Ankle or Wrist Exists"
        MainIK_JNT  = IKJointChain[2]
        WAExists    = True
    else:
        MainIK_JNT = IKJointChain[3]
        

    #needed if the heel/ankle is less than 45% from ball. to create correct rotation when foot is peeling.
     

    MASTER.PrintCheck(["Main IK Leg Joint : ",MainIK_JNT])
    
    IK_Leg = IK_Handle_Create(IKJointChain[0],MainIK_JNT,MainIK_Handle,"ikRPsolver")
    
    #Zero out rotates of joints
    for Joint in IKJointChain:
        if (cmds.objExists(Joint)):
            for Attr in ["X","Y","Z"]:
                cmds.setAttr(Joint + ".rotate" + Attr, 0)
    cmds.setAttr(MainIK_Handle + ".stickiness",1)
    
    #Reverse Foot IK
    IK_Ball     = IK_Handle_Create(IKJointChain[3],IKJointChain[4],IkChain[4],"ikRPsolver")
    IK_ToeEnd   = IK_Handle_Create(IKJointChain[4],IKJointChain[5],IkChain[5],"ikRPsolver")
    
    

    IK_GRPS(            ReverseFoot_GRP  ,None           ,IKJointChain[3],None)
    #set rotation of the ReverseFoot to match rotation of current Leg.
    Temp = cmds.aimConstraint(IKJointChain[4],ReverseFoot_GRP,offset=(0,0,0),weight=1,aimVector=(0,0,1),upVector=(0,1,0),worldUpType="vector",worldUpVector=(0,1,0))
    cmds.delete(Temp)
    
    WaParent = IK_GRPS( HeelPivot_GRP   ,None           ,IKJointChain[3],ReverseFoot_GRP,True)
    IK_GRPS(            Pivot_GRP       ,None           ,IKJointChain[5],HeelPivot_GRP,True)
    IK_GRPS(            HeelPeel_GRP    ,MainIK_Handle  ,IKJointChain[4],Pivot_GRP)
    IK_GRPS(            Tap_GRP         ,IkChain[4]     ,IKJointChain[4],Pivot_GRP)#IkChain[5])
    cmds.parent(IkChain[5],Tap_GRP)
    
    #Hiding " + "GRP"  + " sot Ik Handles dont show up
    cmds.setAttr(HeelPivot_GRP + ".v", 0)
    
    # ATTACH LIMB CONTROLLER
    
    cmds.select(IK_CTRL,r=True)
    cmds.setAttr(MainIK_Handle + ".poleVector", 0,0,0)
    
    
    # SET DRIVEN KEY FOR REVERSE FOOT
    # 1st find out direction of lim so that controllers are connected in the correct direction.
    Dir                     = JointDirection(IKJointChain[3] ,IKJointChain[5])
    AxisOrder               = ['Z', 'Y', 'X']#Foot_Direction(int(Dir[0]),IKJointChain[3] ,IKJointChain[5])
    AttrXYZ                 = ["HeelPeel","Pivot","Tap"]
    B                       = 0
    ReversefootRotatePoints = [IK_CTRL,JointChain[5],JointChain[5]]
    ExAttr                  = ExtraAttr()
    MASTER.PrintCheck(["Dir",Dir,"AxisOrder",AxisOrder,"AttrXYZ",AttrXYZ,"B",B,"ReversefootRotatePoints",ReversefootRotatePoints,"ExAttr",ExAttr],Rigging_IK_ONOFF,["*",""])
    
    # create UtilityNOdes and connect CTRL Attr to UtilityNodes.
    #May need to do a little cleaning... here.  
    for A in range(len(AttrXYZ)):
        #Create Multiply Node
        MutlDivAttr = ("IK_Reverse" + Limb[3] + "_" + Side + "_" + ExAttr[A] + "_" + "multiply")
        if (cmds.objExists(MutlDivAttr)):
            cmds.delete(MutlDivAttr)
        MultDivdAttr = cmds.shadingNode("multiplyDivide",n=MutlDivAttr,asUtility=True)
        cmds.setAttr(MultDivdAttr + ".operation", 1)
        #connect CTRL Attr to Utility Nodes.
        for ELA in range(3):
            if B < len(ExAttr):
                if (cmds.objExists(IK_CTRL + "." + ExAttr[B])):
                    MASTER.PrintCheck(["Shading Nodes connecting to CTRL",(IK_CTRL + "." + ExAttr[B]),(MultDivdAttr + ".input1" + AxisOrder[ELA])],Rigging_IK_ONOFF,"")
                    cmds.connectAttr((IK_CTRL + "." + ExAttr[B]),(MultDivdAttr + ".input1" + AxisOrder[ELA]),force=True)
                else:
                    MASTER.PrintCheck((IK_CTRL + "." + ExAttr[B]) + "Does NOt EXIST",Rigging_IK_ONOFF,"")
            B = B +1
        #connect Utility Nodes to GRP driving Reverse Foot
        cmds.setAttr(MultDivdAttr + ".input2" + AxisOrder[0],int(Dir[0]))
        cmds.setAttr(MultDivdAttr + ".input2" + AxisOrder[1], 1)
        cmds.setAttr(MultDivdAttr + ".input2" + AxisOrder[2],int(Dir[0]))
        cmds.connectAttr((MultDivdAttr + ".output"),(ReversefootRotatePoints[A] + "_" + "IK" + AttrXYZ[A] + "_" + "GRP" + ".rotate"),f=True)
    
    
    IKCTRL_RotValue = cmds.getAttr(ReverseFoot_GRP + ".rotateY")

    if(LimbType == "Leg" or CharType == 2): 
        cmds.setAttr(IK_CTRL + ".translateY",0)
    cmds.makeIdentity(IK_CTRL,apply=True,t=1,r=1,s=1,n=0)
    LimbParent = cmds.listRelatives(IKJointChain[0], p=True )
    IK_ParentSwitcher(Side + "_" + "IK" + "_" + LimbType,IK_CTRL,ParentIK_GRPS[0],ParentIK_GRPS[1],LimbParent[0],IK_CTRL,False)
    
    cmds.parent(IK_CTRL,SubParent)
    

    
    cmds.makeIdentity(IK_CTRL,apply=True,t=1,r=1,s=1,n=0)
    cmds.setAttr(IK_CTRL + ".rotateY",IKCTRL_RotValue)
    if (85<= abs(IKCTRL_RotValue) <= 95) or (265<= abs(IKCTRL_RotValue) <= 275):
        cmds.makeIdentity(IK_CTRL,apply=True,t=1,r=1,s=1,n=0)
    #print "ReverseFoot_GRP : ",ReverseFoot_GRP
    #print IKCTRL_RotValue
    #if(Side == "R"):
    #                cmds.select("kdkdkd")
    #save rotate value for future use. 
    Rigging.Create_Attribute(IK_CTRL,"RotYOffset",AttributeInfo=["double",IKCTRL_RotValue,IKCTRL_RotValue,IKCTRL_RotValue])
    cmds.setAttr(IK_CTRL + "." + "RotYOffset",cb=True,keyable=False,lock=True)
    
    cmds.parentConstraint(IK_CTRL,ReverseFoot_GRP,mo=True,weight=1)
    
    IK_WA = ""
    if(cmds.objExists(IKJointChain[2])):
        IK_WA = IK_Ankle(Side,LimbType,IK_CTRL,IKJointChain,JointChainWA,WA_GRP,WAIK_Handle,WaParent,MainIK_Handle,HeelPeel_GRP,Parent)

    
    
    #re parent IK Chain joint to a seperate node also connect top joint to the body chain through constraints
    if(IncludeFK):
        cmds.parent(IKJointChain[0],LimbIKJNTGRP)
        
    PV_CTRL = PoleVector_SetUp(PVNodes,Side,LimbType,IK_CTRL,MainIK_Handle,IKJointChain,Parent,ReverseFoot_GRP,CharType,PVFlip)

    if(cmds.objExists(IKJointChain[2])):
        #print "skip"
        IKAnklePV_Create(IK_CTRL,WAIK_Handle,IK_WA,JointChainWA,Parent,PV_CTRL)
        IKHandlesList = [WAIK_Handle[0],IK_WA[0]]
    
    #creating proxy legs for better rolling if angle between ankle and foot less then 45%
    ProxyJnts = None
    ProxyIKHandle = None
    if(RollFootFix):
        ProxyInfo = Proxy_ReverseFoot(Side,LimbType,IKJointChain,IkChain,MainIK_Handle,HeelPeel_GRP,Tap_GRP,PV_CTRL)
        #print "ProxyInfo : ", ProxyInfo
        ProxyParent = ProxyInfo[0]
        ProxyJnts   = ProxyInfo[1]
        ProxyIKHandle = ProxyInfo[2]
        cmds.parent(ProxyParent,Parent)
        
    #create IK for AnkleJoint
    #Create Node for rotate Values of Anlke
    MASTER.PrintCheck(["PV_CTRL : ",PV_CTRL,"ReverseFoot_GRP : ",ReverseFoot_GRP,"Parent :",Parent])
    cmds.parent(ReverseFoot_GRP,Parent)
    
        
    DrivenNodes = [[IK_Leg[0],"ikBlend"],[IK_Ball[0],"ikBlend"],[IK_ToeEnd[0],"ikBlend"]]
    
    #**************************                         CleanUP                         **********************************
    #************************   Lock and Hide unused Attributes ********************************    
    #cmds.setAttr(IK_CTRL + ".rotate",l=False,k=True)
    Axis    = ["X","Y","Z"]
    Set     = [True,False,False]
    HideAttr(IK_CTRL          ,"scale"            ,Axis   ,Set[0],Set[1],Set[2])
    HideAttr([PV_CTRL]         ,["scale","rotate"] ,Axis   ,Set[0],Set[1],Set[2])
    HideAttr([PV_CTRL,IK_CTRL],"v"                ,""     ,Set[0],Set[1],Set[2])
    #************************  End Lock and Hide unused Attributes ********************************     
    ExtendJoints = [[IKJointChain[1],Limb[0]],[IKJointChain[3],Limb[1]]]
    MASTER.PrintCheck(["ExtendJoints :",ExtendJoints,"---------"])

    #ExtendLimb_Data = ExtendLimb(Side,IK_CTRL,ExtendJoints)
    Jnts_Distance   = [IKJointChain[0],IKJointChain[3]]
    
    ScaleJoints     = [[IKJointChain[0],Limb[0]],[IKJointChain[1],Limb[3]]]
    IKHandle = IK_Leg[0]
    if (ProxyJnts != None):
        IKHandle = ProxyIKHandle
        Jnts_Distance   = [ProxyJnts[0],ProxyJnts[3]]
    #StretchyLimb(Side,LimbType,IK_CTRL,StrechyJoints,Parent,ExtendLimb_Data,ScaleJoints)
    StretchyLimb(Side,LimbType,IK_CTRL,Jnts_Distance,Parent,ScaleJoints,IKJointChain,ProxyJnts,IKHandle)

    #Cleanup for IK Handles
    IKHandlesList = [MainIK_Handle,IK_Ball[0],IK_ToeEnd[0],IK_Leg[0]]
    return [DrivenNodes,IKHandlesList]

def IK_WALeg_Create(WA_GRP,JointChainWA,JointChain):
    cmds.createNode( 'transform', n=WA_GRP)
    MASTER.PrintCheck(["JNTs in range : "])
    for JNT in range(4):
        MASTER.PrintCheck([JNT])
        cmds.joint(n=JointChainWA[JNT])
        cmds.parent(JointChainWA[JNT],JointChain[JNT])
        ResetAttributes([JointChainWA[JNT]],["translate","rotate","jointOrient"])
    for JNT in range(3,-1,-1):
        if (JNT == 0):
            cmds.parent(JointChainWA[JNT],WA_GRP)
        else:
            cmds.parent(JointChainWA[JNT],JointChainWA[JNT-1])

def IK_Ankle(Side,LimbType,IK_CTRL,JointChain,JointChainWA,WA_GRP,WAIK_Handle,WaParent,MainIK_Handle,HeelPeel_GRP,Parent):
    
    NodeType        = NodeTypes()
    IK_WALeg_Create(WA_GRP,JointChainWA,JointChain)
    IK_WAFullLeg    = IK_Handle_Create(JointChainWA[0],JointChainWA[3],WAIK_Handle[0],"ikRPsolver")
    IK_WA           = IK_Handle_Create(JointChain[2]    ,JointChain[3]  ,WAIK_Handle[1],"ikSCsolver")
    
    
    #create Nodes for
    WALegIKHandle_GRP   = cmds.createNode( 'transform', n= Side + "_WA" + LimbType + "_IKHandle"  + NodeType[5])#,p=WaParent[1]
    WALegIKHandle_GRP2  = cmds.createNode( 'transform', n= Side + "_WA" + LimbType + "_IKHandle2" + NodeType[5],p=WALegIKHandle_GRP)#,p=WaParent[1]
    cmds.matchTransform(WALegIKHandle_GRP,WaParent[1])
    
    cmds.parent(IK_WA[0],JointChainWA[3])
    #WALegIKHandle_GRP  = cmds.createNode( 'transform', n="L_WALeg_IKHandle" + NodeType[5])#,p=WaParent[1]
    #cmds.matchTransform(WALegIKHandle_GRP,WaParent[1])
    
    # Parent constrain WaLeg_IKHandleGRP to WAFoot_JNT
    cmds.parentConstraint(JointChainWA[3],WALegIKHandle_GRP,mo=True,weight=1)
    #Parent MainIK_Handle to WAlEG_IKHandleGRP
    cmds.parent(MainIK_Handle,WALegIKHandle_GRP2)
    #parent WA IKHandle to Reversefoot Node End. (L_Foot_IKCTRL_IKHeelPeel_GRP)
    cmds.parent(IK_WAFullLeg[0],HeelPeel_GRP)#move WaLeg IK handle to ReverseFoot GRP
    
    #Point constraint WA+_GRP to follow main Joint chain. Leg
    cmds.pointConstraint(JointChain[0],JointChainWA[0],weight=1)
    
    #Add Attributes
    AddAttr_SetUp(IK_CTRL,["AnkleFlex","AnkleFlex2","AnkleFlex3"])
    cmds.connectAttr(IK_CTRL + "." + "AnkleFlex", WALegIKHandle_GRP2 + "." + "rz",f=True)
    cmds.connectAttr(IK_CTRL + "." + "AnkleFlex2", WALegIKHandle_GRP2 + "." + "ry",f=True)
    cmds.connectAttr(IK_CTRL + "." + "AnkleFlex3", WALegIKHandle_GRP2 + "." + "rx",f=True)
    
    
    #Clean up
    cmds.parent(WALegIKHandle_GRP,Parent)
    cmds.setAttr(WALegIKHandle_GRP + ".v", 0)
    cmds.parent(WA_GRP,Parent)
    cmds.setAttr(WA_GRP + ".v", 0)
    IKHandle_Lock([IK_WAFullLeg[0]])
    
    return IK_WA
    
def IKAnklePV_Create(IK_CTRL,WAIK_Handle,IK_WA,JointChainWA,Parent,PV_CTRL):
    # --- Create IK Ankle PV control setup... 
    IKAnklePV       = WAIK_Handle[1].replace(NodeTypes()[2],"PV")
    IKAnklePVGRP    = IKAnklePV + "_" + NodeTypes()[5]
    IKAnklePVSubGRP = IKAnklePV + "_" + NodeTypes()[6]
    IKAnklePVGRPOri = IKAnklePV + "_" + NodeTypes()[5] + "Orient"
    IKAnklePVCTRL   = IKAnklePV + "_" + NodeTypes()[3]
    IKAnklePVLocGRP = IKAnklePV + "_" + NodeTypes()[4] + NodeTypes()[5]
    IKAnklePVLoc1   = IKAnklePV + "_" + NodeTypes()[4] + "PV"
    IKAnklePVLoc2   = IKAnklePV + "_" + NodeTypes()[4] + "None"
    
    #create a node to drive the Ankle rotation to match Leg pole vector
    cmds.createNode( 'transform', n=IKAnklePVGRP,p=JointChainWA[2])
#   cmds.createNode( 'transform', n=IKAnklePVSubGRP,p=IKAnklePVGRP )
#   Curves.Ctrl_Curve_Create(IKAnklePVCTRL,"Circle",1,"x")
#   cmds.parent(IKAnklePVCTRL,IKAnklePVSubGRP)
    cmds.createNode( 'transform', n=IKAnklePVGRPOri,p=IKAnklePVGRP )
    cmds.matchTransform(IKAnklePVGRP,JointChainWA[3],pos=True)
    cmds.matchTransform(IKAnklePVGRP,JointChainWA[2],rot=True)
    # lock down the GRP to the leg. 
#   cmds.parentConstraint(JointChainWA[2],IKAnklePVGRP,mo=True,weight=1)

    AimCon = cmds.aimConstraint(PV_CTRL,IKAnklePVGRP,mo=True,weight=1)
    #print "Aim Con : ", AimCon[0]
    Rigging.Create_Attribute(IK_CTRL,"AnklePVSwitch")
    Rigging.SetDriven_AttributesSetup(IK_CTRL,"AnklePVSwitch",AimCon[0],PV_CTRL + "W0",[[0,0],[1,1]],0)
#   MASTER.BreakCode(ScriptLocation)
    cmds.matchTransform(IKAnklePVGRPOri,JointChainWA[3],rot=True)
#   cmds.parent(IKAnklePVGRP,JointChainWA[2])   
    
#   cmds.parentConstraint(IKAnklePVCTRL,IKAnklePVGRPOri,mo=True,weight=1)
    cmds.orientConstraint(IKAnklePVGRPOri,JointChainWA[3],weight=1)
    # parent to group node  
#   cmds.parent(IK_WA[0],JointChainWA[3])
    # --- Create IK Ankle PV control setup...   
    
#   MASTER.BreakCode(ScriptLocation)
#   return IKAnklePVGRP
        
    
    
def HideAttr(CTRLS,AttrPrefix,AttrSuffix,Lock,Keyable,ChannelBox):

    CTRLS       = MASTER.StringToList(CTRLS)
    AttrPrefix  = MASTER.StringToList(AttrPrefix)
    AttrSuffix  = MASTER.StringToList(AttrSuffix)
    #print "CTRLS : ",CTRLS
    #print "Pre   : ",AttrPrefix
    #print "Suff  : ",AttrSuffix
    for CTRL in CTRLS:
        for AP in AttrPrefix:
            for AS in AttrSuffix:
                #print "CTRL : ",CTRL
                #print "AP   : ",AP
                #print "AS   : ",AS
                
                cmds.setAttr(CTRL + "." + AP + AS ,l=Lock   ,k=Keyable,cb=ChannelBox)

def PoleVector_SetUp(PVNodes,Side,LimbType,IK_CTRL,MainIK_Handle,JointChain,Parent,ReverseFoot_GRP,CharType,PVFlip):
    
    PV          = PVNodes[0]
    PV_CTRL     = PVNodes[1]
    PV_GRP      = PVNodes[2]
    PV_SubGRP   = PVNodes[3]
    
    #Create PoleVector CTRL
    #TempNodes = Curves.Ctrl_Curve_ShapeNodeBackUp(PV_CTRL,"Pyramid",1,"",PV_SubGRP,PV_GRP)
    #OLD_CTRL   = TempNodes[0]
    #OLD                = TempNodes[1]
    
    Curves.Ctrl_Curve_Create(PV_CTRL,"Pyramid",1,"")
    #Create PoleVector GRP node
    cmds.createNode( 'transform', n=PV_GRP)
    cmds.createNode( 'transform', n=PV_SubGRP,p=PV_GRP)
    
    #Position PoleVector Ctrl
    cmds.parent(PV_CTRL,JointChain[0])
    cmds.setAttr(PV_CTRL + ".translate",0,0,0)
    cmds.setAttr(PV_CTRL + ".scale",0.2,0.2,0.2)
    #get distance of knee from the root of leg
    TempValue = cmds.getAttr(JointChain[1] + ".translateX")
    
    #cmds.setAttr(PV_CTRL + ".translateX",TempValue*5)
    
    #get knee bend direction or direction the Polvector should be placed
    #to stay in line  with the plane of the leg. 
    YValue = 1
    if (PVFlip):
        YValue = -1
    if(CharType == 2):
        if(LimbType == "Arm"):
            YValue = YValue * -1
    cmds.setAttr(PV_CTRL + ".translateX",TempValue)
    cmds.setAttr(PV_CTRL + ".translateY",YValue*((TempValue*5)))
    cmds.parent(PV_CTRL,ReverseFoot_GRP)
    TempValue = cmds.xform(JointChain[1],q=True,ws=True,t=True)
    
    #cmds.Select ("kdfjdkfjd")
    

    #TEMP_LOC_GRP = cmds.createNode( 'transform', n="TEMP_" + "LOC" + "GRP")# making temp GRP for locators

    Switch_GRP = IK_ParentSwitcher(PV,PV_CTRL,PV_GRP,PV_SubGRP,IK_CTRL,PV_CTRL,False)
    MASTER.PrintCheck(["Parent : ",Parent,"Switch_GRP",Switch_GRP])
    cmds.parent(PV_CTRL,PV_SubGRP)
    cmds.makeIdentity(PV_CTRL,apply=True,t=1,r=1,s=1,n=0)
    # Constrain the elbow IKHandle to the controller
    
    cmds.poleVectorConstraint(PV_CTRL,MainIK_Handle)
    
    cmds.parent(PV_GRP,Parent)
    
    #Curves.Ctrl_Curve_ReplaceShapeNode(PV_CTRL,OLD_CTRL,OLD)
    
    return PV_CTRL
    
def CommentingOUT_PoleVector_SetUp():
    #Creating Locators for Switching between World and Foot influences. 
    PV_LOC          = PV + "_" + NodeType[4]
    SwitchAttr  = ["Foot","World"]
    PV_Orient   = [PV_LOC + "_" + SwitchAttr[0] + "Target",PV_LOC + "_" + SwitchAttr[1] + "Target"]
    
    
    TempList = [PV_GRP]
    for PV_O in PV_Orient:
        TempList.append(PV_O)           
        cmds.spaceLocator(n=PV_O,p=(0,0,0) )
        cmds.setAttr((PV_O + ".v"),0,k=0)
    
    #cmds.parent(PV_Orient,TEMP_LOC_GRP)#grouping Locators temporarilly for moving. 
    
    
    cmds.parent(TempList, IK_CTRL)
    for Item in TempList:
        cmds.setAttr(Item + ".rotate",0,0,0)
    cmds.parent(PV_CTRL,PV_GRP)
    cmds.setAttr(PV_CTRL + ".rotate",0,0,0)
    #cmds.setAttr(PV_CTRL + ".translateY",TempValue[1])
    cmds.makeIdentity(TempList,apply=True,t=1,r=1,s=1,n=0)
    # Constrain the elbow IKHandle to the controller
    cmds.poleVectorConstraint(PV_CTRL,MainIK_Handle)
    # Parent the controller to the IK Foot Controller

    # create a switch to switch between Free world and foot location.
    #adding Attribute to The IK Controller to switch

    SwtichGRP = SwitchControl(PV_CTRL,IK_CTRL,PV_Orient[0],PV_Orient[1],PV_GRP,SwitchAttr)

    cmds.parent(PV_GRP,PV_GRP)
    
    return PV_CTRL

def SwitchControl(PV_CTRL,IK_CTRL,Target1,Target2,PV_GRP,SwitchAttr):
    PV_Attr = "PV_" + "Switch"
    
    #Rigging.Create_Attribute(CTRL,OrientAtt    ,AttributeInfo=["enum",LocString])
    Rigging.Create_Attribute(PV_CTRL,PV_Attr    ,AttributeInfo=["enum",":".join(SwitchAttr)])
    #cmds.addAttr(PV_CTRL,ln=PV_Attr,k=1,at="double",dv=0,min=0,max=10)
    #cmds.setAttr(PV_CTRL + "." +  PV_Attr,e=True,keyable=True)
    #first parent Constrain the IK Controller " + $Type[3]  + " to the world.
    cmds.parentConstraint(IK_CTRL,Target1,mo=True,weight=1)
    cmds.parentConstraint("CHAR_CTRL",Target2,mo=True,weight=1)
    Temp1 = cmds.parentConstraint(Target1,PV_GRP)
    Temp2 = cmds.parentConstraint(Target2,PV_GRP)
    Rigging.SetDriven_AttributesSetup(PV_CTRL,PV_Attr,Temp1[0],Target1 + "W0",[[0,1],[1,0]],0)
    Rigging.SetDriven_AttributesSetup(PV_CTRL,PV_Attr,Temp2[0],Target2 + "W1",[[0,0],[1,1]],0)  
    
def StrechLegJNTS(ExtendJoints):
    StrechJNTS = []
    for EJ in ExtendJoints:
        StrechJNTS.append()

def GetLimbLength(LimbList):
    LimbLength = 0
    for JNT in LimbList:
        LimbLength = LimbLength + (cmds.getAttr(JNT + ".translateX"))
    return LimbLength
    
    
def ExtendLimb(Side,CTRL,ExtendJoints):

    ExtendLimb_UtilSum  = []
    #attribute to define what this is.... 
    Rigging.Create_Attribute(CTRL,"Limb",AttributeInfo=["enum","Extend"])
    OriginLengthAttr    = []
    for JNT in ExtendJoints:
        Node            = JNT[0]
        ExtLimb_Attr    = JNT[1]
        AttrOrig        = ExtLimb_Attr + "Orig"
        UtilNodeDiv     = "ExtendLimb_" + Side + "_" + ExtLimb_Attr + "Length_Divide"
        UtilNodeSum     = "ExtendLimb_" + Side + "_" + ExtLimb_Attr + "Length_Sum"
        OriginLengthAttr.append(AttrOrig)
        ExtendLimb_UtilSum.append(UtilNodeSum)
        #get joint length
        JNTLength   = cmds.getAttr(Node + ".translateX")
        PosNeg      = 1
        if(JNTLength< 0):
            PosNeg = -1
        #Save Joint length
        Rigging.Create_Attribute(CTRL,AttrOrig,AttributeInfo=["double",JNTLength,JNTLength,JNTLength],Keyable=False)
        cmds.setAttr(CTRL + "." + AttrOrig,JNTLength)
        cmds.setAttr(CTRL + "." + AttrOrig,l=True)
        cmds.setAttr(CTRL + "." + AttrOrig,cb=False)
        #create Joint length drivers
        Rigging.Create_Attribute(CTRL,ExtLimb_Attr,AttributeInfo=["double",0],Keyable=True)
        #create utility node to add values. 
        if(cmds.objExists(UtilNodeDiv)):
            cmds.delete(UtilNodeDiv)
        if(cmds.objExists(UtilNodeSum)):
            cmds.delete(UtilNodeSum)
        cmds.shadingNode("multiplyDivide",name=UtilNodeDiv,asUtility=True)
        cmds.shadingNode("plusMinusAverage",name=UtilNodeSum,asUtility=True)
        cmds.connectAttr(CTRL + "." + ExtLimb_Attr      , UtilNodeDiv + "." + "input1X",f=True)
        cmds.setAttr(UtilNodeDiv + "." + "input2X",(100 * PosNeg))
        cmds.setAttr(UtilNodeDiv + "." + "operation",2)
        cmds.connectAttr(UtilNodeDiv + "." + "outputX"  , UtilNodeSum + "." + "input1D[0]",f=True)
        cmds.connectAttr(CTRL + "." + AttrOrig          , UtilNodeSum + "." + "input1D[1]",f=True)
        #make connect driver to Joint
        cmds.connectAttr(UtilNodeSum + "." + "output1D" ,Node + ".translateX",f=True)
        
        #cmds.setAttr(CTRL + "." + AttrOrig,lock=True,keyable=False,channelBox=False )
    
        
    return [OriginLengthAttr,ExtendLimb_UtilSum]


def DeleteIfExists(Node):
    if(cmds.objExists(Node)):
        cmds.delete(Node)
##--------------------------- Strech limb set up START -------------------------------------------
def StretchyLimb_DistanceNode(Side,LimbType,Parent,Jnts_Distance,IK_Handle):
    #Create Limb Measure Node
    #Create Distance Nodes to measure length of joing from Leg to ankle 
    StrechGRP   = "StrechyLimb_" + Side + "_" + LimbType + "_StrechGRP"
    StrechStart = "StrechyLimb_" + Side + "_" + LimbType + "_StrechStart"
    StrechEnd   = "StrechyLimb_" + Side + "_" + LimbType + "_StrechEnd"
    DeleteIfExists(StrechGRP)
    DeleteIfExists(StrechStart)
    DeleteIfExists(StrechEnd)
    cmds.createNode('transform', n=StrechGRP,parent=Parent)
    cmds.createNode('transform', n=StrechStart,parent=StrechGRP)
    cmds.createNode('transform', n=StrechEnd,parent=StrechGRP)
    # create constraints of Distance nodes
    cmds.pointConstraint(Jnts_Distance[0],StrechStart)
    #cmds.aimConstraint(IK_Handle,StrechStart,offset=(0,0,0),weight=1,aimVector=(1,0,0),upVector=(0,1,0),worldUpType="vector",worldUpVector=(0,1,0))
    cmds.pointConstraint(IK_Handle,StrechEnd)
    
    
    MeasureNode = Side + "_" + LimbType + "_" + "Distance"
    DeleteIfExists(MeasureNode)
    cmds.shadingNode("distanceBetween",n=MeasureNode,asUtility=True)
    
    #connect translate info for utility in disnataance node. 
    cmds.connectAttr(StrechStart    + "." + "translate", MeasureNode + "." + "point1",f=True)
    cmds.connectAttr(StrechEnd      + "." + "translate", MeasureNode + "." + "point2",f=True)

    return (StrechGRP,StrechStart,StrechEnd,MeasureNode)

def StrechyLimb_MultiplyPosNeg(Side,LimbType,MeasureNode,PosNeg):
    #add a multipliyer for postive and negative values on the distance..
    #get distance of Joint Positive or negative... 
    MultiplyPosNeg = "StrechyLimb_" + Side + "_" + LimbType + "_" + "MultiplyPosNeg"
    DeleteIfExists(MultiplyPosNeg)
    cmds.shadingNode("multiplyDivide",name=MultiplyPosNeg,asUtility=True)
    cmds.connectAttr(MeasureNode      + "." + "distance", MultiplyPosNeg + "." + "input1X",f=True)
    #cmds.connectAttr(StrechEnd + "." + "translateX", ScaleAmount + "." + "input1X",f=True)
    #cmds.connectAttr(LegLength + "." + "output1D", ScaleAmount + "." + "input2X",f=True)
    cmds.setAttr(MultiplyPosNeg + "." + "input2X",PosNeg)
    cmds.setAttr(MultiplyPosNeg + "." + "operation",1)

    return MultiplyPosNeg

def StrechyLimb_ScaleAmount(Side,LimbType,MultiplyPosNeg,LimbLength,CTRL):
    #scale amount - Measure amount of Scale % that should happen.. 
    ScaleAmount = "StrechyLimb_" + Side + "_" + LimbType + "_" + "Scale"
    DeleteIfExists(ScaleAmount)
    cmds.shadingNode("multiplyDivide",name=ScaleAmount,asUtility=True)
    cmds.connectAttr(MultiplyPosNeg      + "." + "outputX", ScaleAmount + "." + "input1X",f=True)
    #cmds.connectAttr(StrechEnd + "." + "translateX", ScaleAmount + "." + "input1X",f=True)
    #cmds.connectAttr(LegLength + "." + "output1D", ScaleAmount + "." + "input2X",f=True)
    cmds.setAttr(ScaleAmount + "." + "input2X",LimbLength)
    cmds.setAttr(ScaleAmount + "." + "operation",2)

    ##visual only.. 
    ##Rigging.Create_Attribute(CTRL,"StrechtSize")
    ##cmds.connectAttr(ScaleAmount      + "." + "outputX", CTRL + "." + "StrechtSize",f=True)


    return ScaleAmount

def StechyLimb_StretchOffset(CTRL,Side,LimbType,IfOperation,ScaleAmount):
    #create Stretch switch AttributeInfo to turn switch on off.. 
    StretchOffsetAttr = "Amount"
    Rigging.Create_Attribute(CTRL,StretchOffsetAttr,["double",0])
    #Create Stretch switch addition. node... to turn switch on off..
    StretchOffsetControl = "StrechyLimb_" + Side + "_" + LimbType + "_" + "_StrechOffset1"
    DeleteIfExists(StretchOffsetControl)
    cmds.shadingNode("multiplyDivide",name=StretchOffsetControl,asUtility=True)
    cmds.connectAttr(CTRL + "."  + StretchOffsetAttr   , StretchOffsetControl + "." + "input1X",f=True)
    #cmds.connectAttr(StrechEnd + "." + "translateX", ScaleAmount + "." + "input1X",f=True)
    #cmds.connectAttr(LegLength + "." + "output1D", ScaleAmount + "." + "input2X",f=True)
    cmds.setAttr(StretchOffsetControl + "." + "input2X",0.01)
    cmds.setAttr(StretchOffsetControl + "." + "operation",1)

    StretchOffsetControl2 = "StrechyLimb_" + Side + "_" + LimbType + "_" + "_StrechOffset2"
    cmds.shadingNode("plusMinusAverage",name=StretchOffsetControl2,asUtility=True)
    cmds.connectAttr(ScaleAmount            + "." + "outputX"  , StretchOffsetControl2 + "." + "input1D[0]",f=True)
    cmds.connectAttr(StretchOffsetControl   + "." + "outputX"  , StretchOffsetControl2 + "." + "input1D[1]",f=True)
    cmds.setAttr(StretchOffsetControl2 + "." + "operation",1)
    ##visual only.. 
    ##Rigging.Create_Attribute(CTRL,"StretchOffset")
    ##cmds.connectAttr(StretchOffsetControl2      + "." + "output1D", CTRL + "." + "StretchOffset",f=True) 

    
    return StretchOffsetControl2

def StrechyLimb_StretchIf(Side,LimbType,MultiplyPosNeg,LimbLength,IfOperation,StretchOffset):
    #create condition to strectch if Strech end is larger than the original leg length. 
    StretchIf = "StrechyLimb_" + Side + "_" + LimbType + "_" + "StrechIf"
    DeleteIfExists(StretchIf)
    cmds.shadingNode("condition",name=StretchIf,asUtility=True)
    cmds.connectAttr(MultiplyPosNeg      + "." + "outputX", StretchIf + "." + "firstTerm",f=True)
    cmds.setAttr(StretchIf + "." + "secondTerm",LimbLength)
    #cmds.connectAttr(LegLength + "." + "output1D", StretchIf + "." + "secondTerm",f=True)
    cmds.setAttr(StretchIf + "." + "operation",IfOperation)
    cmds.connectAttr(StretchOffset + "." + "output1D", StretchIf + "." + "colorIfTrueR",f=True)
    cmds.setAttr(StretchIf + "." + "colorIfFalseR",1)

    return StretchIf
    
def StechyLimb_StretchControl(CTRL,Side,LimbType,IfOperation,StretchIf):
    #create Stretch switch AttributeInfo to turn switch on off.. 
    StretchControlAttr = "Stretch"
    Rigging.Create_Attribute(CTRL,StretchControlAttr)
    #Create Stretch switch conditional node... to turn switch on off..
    StretchControl = "StrechyLimb_" + Side + "_" + LimbType + "_" + "_StrechSwitch"
    DeleteIfExists(StretchControl)
    cmds.shadingNode("condition",name=StretchControl,asUtility=True)
    cmds.connectAttr(CTRL + "." + StretchControlAttr, StretchControl + "." + "firstTerm",f=True)
    cmds.setAttr(StretchControl + "." + "secondTerm",1)
    #cmds.connectAttr(LegLength + "." + "output1D", StretchIf + "." + "secondTerm",f=True)
    cmds.setAttr(StretchControl + "." + "operation",IfOperation)
    cmds.connectAttr(StretchIf + "." + "outColorR", StretchControl + "." + "colorIfTrueR",f=True)
    cmds.setAttr(StretchControl + "." + "colorIfFalseR",0)
    
    return StretchControl


    
#def StretchyLimb(Side,LimbType,CTRL,StrechyJoints,Parent,ExtendLimb_Data,ScaleJoints):
def StretchyLimb(Side,LimbType,CTRL,Jnts_Distance,Parent,ScaleJoints,IKJointChain,ProxyJnts,IK_Handle):

    #Get limb Length
    LimbLength = GetLimbLength([IKJointChain[1],IKJointChain[3]])
    #adjust for negative lengths. 
    IfOperation = 3
    PosNeg = 1
    if (LimbLength< 0 ):
        IfOperation = 5
        PosNeg = -1
    
    #create strechy node to measure distance from hip to ankle
    SL_DN           = StretchyLimb_DistanceNode(Side,LimbType,Parent,Jnts_Distance,IK_Handle)
    StrechGRP,StrechStart,StrechEnd,MeasureNode = SL_DN[0], SL_DN[1], SL_DN[2], SL_DN[3]
    #set multiplyer +/- 
    MultiplyPosNeg  = StrechyLimb_MultiplyPosNeg(Side,LimbType,MeasureNode,PosNeg)
    #scale amount - Measure amount of Scale % that should happen.. 
    ScaleAmount     = StrechyLimb_ScaleAmount(Side,LimbType,MultiplyPosNeg,LimbLength,CTRL)
    StretchOffset   = StechyLimb_StretchOffset(CTRL,Side,LimbType,IfOperation,ScaleAmount)
    #Auto stretch condition if longer than original
    StretchIf       = StrechyLimb_StretchIf(Side,LimbType,MultiplyPosNeg,LimbLength,IfOperation,StretchOffset)
    #create Stretch switch AttributeInfo to turn switch on off..
    StretchControl  = StechyLimb_StretchControl(CTRL,Side,LimbType,IfOperation,StretchIf)
    
    
    #connect scale values

    cmds.connectAttr( StretchControl + "." + "outColorR",ScaleJoints[0][0] + ".scaleX",f=True)
    cmds.connectAttr( StretchControl + "." + "outColorR",ScaleJoints[1][0] + ".scaleX",f=True)
    #connect proxy legs as well.. 
    
    if(ProxyJnts != None):
        cmds.connectAttr( StretchControl + "." + "outColorR",ProxyJnts[0] + ".scaleX",f=True)
        cmds.connectAttr( StretchControl + "." + "outColorR",ProxyJnts[1] + ".scaleX",f=True)
    #Parent on legGRP
    #L_Hand_IK_GRP



##--------------------------- Strech limb set up  END -------------------------------------------


def IK_CTRL_Create(LimbType,Side,IK_GRPS):
    LimbPivot       = Get_LimbPivot(LimbType)
    Limb            = ReverseFootLimbs(LimbType)
    NodeType        = NodeTypes()
    PositionMatch   = Side + "_" + Limb[3] + "_" + NodeType[1]
    PositionMatch2  = Side + "_" + LimbPivot + "_" + NodeType[1]
    GRP             = IK_GRPS[1]
    ParentGRP       = IK_GRPS[0]
    
    if (cmds.objExists(PositionMatch2)):
        PositionMatch = PositionMatch2
    IK_CTRL                 = Side + "_" + Limb[3] + "_" + "IK" + "_" + NodeType[3]
    
    #TempNodes = Curves.Ctrl_Curve_ShapeNodeBackUp(IK_CTRL,"Foot",1,"",GRP,ParentGRP)
    #OLD_CTRL   = TempNodes[0]
    #OLD                = TempNodes[1]
    
    Curves.Ctrl_Curve_Create(IK_CTRL,"Foot",1,"")
    cmds.matchTransform(IK_CTRL,PositionMatch,pos=True)
    
    return IK_CTRL

def IK_Switch_Create(Side,LimbType,LIMB_GRP,FKIK_GRPS,IKFKConGRP,DrivenNodes,DrivenCons):
    PrintNote = "IK_Switch_Create(Side,LimbType,LIMB_GRP,FKIK_GRPS,DrivenNodes,DrivenCons):"
    MASTER.PrintCheck([PrintNote,"Side : ",Side,"LimbType : ",LimbType,"LIMB_GRP : ",LIMB_GRP,"FKIK_GRPS : ",FKIK_GRPS,"DrivenNodes : ",DrivenNodes,"DrivenCons : ",DrivenCons],Rigging_IK_ONOFF,["*",""])
    SwitchCTRL  = Side + "_" + LimbType + "_" + "SwitchCTRL"
    Limbs       = ReverseFootLimbs(LimbType)
    NodeType    = NodeTypes()

    MASTER.PrintCheck(["Setting Attributes: ","SwitchCTRL :",SwitchCTRL,"Limbs : ",Limbs,"NodeType : ",NodeType],Rigging_IK_ONOFF,["",""])
    
    
    #Create Switch Ctrl
    Curves.Ctrl_Curve_Create(SwitchCTRL,"Arrow1",1,"")
    cmds.scale(0.2,0.2,0.2,SwitchCTRL)
    cmds.makeIdentity(SwitchCTRL,apply=True,t=1,r=1,s=1,n=0)
    cmds.move(0,0,0.5,(SwitchCTRL + ".scalePivot",SwitchCTRL + ".rotatePivot"))
    #cmds.makeIdentity(SwitchCTRL,apply=True,t=1,r=1,s=1,n=0)
    #Place Switch Ctrl
    PositionMatch   = Side + "_" + Limbs[3] + "_" + NodeType[1]
    cmds.matchTransform(SwitchCTRL,PositionMatch,pos=True)
    #GRP CTRL
    cmds.parent(SwitchCTRL,LIMB_GRP)
    SwitchCon = cmds.parentConstraint(Side + "_" + Limbs[3] + "_" + NodeType[1],SwitchCTRL,mo=True,weight=1)
    
    cmds.parent(SwitchCon[0],IKFKConGRP)
    #Lock location and remove Attributes
    AttrPrefix = ["translate","rotate","scale"]
    AttrSuffix = ["X","Y","Z"]
    HideAttr([SwitchCTRL],AttrPrefix,AttrSuffix,True,False,False)
    #Add Switch Attribute 
    cmds.addAttr(SwitchCTRL,ln="IKSwitch",k=1,at="enum",en="IK:FK:")
    #Make Switch Connections. 
    OnOff = [[0,1],[1,0]]
    
    for Driven in DrivenNodes:
        Rigging.SetDriven_AttributesSetup(SwitchCTRL,"IKSwitch",Driven[0],Driven[1],OnOff,0)
    # commenting out don't need to create set driven keys for the FK legs since they are seperate from the main limb chain.
    #for DC in DrivenCons:
    #   print DC
    #   print SwitchCTRL
    #   Rigging.SetDriven_AttributesSetup(SwitchCTRL,"IKSwitch",DC[0],DC[1],[[0,0],[1,1]],0)
    
    #Turn 
    
    Rigging.SetDriven_AttributesSetup(SwitchCTRL,"IKSwitch",FKIK_GRPS[0],"visibility",[[0,1]],0)    
    Rigging.SetDriven_AttributesSetup(SwitchCTRL,"IKSwitch",FKIK_GRPS[0],"visibility",[[1,0]],0) 
    #MASTER.BreakCode()       
    Rigging.SetDriven_AttributesSetup(SwitchCTRL,"IKSwitch",FKIK_GRPS[1],"visibility",[[0,0]],0)
    Rigging.SetDriven_AttributesSetup(SwitchCTRL,"IKSwitch",FKIK_GRPS[1],"visibility",[[1,1]],0)    
    
    
    #MASTER.PrintCheck("check 3",Rigging_IK_ONOFF,["*",""])
    return [SwitchCTRL,"IKSwitch"]

def IKFK_GRPS_Create(Limb,Side,LIMB_GRP):
    Prefix      = Side + "_" + Limb[3]
    IKFK_GRPS   = ["IK","FK"]
    Suffix      = ["GRP","SubGRP"]
    GRPNodes    = []
    
    #FKIK_GRPS = [Prefix  + "_" + IKFK[0] + "_" + Suffix[0],Prefix  + "_" +  IKFK[1] + "_" + Suffix[0]]
    for IKFK in IKFK_GRPS:
        for Suff in Suffix:
            GRP = Prefix  + "_" + IKFK + "_" + Suff
            Parent = Prefix  + "_" + IKFK + "_" + Suffix[0]
            GRPNodes.append(GRP)
            if(cmds.objExists(GRP)):
                cmds.delete(GRP)
            cmds.createNode('transform', n=GRP)
            if(Suffix[0] == Suff):
                cmds.parent(GRP,LIMB_GRP)
            if(Suffix[1] == Suff):
                cmds.parent(GRP,Parent)
                
    return GRPNodes

def FindJoint(Side,Joint):
    Suffix = NodeTypes()
    Joint_Name = Side + "_" + Joint
    for S in Suffix:
        if(cmds.objExists(Side + "_" + Joint + "_" + S)):
            Joint_Name = Side + "_" + Joint + "_" + S
    return Joint_Name
            
    
def IK_ParentSwitcher(Name,CTRL,ParentGRP,GRP,Parent,IK_CTRL,MatchJoint):
    MatchJoint = Name
    SwithGRP = Rigging.Set_ParentSwitcher(Name,CTRL,ParentGRP,GRP,Parent,IK_CTRL,MatchJoint)
    cmds.scaleConstraint(Parent, GRP,mo=True)
    Note = "Exiting..... IK_ParentSwitcher"
    MASTER.PrintCheck([Note,"returning... ",SwithGRP ],Rigging_IK_ONOFF,["*",""])
    return SwithGRP

def IK_KeepCurves(LimbType,DetachList = True):
    GRPS        = ["_GRP","_CTRL_GRP"]
    ShapeListGRP    = "_OldShapeList"
    List1           = []
    List2           = []
    
    if(DetachList):
        for GRP in GRPS:
            LIMB_GRP = LimbType.upper() + GRP
            
            #print "DetachList ... "
            if(cmds.objExists(LIMB_GRP)):
                #print "LIMB_GRP.... "
                ShapeListGRP = LimbType.upper() + ShapeListGRP + GRP
                List1 = Rigging.Preserve_CTRLShape(LIMB_GRP)
                if(not cmds.objExists(ShapeListGRP)):
                    cmds.createNode('transform', n=ShapeListGRP)
                else:
                    Parent = cmds.listRelatives(ShapeListGRP,p=True)
                    if(Parent[0] != None):
                        cmds.parent(ShapeListGRP,w=True)
                    List2 = cmds.listRelatives(ShapeListGRP,ad=True)
                    #print "List2", List2
                    if(List2 != None):
                        for L in List2:
                            List2.append()
                    else:
                        List2 = []
                for CTRL in List1:
                    cmds.parent(CTRL[1][0][2],ShapeListGRP)
                cmds.delete(LIMB_GRP)
            else:
                print "LIMB_GRP does not exits.. skipping. "
    CTRLShapeList = List1 + List2
    #check to see if the CTRLs have been detached to return new Shape nodes name..
    for GRP in GRPS:
        LIMB_GRP = LimbType.upper() + GRP
        Temp = LimbType.upper() + ShapeListGRP + GRP
        if(cmds.objExists(Temp)):
            ShapeListGRP = Temp
            
    return [ShapeListGRP,CTRLShapeList]
        
def IK_Setup(LimbType   = "Leg",CharType=1,IncludeFK=False,RollFootFix=False,ExtraParentSwitchLimbs=False,ZeroJoints=1,PVFlip=0):
    Limb        = ReverseFootLimbs(LimbType)
    Sides       = ["L","R"]
    LIMB_GRP    = LimbType.upper() + "_GRP"
    NodeType    = NodeTypes()
    ExAttr      = ExtraAttr() 
    
    PrintNote = "Setting up Attributes : "
    MASTER.PrintCheck([PrintNote,"Limb : ",Limb,"Sides : ",Sides,"LIMB_GRP : ",LIMB_GRP,"NodeType : ",NodeType,"ExAttr : ",ExAttr])
    
    #clean LIMB_GRP by removing CTRLS to preserve. and deleting the Limb NOde to start clean. 
    KeepCurvesInfo  = IK_KeepCurves(LimbType)
    ShapeListGRP    = KeepCurvesInfo[0]
    CTRLShapeList   = KeepCurvesInfo[1]
    #print ShapeListGRP
    #print CTRLShapeList
    
#   for CTRL in CTRLShapeList:
##      print "CTRLShape.."
#       for C in CTRL:
#           print C
        
    
    LIMB_GRP = cmds.createNode('transform', n=LIMB_GRP)
    cmds.parent(LIMB_GRP,"CTRLS_GRP")
    UnlockList = Sides
    #print UnlockList
    ProBarInfo = ["Rigging_" + LimbType + "_IK_Limbs",None]
    for Side in Sides:
        ProBarInfo = MASTER.ProgressBar_Run(WindowName= ProBarInfo[0],List = UnlockList,ProgressControl = ProBarInfo[1])
        # Attibute setup ofr different Joint chains
        IKFKConGRP      = Side + "_" + "IK" + "FK" + "_" + LimbType + "_" + NodeType[5]
        JointChain      = []
        IKJointChain    = []
        FKJointChain    = []

        for L in Limb:

            JointChain.append(  Side + "_"              + L + "_" + NodeType[1])
            IKJointChain.append(Side + "_" + "IK" + "_" + L + "_" + NodeType[1])
            FKJointChain.append(Side + "_" + "FK" + "_" + L + "_" + NodeType[1])
            
        if(ZeroJoints == 1):
#           print "ResetBack Joints to rotate 0 value"
            ResetAttributes(JointChain,["rotate"])
        if(ZeroJoints == 2):
#           print "zero Joints at current position keep orientation"
            Skeleton.ZeroRotations(True,JointChain)
        
        
        #print "LimbList : ", Limb
        #print "NodeTypeList : ",NodeType    
        #print "Side : ",Side
        #print "Limb : ",Limb[0]
        #print "NodeType : ", NodeType[1]
            
        if(cmds.objExists(Side + "_" + Limb[0] + "_" + NodeType[1])):
            cmds.createNode('transform', n=IKFKConGRP,p=LIMB_GRP)
            IKFK_GRPS   = IKFK_GRPS_Create(Limb,Side,LIMB_GRP)
            IK_CTRL     = IK_CTRL_Create(LimbType,Side,IKFK_GRPS[0])
            AddAttr_SetUp(IK_CTRL,ExAttr)
            

            ParentIK_GRPS   = [IKFK_GRPS[0],IKFK_GRPS[1]]
            ParentFK_GRPS   = [IKFK_GRPS[2],IKFK_GRPS[3]]
            
            IKReverseList   = IK_ReverseFoot_SetUp(Side,LimbType,ParentIK_GRPS,IK_CTRL,IncludeFK,CharType,RollFootFix,PVFlip)
            DrivenNodes     = IKReverseList[0]
            IKHandleList    = IKReverseList[1]
            DrivenCons      = []
            
            if(IncludeFK):
                LimbFKJNTGRP    = Side + "_" + "FK" + "_" + LimbType + "_" + NodeType[1] + NodeType[5]

                cmds.createNode( 'transform', n=LimbFKJNTGRP,p=ParentFK_GRPS[0])
                cmds.setAttr(LimbFKJNTGRP + "." + "v",0)
                TempParent = cmds.listRelatives(JointChain[0],p=True)
                CreateJNTChain(JointChain,FKJointChain,TempParent)
                
                ##turn off the IKhandle influence...
                for DN in DrivenNodes:
                    cmds.setAttr(DN[0] + "." + DN[1],0)
                MASTER.PrintCheck(["Start FK...."])
                
                for JNT_Name in FKJointChain:
                    #JNT_Name = FKJointChain[i]
                    #CTRL_Name = JointChain[i]
                    if(cmds.objExists(JNT_Name)):
                        if ("End_RigJNT" not in JNT_Name):
                            MatchRot            = True
                            SimpleParent        = False
                            SpineParent         = True
                            MainParentCTRLGRP   = ParentFK_GRPS[0]
                            CurveType           = "Circle"
                            Axis                = "x"
                            FKConstraints       = ["Point","Orient"]
                            ShadowParent        = False       
                            FK_Info             = Rigging.FK_CTRL_Setup(JNT_Name,CurveType,FKConstraints,Axis,MatchRot,SimpleParent,SpineParent,ExtraParentSwitchLimbs, ShadowParent,MainParentCTRLGRP)
                            for FK_DrivenNodes in FK_Info[2]:
                                DrivenCons.append(FK_DrivenNodes)
                
                
                cmds.parent(FKJointChain[0],LimbFKJNTGRP) # placing FK joints in correct parent.  doing this now because when rigging need to make sure the correct parent joint gets rigged. 
            else:
                MASTER.PrintCheck(["nno FK this time!!!!"])
            
            #connect IK/FK to limb chain..
            if(IncludeFK):
                IKSwitchNodes = IK_Switch_Create(Side,LimbType,LIMB_GRP,[ParentIK_GRPS[0],ParentFK_GRPS[0]],IKFKConGRP,DrivenNodes,DrivenCons)
                ScaleIK_GRP = Side + "_" + LimbType + "_IKScale_GRP"
                DeleteIfExists(ScaleIK_GRP)
                cmds.createNode('transform', n=ScaleIK_GRP,p=ParentIK_GRPS[0])
                for i in range(len(JointChain)):
                    if(cmds.objExists(JointChain[i])):
                        #creating Nodes for stretchy Ik not to transfer the IK scale but only translate to the rest of the rig. 
                        NewIKJoint = "Scale_" + IKJointChain[i]
                        cmds.createNode('transform', n=NewIKJoint,p=ScaleIK_GRP)
                        cmds.parentConstraint(IKJointChain[i],NewIKJoint)
                        Drivers = [NewIKJoint,FKJointChain[i]]
                        Driven  = JointChain[i]
                        ConParentGRP = None
                        ConInfo = Rigging.ConstraintNodes(Drivers,Driven,IKFKConGRP,["Point","Orient","Scale"],False)
                        OnOff = [[0,1],[1,0]]
                        for i in range(len(ConInfo)):
                            #print i, len(ConInfo)
                            CI = ConInfo[i]
                            OnOff = [[i-1,0],[i,1],[i+1,0]]
                            if(i==0):
                                OnOff = [[i,1],[i+1,0]]
                            if(i==len(ConInfo)-1):
                                OnOff = [[i-1,0],[i,1]]
                            for C in CI:
                                Rigging.SetDriven_AttributesSetup(IKSwitchNodes[0],IKSwitchNodes[1],C[0],C[1],OnOff,0)
        IKHandle_Lock(IKHandleList)
    #print "shapeList grp check....",ShapeListGRP
    
    if(cmds.objExists(ShapeListGRP)):
        #print "replacing CTRLS"
        CTRLShapeListNew = Rigging.List_CTRLS(ShapeListGRP,"CTRL_OLD")
        if(len(CTRLShapeListNew)  > 0):
            for CSL in CTRLShapeListNew:
                #print CSL
                CTRL        = CSL.replace("_OLD","")
                GRP         = CSL.replace("CTRL","SubGRP")
                ParentGRP   = CSL.replace("CTRL","GRP")
                CTRL_OLD    = [GRP,ParentGRP,CSL]
                OLD         = "_OLD"
                Curves.Ctrl_Curve_ReplaceShapeNode(CTRL,CTRL_OLD,OLD)
                #print CTRL, CTRL_OLD, OL D
                
        cmds.parent(ShapeListGRP,LIMB_GRP)
        cmds.setAttr(ShapeListGRP + "." + "v",0)
        List = cmds.listRelatives(ShapeListGRP,ad=True)
        #print List
        if(List != None):
            for L in List:
                 T = L.replace(OLD,"")
                 cmds.rename(L,T)
    else:
        print "shapelsitGRP does not exits...",ShapeListGRP
                 
def IKHandle_Lock(IKHandleList):
    #print IKHandleList
    for S in IKHandleList:
        #print S
        List = cmds.listAttr(S,cb=True)
        #print List
        for L in List:
            #print L
            #check to see if has incomming connection. 
            Node = S + "." + L
            if (cmds.listConnections(Node,c=True ) == None):
                cmds.setAttr(Node,l=True)