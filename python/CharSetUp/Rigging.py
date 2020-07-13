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
import Anim
import Skeleton
import Skinning
import MASTER
import UI

Rigging_ONOFF = True


def Sides():
    Sides    = ["L","R"]
    return Sides
    
def BASE_NodeTypes():
    Suffix_Types            = ["GRP","CTRL","JNT","GEO","LOC","OFST","Rig","SubGRP","RigJNT"]
    return Suffix_Types

def CTRLS_Types(Part):
    Base = ["World","Main","Move"]

def CheckSide(Node):
    RigSides = Sides()
    OppositeSide = ""
    NodeSide     = ""
    MirrorExist  = None
    HasSide      = None
    MirrorNode   = None
    StripName    = ""
    for Side in RigSides:
        #print "Side",Side
        if(Node.startswith(Side + "_")) :
            NodeSide = Side
            HasSide = True
        else:
            OppositeSide = Side
    if(HasSide):
        #print "HasSide", HasSide
        MirrorNode = Node.replace(NodeSide + "_", OppositeSide + "_")
        #print MirrorNode
        if(cmds.objExists(MirrorNode)):
            if(not cmds.listRelatives(Node,p=True)[0].startswith(NodeSide + "_")):
                MirrorExist = False
        else:
            MirrorNode = None   

    return (MirrorExist,[NodeSide + "_",OppositeSide + "_"],MirrorNode)




def Curves2CVs(OddEvenAll="All"):
    if(OddEvenAll == "All"):
        import maya.mel as mel
        mel.eval('selectCurveCV("all");')
    else:
        Sel = cmds.ls(sl=True)
        ShapeNodes = []
        Selection = []
        cmds.select(cl=True)
        
        for S in Sel:
            #print S
            ShapeNodes 	= cmds.listRelatives(S,type="nurbsCurve")# number of CVs = degree + spans.
            for ShapeNode in ShapeNodes:
                spans = cmds.getAttr( ShapeNode + '.spans' )
                for i in range(spans):
                    if i % 2 == 0:
                        Even.append(ShapeNode + ".cv[" + str(i) + "]")
                    else:
                        Odd.append(ShapeNode + ".cv[" + str(i) + "]")
        cmds.select(Even)
        if(OddEvenAll == "Odd"):
            cmds.select(Odd)

def FK_CTRL_Disconnect(List):
    #MASTER.BreakCode()
    if(str(type(List)) == "<type 'list'>"):
#        Char = "CHAR_CTRL"
        List.append(List.pop(List.index(Char)))
        for L in List:
            if(cmds.listRelatives(L,p=True)!=None):
                #print L,cmds.listRelatives(L,p=True)
                cmds.parent(L,w=True)
                
        List.pop(List.index(Char))
        FK_CTRL_Delete(List)
    else:
        if(cmds.listRelatives(List,p=True)!=None):
            cmds.parent(List,w=True)
            FK_CTRL_Delete([List])
			
def ReScale_CTRL_Disconnect(CTRLsGRP,List):
    #MASTER.BreakCode()
    for L in List:
        NewParent = cmds.createNode('transform', n=L[0] + "_Temp")
        for CTRL in L[1]:
            cmds.parent(CTRL,NewParent)
        cmds.delete(L[0])
        cmds.rename(NewParent,L[0])
    cmds.delete(CTRLsGRP)
    cmds.createNode('transform',n=CTRLsGRP)
    for L in List:
        cmds.parent(L[0],CTRLsGRP)

def FK_CTRL_TopGRP(CTRL):
    FK_Names     = FK_CTRL_GetName(CTRL)
    Name         = FK_Names[0]
    Suffix       = BASE_NodeTypes()
    ParentGRP    = Name     + "_" + Suffix[0]
    GRP          = Name     + "_" + Suffix[7]
    ReturnValue = None
    #print "CTRL Name : ",Name
    if(cmds.objExists(ParentGRP)):
        ReturnValue =  ParentGRP
    elif (cmds.objExists(GRP)):
        ReturnValue =  GRP
    else:
        ReturnValue = CTRL
    
    return ReturnValue       
            
def FK_CTRL_Delete(List):
    #MASTER.BreakCode()
    if(str(type(List)) == "<type 'list'>"):
        for L in List:
            #Find Top CTRL Node to delete
            TopGRP = FK_CTRL_TopGRP(L)
            #print TopGRP
            TempList = TopGRP.split("_")
            
            if("CTRL" !=  TempList[len(TempList)-1]):
                cmds.delete(TopGRP)
            

def SetDriven_AttributesSetup(Driver,Attribute,Driven,Attribute2,OnOff,defualtValue,KeyTangent=["spline","spline"]):
    PrintNote = "SetDriven_AttributesSetup(Driver,Attribute,Driven,Attribute2,OnOff,defualtValue):"
    MASTER.PrintCheck([PrintNote,"Driver : ",Driver,"Attribute : ",Attribute,"Driven : ",Driven,"Attribute2 : ",Attribute2,"OnOff : ",OnOff,"defualtValue : ",defualtValue],Rigging_ONOFF,["*",""])
    #OnOff is an array [[DriverValue,DrivenValue],[DriverValue,DrivenValue],[DriverValue,DrivenValue]]
    #setting up  Visibility on of settings
    #remove connections:
    
    for Value in OnOff:
        MASTER.PrintCheck(["Value",Value])
        cmds.setAttr(Driver + "." + Attribute,Value[0])
        cmds.setAttr(Driven + "." + Attribute2,Value[1])
        cmds.setDrivenKeyframe(Driven + "." + Attribute2,cd=Driver + "." + Attribute,itt=KeyTangent[0],ott=KeyTangent[1])
    cmds.setAttr(Driver + "." + Attribute,defualtValue)

def Create_Attribute(Node,Attribute,AttributeInfo=["double",0.000000,1.000000,1.000000],Keyable=True):#AttributeInfo=["enum","value1:valeu2:value3"]
    PrintNote = "Create_Attribute(Node,Attribute,AttributeInfo=[`double`,0.000000,1.000000,1.000000],Keyable=True):"
    MASTER.PrintCheck([PrintNote,Node,Attribute,AttributeInfo,Keyable],Rigging_ONOFF,["*",""])
    TempList = cmds.ls (sl= True)
    cmds.select(Node)
    if(cmds.objExists(Node + "." + Attribute)):
        cmds.deleteAttr(n=Node,at=Attribute)
    if(AttributeInfo[0] == "enum"):
        cmds.addAttr(Node,ln=Attribute,at=AttributeInfo[0],en=AttributeInfo[1])
    else:
        if(len(AttributeInfo)>2):# - if attribute is longer than that then it has limits
            cmds.addAttr(Node,ln=Attribute,at=AttributeInfo[0],min=AttributeInfo[1],max=AttributeInfo[2],dv=AttributeInfo[3])
        else:# it has no limits.. 
            cmds.addAttr(Node,ln=Attribute,at=AttributeInfo[0],dv=AttributeInfo[1])
    
    cmds.setAttr(Node + "." + Attribute,cb=True)
    cmds.setAttr(Node + "." + Attribute,keyable=Keyable)
    
    cmds.select(TempList)
		
def Get_ParentLocators():
    ParentSwitchGRP = "ParentSwitch_GRP"
    Locators        = []
    if(cmds.objExists(ParentSwitchGRP)):
        Locators = cmds.listRelatives(ParentSwitchGRP,c=True)
    return Locators

def Locator_Lists(SpineParent=True,ExtraParentSwitchLimbs=True):
    Base      = ["Base"       ,["World","CHAR"]]
    Simple    = ["Simple"     ,["COG"]]
    Spine     = ["Spine"      ,["Hips","Chest","Head"]]
    Extra     = ["ExtraPivots",["L_ExtraPivot","R_ExtraPivot","ExtraPivot"]]
    Limbs     = ["Limbs"      ,["L_Hand","R_Hand","L_Foot","R_Foot","Tail","TailEnd","LipBottom","Jaw"]]
    Locators  = [Base,Simple]
    if (SpineParent):
        Locators = [Base,Simple,Spine,Extra]
    if(ExtraParentSwitchLimbs):
        Locators.append(Limbs)

    return Locators

def Locator_Type(SpineParent,ExtraParentSwitchLimbs):
    TLocators = Locator_Lists(SpineParent,ExtraParentSwitchLimbs)
    Locators = []
    for TL in TLocators:
        Locators.append(TL[0])
    return Locators
            
def FindChildren(Node,Type):
    PrintNote = "FindChildren(Node,Type):"
    MASTER.PrintCheck([PrintNote,Node,Type],Rigging_ONOFF,["*",""])
    
    cmds.select(Node,hi=True)
    Children = cmds.ls( sl=True,type=Type )
    MASTER.PrintCheck(["Children",Children])
    Children.pop(0)
    return Children
    
def ParentSwitchList(JNT):
    PrintNote = "ParentSwitchList(JNT):"
    MASTER.PrintCheck([PrintNote,JNT],Rigging_ONOFF,["*",""])

    #replacing sub_RigJNT iwth RigJNT to assure that the ParentSwitch list is created without any downchain cycle issues for other CTRLRS connecting to it. 
    List = Get_ParentLocators()
    LList =[x.replace('_LOC','') for x in List]
    #find Children of Joint
    Children = cmds.listRelatives(JNT,ad=True)
    CList = []
    if (Children != None):
        CList = [x.replace('_RigJNT','') for x in Children ]
    #remove children from LOC list. 
    Locators = [x for x in LList if x not in CList]
    
    MASTER.PrintCheck(["List : ",List,"LList : ",LList,"Children : ",Children,"CList : ",CList,"Locators : ",Locators])
    return Locators

def Set_ParentSwitcher(Name,CTRL,ParentGRP,GRP,Parent,JNT,MatchRot="JNT",MatchPos= None,ParentSwitchTypeList=["Base","Simple","Spine"],ShadowParent=False):
    PrintNote = "Set_ParentSwitcher(Name,CTRL,ParentGRP,GRP,Parent,JNT,MatchRot=True,MatchPos=False,ParentSwitchTypeList=['Base','Simple','Spine']):"
    MASTER.PrintCheck([PrintNote,"Name : ",Name,"CTRL : ",CTRL,"ParentGRP : ",ParentGRP,"GRP : ",GRP,"Parent : ",Parent,"JNT : ",JNT,"MatchRot : ",MatchRot,"MatchPos : ",MatchPos,"ParentSwitchTypeList : ",ParentSwitchTypeList],Rigging_ONOFF,["*",""])
    
    ParentSwitchGRP = "ParentSwitch_GRP"
    CTRLSwitchGRP   = Name + "Switch_GRP"
    ParentAtt       = ["Parent","Switcher"]
    OrientAtt       = "Orient"
    PosAtt          = "Position"
    Remove          = ""
    ParentLoc       = ParentGRP + "LOC"
    MatchRot        = Match_Node(MatchRot,Name,CTRL)
    MatchPos        = Match_Node(MatchPos,Name,CTRL)
    #SubJNTCheck         = False
    #TempTest                 = Parent.replace("_RigJNT","Sub_RigJNT")
    #TempTest                 = TempTest.replace("_CTRL","Sub_CTRL")
    
    
    #if ((cmds.objExists(TempTest)) == False):
    #    if("Sub_" not in JNT):
    #        SubJNTCheck = True
        
    TempLocators = ParentSwitchList(JNT)

    
    #Cleanup by removing Limbs with specific attribute. 
    Locators = []
    for TL in TempLocators:
        for EL in ParentSwitchTypeList:
            if (cmds.getAttr(TL + "_LOC" + "." + "ParentType") == EL):
                Locators.append(TL)
    
    Locators.insert(0,"Parent")
    MASTER.PrintCheck(["JNT :",JNT,"Parent : ",Parent,"Locators",Locators])

    if CTRL.endswith('_CTRL'):
        Remove = CTRL[:-5]
    
    if Remove in Locators: Locators.remove(Remove)
    LocString = ":".join(Locators )
    Create_Attribute(CTRL,ParentAtt[0]    ,AttributeInfo=["enum",ParentAtt[1]])
    cmds.setAttr(CTRL + "." + ParentAtt[0],cb=True,keyable=False,lock=True)
    Create_Attribute(CTRL,OrientAtt    ,AttributeInfo=["enum",LocString])
    Create_Attribute(CTRL,PosAtt        ,AttributeInfo=["enum",LocString])
    
    # Make ParentLoc for CTRL
    if(cmds.objExists(ParentLoc)):
        cmds.delete(ParentLoc)
    
    #create GRP for parent Locators.
    if(cmds.objExists(CTRLSwitchGRP)):
        cmds.delete(CTRLSwitchGRP)
    cmds.createNode('transform', n=CTRLSwitchGRP)
    cmds.parent(CTRLSwitchGRP,ParentGRP)
    cmds.setAttr(CTRLSwitchGRP + "." + "v", 0)
    #create locators for all Parents 
    

    
    #make constraints and SetDriven Keys
    ONOffValues = SetDrivenKeyParentSwitcher_Values(Locators)
    Version = 0
    for L in range(len(Locators)):
        Loc         = Locators[L]
        ONOff         = ONOffValues[L]
        DriverLoc    = Loc + "_LOC"
        DrivenLoc     = Name + DriverLoc
        create        = True
        
        PrintNote     = " 1 Creating Locators and connections for the parent Switcher... "
        MASTER.PrintCheck([PrintNote,"Parent:",Parent,"Loc:",Loc,"ONOff:",ONOff,"DrivenLoc:",DrivenLoc,"create:",create],Rigging_ONOFF,["*",""])
    
        if Loc == "Parent":
            DriverLoc = Parent.replace("Sub_RigJNT","_RigJNT")
            DrivenLoc = Name + DriverLoc + "_LOC"
            
        if Loc == "SubParent":
            #check to see if there is a Subparent
            if ("Sub_CTRL" in CTRL):
                create = False
            else:
                if("Sub_RigJNT" in Parent):
                    DriverLoc = Parent
                else:
                    DriverLoc = Parent.replace("_RigJNT","Sub_RigJNT")
                DrivenLoc = Name + DriverLoc + "_LOC"
                
        DrivenLocS     = DrivenLoc + "Shadow"
        PrintNote     = "Updated Values.... "
        MASTER.PrintCheck([PrintNote,"Parent:",Parent,"Loc:",Loc,"ONOff:",ONOff,"DrivenLoc:",DrivenLoc,"create:",create],Rigging_ONOFF,["*",""])        
        #create locators and connect them.
        if (cmds.objExists(DriverLoc) and create):
            MASTER.PrintCheck(["Creating Locator and connection of "  + DrivenLoc])
            cmds.spaceLocator(n=DrivenLoc,p=(0, 0, 0))
            MatchJNT = JNT
            MOffset = True
            DrivenLocFinal = DrivenLoc
            if (ShadowParent):
                cmds.spaceLocator(n=DrivenLocS,p=(0, 0, 0))
                cmds.connectAttr(DrivenLoc + ".translateX",DrivenLocS + ".translateX",f=True)
                cmds.connectAttr(DrivenLoc + ".translateZ",DrivenLocS + ".translateZ",f=True)
                MatchJNT     = JNT
                MOffset     = True
                DrivenLocFinal = DrivenLocS
                #check if Locator has corresponding JNT
                Temp = DriverLoc.replace("LOC","RigJNT")
                if(cmds.objExists(Temp)):
                    DriverLoc = Temp
                cmds.pointConstraint(DriverLoc,DrivenLoc)
                cmds.orientConstraint(DriverLoc,DrivenLoc)
                cmds.parent(DrivenLocS,CTRLSwitchGRP)
                Curves.Ctrl_Curve_SetColor(CTRL,[0.4, 0.2, 0.8])
            else:
                if(MatchPos != None):
                    cmds.matchTransform(DrivenLoc,JNT,pos=True)
                if(MatchRot != None):
                    cmds.matchTransform(DrivenLoc,JNT,rot=True)
                cmds.parentConstraint(DriverLoc,DrivenLoc,mo=True)
            
            cmds.parent(DrivenLoc,CTRLSwitchGRP)
            ConstraintAttr     = DrivenLocFinal + "W"+ str(Version)
            PointCon         = cmds.pointConstraint(DrivenLocFinal,GRP)
            OrientCon         = cmds.orientConstraint(DrivenLocFinal,GRP)
            SetDriven_AttributesSetup(CTRL,PosAtt        ,PointCon[0]    ,ConstraintAttr,ONOff,0)
            SetDriven_AttributesSetup(CTRL,OrientAtt,OrientCon[0]    ,ConstraintAttr,ONOff,0)
            Version += 1 

    
    return CTRLSwitchGRP
       
def SetDrivenKeyParentSwitcher_Values(Locators,On=1,Off=0):
    ONOffValues = []
    for L in range(len(Locators)):
        if L == 0:
            ONOffValues.append([[L,On],[L+1,Off]])
        elif L == len(Locators)-1:
            ONOffValues.append([[L-1,Off],[L,On]])
        else:
            ONOffValues.append([[L-1,Off],[L,On],[L+1,Off]])
    return ONOffValues

def List_CTRLS(Node,Suffix = "CTRL"):
    List = cmds.listRelatives(Node,ad=True)
    NList = [L  for L in List if L.endswith(Suffix)]
    return NList
    
def Preserve_CTRLShape(Node):
    CTRL_List = List_CTRLS(Node)
    #print List
    #MASTER.BreakCode()
    ShapesOld = []
    PreservedShapeList = []
    for CTRL in CTRL_List:
        GRP            = CTRL.replace("CTRL","SubGRP")
        ParentGRP    = CTRL.replace("CTRL","GRP")
        ShapesOld     = Curves.Ctrl_Curve_ShapeNodeBackUp(CTRL,GRP,ParentGRP)
        PreservedShapeList.append([CTRL,ShapesOld])    
        #FK_CTRL_Disconnect(List)
    return PreservedShapeList

def FK_CTRL_GetName(InputName):
    InputName2 = InputName
    Suffix = BASE_NodeTypes()


    #print InputName2
    
    #Setting up Naming conventions for joints & ctrls
    if InputName2.endswith("_" + Suffix[6] + Suffix[2]):#RigJNT
        Name            = InputName2[:-(len(Suffix[6] + Suffix[2])+1)]
    elif InputName2.endswith("_" + Suffix[2]):#JNT
        Name            = InputName2[:-(len(Suffix[2])+1)]     
        TempJNT        = Name + "_" + Suffix[6] + Suffix[2]
        if(cmds.objExists(TempJNT)):
            InputName2    = TempJNT
    elif InputName2.endswith("_" + Suffix[1]):#CTRL
        Name            = InputName2[:-(len(Suffix[1])+1)]
        TempJNT        = Name + "_" + Suffix[6] + Suffix[2]
        if(cmds.objExists(TempJNT)):
            InputName2    = TempJNT
        else:
            TempJNT        = Name + "_" + Suffix[2]
            if(cmds.objExists(TempJNT)):
                InputName2    = TempJNT
    else:
        Name = InputName2
    
    
    Sides = ["L","R"]
    for S in Sides: #to remove if there is the new FK extra JNT so names are simpler. 
        if Name.startswith(S + "_" + "FK" + "_"):#
            #print "starts wiithhhhh....."
            Name = Name.replace(S + "_" + "FK" + "_",S + "_")
                
    return [Name,InputName2] # returns the Name without suffix and returns the supposedly JNT to rig too. 

def Match_Node(MatchType,JNT_Name,CTRL):
    MatchOrient = None
    if ( MatchType != None):
        MatchOrient = JNT_Name
        OLD = "_OLD"
        if(MatchType == "CTRL"):
            #find to see if the there are temp CTRL's
            if cmds.objExists(CTRL):
                MatchOrient = CTRL
            elif cmds.objExists(CTRL + OLD):
                MatchOrient = CTRL + OLD
            else:
                MatchOrient = JNT_Name
        #if(MatchType == "World"):
        #    MatchOrient = "CHAR_CTRL"
    return MatchOrient
    
def FK_CTRL_Setup(JNT_Name,CurveType,FKConstraints=["Point","Orient","Scale"],Axis="x",MatchOrient="JNT",SimpleParent=True,SpineParent = True,ExtraParentSwitchLimbs=False,ShadowParent=False,MainParentCTRLGRP = "CTRLS_GRP"):

    #Get Suffix Types Names
    Suffix      = BASE_NodeTypes()
    FK_Names    = FK_CTRL_GetName(JNT_Name)
    Name        = FK_Names[0]
    JNT_Name    = FK_Names[1]

    ParentGRP   = Name     + "_" + Suffix[0]
    GRP         = Name     + "_" + Suffix[7]
    CTRL        = Name     + "_" + Suffix[1]
    
    OLD_CTRL    = None
    OLD         = None
    #set the rotation to match.. - JNT CTRL or world... 

    #Extra Parent locator List type creation. 
    TempList    = Locator_Lists(SpineParent,ExtraParentSwitchLimbs) 
    ParentSwitchTypeList = []
    for TL in TempList:
        ParentSwitchTypeList.append(TL[0])

    MASTER.PrintCheck(["Setting up Names for different Nodes+++ ","JNT_Name",JNT_Name,"ParentGRP",ParentGRP,"GRP",GRP,"CTRL",CTRL],Rigging_ONOFF,["*",""])

    if(cmds.objExists(CTRL)):
        TempNodes     = Curves.Ctrl_Curve_ShapeNodeBackUp(CTRL,GRP,ParentGRP)
        OLD_CTRL     = TempNodes[0]
        OLD            = TempNodes[1]
        CurveType     = "Circle"
    
    ConstraintDelete([JNT_Name])
    
    Curves.Ctrl_Curve_Create(CTRL,CurveType,1,Axis)
    
    #create Empty Node
    cmds.createNode('transform', n=GRP)
    cmds.createNode('transform', n=ParentGRP)
    #Parent
    cmds.parent(CTRL,GRP)
    cmds.parent(GRP,ParentGRP)
    #Constrian
    #Find Joint parent
    Parent = cmds.listRelatives(JNT_Name, p=True )
    #move GRP to JNT location
    MASTER.PrintCheck(["Matching Joint Rotation of ",MatchOrient])
    #Anim.MatchTransforms(GRP,OrientMatch,Trans=True,Rot=MatchRot)
    MatchOrient = Match_Node(MatchOrient,JNT_Name,CTRL)
    #print " MatchOrient : ",MatchOrient 
    
    cmds.matchTransform(GRP,JNT_Name,pos=True)
    if (MatchOrient != None):
        cmds.matchTransform(GRP,MatchOrient,rot=True)
    #Parent constraint GRP to Parent
    
    if (SimpleParent):
        if(Parent != None):
            cmds.parentConstraint(Parent, ParentGRP,mo=True)
            cmds.scaleConstraint(Parent, ParentGRP,mo=True)
    else:
        MatchPos = JNT_Name
        Set_ParentSwitcher(Name,CTRL,ParentGRP,GRP,Parent[0],JNT_Name,MatchOrient,MatchPos,ParentSwitchTypeList,ShadowParent)
        cmds.scaleConstraint(Parent, GRP,mo=True)
    
    
    if(OLD_CTRL != None):
        Curves.Ctrl_Curve_ReplaceShapeNode(CTRL,OLD_CTRL,OLD)
	Curves.Ctrl_Curve_SetColor(CTRL)
    #constriant CTRL to Joint
    FKConstrained = []
    HideLoc = "Hide_LOC"
    
    AddHideAttr = cmds.objExists(HideLoc)
    HideAttr = "Hide"
    MaintainOffset = True
    if(AddHideAttr):
        #Add New Attribute
        Create_Attribute(CTRL,HideAttr)
        MaintainOffset = False
    
    for FK_C in FKConstraints:
        #print CTRL , JNT_Name
        if (FK_C == "Point"):
            PointCon     = cmds.pointConstraint(CTRL,JNT_Name,mo=MaintainOffset)
            PointCon.append(CTRL + "W0")
            FKConstrained.append(PointCon)
            cmds.parent(PointCon[0],GRP)
            if(AddHideAttr):
                PointCon2     = cmds.pointConstraint(HideLoc,JNT_Name,mo=MaintainOffset)
                PointCon2.append(HideLoc + "W1")
                FKConstrained.append(PointCon2)
                #cmds.parent(PointCon2[0],GRP)
                SetDriven_AttributesSetup(CTRL,HideAttr,PointCon[0]    ,PointCon[1]    ,[[0,1],[1,0]],0)
                SetDriven_AttributesSetup(CTRL,HideAttr,PointCon2[0],PointCon2[1]    ,[[0,0],[1,1]],0)
        
        if (FK_C == "Orient"):    
            RotCon         = cmds.orientConstraint(CTRL,JNT_Name,mo=MaintainOffset)
            RotCon.append(CTRL + "W0")
            FKConstrained.append(RotCon)
            cmds.parent(RotCon[0],GRP)
            if (AddHideAttr):
                RotCon2         = cmds.orientConstraint(HideLoc,JNT_Name,mo=MaintainOffset)
                RotCon2.append(HideLoc + "W1")
                FKConstrained.append(RotCon2)
                #cmds.parent(RotCon2[0],GRP)
                SetDriven_AttributesSetup(CTRL,HideAttr,RotCon[0]    ,RotCon[1]    ,[[0,1],[1,0]],0)
                SetDriven_AttributesSetup(CTRL,HideAttr,RotCon2[0]    ,RotCon2[1]    ,[[0,0],[1,1]],0)
        
        if (FK_C == "Scale"):
            ScaleCon     = cmds.scaleConstraint(CTRL,JNT_Name,mo=MaintainOffset)
            ScaleCon.append(CTRL + "W0")
            FKConstrained.append(ScaleCon)
            cmds.parent(ScaleCon[0],GRP)
            if (AddHideAttr):
                ScaleCon2     = cmds.scaleConstraint(HideLoc,JNT_Name,mo=MaintainOffset)
                ScaleCon2.append(HideLoc + "W1")
                FKConstrained.append(ScaleCon2)
                #cmds.parent(ScaleCon2[0],GRP)
                SetDriven_AttributesSetup(CTRL,HideAttr,ScaleCon[0]    ,ScaleCon[1]    ,[[0,1],[1,0]],0)
                SetDriven_AttributesSetup(CTRL,HideAttr,ScaleCon2[0],ScaleCon2[1]    ,[[0,0],[1,1]],0)
    

    
    if(cmds.objExists(MainParentCTRLGRP)):
        cmds.parent(ParentGRP,MainParentCTRLGRP)
    return [CTRL,ParentGRP,FKConstrained]

def ConstraintNodes(Drivers,Driven,ConParentGRP,ConstraintTypes =["Point","Orient","Scale"],Offset=True):
    ConstrainedInfo = []

    for i in range(len(Drivers)):
        Con = []
        for CType in ConstraintTypes:
            if (CType == "Point"):
                PointCon     = cmds.pointConstraint(Drivers[i],Driven,mo=Offset)
                PointCon.append(Drivers[i] + "W" + str(i))
                Con.append(PointCon)
                if(ConParentGRP != None):
                    CheckParent = cmds.listRelatives(PointCon[0],p=True)
                    if(CheckParent[0] != ConParentGRP):
                        cmds.parent(PointCon[0],ConParentGRP)
            if (CType == "Orient"):    
                RotCon         = cmds.orientConstraint(Drivers[i],Driven,mo=Offset)
                RotCon.append(Drivers[i] + "W" + str(i))
                Con.append(RotCon)
                if(ConParentGRP != None):
                    CheckParent = cmds.listRelatives(RotCon[0],p=True)
                    if(CheckParent[0] != ConParentGRP):
                        cmds.parent(RotCon[0],ConParentGRP)
            if (CType == "Scale"):
                ScaleCon     = cmds.scaleConstraint(Drivers[i],Driven,mo=Offset)
                ScaleCon.append(Drivers[i] + "W" + str(i))
                Con.append(ScaleCon)
                if(ConParentGRP != None):
                    CheckParent = cmds.listRelatives(ScaleCon[0],p=True)
                    if(CheckParent[0] != ConParentGRP):
                        cmds.parent(ScaleCon[0],ConParentGRP)
        ConstrainedInfo.append(Con)
    #print 0.1, ConstrainedInfo
    return ConstrainedInfo

def ConstraintDelete(List):
	for L in List:
		Axis = ["x"]
    	Trans = ["t","r","s"]
    	for T in Trans:
        	for A in Axis:
        		Con = cmds.listConnections( L + "." + T + A, d=False, s=True )
        		#print Con
            	if (Con == None):
            		print "nope.."
            	else:
                	for C in Con:
                		cmds.delete(C)

def CTRL_SubJNT(JNT):
	# getting variables to find the correct JNT to rename.. 
	FK_Names 	= FK_CTRL_GetName(JNT)
	Sub 		= "Sub"
	SubRigJNT 	= None
	SubJNT		= None
	RigJNT 		= FK_Names[0] + "_RigJNT"
	JNT 		= FK_Names[0] + "_JNT"
	
	if cmds.objExists(RigJNT):
		SubRigJNT 	= FK_Names[0] + Sub + "_RigJNT"
		if  not cmds.objExists(SubRigJNT):
			cmds.joint(n= SubRigJNT,p=(0,0,0))
			cmds.parent(SubRigJNT,RigJNT)
			Axis = ["X","Y","Z"]
			Trans = ["translate","rotate","jointOrient"]
			for T in Trans:
				for A in Axis:
					cmds.setAttr(SubRigJNT + "." + T + A,0)
		
	if cmds.objExists(JNT):
		SubJNT 		= FK_Names[0] + Sub + "_JNT"
		if  not cmds.objExists(SubJNT):	
			cmds.rename(JNT,SubJNT)
			ConstraintDelete([SubJNT])
			Skeleton.Connect_JNTS([SubJNT],False)
			
	if cmds.objExists(SubRigJNT):		
		return SubRigJNT
	else:		
		return SubJNT

def LOC_LISTExits():
    ParentSwitchGRP = "ParentSwitch_GRP"
    LOC_List = cmds.listRelatives(ParentSwitchGRP,c=True)
    return LOC_List

def LOC_AddAttributes(L,LOC_Type):
    #print L,LOC_Type
    if cmds.objExists(L):
        #print L + " : Exists.."
        if(cmds.objExists(L + "." + "ParentType") == False):
            print "Adding Attribute... "
            cmds.addAttr(L,     ln="ParentType",dt="string")
        else:
            print "attribute exists.. "
        cmds.setAttr(L + "." + "ParentType",lock=False)
        cmds.setAttr(L + "." + "ParentType",LOC_Type,type="string")
        cmds.setAttr(L + "." + "ParentType",lock=True)

def LOC_Attributes_Set():
    Locators    = Locator_Lists()#get list with attributes... 
    LOC_Exists    = LOC_LISTExits()#find what locators actually exists.. 
    #got through list of actuall locators.. inside of ParentSwitch_GRP
    for L in LOC_Exists:
        LOC_Type = "Other"
        #print "here... ", L
        for LOC in Locators:
            #check list of colators and see what matches. with list and type.. 
            LOC_List = LOC[1]
            for LL in LOC_List:
                if LL.lower() in L.lower():
                    LOC_Type = LOC[0]
                    cmds.rename(L,LL + "_LOC")
                    L=LL + "_LOC"
        #print "New : ", L
        LOC_AddAttributes(L,LOC_Type)


def Base_HidLoc_GRP(Parent = False):
    if Parent == False:
        BASE_SubGRPS    = [ ["IG",["JNTS","GEO"]] , ["RIG",["JNTS","CTRLS","EXTRAS"]] ]
        Parent          = BASE_SubGRPS[1][0] + "_" + BASE_SubGRPS[1][1][2]
    HideSwitch_GRP  = "HideSwitch_GRP"
    Hide_LOC        = "Hide_LOC"  
    if(cmds.objExists(Hide_LOC)==False):
        cmds.createNode( 'transform', n=HideSwitch_GRP,p=Parent)
        cmds.spaceLocator(n=Hide_LOC,p=(0, 0, -10))
        cmds.parent(Hide_LOC,HideSwitch_GRP)
        cmds.setAttr(HideSwitch_GRP + "." + "v", 0)
        AttList = [["translate",[0,0,-10]],["rotate",[0,0,0]],["scale",[0,0,0]]]
    axisList = ["X","Y","Z"]
    for Attr in AttList:
        i= 0
        for axis in axisList:
            cmds.setAttr(Hide_LOC + "." + Attr[0] + axis,Attr[1][i])
            cmds.setAttr(Hide_LOC + "." + Attr[0] + axis,l=True)
            i += 1
                
def BASE_ParentSwitch_GRP(Parent):
    ParentSwitchGRP = "ParentSwitch_GRP"
    
    #get list of all JNTs in Hierchy
    #JNTS             = cmds.listRelatives("COG" + RigSuffix,ad=True)
    Locators    = Locator_Lists()
    #create ParentSwitch Group
    if(cmds.objExists(ParentSwitchGRP) == False):
        cmds.createNode( 'transform', n=ParentSwitchGRP,p=Parent)
        cmds.setAttr(ParentSwitchGRP + "." + "v", 0)
    #create and connect Locators. 
    for LOC in Locators:
        LOC_Type = LOC[0]
        LOC_List = LOC[1]
        for L in LOC_List:
            RigSuffix = "_RigJNT"
            ConstrainOn = True
            JNTNode = L + RigSuffix
            LOCNode = L + "_LOC"
            if(cmds.objExists(JNTNode) or (LOC_Type == "Base")):
                if (cmds.objExists(LOCNode) == False):
                    cmds.spaceLocator(n=LOCNode,p=(0, 0, 0))
                    cmds.parent(LOCNode,ParentSwitchGRP)
                    #Add extra attibute with LOC type. 
                if(cmds.objExists(LOCNode + "." + LOC_Type) == False):
                    LOC_AddAttributes(LOCNode,LOC_Type)
                if (LOC_Type == "Base"):
                    if(cmds.objExists(L + "_CTRL")):
                        RigSuffix = "_CTRL"
                JNTNode = L + RigSuffix
                #constrain if there is an object to constrain. 
                if(cmds.objExists(JNTNode)):
                    #remove any previous connections... 
                    deleteConnection_Node(LOCNode)
                    cmds.parentConstraint(JNTNode,LOCNode,mo=True)
        
def Base_CTRL_Nodes(Parent):
    CTRLS = ["Head","Legs","Arms","Hands","Torso","Face","Hair","Tail","Ears","Props","Extras"]
    GRPList = []
    for CTRL in CTRLS:
        Vis_GRP     = CTRL + "_" + "Vis_GRP"
        #MainVis_GRP = CTRL + "_" + "MainVis_GRP"
        #SubVis_GRP  = CTRL + "_" + "SubVis_GRP"
        if(cmds.objExists(Vis_GRP) == False):
            cmds.createNode( 'transform', n=Vis_GRP,p=Parent)
        #if(cmds.objExists(MainVis_GRP) == False):
        #    cmds.createNode( 'transform', n=MainVis_GRP,p=Parent)
        #if(cmds.objExists(SubVis_GRP) == False):
        #    cmds.createNode( 'transform', n=SubVis_GRP,p=Parent)
        #GRPList.append(Vis_GRP)
    #return GRPList

def BASECTRL_VisibilitySwitch(Include_GEO = False,CTRL = None,CTRL_GRP=None):
    #determine wether the list is from selected GRP or from selected nodes.. 
    #print "CTRL_GRP ", CTRL_GRP
    #print "CTRL " , CTRL
    
    List = []
    SubList = []
    if(CTRL == None):
        
        Temp = cmds.ls(sl=True)
        CTRL = Temp.pop(0)
        
        #if Temp list is larger than 2 then it is selection nodes instead of the list. 
        if (len(Temp)>1):
            List = Temp
        else:
            List = Temp
    else:
        VisList = cmds.listRelatives(CTRL_GRP,ad=True,type="transform")
        List = [x for x in VisList if x.endswith("_Vis_GRP")]
        TempList = cmds.listRelatives(CTRL_GRP,ad=True)
        SubList = [x for x in TempList if x.endswith("Sub_GRP")]

    if(Include_GEO):
        newList = cmds.listRelatives("IG_GEO",type="transform")
        List = List + newList
    #pprint "List    : ",List
    print "SubList : ",SubList
    #cmds.select("kdkdkd")
    print "CTRL : ", CTRL
    Create_Attribute(CTRL,"CTRL_Vis",["enum","On/Off"],False)
    SubCTRLS = "Sub"
    Create_Attribute(CTRL,SubCTRLS,["double",0.000000,1.000000,1.000000],False)
    #print List
    #print CTRL
    for L in List:
        Attr = L.split("_")[0]
        if (cmds.objExists(L)):
            Create_Attribute(CTRL,Attr,["double",0.000000,1.000000,1.000000],False)
            #set visibility switch..
            deleteConnection_Attr(L + "." + "visibility")
            SetDriven_AttributesSetup(CTRL,Attr,L,"visibility",[[0,0],[1,1]],1)
            #check to see if Sub cTRL grp exists.& add to the list. 
    print "SubGRP List"
    for SubGRP in SubList:
        print SubGRP
        SetDriven_AttributesSetup(CTRL,SubCTRLS,SubGRP,"visibility",[[0,0],[1,1]],1)
     
def getParent_Node():
    GRPList = []
    CTRLS_GRP       = ["CTRLS_GRP"]
    List = cmds.listRelatives(CTRLS_GRP,c=True)
    for L in List:
        GRPList.append(L.split("_")[0])
    return GRPList
   
def BASECTRLS_Setup():
    
    Types           = BASE_NodeTypes
    BASE_GRP        = "CHAR"
    BASE_SubGRPS    = [ ["IG",["JNTS","GEO"]] , ["RIG",["JNTS","CTRLS","EXTRAS"]] ]
    CTRLS_GRP       = ["CTRLS_GRP"]
    BASE_CTRL       = BASE_GRP + "_CTRL"
    RIG_CTRLS       = BASE_SubGRPS[1][0] + "_" + BASE_SubGRPS[1][1][1]
    Rig_Extras      = BASE_SubGRPS[1][0] + "_" + BASE_SubGRPS[1][1][2]
    Rig_JNTSGRP     = BASE_SubGRPS[1][0] + "_" + BASE_SubGRPS[1][1][0]
    
    #CREATE BASE GRP
    
    Test = cmds.objExists(BASE_GRP)
    if(cmds.objExists(BASE_GRP) == False):
        cmds.createNode( 'transform', n=BASE_GRP)
    for SubGRPS in BASE_SubGRPS:
        #print SubGRPS
        if(cmds.objExists(SubGRPS[0]) == False):
            cmds.createNode( 'transform', n=SubGRPS[0],p=BASE_GRP)
        for SSGRPS in SubGRPS[1]:
            if(cmds.objExists(SubGRPS[0] + "_" + SSGRPS) == False):
                cmds.createNode( 'transform', n=(SubGRPS[0] + "_" + SSGRPS),p=SubGRPS[0])
    if(cmds.objExists(BASE_CTRL) == False):
        Curves.Ctrl_Curve_Create(BASE_CTRL,"XArrows",1,"")
        cmds.parent(BASE_CTRL,RIG_CTRLS)
        #create constraint
        Temp = cmds.parentConstraint(BASE_CTRL,Rig_JNTSGRP)
        Temp2 = cmds.scaleConstraint(BASE_CTRL,Rig_JNTSGRP)
        cmds.parent(Temp,BASE_CTRL)#parenting constraint
        
    if(cmds.objExists(CTRLS_GRP[0]) == False):
        MASTER.PrintCheck(["BASE_CTRL",BASE_CTRL])
        cmds.createNode( 'transform', n=CTRLS_GRP[0],p=BASE_CTRL)
        
    Base_CTRL_Nodes(CTRLS_GRP[0])
    BASE_ParentSwitch_GRP(Rig_Extras)    
    Base_HidLoc_GRP(Rig_Extras)
    #BASECTRL_VisibilitySwitch([BASE_CTRL],CTRL_GRP)
    
    cmds.select(clear=True)
    BASECTRL_VisibilitySwitch(BASE_CTRL,CTRLS_GRP)
    
    #return [BASE_GRP,BASE_SubGRPS,[BASE_CTRL]]

def MultiNodeCTRL(Node,DropDownList,JNTS):
    # Create Attribute for cTRL
    AttrName = "Switch"
    NewDropDownList = ["All"] + DropDownList
    #print "DropDownList : ",DropDownList
    #print "NewDropDownList :" , NewDropDownList
    #print Node
    #print JNTS
    Create_Attribute(Node,AttrName,AttributeInfo=["enum",":".join(NewDropDownList)],Keyable=True)
    # make connections...
    OnOffScale = SetDrivenKeyParentSwitcher_Values(NewDropDownList,On=1,Off=0)
    OnOffTrans = SetDrivenKeyParentSwitcher_Values(NewDropDownList,On=0,Off=-.1)
    #print DropDownList
    #print OnOffScale
    #print OnOffTrans
    #cmds.select("2222")
    Transforms = ["sx","sy","sz"]
 
    for i in range(1,len(NewDropDownList)):
        #create values for "all" attribute for them to be all on.. 
        AllOnOffScale = [[0,1]]
        AllOnOffTrans = [[0,0]]
        if (i > 1):
            AllOnOffScale = [[0,1],[1,0]]
            AllOnOffTrans = [[0,0],[1,-.1]]
        for attr in Transforms:
            SetDriven_AttributesSetup(Node,AttrName,JNTS[i-1],attr,OnOffScale[i] + AllOnOffScale,0)
        SetDriven_AttributesSetup(Node,AttrName,JNTS[i-1],"tz",OnOffTrans[i] + AllOnOffTrans,0)
        #PrintNote = "SetDriven_AttributesSetup(Driver,Attribute,Driven,Attribute2,OnOff,defualtValue):"
    
def MultiJointCTRL(Node,JNTS):
    #print "MultiJointCTRL STart...."
    ListAllParts = []
    for List in JNTS:
        TempList2 = []
        TempList = List.split('_')
        for e in range(len(TempList)):
            ListAllParts.append(TempList[e])
    #print "ListAllParts : ", ListAllParts
    #Make list of duplicates
    
    Duplicates = []
    for x in ListAllParts:
        if ListAllParts.count(x) > 1:
            Duplicates.append(x)
            
    Duplicates = list(set(Duplicates))
    #print "Duplicates :", Duplicates
    
    DropDownList = []
    for JntName in JNTS:
        #print "JntName :", JntName
        JntNameParts = JntName.split('_')
        #print "JntnameParts: ", JntNameParts
        ShortName = []
        for Part in JntNameParts:
            #print "Parts :", Part
            Keep = True
            for Dup in Duplicates: 
                #print "Dup : ", Dup
                if(Part == Dup):
                    #print "duplicate"
                    Keep = False
                    break
            #print "Keep : ", Keep
            if(Keep):
                ShortName.append(Part)
                #print "SN : ", ShortName
        #print "SN : ",ShortName
        DropDownList.append('_'.join(map(str,ShortName) ))
        "DD : ",DropDownList
    #print "DropDownList :", DropDownList        

        # create CTRL
    #if(cmds.objExists(Name)):
    #    cmds.delete(Name)
    #cmds.createNode('transform',n=Name)
    # create attribute to CTRL
    
    MultiNodeCTRL(Node,DropDownList,JNTS)

def SquashStretch_Switch(JNTS):
    Attr = "Squash"
    Attr2 = "Amount"
    
    #create start end Nodes
    #to get length of the joint chain.
    StartNode    = JNTS[0] + "_" + Attr
    EndNode        = JNTS[len(JNTS)-1] + "_" + Attr
    cmds.createNode('transform', n=StartNode)
    cmds.createNode('transform', n=EndNode)
    cmds.matchTransform(StartNode,JNTS[0])
    cmds.matchTransform(EndNode,JNTS[len(JNTS)-1])
    # get positions of the Nodes. 
    Pos = cmds.xform(JNTS[0],q=True,t=True,ws=True)
    Pos2 = cmds.xform(JNTS[len(JNTS)-1],q=True,t=True,ws=True)
    
    #print "Pos : ",Pos
    #print "Pos2 : ", Pos2
    ScaleCurve = Attr + "_ScaleCurve"
    
    Pos     = [Pos, Pos2]
    Knots = [ X for  X in range(len(Pos))]
    ScaleCurve = cmds.curve(n=ScaleCurve, d=1, p=Pos,k=Knots )    
    #print ScaleCurve
    cmds.cluster((ScaleCurve + ".cv[0]", ScaleCurve + ".cv[0]"),n= Attr + "_" + "Cluster0")
    cmds.cluster((ScaleCurve + ".cv[1]", ScaleCurve + ".cv[1]"),n= Attr + "_" + "Cluster1")
    # create utility to get curve length
    SquashLenth = "SquashLength"
    SquashLenth = cmds.shadingNode("curveInfo",name=SquashLenth,asUtility=True)
    #get shapenode
    ScaleCurveShape = cmds.listRelatives(ScaleCurve,c=True,type="shape")
    #print ScaleCurveShape

    #connectAttr -f curveShape1.worldSpace[0] curveInfo1.inputCurve;
    cmds.connectAttr(ScaleCurveShape[0] + ".worldSpace[0]"        , SquashLenth + "." + "inputCurve",f=True)
    #get percentage of curve length
    UtilNodeDiv = SquashLenth + "_" + "PercentNode"
    cmds.shadingNode("multiplyDivide",name=UtilNodeDiv,asUtility=True)

    cmds.connectAttr(SquashLenth + "." + "arcLength"        , UtilNodeDiv + "." + "input1X",f=True)
    OriginalValue = cmds.getAttr(UtilNodeDiv + "." + "input1X")
    cmds.setAttr(UtilNodeDiv + "." + "input2X",OriginalValue)
    cmds.setAttr(UtilNodeDiv + "." + "operation",2)#devide
    
    #to preserve volume add invers effect on the other sides. 
    UtilNodesqueeze =  SquashLenth + "_" + "SqeezeNode"
    cmds.shadingNode("multiplyDivide",name=UtilNodesqueeze,asUtility=True)
    cmds.connectAttr(UtilNodeDiv + "." + "outputX"        , UtilNodesqueeze + "." + "input1X",f=True)
    cmds.setAttr(UtilNodesqueeze + "." + "operation",3)#power
    cmds.setAttr(UtilNodesqueeze + "." + "input2X",0.5)
    #create the devide node
    UtilNodesInvertDiv =  SquashLenth + "_" + "InvertDivNode"
    cmds.shadingNode("multiplyDivide",name=UtilNodesInvertDiv,asUtility=True)
    cmds.connectAttr(UtilNodesqueeze + "." + "outputX"        , UtilNodesInvertDiv + "." + "input2X",f=True)
    cmds.setAttr(UtilNodesInvertDiv + "." + "input1X",1)
    cmds.setAttr(UtilNodesInvertDiv + "." + "operation",2)#Devide

    
    #create the devide node - to be greater effect on center joints. 
    ExtraEffect = []
    #get direnction of stretch....
    Axis = ["x","y","z"]
    TempValues = 0
    Index = 0 
    for A in range(len(Axis)):
        Temp = cmds.getAttr(JNTS[1] + "." + "t" + Axis[A])
        #print (str(Temp) + " : " + str(A)+ "_" + JNTS[1] ) 
        if Temp > TempValues:
            TempValues = Temp
            Index = A
    if Index == 1:
        Axis = ["y","x","z"]
    if Index == 2:
        Axis = ["z","y","x"]
    #print Axis
    #cmds.select("kdkdkdkd")    
    #get length of JNT list to get this pattern - [ 0,1,2,3,4,5,4,3,2,1,0] - meaning biggest effect in center of list
    Length = len(JNTS)/2
    AddMinus = 1
    Step = -1
    for i in range(len(JNTS)):
        if (i>Length):
            AddMinus = -1
        Step = Step + AddMinus
        UtilNodesExtra =  JNTS[i] + "_" + SquashLenth + "_" + "_ExtraNode"
        cmds.shadingNode("multiplyDivide",name=UtilNodesExtra,asUtility=True)
        cmds.connectAttr(UtilNodesInvertDiv + "." + "outputX"        , UtilNodesExtra + "." + "input1X",f=True)
        cmds.setAttr(UtilNodesExtra + "." + "input2X",float(str(1) + "." + str(Step)))
        cmds.setAttr(UtilNodesExtra + "." + "operation",1)#multiply
        
        #make final connections.. - for squash and strech.. 
        cmds.connectAttr(UtilNodeDiv        + "." + "outputX" , JNTS[i] + "." + "s" + Axis[0],f=True)
        cmds.connectAttr(UtilNodesInvertDiv + "." + "outputX" , JNTS[i] + "." + "s" + Axis[1],f=True)
        cmds.connectAttr(UtilNodesInvertDiv + "." + "outputX" , JNTS[i] + "." + "s" + Axis[2],f=True)
    
    Create_Attribute(Node,Attr,["long",0,1,0])
    Create_Attribute(Node,Attr2,["double",10])    
    
def ChangeSelectedType(Suffix,List = None):
	# change selection to selected type..
	if List == None:
		List = cmds.ls(sl=True)
	NewList = []
	#get list of possible suffixes to remove
	Suffixes = BASE_NodeTypes()
	#print List
	#remove suffix
	for Node in List:
		#print Node
		for S in Suffixes[::-1]:
			if ("_" + S) in Node:
				Node = Node.replace(S,Suffix)
				#print "node : ", Node
				NewList.append(Node)
	
	cmds.select(NewList)
		
def other():    
    
    #order of Joints bottom to top
    #on off utility
    #multiply utility
    for Jnt in JNTS:
        UtilNodeDiv = Jnt + "_" + Attr + "_UtilNode"
        cmds.shadingNode("multiplyDivide",name=UtilNodeDiv,asUtility=True)
        cmds.connectAttr(Node + "." + Attr2        , UtilNodeDiv + "." + "input1X",f=True)
        cmds.setAttr(UtilNodeDiv + "." + "input2X",.01)
        cmds.setAttr(UtilNodeDiv + "." + "operation",1)
        cmds.connectAttr(UtilNodeDiv + "." + "outputX"    , Jnt + "." + "sx",f=True)
        cmds.connectAttr(UtilNodeDiv + "." + "outputX"    , Jnt + "." + "sx",f=True)
        cmds.connectAttr(UtilNodeDiv + "." + "outputX"    , Jnt + "." + "sx",f=True)
        cmds.connectAttr(CTRL + "." + AttrOrig            , UtilNodeSum + "." + "input1D[1]",f=True)
    
def Rig_CTRLList(CTRLsGRP):
    #Find all nodes with CTRL name;
    CTRL_GRPNodes = cmds.listRelatives(CTRLsGRP,c=True)
    #print "GRP Nodes"
    #print CTRL_GRPNodes
    List = []
    for GRP in CTRL_GRPNodes:
        #print GRP
        TempList = cmds.listRelatives(GRP,ad=True,type="transform")
        #print TempList
        
        if TempList !=None:
            TempCTRLs = []
            for Temp in TempList:
                if Temp.endswith("_CTRL"):
                    TempCTRLs.append(Temp)
            if len(TempCTRLs) >0:
                List.append([GRP,TempCTRLs])
    #List = cmds.ls("*_CTRL")
    #print List
    
    return List
    
def FK_CTRLList(CTRLsGRP):
    #Find all nodes with CTRL name;
    CTRL_GRPNodes = cmds.listRelatives(CTRLsGRP,c=True)
    #print "GRP Nodes"
    #print CTRL_GRPNodes
    List = []
    for GRP in CTRL_GRPNodes:
        #print GRP
        TempList = cmds.listRelatives(GRP,ad=True,type="transform")
        #print TempList
        
        if TempList !=None:
            for Temp in TempList:
                if Temp.endswith("_CTRL"):
                    List.append(Temp)
    return List
    
def Char_PreScaleSetup():
    #Get character
    #find All CTRLS
    CTRLsGRP    = "CTRLS_GRP"
    CharCTRL    = "CHAR_CTRL"
    CTRL_List   = Rig_CTRLList(CTRLsGRP)
    # - remove all Controllers & delete parent Nodes that contain all the connections. 
    ReScale_CTRL_Disconnect(CTRLsGRP,CTRL_List)
    #Delete children of CHAR_CTRL
    DeleteMe = cmds.listRelatives(CharCTRL,c=True,type='transform')
    cmds.delete(DeleteMe)
    # - Parent to Main Control 
    cmds.parent("RIG_JNTS",CharCTRL)
    cmds.parent(CTRLsGRP,CharCTRL)
    
    cmds.select(CharCTRL)
    
def Char_SetScale():
    CTRLsGRP    = "CTRLS_GRP"
    RIG_JNTS    = "RIG_JNTS"
    GeoSelected = cmds.ls(sl=True,type="transform")
	
    #Duplicate Geo at new Scale.. 
    for Geo in GeoSelected:
        #print Geo
        NewGeo = cmds.duplicate(Geo,n= Geo + "_New")[0]

    #reset values to be scale of 1 for all ... currently the joints are scaled up and they need to be a value of 1
    CharCTRL    = "CHAR_CTRL"
    Scale = cmds.getAttr(CharCTRL + ".scaleX")
    Create_Attribute(CharCTRL,"NewScale",AttributeInfo=["double",Scale,Scale,Scale],Keyable=False)
    UnlockList = cmds.listRelatives(CharCTRL,ad=True,type="transform")
    ProBarInfo = ["Unlocking Attributes of JNTS & CTRLS",None]
    for Unlock in UnlockList:
        ProBarInfo = MASTER.ProgressBar_Run(WindowName= ProBarInfo[0],List = UnlockList,ProgressControl = ProBarInfo[1])
        deleteConnection_Node(Unlock)
    # moving All CTRls ecept the Char Control to seperate node. 
    TempNode = "Temp_ShapeNode"
    cmds.createNode('transform', n=TempNode)
    cmds.parent(cmds.listRelatives(CTRLsGRP,c=True,type="transform"),TempNode)
    cmds.makeIdentity(CharCTRL,apply=True,t=1,r=1,s=1,n=2)
    # move all parts back main CTRL and Rig joints now that they have been reset..
    #cmds.parent(CharCTRL,"RIG_CTRLS")
    cmds.parent(RIG_JNTS,"RIG")
    # - Re-set Joint Scale in new Position. 
    IG_JNTS = "IG_JNTS"
    #Rig_JNTS = "RIG_JNTS"
    IG_JNTList = cmds.listRelatives(IG_JNTS,ad=True,type="joint")
    #RIG_JNTList = cmds.listRelatives(Rig_JNTS,ad=True,type="joint")
    #Skeleton.ZeroRotations(KeepOrientation=True,RIG_JNTList,WorldOrient=False,ScaleReset = True)
    # - Skin New Mesh
    # - add all joints for influence
    # - unlock all joints
    # - copy Skin from first mesh
    cmds.dagPose(IG_JNTList[0],bp=True,save=True)
    
    for Geo in GeoSelected:
        NewGeo = Geo + "_New"
        NewSkin = cmds.skinCluster(NewGeo,IG_JNTList)
        Skinning.CopyWeights_PerVertName([Geo,NewGeo])
        cmds.delete(Geo)
        cmds.rename(NewGeo,Geo)
    # - Re-Rig Character. 
    #find to see if there are IK legs and Feet. 
    LOC_Attributes_Set()
    
    UI.RiggingIK_Create()
    FK_RigList = FK_CTRLList(TempNode)
    cmds.select(FK_RigList)
    UI.CharSetUp_CreateFKCTRL()
    cmds.delete(TempNode)
    HideNodes_Rig()
    MASTER.UI_Complete("Scale_Set")

def deleteConnection_Node(Node,AttList = ["translate","rotate","scale"],axisList = ["X","Y","Z"],LockAttr=False):
        for Attr in AttList:
            for axis in axisList:
                print (Node + "." + Attr + axis)
                if(cmds.objExists(Node + "." + Attr + axis)):
                    
                    deleteConnection_Attr(Node + "." + Attr + axis)
                    cmds.setAttr(Node + "." + Attr + axis,l=LockAttr)
                
def deleteConnection_Attr(plug):
	#print "plug : ", plug
	#print cmds.connectionInfo(plug, isDestination=True)
	if cmds.connectionInfo(plug, isDestination=True):
		#print "in connection info.. "
		plug = cmds.connectionInfo(plug, getExactDestination=True)
		#print "plug : ",plug
		readOnly = cmds.ls(plug, ro=True)
		#print readOnly
		#delete -icn doesn't work if destination attr is readOnly 
		if readOnly:
			#print "in"
			source = cmds.connectionInfo(plug, sourceFromDestination=True)
			cmds.disconnectAttr(source, plug)
		else:
			#print "delete"
			cmds.delete(plug, icn=True)
			
def HideNodes_Rig():
    List = ["RIG_JNTS","IG_JNTS","Switch_GRP","RigJNTGRP","CTRL_IKHeelPivot_ParentGRP","RIG_EXTRAS"]
    NewList = []
    for L in List:
        Temp = (cmds.ls("*" + L))
        NewList = NewList + Temp
    #print NewList
    for L in NewList:
        cmds.setAttr(L + "." + "visibility",0)

def CTRLS_GRP_Connect():
    CTRLGRP = "CTRLS_GRP"
    NewParent = "RIG_CTRLS"
    JNTGRP     = "RIG_JNTS"
    Driver = "CHAR_CTRL"
    # check to see what the parent is.
    ParentNode = cmds.listRelatives(CTRLGRP,p=True)[0]
    print ParentNode
    if ParentNode != NewParent:
        cmds.parent(CTRLGRP,NewParent)
    # check to see if it has inputs..
    deleteConnection_Node(CTRLGRP)
    deleteConnection_Node(JNTGRP)
    #Make parent constraint
    cmds.parentConstraint(Driver,JNTGRP,mo=True)
    cmds.scaleConstraint(Driver,JNTGRP,mo=True)
    
def Add_SpaceSwitch_LOC(Node,Type = "JNT"):
    Suffix_List = ["_CTRL","_RigJNT","_JNT"]
    Suffix = [Suffix for Suffix in Suffix_List if Suffix in Node]
    ConstrainOn = True
    JNTNode = L + RigSuffix
    LOCNode = L + "_LOC"
    if(cmds.objExists(JNTNode) or (LOC_Type == "Base")):
        if (cmds.objExists(LOCNode) == False):
            cmds.spaceLocator(n=LOCNode,p=(0, 0, 0))
            cmds.parent(LOCNode,ParentSwitchGRP)
            #Add extra attibute with LOC type. 
        if(cmds.objExists(LOCNode + "." + LOC_Type) == False):
            LOC_AddAttributes(LOCNode,LOC_Type)
        if (LOC_Type == "Base"):
            if(cmds.objExists(L + "_CTRL")):
                RigSuffix = "_CTRL"
        JNTNode = L + RigSuffix
        #constrain if there is an object to constrain. 
        if(cmds.objExists(JNTNode)):
            #remove any previous connections... 
            deleteConnection_Node(LOCNode)
            cmds.parentConstraint(JNTNode,LOCNode,mo=True)