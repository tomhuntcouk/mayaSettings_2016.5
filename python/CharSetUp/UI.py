####################################################
#
# Character UI Setup for character Rigging tools
# Creator = Leo Michalek
# Created 18.08.2016
#
#
####################################################

import maya.cmds as cmds
from functools import partial
import Skinning 
import Rigging 
import Rigging_IK
import MASTER
import Curves
import Anim
import tweenMachine
import RenderTools
import Skeleton

from inspect import currentframe, getframeinfo

global UI_ONOFF
global Original
global Target

UI_ONOFF = True

def CharSetup_LabelTextField(Name,Label = "",Value = "",description = "TEMP -- Need to add Description",Enable=True,Width=75):
    cmds.text("Text_" + Name, label=Label,en=Enable)
    TexFieldname = cmds.textField("TextField_" + Name)
    cmds.textField(TexFieldname,it=Value,edit=True,ann=description,w=Width,en=Enable)
    return   TexFieldname

def ImportPtvsd():
    import ptvsd
    ptvsd.enable_attach("my_secret", address = ('0.0.0.0', 3000))
    print ("import ptvsd")
    print ('ptvsd.enable_attach("my_secret", address = ("0.0.0.0", 3000))')
def UI_ChangeColorTest(Color,Adj):
    NewColor = []
    for C in range(len(Color)):
        NewColor.append(Color[C] + (0.1*Adj[C]))
        
    return NewColor       
          
def UI_ColorSettings(BGColor,Multiplier):
    ButtonColor = tuple((x * .8) for x in BGColor)
    return [ButtonColor]
    
def TEst_Test_UI(printMe):
    print ("testworks!!!!   -  " + printMe)

def CharSetup_aTools_launchInstall():
    import aTools_install
    aTools_install.aTools_launchInstall()

def CharSetup_BHGhost_Run():
    import maya.mel as mel
    mel.eval('bhGhost')

def CharSetup_MGToolsPro_Run():
    import maya.mel as mel
    mel.eval('installMGTools')

def CharSetup_StudioLibrary():
    import studiolibrary
    studiolibrary.main()

def CharSetUp_VertexColorToggle(OnOff):

    sel = cmds.ls(sl=True)

    for s in sel:
        Child = cmds.listRelatives(s=True)[0]
        cmds.setAttr(Child + ".displayColors", OnOff)

def CharSetUp_MakeRef(OnOff,sel=None):
    Override = 0
    DisplayType = 0
    if(OnOff):
        Override = 1
        DisplayType = 2
    if sel == None:
        sel = cmds.ls(sl=True)
    for S in sel:
        cmds.setAttr(S + ".overrideEnabled",Override)
        cmds.setAttr(S + ".overrideDisplayType",DisplayType)

def CharSetUp_Set_Print():
    #get if it's turned on
    Set = False
    if cmds.checkBox("checkBox_PrintInfo",ex=True):
        Set = cmds.checkBox("checkBox_PrintInfo",q=True,v=True) 
    return Set

def CharSetup_ConnectMesh_byName():
    Type    = cmds.radioButtonGrp("radioButtonGRP_ConnectMesh_ByName",q=True,select=True)
    #print Type
    #if (Type)
    #Offset =  cmds.checkBox("checkBox_ConstrainMO",q=True,v=True)
    #Skinning.Constrain2MatchingJoints(Offset)   

def CharSetup_FilterSelectionToMesh():
    Sel = cmds.ls(sl=True)
    List = []
    for S in Sel:
        cmds.select(S)
        cmds.select(hi=True)
        geometry = cmds.ls(sl=True,geometry=True)
        print (geometry)
        print (len(geometry))
        transforms = cmds.listRelatives(geometry, p=True, path=True)
        List = list(set(List+transforms))
    #print "Done"    
    #print List
    #print len(List)
    cmds.select(List, r=True)
    return List

def CharSetUp_AnimPicker():
    import maya.mel as mel
    mel.eval('AnimSchoolPicker')

def CharSetUp_GetAxisDirection():
    Axis = ["x","y","z"]
    Direction = cmds.radioButtonGrp("FKCurve_AXIS_SELECT",q=True,select=True)
    return Axis[Direction-1]

def CharSetUp_GetCTRLMatchOrient():
    MatchOrient = "JNT"
    Direction   = cmds.radioButtonGrp("FKCurve_MatchOrient_SELECT",q=True,select=True)
    if Direction == 2:
        MatchOrient = None
    if Direction == 3:
        MatchOrient = "CTRL"
        
    print ("MatchOrient : ",MatchOrient)
    return MatchOrient




def CharSetUp_GetParentSwitch():
    
    ParentType  = cmds.checkBox("FKCurve_ParentSwitch_SELECT",q=True,v=True)
    PSLimbs     = cmds.checkBox("FKCurve_ParentSwitchLimbs_SELECT",q=True,v=True)
    PSSpine     = cmds.checkBox("FKCurve_ParentSwitchSpine_SELECT",q=True,v=True)
    PSShawdow   = cmds.checkBox("FKCurve_ParentSwitchShadow_SELECT",q=True,v=True)
    PSMultiNode = cmds.checkBox("FKCurve_ParentSwitchMultiNode_SELECT",q=True,v=True)
    ParentCTRL   = cmds.checkBox("FKCurve_ParentCTRL",q=True,v=True)
    #ExtraLimbs = Rigging.Locator_Type(PSLimbs)
    return [not ParentType,PSSpine,PSLimbs,PSShawdow,PSMultiNode,ParentCTRL]

def CharSetUp_GetSubJNT():
    SubJNT      = cmds.checkBox("FKCurve_SubJNT_SELECT",q=True,v=True)
    SubCTRLOnly = cmds.checkBox("FKCurve_SubCTRLOnly_SELECT",q=True,v=True)
    return [SubJNT,SubCTRLOnly]
    


def CharSetUp_OnlyCurve_Create():
    
    NodeType = Rigging.BASE_NodeTypes()
    CurveType = cmds.optionMenu("Curve_Shape_Menu", query = True, value = True)
    Curves.Ctrl_Curve_Create(CurveType + "_" + NodeType[1] ,CurveType,1,"") 

def getParent_Node_UI():
    ParentNodeList = Rigging.getParent_Node()
    CheckBoxWindow = "ParentNode_CheckBoxWindow"
    if cmds.window(CheckBoxWindow,exists = True):
        cmds.deleteUI(CheckBoxWindow)
    CheckBoxWindow = cmds.window(CheckBoxWindow,title="Select_Visibility_Parent_Node" )
    cmds.columnLayout(bgc=(0.4,0.5,0.4),cal="center")
    for Node in ParentNodeList:
        cmds.checkBox("checkbox_ParentNode_" + Node,label=Node,ann="temp")
    cmds.button( label='<',c='UI.CharSetup_RotateValues(-1)',ann="temp")
    cmds.setParent( '..' )
    cmds.showWindow( CheckBoxWindow )
        

    
def CharSetUp_FK_CTRL_Setup(FKConstraints   = ["Point","Orient","Scale"]):


    NodeType        = Rigging.BASE_NodeTypes()
    CurveType       = cmds.optionMenu("Curve_Shape_Menu", query = True, value = True)
    CurveTypeSub    = cmds.optionMenu("For_SubJNT_Menu", query = True, value = True)
    AxisDir         = CharSetUp_GetAxisDirection()
    MatchOrient     = CharSetUp_GetCTRLMatchOrient()
    
    SimpleParent    = CharSetUp_GetParentSwitch()[0]
    SpineParent     = CharSetUp_GetParentSwitch()[1]
    ExtraParentSwitchLimbs  = CharSetUp_GetParentSwitch()[2]
    SubJNT          = CharSetUp_GetSubJNT()[0]
    SubCTRLOnly     = not CharSetUp_GetSubJNT()[1]
    ShadowParent    = CharSetUp_GetParentSwitch()[3]
    PSMultiNode     = CharSetUp_GetParentSwitch()[4]
    ParentCTRL      = CharSetUp_GetParentSwitch()[5]
    ParentNodeList  = []

    
    # select parent node if selected:
    if (ParentCTRL):
        ParentNodeList = getParent_Node_UI()
        
    CTRL_List       = []
    Nodes           = cmds.ls( sl=True)
    Sel             = Nodes
  
    cmds.select(cl=True)
    if (PSMultiNode):
        Sel = [Nodes[0]]
    print ("Sel 2: ")
    print (Sel)
    UnlockList = Sel
    ProBarInfo = ["Rigging... FK CTRLS",None]
    for S in Sel:
        print ("ProBarInfo: ")
        print (ProBarInfo)
        ProBarInfo = MASTER.ProgressBar_Run(WindowName= ProBarInfo[0],List = UnlockList,ProgressControl = ProBarInfo[1])

        if(SubCTRLOnly):# this is to create ony a sub controller. 
            NewCTRL = Rigging.FK_CTRL_Setup(S,CurveType,FKConstraints,AxisDir,MatchOrient,SimpleParent,SpineParent,ExtraParentSwitchLimbs,ShadowParent)
            CTRL_List.append(NewCTRL[0])
        if(SubJNT):
            NewJNT = Rigging.CTRL_SubJNT(S)
            NewCTRL = Rigging.FK_CTRL_Setup(NewJNT,CurveTypeSub,FKConstraints,AxisDir,MatchOrient,SimpleParent,SpineParent,ExtraParentSwitchLimbs,ShadowParent)
            CTRL_List.append(NewCTRL[0])
        print ("ProBarInfo: ")
        print (ProBarInfo)

    KeyTanget_Values = Anim.KeyTangets_Get()
    Anim.KeyTangents_Set("Stepped")
    if (PSMultiNode):#PSMultiNode - is to rig a controller that drives the visibility of other JNTS or Nodes..  # 1st object selected drives the consequent selected nodes.. 
        Nodes.pop(0)#remove the 1st node that will be the driving  controller.
        Rigging.MultiJointCTRL(NewCTRL[0],Nodes)
    cmds.select(CTRL_List)
    Anim.KeyTangents_Set(KeyTanget_Values)
    
def CharSetUp_SquashStretch_Switch():

    Sel = cmds.ls(sl=True)

    FKConstraints   = ["Point","Orient"]

    #CharSetUp_FK_CTRL_Setup(FKConstraints)

    Rigging.SquashStretch_Switch(Sel)   

def CharSetUp_FK_CTRL_Disconnect():
    Sel = cmds.ls( sl=True )
    Rigging.FK_CTRL_Disconnect(Sel)

def CharSetUp_FK_CTRL_Delete():
    Sel = cmds.ls( sl=True )
    Rigging.FK_CTRL_Delete(Sel)

def CharSetup_RotateValues(Direction):
    print ("CharSetup_RotateValues(Direction):")
    Axis = [0,0,0]
    Value = cmds.textField("TextField_RotateAmount",q=True,text=True)
    print (Direction)
    print (cmds.checkBox("RotateAxisX",q=True,v=True))
    if (cmds.checkBox("RotateAxisX",q=True,v=True)):
        Axis[0] = int(Value) * int(Direction)
    if (cmds.checkBox("RotateAxisY",q=True,v=True)):
        Axis[1] = int(Value) * int(Direction)
    if (cmds.checkBox("RotateAxisZ",q=True,v=True)):
        Axis[2] = int(Value) * int(Direction)
    
    print (Axis)
    CharSetup_RotateExecute(Axis)

def CharSetup_RotateExecute(Axis):
    PrintNote = "CharSetup_RotateExecute(Axis):"
    MASTER.PrintCheck([PrintNote,"Axis : ",Axis],UI_ONOFF,["*",""])
    
    cmds.rotate(Axis[0], Axis[1], Axis[2])#r=True,ocp=True,ws=True)

def CharSetUp_Rotate():
    
    FrameLayout = cmds.frameLayout(label='Rotate Curve',cl = True)
    
    
    cmds.rowColumnLayout(numberOfColumns=3)
    Test = cmds.checkBox("RotateAxisX",label="X",ann="Rotate selection on the X axis")
    Test = cmds.checkBox("RotateAxisY",label="Y",ann="Rotate selection on the Y axis")
    Test = cmds.checkBox("RotateAxisZ",label="Z",ann="Rotate selection on the Z axis")
    cmds.setParent( '..' )
    cmds.text(label="rotation amount",ann="amount of rotation for sellected object")
    cmds.rowColumnLayout(numberOfColumns=8)
    cmds.button( label='<',c='UI.CharSetup_RotateValues(-1)',ann=" - negative Rotation on axis checked and by amount inputed")
    
    name = cmds.textField("TextField_RotateAmount",ann="amount of rotation for sellected object")

    cmds.textField(name,it="90",edit=True)
    cmds.button( label='>',c='UI.CharSetup_RotateValues(1)',ann=" + positive Rotation on axis checked and by amount inputed")
    cmds.setParent( '..' )
    cmds.setParent( '..' )

def CharSetUp_SetColor(SetColor,*args):
    Sel = cmds.ls(sl=True)
    print ("Start....")
    for S in Sel:
        print (S)
        Curves.Ctrl_Curve_SetColor(S,SetColor)

def CharSetUp_SetColor_UI():
    FrameLayout = cmds.frameLayout(label='Set Curve Color',cl = True)
    ColumnMax = 11
    Colors  = Curves.ColorPallette()
    Columns = len(Colors)
    if len(Colors) > ColumnMax:
        Columns = ColumnMax
    cmds.rowColumnLayout(numberOfColumns=Columns)
    size = 15
    for Color in Colors:
        cmds.button(l='', c=partial(CharSetUp_SetColor,Color),bgc=Color,w=size,h=size)

    cmds.setParent( '..' )


def CharSetUp_ZeroRotations():
    MASTER.PrintCheck(["CharSetUp_ZeroRotations()"],UI_ONOFF,["*",""])
    JNTS = None
    KeepOrient = cmds.checkBox("CheckBox_ZeroRotKeepOrient",q=True,v=True)
    WorldOrient = cmds.checkBox("CheckBox_ZeroRotWorld",q=True,v=True)
    ScaleReset = cmds.checkBox("CheckBox_ZeroRotScaleReset",q=True,v=True)
    Skeleton.ZeroRotations(KeepOrient,JNTS,WorldOrient,ScaleReset)

def CharSetUp_CountJoints(Count=False):
    
    TextNameField   = "text_CountJoints"
    TestString      = " Select Parent Joint "
    if Count:
        NumberJoints    = Skeleton.CountJoints()
        TestString = "   " + str(len(NumberJoints))  + " Joints in Skeleton"
    
    if (cmds.text(TextNameField,ex=True)):
        cmds.text(TextNameField,label=str(TestString),edit = True)
        
    else:
        cmds.text(TextNameField,label=str(TestString),align='center')

def CharSetUp_LabelJoint_Values():
    LabelJoints = "LabelJoints"
    CheckBox    = "checkBox_"  + LabelJoints
    Hierarchy   = CheckBox + "_Hierarchy"
    Left        = [LabelJoints + "_Left","Left"]
    Right       = [LabelJoints + "_Right","Right"]
    Prefix      = [LabelJoints + "_Prefix","Prefix"]
    Suffix      = [LabelJoints + "_Suffix","Suffix"]
    return [LabelJoints,Hierarchy,CheckBox,Left,Right,Prefix,Suffix]

def CharSetUp_LabelJoint_OnOff():
    CheckBox    = CharSetUp_LabelJoint_Values()[2]
    Left        = CharSetUp_LabelJoint_Values()[3]
    Right       = CharSetUp_LabelJoint_Values()[4]
    Prefix      = CharSetUp_LabelJoint_Values()[5]
    Suffix      = CharSetUp_LabelJoint_Values()[6]
    List        = CharSetUp_LabelJoint_Values()
    ONOFF = cmds.checkBox(List[2],q=True,v=True)
    
    List.pop(0)
    List.pop(0)
    List.pop(0)

    cmds.radioButtonGrp("radioButton_LabelSide_fix",e=True,en=ONOFF)
    print (ONOFF)
    print (List)
    for L in List:
        cmds.text("Text_" + L[0],e=True,en=ONOFF)
        cmds.textField("TextField_" + L[0],e=True,en=ONOFF)
    
    #cmds.text(Left[1],e=True,en=ONOFF)
    #cmds.textField(Right[0],e=True,en=ONOFF)
    #cmds.text(Left[1],e=True,en=ONOFF)
    #cmds.textField(Prefix[0],e=True,en=ONOFF)
    #cmds.text(Left[1],e=True,en=ONOFF)
    #cmds.textField(Suffix[0],e=True,en=ONOFF)
    
def CharSetUp_LabelJoints_Create(ButtonColor):
    Hierarchy    = CharSetUp_LabelJoint_Values()[1]
    CheckBox    = CharSetUp_LabelJoint_Values()[2]
    Left        = CharSetUp_LabelJoint_Values()[3]
    Right       = CharSetUp_LabelJoint_Values()[4]
    Prefix      = CharSetUp_LabelJoint_Values()[5]
    Suffix      = CharSetUp_LabelJoint_Values()[6]
    FrameLayout = cmds.frameLayout(label='Label Joints',cl = True, collapsable = True,bv=True)
    cmds.checkBox(Hierarchy,label="Include Children",v=False,ann="check to include all children of selection")
    cmds.checkBox(CheckBox,label="Change Label options",v=False,cc='UI.CharSetUp_LabelJoint_OnOff()',ann="check to enable to change the options for labeling")
    cmds.rowColumnLayout(numberOfColumns=3,cal=[3,"center"])
    LabelName  = "Sides : "
    CB_Options = ["Prefix","Infix","Suffix"]
    offset  = 9
    ColumnWidths = [len(LabelName) * 5, len(CB_Options[0]) * offset,len(CB_Options[1]) * offset,len(CB_Options[2]) * offset]
    cmds.radioButtonGrp("radioButton_LabelSide_fix",en=False,nrb=3, label=LabelName, labelArray3=CB_Options,cl4=("left","center","center","center"),cw4=ColumnWidths,sl=1)
    cmds.setParent( '..' )
    cmds.rowColumnLayout(numberOfColumns=4,cal=[4,"center"])
    Sides = Rigging.Sides()
    Temp = CharSetup_LabelTextField(Left[0],Left[1],Sides[0],"Left Naming Convention - to determine side for labeling joints - example (L_Leg_JNT) - type in 'L_' to determine side for labeling",False)
    CharSetup_LabelTextField(Right[0],Right[1],Sides[1],"Right Naming Convention - to determine side for labeling joints - example (R_Leg_JNT) - type in 'R_' to determine side for labeling",False)
    cmds.setParent( '..' )
    cmds.text("text_LabelTextToremove",en=False,label="Text to remove",align='left',ann="text to remove in front of the joint or at the end")
    cmds.rowColumnLayout(numberOfColumns=4,cal=[4,"center"])
    CharSetup_LabelTextField(Prefix[0],Prefix[1],"","string to remove for labels - example (Jnt_left_leg) - type in 'Jnt_' to remove from the label name",False,65)
    CharSetup_LabelTextField(Suffix[0],Suffix[1],"JNT","string to remove for labels - example (left_leg_JNT) - type in '_JNT' to remove from the label name",False,73)
    cmds.setParent( '..' )
    cmds.button(l="Label Joints",c='UI.CharSetup_JointLabel()',bgc= ButtonColor,ann="uses the name of the joint as the label. -- and uses the correct left/Right attributes - this is very helpful when wanting to copy weights from one mesh to another and using labels as an option.")
    cmds.setParent( '..' )
    
def CharSetup_JointLabel():
    #get settings
    Locations   = ["Prefix","Infix","Suffix"]
    RadioSelect = cmds.radioButtonGrp("radioButton_LabelSide_fix",q=True,sl=True)
    LJointInfo  = CharSetUp_LabelJoint_Values()
    
    Hierarchy   = cmds.checkBox(LJointInfo[1],q=True,v=True)
    CheckBox    = cmds.checkBox(LJointInfo[2],q=True,v=True)
    Text        = cmds.textField("textfield_NameSpace",q=True,text=True)
    Test        = LJointInfo[3][0]
    Left        = [Locations[RadioSelect-1],2,cmds.textField("TextField_" + LJointInfo[3][0],q=True,text=True)]
    Right       = [Locations[RadioSelect-1],1,cmds.textField("TextField_" + LJointInfo[4][0],q=True,text=True)]
    PrefixText  = [Locations[0],cmds.textField("TextField_" + LJointInfo[5][0],q=True,text=True)]
    SuffixText  = [Locations[2],cmds.textField("TextField_" + LJointInfo[6][0],q=True,text=True)]
    Sides       = [Left[2],Right[2]]
    RemoveList  = [PrefixText,SuffixText]
    List        = [Left,Right,PrefixText,SuffixText]

    Skeleton.UpdateJointLabel(RadioSelect,CheckBox,Hierarchy,Sides,RemoveList)

def CharSetUp_Skeleton_Select():
    List = []
    Suffix = "_JNTS"
    Status     = cmds.checkBoxGrp("CheckBox_SelectJNTS",q=True,va2=True)
    Names      = cmds.checkBoxGrp("CheckBox_SelectJNTS",q=True,la2=True)
    for S in range(len(Status)):
        GRP = Names[S] + Suffix
        if cmds.objExists(GRP):
            JNT = cmds.listRelatives(GRP,c=True,type='joint')[0]
            if Status[S]:
                List.append(JNT)
    cmds.select(List)   
      
def CharSetUp_Skeleton_Display():
    Status     = cmds.checkBoxGrp("CheckBox_DisplayJNTS",q=True,va2=True)
    Names      = cmds.checkBoxGrp("CheckBox_DisplayJNTS",q=True,la2=True)
    for S in range(len(Status)):
      print ('Joint: ',Names[S] , Status[S])
      Skeleton.ShowSkeleton([Names[S]],Status[S])

def CharSetUp_Skeleton_UI_Display(ButtonColor):
    
    FrameLayout = cmds.frameLayout(label='Display Options',cl = True, collapsable = True,bv=True)
    cmds.rowColumnLayout(numberOfColumns=2,cal=[2,"center"])
    cmds.button(l="Count # of Joints",  c='UI.CharSetUp_CountJoints(True)',bgc=ButtonColor,ann="counts number of Joints in a sckeleton chain: select top Joint in the skeleton chain and run button")
    CharSetUp_CountJoints(False)
    cmds.setParent( '..' )
    cmds.separator(h=5)
    LabelName  = "Select Joints  : "
    CB_Options = ["RIG","IG"]
    offset = 15
    cmds.checkBoxGrp("CheckBox_SelectJNTS",numberOfCheckBoxes=2, label=LabelName, labelArray2=CB_Options,cl3=("left","left","left"),ofc = 'UI.CharSetUp_Skeleton_Select()',onc='UI.CharSetUp_Skeleton_Select()',cw3=[len(LabelName) * 5, len(CB_Options[0]) * offset,len(CB_Options[1]) * offset])
    LabelName  = "Display Joints : "
    cmds.checkBoxGrp("CheckBox_DisplayJNTS",numberOfCheckBoxes=2, label=LabelName, labelArray2=CB_Options,cl3=("left","left","left"),ofc = 'UI.CharSetUp_Skeleton_Display()',onc='UI.CharSetUp_Skeleton_Display()',cw3=[len(LabelName) * 5, len(CB_Options[0]) * offset,len(CB_Options[1]) * offset])
    cmds.separator(h=5)
    cmds.rowColumnLayout(numberOfColumns=2,cal=[2,"center"])
    cmds.button(l="Toggle JointOrient", c='Skeleton.JointOrient_ToggleDisplay()',bgc=ButtonColor,ann=" Displays on channel box the Joint Orient attribute: Helpful for adjusting Joint orientation")
    cmds.button(l="Toggle Local Axis",  c='Skeleton.LocalAxis_ToggleDisplay()',bgc=ButtonColor,ann="Displays on the Joint in 3D view the orientation handles (X,Y,Z): good for understanding what the actual orientation of the joint is")
   
    cmds.setParent( '..' )
    cmds.setParent( '..' )
    #cmds.setParent( '..' )




def CharSetUp_Skeleton_SkelTemplate_Create():
    BodyParts = Skeleton.SkeletonTemplate_Parts()
    BuildParts = []
    SkeletonType = cmds.radioButtonGrp("radioButtonGrp_CharType",q=True,select=True)
    
    for Part in BodyParts:
        print (Part)
        Selected    = cmds.checkBox("CheckBox_CreateSkeleton_" + Part[0],q=True,v=True)
        if cmds.intFieldGrp("intFieldGrp_" + Part[0] + "_" + "Length",exists= True):
            print ("Does Exists")
            Length      = cmds.intFieldGrp("intFieldGrp_" + Part[0] + "_" + "Length",q=True,v=True)[0]
            BuildParts.append([Part[0],Selected,Length])
        else:
            print ("Nope... ")
            BuildParts.append([Part[0],Selected,"None"])
    for Part in BuildParts:
        if(Part[1]):
            Skeleton.JointChain_Create(JointType=[Part[0],Part[2]])




def CharSetUp_Skeleton_UI_SkelTemplate_Create(ButtonColor):
    BodyParts = Skeleton.SkeletonTemplate_Parts()
    FrameLayout = cmds.frameLayout(label='Create Skeleton',cl = True, collapsable = True,bv=True)
    cmds.button(l='From Selected Nodes', c='Skeleton.CreateSkeleton_SelectionList()',bgc= ButtonColor,ann="Create skeleton from selected items, and their hiarchies, add Rig_JNT at the end")
    
    FrameLayout = cmds.frameLayout(label='Template',cl = True, collapsable = True,bv=True)
    cmds.rowColumnLayout(numberOfColumns=1,cal=[1,"center"]) 
    
    Title = 'Char Type'
    RButton = cmds.radioButtonGrp("radioButtonGrp_CharType",label=Title, labelArray2=['Biped', 'Quadruped'], numberOfRadioButtons=2,select=1,cw3=(len(Title)*6,50,30),bgc=ButtonColor,ann="select type of Character, may affect the way the Legs PV gets set up.. may need to double check the description options to be more accurate with what it does.. ")
    #cmds.checkBox("CheckBox_CreateSkeleton_" + BodyParts[0][0],   label=BodyParts[0][0],ann="")
    #cmds.intFieldGrp("intFieldGrp_" + BodyParts[0][0] + "_" + "Length", numberOfFields=1,cal=(1,"left"),label='Length : ', extraLabel='Joints', value1=BodyParts[0][1],cw=[(1,44),(2,30)])
    for Part in BodyParts:
        if len(Part)>1:
            cmds.rowColumnLayout(numberOfColumns=2,cal=[(1,"left"),(2,"right")],columnWidth=[(1, 50), (2, 150)])
        Test = cmds.checkBox("CheckBox_CreateSkeleton_" + Part[0],   label=Part[0],ann="")
        if len(Part)>1:
            cmds.intFieldGrp("intFieldGrp_" + Part[0] + "_" + "Length", numberOfFields=1,cal=(1,"left"),label='Length : ', extraLabel='Joints', value1=Part[1],cw=[(1,44),(2,30)])
            cmds.setParent( '..' )
        
    
    cmds.setParent( '..' )
    cmds.button(l="Create Skeleton HelperNodes",  c='UI.CharSetUp_Skeleton_SkelTemplate_Create()',bgc= ButtonColor,ann="Create Skeleton Helper Nodes")
    cmds.button(l="Create Skeleton",  c='Skeleton.JointHelper_To_Joint()',bgc= ButtonColor,ann="Create Template Skeleton from Helper Nodes")
    #cmds.separator(h=5)
    cmds.setParent( '..' )
    cmds.setParent( '..' )
    


def CharSetUp_Skeleton_ScaleCompensate(Value):
    Hierarchy = cmds.checkBox("CheckBox_ScaleCompensate_Hierarchy",q=True,v=True)
    Skeleton.ScaleCompensate(Hierarchy,Value)
          
def CharSetUp_Skeleton_UI_Edit(ButtonColor):
    
    FrameLayout = cmds.frameLayout(label='Editing Tools',cl = True, collapsable = True,bv=True)
    cmds.button(l="Move Joint Chain Tool",  c='Skeleton.PlaceJNT()',bgc= ButtonColor,ann="Creates a temporary node to move joint chain: Creates a parent node that then you can move, rotate position to a better placement, without worring about adding rotation values to joints")
    #cmds.separator(h=5)
    FrameLayout = cmds.frameLayout(label='Reset the Rotation of Joints to 0',cl = True, collapsable = False,bv=True)
    cmds.rowColumnLayout(numberOfColumns=2,cal=[2,"center"]) 
    cmds.button(l="Reset \n Rotations",c='UI.CharSetUp_ZeroRotations()',bgc= ButtonColor,ann="zeroes the rotations of a joint chain: look at the options for how the joints will be affected")
    cmds.rowColumnLayout(numberOfColumns=1,cal=[1,"center"]) 
    Test = cmds.checkBox("CheckBox_ZeroRotKeepOrient",label="Keep Current Orient",ann="Will keep the joints are their current orientation, but will set the rotation to zero")
    Test = cmds.checkBox("CheckBox_ZeroRotWorld",label="Match World Orient",ann="Will change the orientation of the joints and matcht the orientation of the Scene")
    Test = cmds.checkBox("CheckBox_ZeroRotScaleReset",label="Reset Scale",ann="Will include and reset any scale values to 1")
    cmds.setParent( '..' )
    cmds.setParent( '..' )
    cmds.setParent( '..' )
    cmds.button(l="Mirror Joints",c='Skeleton.MirrorJoints()',bgc= ButtonColor,ann="Mirrors multiple selected joints: uses the 'L_' & 'R_' prefixes")
    cmds.button(l="Mirror Joints from Root",c='Skeleton.Skeleton_MirrorFromRoot()',bgc= ButtonColor,ann="Mirrors multiple joints, from selected Root joint, searches hiarchy of joints see it it has a side and if the parent is not a side & checks if there is a mirror. If it's not mirrored then it mirrors the joint: uses the 'L_' & 'R_' prefixes")
    
    cmds.separator(h=5)
    
    cmds.text("TextField_ScaleCompensate",label="Joint Scale Compensate : ",align='left',ann="Turn ON or OFF the Joint settings to compensate scale effected by its parent: Used for setting all the Skeletons to OFF to create a controlled natural scale of all joints for easier animation")
    cmds.rowColumnLayout(numberOfColumns=3,cal=[3,"center"]) 
    cmds.button(l='ON',     c='UI.CharSetUp_Skeleton_ScaleCompensate(1)',bgc=ButtonColor,ann="ON - Normal on setting of how maya deals with Joint scale")
    cmds.button(l='OFF',    c='UI.CharSetUp_Skeleton_ScaleCompensate(0)',bgc=UI_ChangeColorTest(ButtonColor,[3,0,0]),ann="OFF - great for scaling entire or character or parts")
    Test = cmds.checkBox("CheckBox_ScaleCompensate_Hierarchy",label="Hierarchy",ann="Select entire Hierarchy of joints from current selection to be included in the Scale compensate setting")
    cmds.setParent( '..' )
    cmds.separator(h=5)

    
    cmds.setParent( '..' )
    
def CharSetUp_Skeleton_UI_IGJoints(ButtonColor):   
    FrameLayout = cmds.frameLayout(label='IG Joints',cl = True, collapsable = True,bv=True)
    
    cmds.rowColumnLayout(numberOfColumns=2,cal=[2,"center"])
    cmds.button(l="Create IG Joints ",c='Skeleton.CreateIGJNTS()',bgc= ButtonColor,ann="Duplicates selected Skeleton Chain, changes suffix from RigJNT to JNT and places new skeleton in the IG_JNTS Node")
    cmds.button(l="Remove `End_JNTS`",c='Skeleton.RemoveEndJNTS("JNT")',bgc= ButtonColor,ann="removes extra Joints that have an 'End_'")
    cmds.setParent( '..' )
    cmds.button(l="Connect JNTS to RigJNTS",c='Skeleton.Connect_JNTS()',bgc= ButtonColor,ann="Connects/Constraints IG_JNTS with Rig_JNTS: Must selected top Joint of IG Joint skeleton")
    CharSetUp_LabelJoints_Create(ButtonColor)
    cmds.setParent( '..' )


def Normals_Display():
    Value   = cmds.intSlider("IntSlider_NormalsDisplay",q=True,value=True)
    List    = cmds.ls(sl=True,type="transform")
    for Geo in List:
        #get shape node... 
        GeoShape = cmds.listRelatives(Geo,c=True,type="shape")[0]
        if Value == 0:
            cmds.setAttr(GeoShape + ".displayNormal",0)
        else:
            cmds.setAttr(GeoShape + ".displayNormal",1)
            cmds.polyOptions(Geo,sn = Value)  
               
def Skining_ReverseNomals():
    List = cmds.ls(sl=True,type="transform")
    for Geo in List:
        Skinning.ReverseNormals(Geo)


def CopySkinWeightsBy():
    Temp = cmds.radioButtonGrp("radioButtonGRP_SkinningVertNameVSWorldSpace",q=True,sl=True)
   
    if Temp == 2:
        return True
    else:
        return False 


def Skining_CleanHistory():
    List = cmds.ls(sl=True,type="transform")

    for Geo in List:
        Skinning.CleanUpHistory_ReSkin(Geo,CopySkinWeightsBy())


def Skining_CleanHistory_ReSkinOriginal():
    List = cmds.ls(sl=True,type="transform")
   
    for Geo in List:
        #- duplicate mesh and copy skinning info
        newGeo = Skinning.CleanUpHistory_ReSkin(Geo,CopySkinWeightsBy(),False)
        #- unbind original. reskin and copy weights.
        import pymel.core as pm
        pm.skinCluster(Geo, edit=True, unbind=True)
        TempGeo          = cmds.duplicate(Geo,n= Geo + "_NewTemp")[0]
        cmds.delete(Geo)
        cmds.rename(TempGeo,Geo)
        Skinning.CleanUpHistory_ReSkin(newGeo,True,True,Geo)
        
def Skinning_CopyWeights_MeshList_Options():
    Options = cmds.radioButtonGrp("radioButtonGRP_CopySkinningBySelOrPrefix",q=True,sl=True)
    print ("Options : ", Options )
    ONOFF = False
    if Options == 2 :
        ONOFF = True
    print (ONOFF)
    OriginalPrefix =    cmds.textField("TextField_SkinningOriginalGeo_Prefix",e=True,en=ONOFF)
    NewPrefix =         cmds.textField("TextField_SkinningNewGeo_Prefix"     ,e=True,en=ONOFF)
    
def Skining_CopyWeights_MeshList():
    List = CharSetup_FilterSelectionToMesh()
    
    
    Options = cmds.radioButtonGrp("radioButtonGRP_CopySkinningBySelOrPrefix",q=True,sl=True)
    print ("Options :", Options)
    if (Options == 2):
        print ("Skinning by Prefix: ")
        OriginalPrefix =    cmds.textField("TextField_SkinningOriginalGeo_Prefix",q=True,text=True,en=True)
        NewPrefix =         cmds.textField("TextField_SkinningNewGeo_Prefix"     ,q=True,text=True,en=True)
        for Geo in List:
            #get suffix
            Suffix = ""
            if(Geo.startswith( OriginalPrefix )):
                Suffix = Geo[len(OriginalPrefix):]
            if(Geo.startswith( NewPrefix )):
                Suffix = Geo[len(NewPrefix):]
            
            print ("Selected:",Geo)
            print ("Original:",OriginalPrefix + Suffix)
            print ("New     :",NewPrefix + Suffix)
            if(cmds.objExists(OriginalPrefix + Suffix) and cmds.objExists(NewPrefix + Suffix)):
            		print (OriginalPrefix + Suffix + " & " + NewPrefix + Suffix + " exists")
            		Skinning.CleanUpHistory_ReSkin(OriginalPrefix + Suffix ,CopySkinWeightsBy(),False,NewPrefix + Suffix)
            else:
            		print (OriginalPrefix + Suffix + " & " + NewPrefix + Suffix + " DONT exists skinning skipped") 
    else:
    	print ("Skinning by selection")
        OriginalPrefix =    cmds.textField("TextField_SkinningOriginalGeo_Prefix",q=True,text=True,en=False)
        NewPrefix =         cmds.textField("TextField_SkinningNewGeo_Prefix"     ,q=True,text=True,en=False)
        SkinnedGeo = List.pop(0)
        for Geo in List:
            Skinning.CleanUpHistory_ReSkin(SkinnedGeo ,CopySkinWeightsBy(),False,Geo)
    
def Skining_CombineSkinMesh():
    OriName = cmds.ls(sl=True)[0]
    cmds.select(hi=True)
    geometry = cmds.ls(sl=True,geometry=True)
    transforms = cmds.listRelatives(geometry, p=True, path=True)
    cmds.select(transforms, r=True)
    
    List = cmds.ls(sl=True,type="transform")
    
    NewGeo = []
    for Geo in List:
        NewGeo.append(Skinning.CleanUpHistory_ReSkin(Geo,DeleteOriginal=False))

    NewComboGeo = Skinning.CombineSkinnedMesh_KeepOriginal(OriName + "_New",NewGeo)
    hasParent = bool(cmds.listRelatives(OriName, parent=True))
    if(hasParent):
        Parent = cmds.listRelatives(OriName, parent=True)
        cmds.parent(NewComboGeo,Parent)
    

def CharSetUp_GEOSelectability(Value):
    GEOGRP = "IG_GEO"
    CharSetUp_MakeRef(Value,[GEOGRP])
    
def CharSetUp_Skeleton_UI_ReverseNormals(ButtonColor):
    FrameLayout = cmds.frameLayout(label='Reverse Normals',cl = True, collapsable = True,bv=True)
    cmds.text( label='Toggle Geo GRP Selectionability')
    cmds.checkBox("CheckBox_GeoRef",label="Make Geo selectable", ofc = 'UI.CharSetUp_GEOSelectability(1)',onc='UI.CharSetUp_GEOSelectability(0)',ann= "turn on ot set the IG_GEO GRP selectable, so that you can select  any geo inside that grp.")
    cmds.text("TextField_DisplayNormalSize",label="Display: Change Normal Size",align='left',ann="For selected Mesh, Use slider to change the dispaly of the Normals")
    Test = cmds.intSlider("IntSlider_NormalsDisplay",dc='UI.Normals_Display()', minValue=0, maxValue=100, value=0,ann="For selected Mesh, Use slider to change the dispaly of the Normals")
    cmds.separator(h=5)
    cmds.button(l='Reverse Normals', c='UI.Skining_ReverseNomals()',bgc= ButtonColor,ann="Normals of Selected Objects will be reversed")
    cmds.setParent( '..' )
    
    
def CharSetUp_Skeleton_UI_Skinning(ButtonColor):   
    FrameLayout = cmds.frameLayout(label='Mesh Skinning & Influence Tools',cl = True, collapsable = True,bv=True)
    RBOptions = ['World Space','Vert Name']
    RButton = cmds.radioButtonGrp("radioButtonGRP_SkinningVertNameVSWorldSpace",labelArray2=RBOptions, numberOfRadioButtons=2,select=2,ann="Copy skins by the position of the verts in space or by vert Name")
    cmds.button(l='Copy Skins Weights (by vert Name)', c='Skinning.CopyWeights_PerVertName()',bgc= ButtonColor,ann="Copy Weight info from first selected Mesh to second selected mesh: Must have 2 Skinned Meshes, Both Meshes Vert order/count must be exact. Could be differnt position or could have adjustments to mesh as long as the Vert count remains the same: great for copying weights from one mesh to the other, especially for adjusted meshes")
    
    cmds.button(l='Remove History (Re-Skin mesh)', c='UI.Skining_CleanHistory()',bgc= ButtonColor,ann="Select Mesh to cleanup, this will create a duplicate and skin the duplicate with the weights of the original, remove the orignal - leaving you with a clean mesh with no extra history")
    
    cmds.button(l='Remove History (Un-bind & Re-Bind mesh)', c='UI.Skining_CleanHistory_ReSkinOriginal()',bgc= (1,.85,.25),ann="Select Mesh to cleanup, this will create a duplicate and skin the duplicate with the weights of the original, unbind the orignal so that mesh goes back to it's original position and bind original and copy skin weights again to it then deleting copied mesh. - leaving you with a clean mesh with no extra history")
    
    cmds.separator(h=5)
    Title = "Copy by Selection or by Name"
    RBOptions = ['Selection (1st is Origin)','Prefix/List']
    RButton = cmds.radioButtonGrp("radioButtonGRP_CopySkinningBySelOrPrefix",labelArray2=RBOptions, numberOfRadioButtons=2,select=1,cc="UI.Skinning_CopyWeights_MeshList_Options()",ann="by Prefix; determing Origin and target by prefix, By selection Determine Origin by 1st Selected, all subsequent selected get the 1st selected skinning")
    
    
    cmds.text( label='List of Meshes to skin',ann="Select list of original or New Mesh, Add prefix info for both, - this will skinn new mesh and copy weights by options selected. by vert order or by points in space")
    CharSetup_LabelTextField("SkinningOriginalGeo_Prefix","Original Prefix","","add prefix",False,65)
    CharSetup_LabelTextField("SkinningNewGeo_Prefix","Target Prefix","","add prefix",False,65)
    cmds.button(l='Copy Weights to New Meshes', c='UI.Skining_CopyWeights_MeshList()',bgc= (1,.85,.25),ann="Select list of original or New Mesh, Add prefix info for both, - this will skinn new mesh and copy weights by options selected. by vert order or by points in space")
    
    cmds.separator(h=5)
    
    cmds.button(l='Duplicate & Combine Skinned Mesh', c='UI.Skining_CombineSkinMesh()',bgc= ButtonColor,ann="Duplicate selected skinned mesh, copy the skin weights from the original and combine all selected pieces")
    
    cmds.separator(h=5)
    cmds.text("TextField_Connectmesh_byName",label="Connect Mesh by Name: choose type",align='left',ann="choose type of connection to make, selected desired meshes and run.")
    Title = "Influence Type"
    RBOptions = ['Constraint','Bind/Skin']
    RButton = cmds.radioButtonGrp("radioButtonGRP_ConnectMesh_ByName",labelArray2=RBOptions, numberOfRadioButtons=2,select=2,ann="Select what type of influence will be used when creating an influence for the seleted Mesh(es)")
    Title = "Maintain Offset"
    Test = cmds.checkBox("checkBox_ConstrainMO",label=Title,ann="If checked when constraining will maintain offset and the mesh will not move")
    cmds.button(l='Create Mesh influence by Name', c='UI.CharSetup_ConnectMesh_byName()',bgc= ButtonColor,ann="Connects Mesh 100 % to Joint with same name, influence type will be determined by the Options selected: Joint needs to have the same name plus the '_JNT' suffix , if there isnt a joint witht the same name the Mesh will not be connected")
    cmds.separator(h=5)
    cmds.button(l='Select Verts effected', c='Skinning.SelectVertsInfluencedByJNTS()',bgc= ButtonColor,ann="Selects Verts that are influenced by selected Joints: 1st Select the Mesh, then selecte the Joints")
    #cmds.button(l='Constrain Selected Mesh with matching Joint', c='UI.CharSetup_Constrain2MatchingJoints()',bgc= ButtonColor,ann="Constrains Mesh to Joint with same name: Joint will have the same name plus the '_JNT' suffix")
    
    cmds.setParent( '..' )
    CharSetUp_Skeleton_UI_ReverseNormals(ButtonColor)
    cmds.setParent( '..' )
    
    
    
def CharSetUp_Skeleton_UI(UIName):
    BackgroundColor = [0.3235294342041016, 0.3470588445663452, 0.3470588445663452]
    ButtonColor = UI_ColorSettings(BackgroundColor,1)[0]
    ButtonColor = [0.4215686440467834, 0.5568628191947937, 0.5764706611633301]
    Layout = cmds.rowColumnLayout()#bgc=tuple(BackgroundColor))
    
    CharSetUp_Skeleton_UI_Display(ButtonColor)
    
    CharSetUp_Skeleton_UI_SkelTemplate_Create(ButtonColor)
    
    CharSetUp_Skeleton_UI_Edit(ButtonColor)
    CharSetUp_Skeleton_UI_IGJoints(ButtonColor)
    CharSetUp_Skeleton_UI_Skinning(ButtonColor)
    return Layout

def GetLimbs_Selected():
    LIMBS = []
    if(cmds.checkBox("checkBox_IKLimb_Arm" ,q=True,v=True)):
        PVFlip      = cmds.checkBox("checkBox_PVFlip_Arm"           ,q=True,v=True)
        BigFootFix = cmds.checkBox("checkBox_BigFootFix_Arm"   ,q=True,v=True)
        LIMBS.append(["Arm",PVFlip,BigFootFix])

    if (cmds.checkBox("checkBox_IKLimb_Leg" ,q=True,v=True)):
        PVFlip      = cmds.checkBox("checkBox_PVFlip_Leg"           ,q=True,v=True)
        BigFootFix = cmds.checkBox("checkBox_BigFootFix_Leg"   ,q=True,v=True)
        LIMBS.append(["Leg",PVFlip,BigFootFix])

    return LIMBS

def RiggingIK_Create():
    #PVFlip      = cmds.checkBox("checkBox_PVFlip"                   ,q=True,v=True)
    #RollFootFix = cmds.checkBox("checkBox_RollingFootFix"           ,q=True,v=True)
    IncludeFK   = cmds.checkBox("checkBox_IncluedFK"                ,q=True,v=True)
    CharType    = cmds.radioButtonGrp("radioButtonGrp_CharType"     ,q=True,select=True)
    ZeroJoints  = cmds.radioButtonGrp("radioButtonGrp_ZeroJoints"   ,q=True,select=True)
    ExtraParentSwitchLimbs = False
    LIMBS = GetLimbs_Selected()

    CharSetUp_SceneUnits_Set()
    print ("LIMBS : ", LIMBS)
    for LimbList in LIMBS:
        Limb = LimbList[0]
        PVFlip = LimbList[1]
        BigFootFix = LimbList[2]
        Rigging_IK.IK_Setup(Limb,CharType,IncludeFK,BigFootFix,ExtraParentSwitchLimbs,ZeroJoints,PVFlip)

def Get_ReverseFootLimbs_List(LimbType):
        String = ', '.join(Rigging_IK.ReverseFootLimbs(LimbType))
        return String

def Delete_Limb():
    LIMBS       = GetLimbs_Selected()
    DetachList  = True
    for Limb in LIMBS:
        Rigging_IK.IK_KeepCurves(Limb,DetachList)


def PythonDebug():
    import ptvsd
    ptvsd.enable_attach("my_secret", address = ('0.0.0.0', 3000))

def CharSetUp_PrintScreen():
    Test = cmds.checkBox("checkBox_PrintInfo",label="Print Script Info",v=False,bgc=(1,.85,.25),cc= "UI.CharSetUp_Set_Print()",ann="will print extra info if needed when running scripts")
    cmds.button(l='Turn On Python debug', c='UI.PythonDebug()',bgc=(0.556,0.804,0.611))
    

def CharSetUp_SceneUnits(ButtonColor):
    Title = 'Scene Units'
    RButton = cmds.radioButtonGrp("radioButtonGrp_SceneUnit",label=Title, labelArray2=['cm', 'm'], numberOfRadioButtons=2,select=2,cw3=(len(Title)*6,50,30),ann="WIP: not working - should effect the scale of the controller when created.. ")

def CharSetUp_SceneUnits_Set():
    SceneUnits  = cmds.radioButtonGrp("radioButtonGrp_SceneUnit"    ,q=True,select=True)
    SetSceneUnit = MASTER.Scene_UnitSettings_Set(SceneUnits-1,False)
    
def CharSetUp_BASECTRLS_Setup():
    CharSetUp_SceneUnits_Set()
    Rigging.BASECTRLS_Setup()

def CharSetUp_BASECTRLS_VisibilitySwitch_Setup():
    Include_Geo = cmds.checkBox("checkBox_VisGEO",q=True,v=True)
    Rigging.BASECTRL_VisibilitySwitch(Include_Geo,"CHAR_CTRL","CTRLS_GRP")

def CharSetUp_BASECTRLS_Visibility_BySelection_Setup():
    Include_Geo = cmds.checkBox("checkBox_VisGEO",q=True,v=True)
    Rigging.BASECTRL_VisibilitySwitch(Include_Geo)


#####################################################
################ Rigging UI  ########################
def CharSetUp_CreateFKCTRL_Mirror():
    MirrorFKCTRL    = cmds.checkBox("FKCurve_FKCTRLMirror_SELECT",q=True,v=True)
    #print "Mirror"
    #print MirrorFKCTRL
    if(MirrorFKCTRL):
        List = cmds.ls(sl=True)
        NewList = []
        for Node in List:
            NewList.append(Node)
            Mirror = Rigging.CheckSide(Node)
            #print "CheckSide"
            #print Mirror
            if(not Mirror[2] == None):
                #print "INNNNN"
                #print Mirror[2]
                NewList.append(Mirror[2])
        #print NewList
        cmds.select(NewList)
    
def CharSetUp_CreateFKCTRL():
    #print ("TEST ")
    #print cmds.ls(sl=True)
    CharSetUp_SceneUnits_Set()
    CharSetUp_CreateFKCTRL_Mirror()
    #print ("TEST 2")
    #print cmds.ls(sl=True)
    if(not cmds.checkBox("FKCurve_FKCTRL_SELECT",q=True,v=True)):
        CharSetUp_OnlyCurve_Create()
    if( cmds.checkBox("FKCurve_FKCTRL_SELECT",q=True,v=True) ):
        CharSetUp_FK_CTRL_Setup()
    #if(cmds.checkBox("FKCurve_ParentSwitchShadow_SELECT",q=True,v=True)):
    #    CharSetUp_FK_CTRL_Setup()
    #if(cmds.checkBox("FKCurve_ParentSwitchMultiNode_SELECT",q=True,v=True)):
    #    CharSetUp_FK_CTRL_Setup()

   


        
def CharSetUp_DropDownMenu(Name,List,description = "needs a description",ButtonColor = None):
    OM = []
    cmds.rowColumnLayout(numberOfColumns=2)
    cmds.text(l=Name,ann=description)
    if ButtonColor == None:
        OM = cmds.optionMenu(Name + "_Menu",ann=description)
    else:
        OM = cmds.optionMenu(Name + "_Menu",bgc=ButtonColor,ann=description)
    for L in List:
        cmds.menuItem(  label=L)
    
    cmds.setParent( '..' )
    print ("MyOPtionMenu")
    print (OM)

def CharSetup_Rigging_UI_SubCTRL():
    cmds.rowColumnLayout(numberOfColumns=2)
    Title = "Add Sub JNT"
    cmds.checkBox("FKCurve_SubJNT_SELECT",label=Title,ann="Check if you want to add a sub joint to the current selected joint/node: great for creating a sub controller when rigging new ojbect but also for already rigged objects")
    
    Title = "Sub CTRL Only"
    cmds.checkBox("FKCurve_SubCTRLOnly_SELECT",label=Title,ann="Check if you want to by pass creating a controller for the selected joint/ctrl curve and create sub ctrl only: great if you have already rigged the selected object and just want to add a sub controller")
    cmds.setParent( '..' )
    Name = "For SubJNT"
    List = Curves.Type()
    CharSetUp_DropDownMenu(Name,List,"Select curve shape type for creating control curve")
    
    
    
def CharSetUp_Rigging_UI_CreateCTRLCurves(ButtonColor):
    
    #create CTRL Curves.. 
    FrameLayout = cmds.frameLayout(label='Create FK CTRLS',cl = True, collapsable = True,bv=True)
    Name = "Curve Shape"
    List = Curves.Type()
    CharSetUp_DropDownMenu(Name,List,"Select curve shape type for creating control curve")
    cmds.text("TextField_FKCTRL_Type",label="FK Control Type",align='center',ann="Select the type of FK Control to create")
    Title = "FK CTRL"
    Test = cmds.checkBox("FKCurve_FKCTRL_SELECT",label=Title,v=True,ann="Create an FK controller that will drive selected objects, or re-rig selected Controller")
    Title = "Mirror Selection"
    Test = cmds.checkBox("FKCurve_FKCTRLMirror_SELECT",label=Title,v=True,ann="Rig both sides.. or rig even if only one side is selected")
    Title = "Shadow CTRL"
    cmds.checkBox("FKCurve_ParentSwitchShadow_SELECT",label=Title,ann="Create an FK controller that will be driven to some extent by the hips/Cog of the character, but not effected on the Translate Y")
    Title = "Multi Node Switch CTRL"
    cmds.checkBox("FKCurve_ParentSwitchMultiNode_SELECT",label=Title,ann="Creat an FK controller that drives other Joints, 1st selected object acts as parent of other selected joints/nodes - (child nodes will not have a control curve)- . also has a value to show all child nodes or to hide/scale to 0. this is good for swapping of body parts, meshes of a rig (like different shape eyes.weapons.. ect) each body part should be driven/skinned 100 percent by one of the child joints")
    cmds.separator(h=1)
    cmds.text("TextField_FKCTRL_Type_Extras",label=" Add other Controls to selection",align='center',ann="Select the type of extra FK Controls to create")
    CharSetup_Rigging_UI_SubCTRL()
    Title = "Create Parent CTRL"
    cmds.checkBox("FKCurve_ParentCTRL",label=Title,ann=" WIP : nothing yet.. - meant for....creating a parent ctrL.. need to re- think this. ")
    cmds.separator(h=1)
    cmds.text("TextField_FKCTRL_SpaceSwitchingOptions",label=" Space Switching Options",align='center',ann="Select the type of extra FK Controls to create")
    
    Title = "Basic"
    cmds.checkBox("FKCurve_ParentSwitch_SELECT",label=Title,ann="Add a space/parent switch options - basic parent switch options - (world,Char-Main controller-,Parent or currently selected object)")
    Title = "Spine"
    cmds.checkBox("FKCurve_ParentSwitchSpine_SELECT",label=Title,ann="Add a space/parent switch options - adding the spine of the character (Hips,chest,Head)")
    Title = "Extra Limbs/Nodes"
    cmds.checkBox("FKCurve_ParentSwitchLimbs_SELECT",label=Title,ann="Add a space/parent switch options - adding the Extra nodes of the character (anything in the ParentSwitch_GRP)")
    cmds.separator(h=1)
    cmds.text("TextField_FKCTRL_OrientationSetup",label=" Control orientation & component display",align='center',ann="Select the type of extra FK Controls to create")
    
    Title = 'CTRL Orient'
    Note    = "Selection to define what will be the CTRL's created orientation will it match the JNT, world or Previous/current CTRL orientation."
    Note1   = "Match the JNT's orientation"
    Note2   = "Match the Worlds's orientation"
    Note3   = "Match the Current CTRL's orientation - good for re-regging multiple FK controls with different orientation types. " 
    RButton = cmds.radioButtonGrp("FKCurve_MatchOrient_SELECT",label=Title, labelArray3=['JNT', 'World',"Ctrl"], numberOfRadioButtons=3,select=1,cw4=(len(Title)*6,40,50,30),ann=Note,an1 = Note1,an2=Note2,an3=Note3)
    Title = 'Display FK Axis Alignment'
    RButton = cmds.radioButtonGrp("FKCurve_AXIS_SELECT",label=Title, labelArray3=['X', 'Y', 'Z'], numberOfRadioButtons=3,select=1,cw4=(len(Title)*6,30,30,30),ann="Select what orientation the component/Display of curve will be oriented - mostly for primitives like the circle and what direction the curve will be created in")
    cmds.separator(h=1)
    cmds.button(l='Create CTRL Curve', c='UI.CharSetUp_CreateFKCTRL()',bgc =ButtonColor,ann="run to creat Control curve for rigging nodes.. selected Joints or already selected rigged Control curves: look at the available options for rigging.")
    cmds.separator(h=1)
    cmds.button(l='Squash & Stretch Attr', c='UI.CharSetUp_SquashStretch_Switch()',bgc =ButtonColor,ann="WIP-- great for adding a squash and stretch attribute on CTRL..")
    cmds.separator(h=1)
    cmds.rowColumnLayout(numberOfColumns=2,cal=[(1,"center"),(2,"center")],cs=[(1,2),(2,2),(3,2)])
    
    cmds.button(l='Disconnect FK CTRL', c='UI.CharSetUp_FK_CTRL_Disconnect()',bgc =ButtonColor,ann="Disconnect selected FK controller(s) so that its not a child of current parent, still drives the joints its connected to.")
    cmds.button(l='Delete FK CTRL', c='UI.CharSetUp_FK_CTRL_Delete()',bgc =ButtonColor,ann="Remove selected FK controller(s) and entire FK control group")
    cmds.setParent( '..' )
    cmds.setParent( '..' )



def CharSetUp_CTRL_VisSwitch():
    Attribute = cmds.textField("TextField_VisSwitchAttributeName",q=True,text=True)
    Prefix = cmds.textField("TextField_VisSwitchPrefixRemove",q=True,text=True)
    List = cmds.ls(sl=True)
    print ("Selection: ")
    print (List)
    Driver = List[0]
    List[0] = "ALL"
    #check to see if Attribute Exists Delete and Re-Create
    print (List)
    print (Attribute)
    strList = map( str, List)
    strList = map( lambda x: x.replace( Prefix, ''), strList)
    print (strList)
    Rigging.Create_Attribute(Driver,Attribute,AttributeInfo=["enum",":".join(strList)],Keyable=False)
    List.pop(0)

    print (List)
    Count = 1
    for Driven in List:
        VisList = []
        L0,L1, L2, L3, L4 = [0,1], [Count-1,0], [Count,1],[Count+1,0],[1,0]
        if Count == 1:
            VisList = [L0,L2, L3]
        elif Count == len(List):
            VisList = [L0,L1, L2,L4]
        else:
            VisList = [L0,L1,L2,L3,L4]
        Count +=1
        import unicodedata
        DrivenText = unicodedata.normalize('NFKD', Driven).encode('ascii','ignore')
        Rigging.SetDriven_AttributesSetup(Driver,Attribute,DrivenText,"visibility",VisList,1,KeyTangent=["flat","step"])
        
            


def CharSetUp_Rigging_UI_OtherCTRLS(ButtonColor):
    print ("test")
    #create CTRL Curves.. 
    FrameLayout = cmds.frameLayout(label='CTRLs Misc',cl = True, collapsable = True,bv=True)
    cmds.text(l="Attribute Name")
    cmds.textField("TextField_VisSwitchAttributeName",ann="name of Attribute for selected Controller, if already has attribute will update attribute")
    cmds.text(l="Prefix to Remove")
    cmds.textField("TextField_VisSwitchPrefixRemove",ann="prefix to remove from selected groups so that the list is cleaner")
    cmds.button(l="Vis Switch",   c='UI.CharSetUp_CTRL_VisSwitch()',bgc =ButtonColor,ann="Select Driver, select Driven, will create attribute of selected items to switch visibility")
    
    cmds.setParent( '..' )

def CharSetUp_Rigging_UI_ChangeSelectedType(ButtonColor):
    FrameLayout = cmds.frameLayout(label='Switch Selection Type',cl = False, collapsable = True,bv=True,ann="switches selection from current object if it ends with CTRL,JNT,RigJNT - to the specific type: great from switching selection from JNT RigJNT and CTRL's")
    
    cmds.rowColumnLayout(numberOfColumns=3,cal=[(1,"center"),(2,"center"),(3,"center")],cs=[(1,2),(2,2),(3,2)],cw=[(1,55),(2,55),(3,55)])
    cmds.button(l="CTRL",   c='Rigging.ChangeSelectedType("CTRL")',bgc =ButtonColor,ann="Switch to Controller")
    cmds.button(l="JNT",    c='Rigging.ChangeSelectedType("JNT")',bgc =ButtonColor,ann="Switch to In Game Joint")
    cmds.button(l="RigJNT", c='Rigging.ChangeSelectedType("RigJNT")',bgc =ButtonColor,ann="Switch to Rig Joint")
    
    cmds.setParent( '..' )
    cmds.setParent( '..' )
    
def CharSetUp_Rigging_UI_FKIK(ButtonColor):
    FrameLayout = cmds.frameLayout(label='IK legs/Arms setup',cl = True, collapsable = True,bv=True,ebg=True,bgc=(0.556,0.404,0.311),hlc=(0.856,0.804,0.811),ann="IK/FK limb set up: setup needs to have very specific joint names to work.")
    Title = 'Char Type'
    RButton = cmds.radioButtonGrp("radioButtonGrp_CharType",label=Title, labelArray2=['Biped', 'Quadruped'], numberOfRadioButtons=2,select=1,cw3=(len(Title)*6,50,30),bgc=ButtonColor,ann="select type of Character, may affect the way the Legs PV gets set up.. may need to double check the description options to be more accurate with what it does.. ")
    cmds.separator(h=1)
    #cmds.rowColumnLayout(numberOfColumns=2)
    #LabelName = 'Limbs :'
    #CB_Options = ['Arms', 'Legs']
    #offset = 12
    #cmds.checkBoxGrp("checkBox_IKLimbs",numberOfCheckBoxes=2, label=LabelName, labelArray2=CB_Options,cl3=("left","left","left"),cw3=[len(LabelName) * 7, len(CB_Options[0]) * offset,len(CB_Options[1]) * offset])
    #cmds.checkBox("checkBox_IKArms",label="Arms",v=True,bgc=(0.556,0.404,0.311),hlc=(0.856,0.804,0.811),ann="Check to Rig Arms: will look for specific naming convention")
    #cmds.checkBox("checkBox_IKLegs",label="Legs",v=True,ann="Check To Rig Legs: will look for specific naming convention of legs..")
    #cmds.setParent( '..' )
    #LabelName = 'Pole Vector flip :'
    #CB_Options = ['Arms', 'Legs']
    #offset = 12
    #cmds.checkBoxGrp("checkBox_IKLimbs",numberOfCheckBoxes=2, label=LabelName, labelArray2=CB_Options,cl3=("left","left","left"),cw3=[len(LabelName) * 7, len(CB_Options[0]) * offset,len(CB_Options[1]) * offset])
    cmds.rowColumnLayout(numberOfColumns=2,cal=[(1,"center"),(2,"center")],cs=[(1,2),(2,2)])
    cmds.checkBox("checkBox_IKLimb_Arm",label="Arm",v=False,ann="Rig Arm")
    cmds.checkBox("checkBox_IKLimb_Leg",label="Leg",v=False,ann="Rig Leg")
    
    cmds.checkBox("checkBox_PVFlip_Arm",label="PV Flip",v=False,ann="Arm - check if you want the Pole Vector to change to be opposite of current location")
    cmds.checkBox("checkBox_PVFlip_Leg",label="PV Flip",v=False,ann="leg - check if you want the Pole Vector to change to be opposite of current location")
    
    cmds.checkBox("checkBox_BigFootFix_Arm",label="Big Foot Fix",v=False,ann="Rolling Foot Fix - Add Proxy Arms - if the angle of the ankle and the palm of hand is less than 45 degrees there will be issues for the feet peeling without sliding.. this adds a proxy joint to adjust for that and make the hand peeling less off... may need to find a better solution later.")
    cmds.checkBox("checkBox_BigFootFix_Leg",label="Big Foot Fix",v=False,ann="Rolling Foot Fix - Add Proxy Legs - if the angle of the ankle and the ball of foot is less than 45 degrees there will be issues for the feet peeling without sliding.. this adds a proxy joint to adjust for that and make the foot peeling less off... may need to find a better solution later.")
    
    cmds.setParent( '..' )
    
    #cmds.checkBox("checkBox_RollingFootFix",label="Rolling Foot Fix - Add Proxy Legs",v=False,ann="if the angle of the ankle and the ball of foot is less than 45 degrees there will be issues for the feet peeling without sliding.. this adds a proxy joint to adjust for that and make the foot peeling less off... may need to find a better solution later.")
    cmds.separator(h=1)
    cmds.checkBox("checkBox_IncluedFK",label="Include FK CTRLS",v=True,ann="Check if you want to also include the FK controls when rigging.")
    cmds.checkBox("checkBox_IncluedFKSub",label="Include Sub CTRLS",v=True,ann="WIP.. not working yet... Check if you want to also include the Sub controls when rigging.")

    #cmds.checkBox("checkBox_KeepPosZeroRot",label="Zero Rotate Joints - reset to original position",v=True)
    #cmds.checkBox("checkBox_IncluedFK",label="Zero Rotate Joints - Keep position and Orientation",v=True)
    cmds.button(l='Create IK CTRL`s', c='UI.RiggingIK_Create()',bgc =ButtonColor,ann="Create the IK Joints with selected options..")
    cmds.button(    l="Delete CTRL's (Keep Curves)", c='UI.Delete_Limb()',bgc =UI_ChangeColorTest(ButtonColor,[3,0,0]),ann="Deletes the IK/FK leg setup of whatever is selected in the options above Arm or Leg")
    
    FrameLayout = cmds.frameLayout(label="Reset/Fix Joint Rotations", cl = True, collapsable = True,ann="sometimes the joints are not zeroed out and they need to be for the IK setup to work correctly.. this resets all joints so they have no rotation values.. look at options to see how the Joints are effected.. ")
    RButton = cmds.radioButtonGrp("radioButtonGrp_ZeroJoints",vr=True,labelArray2=['reset position', 'Keep position & Orientation'], numberOfRadioButtons=2,select=1,cw3=(len(Title)*6,50,30),ann="reset Position: zeros joints where they are.. meaning they may move if they have rotation values. Keep position & orientation: this will kee the placement and the orientation, but still zero out the joints values")
    cmds.setParent( '..' )
    
    FrameLayout = cmds.frameLayout(label='Limb Naming conventions',cl = True, collapsable = True,bv=True,ann="IK/FK limb List of naming convetions")
    cmds.text(      l=Get_ReverseFootLimbs_List("Arm"),ann="List of naming convetion of arm limb")
    cmds.text(      l=Rigging_IK.Get_LimbPivot("Arm"),ann="List of naming convetion of hand pivot joint")
    cmds.separator(h=10)
    cmds.text(      l=Get_ReverseFootLimbs_List("Leg"),ann="List of naming convetion of Leg limb")
    cmds.text(      l=Rigging_IK.Get_LimbPivot("Leg"),ann="List of naming convetion of foot pivot joint")
    cmds.setParent( '..' )
    

    cmds.setParent( '..' )




                    
def CharSetUp_Rigging_UI_RigBase(ButtonColor):
    FrameLayout = cmds.frameLayout(label='Rig Base Setup',cl = True, collapsable = True,bv=True,ebg=True,bgc=(0.556,0.404,0.311),hlc=(0.856,0.804,0.811),ann="Base Rig setup menu")
        
    Test = cmds.checkBox("checkBox_VisGEO",label="Included Geo",ann="inclued top nodes in GEO Group")
    cmds.button(l='Create RIG Base', c='UI.CharSetUp_BASECTRLS_Setup()',bgc =ButtonColor,ann="Create Base Control: sets the structure of the Rig set up.. (Nodes & Hiarchy ect, with base Control)")
    FrameLayout = cmds.frameLayout(label='Base Rig Cleanup',cl = True, collapsable = True,bv=True,ann="Cleanup Base Rig options")
    cmds.button(l='Rig Base - VisSwitch', c='UI.CharSetUp_BASECTRLS_VisibilitySwitch_Setup()',bgc =ButtonColor,ann="Adds, visibilit switch for controls, if base control does not have visibility switch setup")
    cmds.button(l='VisSwitch CTRL & Nodes/Attributes', c='UI.CharSetUp_BASECTRLS_Visibility_BySelection_Setup()',bgc =ButtonColor,ann="May need to add better description, Adds visibility switch to 1st selected node & controls all other nodes selected visibility")
    cmds.button(l='Add Space/Parent Switch Nodes', c='Rigging.LOC_Attributes_Set()',bgc =ButtonColor,ann="Add Space/Parent Switch nodes - base nodes to set up")
    
    cmds.button(l='Add HideCTRL LOC set up', c='Rigging.Base_HidLoc_GRP()',bgc =ButtonColor,ann="Add Hide LOC set up to hide/scale to zero joints")
    
    cmds.rowColumnLayout(numberOfColumns=2,cal=[(1,"center"),(2,"center")],cs=[(1,2),(2,2)])
    cmds.button(l='Hide Nodes ',            c='Rigging.HideNodes_Rig()',bgc =ButtonColor,ann="Cleanup - Hide nodes that should not appear. ")
    cmds.button(l='Connect CTRL GRP',       c='Rigging.CTRLS_GRP_Connect()',bgc =ButtonColor,ann="Connect Main CTRL to rest of Character")
    cmds.setParent( '..' )
    cmds.setParent( '..' )
    cmds.setParent( '..' )
    
def CharSetUp_Rigging_UI_ReRig(ButtonColor):
    FrameLayout = cmds.frameLayout(label='Re Rig Character Menu',cl = True, collapsable = True,bv=True,ebg=True,bgc=(0.556,0.404,0.311),hlc=(0.856,0.804,0.811),ann="Options for re-Rigging complete Character")
    cmds.rowColumnLayout(numberOfColumns=2,cal=[(1,"center"),(2,"center")],cs=[(1,2),(2,2)])
    cmds.button(l='Pre Scale Char Setup',   c='Rigging.Char_PreScaleSetup()',bgc =ButtonColor,ann="Run to Set up the Rig for Pre-Rig scalling")
    cmds.button(l='Set Scale Char',         c='Rigging.Char_SetScale()',bgc =ButtonColor,ann="After scaled character- run to re rig.")
    cmds.button(l='Hide Nodes ',            c='Rigging.HideNodes_Rig()',bgc =ButtonColor,ann="Cleanup - Hide nodes that should not appear. ")
    cmds.button(l='Connect CTRL GRP',       c='Rigging.CTRLS_GRP_Connect()',bgc =ButtonColor,ann="Connect Main CTRL to rest of Character")
    cmds.setParent( '..' )
    cmds.setParent( '..' )
    
    
def CharSetUp_Rigging_UI_Curves2CVs():
    FrameLayout = cmds.frameLayout(label='Curve to CVs',cl = False, collapsable = True,bv=True,ann="Switch Selection of Curves to CV's")
    cmds.rowColumnLayout(numberOfColumns=3,cal=[(1,"center"),(2,"center"),(3,"center")],cs=[(1,2),(2,2),(3,2)],cw=[(1,55),(2,55),(3,55)])
    cmds.button(l="All", c='Rigging.Curves2CVs("All")',bgc=(1,.5,1),ann="Select All CV's")
    cmds.button(l="Odd", c='Rigging.Curves2CVs("Odd")',bgc=(1,1,0),ann="Select Only Odd numbered CV's")
    cmds.button(l="Even's", c='Rigging.Curves2CVs("Even")',bgc=(.5,.5,1),ann="Select Only Even numbered CV's")
    cmds.setParent( '..' )
    cmds.setParent( '..' )
    
def CharSetUP_Rigging_UI_EditCurves(ButtonColor):
    
    FrameLayout = cmds.frameLayout(label='Edit Curves',cl = False, collapsable = True,bv=True,ann=" Curve Editing Tools: to help adjust the look and shape of the curves when creating the Character Controls")
    
    CharSetUp_Rigging_UI_Curves2CVs()
    CharSetUp_SetColor_UI()
    CharSetUp_Rotate()
    
    cmds.setParent( '..' )
    
  
def CharSetUp_Rigging_UI(UIName):
    BGColor = [0.4215686440467834, 0.4568628191947937, 0.4764706611633301]
    ButtonColor = [0.4215686440467834, 0.5568628191947937, 0.5764706611633301]
    HLColor     = [0.4215686440467834, 0.5568628191947937, 0.5764706611633301]
    Layout = cmds.rowColumnLayout()
    CharSetUp_PrintScreen()
    CharSetUp_SceneUnits(ButtonColor)
    CharSetUp_Rigging_UI_RigBase(ButtonColor)
    CharSetUp_Rigging_UI_ReRig(ButtonColor)
    CharSetUp_Rigging_UI_FKIK(ButtonColor)
    CharSetUp_Rigging_UI_CreateCTRLCurves(ButtonColor)

    CharSetUp_Rigging_UI_OtherCTRLS(ButtonColor)
    
    CharSetUp_Rigging_UI_ChangeSelectedType(ButtonColor)
    CharSetUP_Rigging_UI_EditCurves(ButtonColor)
    cmds.setParent( '..' )
    return Layout

    
#####################################################
################ Rigging UI  ########################


def Get_FrameCount():
    Min         = cmds.playbackOptions( q=True,min=True) 
    Max         = cmds.playbackOptions( q=True,max=True) 
    FrameCount  = Max - Min
    return FrameCount

def fps_Settings():
    import maya.mel as mel
    fps = mel.eval('float $fps = `currentTimeUnitToFPS`')   
    return fps

def UI_UpdateFrameCount():
    FrameCount      = Get_FrameCount()
    scene_fps = fps_Settings()
    print (scene_fps)
    #get fps
    TimeLength = 0 
    TimeLength2= 0
    if (FrameCount > 0):
        TimeLength = FrameCount / scene_fps
    if (FrameCount > 1):
            TimeLength2 = (FrameCount-1) / scene_fps
    FrameCountText  = "Frames: " + str(FrameCount) + " Half = " + str(FrameCount/2)
    FPSCountText    = "FPS : "+ str(scene_fps) + " Time: " + str(round(TimeLength,2)) + "...minus 1 frame: " + str(round(TimeLength2,2))
    TextNameField   = "text_FrameCount"
    TextNameField2   = "text_FPSCount"
    if (cmds.text(TextNameField,ex=True)):
        cmds.text(TextNameField,label=str(FrameCountText),edit = True)
        cmds.text(TextNameField2,label=str(FPSCountText),edit = True)
    else:
        cmds.text(TextNameField,label=str(FrameCountText),align='center',ann="Frame count on current time slider - updated when button pressed..")
        cmds.text(TextNameField2,label=str(FPSCountText),align='center',ann="FPS count on current time slider - updated when button pressed..")
        

def UI_PrefixTexfields(GetInfo=False):
    Original    = "TextField_PrefixOriginal"
    Target      = "TextField_PrefixTarget"
    UseOriginal = "checkBox_UseOriginal"
    UseTarget   = "checkBox_UseTarget"
    Info        = [Original,Target,UseOriginal,UseTarget]
    if(GetInfo):
        Info = []
        if(cmds.checkBox(UseOriginal    ,q=True,v=True)):
            Info.append(str(cmds.textField(Original     ,q=True,text=True)))
        if(cmds.checkBox(UseTarget      ,q=True,v=True)):
            Info.append(str(cmds.textField(Target       ,q=True,text=True)))
        
        

    #print "info...: ",Info
    #cmds.select("kdkdkdkdkdkd")    
    return Info


def SetSelectionPrefix():# not currently used?
    OriginalTextField = UI_PrefixTexfields()[0]
    cmds.textField(PrefixTexfields[0],ann="temp")


def UI_Prefix():
    PrefixTexfields = UI_PrefixTexfields()
    width = 58
    cmds.rowColumnLayout(numberOfColumns=2)
    cmds.checkBox(PrefixTexfields[2]    ,l="Original",bgc=(1,0.5,0),ann="Wip.. not working yet: use original or add option to use the string added in the field")
    
    #cmds.text( label='Original',w=width)
    PrefixOriginal = cmds.textField(PrefixTexfields[0],tx="",bgc=(1,0.5,0),ann="Wip.. not working yet: add original prefix/namespace here.. ")
    cmds.textField(PrefixTexfields[0],edit=True,w=width)
    cmds.checkBox(PrefixTexfields[3]    ,l="Target",bgc=(1,0.5,0),ann="Wip.. not working yet: use Target or add option to use the string added in the field")
    #cmds.text( label='Target',w=width)
    PrefixTarget = cmds.textField(PrefixTexfields[1],tx="",bgc=(1,0.5,0),ann="Wip.. not working yet: add Target prefix/namespace here.. ")
    cmds.textField(PrefixTarget,edit=True,w=width)
    cmds.setParent( '..' )

def UI_SetPrefix():
    Sel             = Anim.SaveSelection()
    Prefix          = Sel[0]
    List            = Sel[1]
    PrefixTexfields = UI_PrefixTexfields()
    cmds.textField(PrefixTexfields[0],edit=True,tx=Prefix)
    return Sel


def SavePoseButton():
    #UI_SetPrefix()
    Anim.SavePose(False,True)
    

def SaveSelectionButton():
    Sel = UI_SetPrefix()
    
    OriSel = []
    for S in Sel[1]:
        Pre = ""
        if Sel[0] != "":
            Pre = Sel[0] + ":"
        OriSel.append(Pre + S)
    
    print (OriSel)
    cmds.select(OriSel)
    

def SelectFromSavedButton():
    PrefixTexfields = UI_PrefixTexfields()
    Original        = cmds.textField(PrefixTexfields[0] ,q=True,text=True)
    Target          = cmds.textField(PrefixTexfields[1] ,q=True,text=True)      
    UseOriginal     = cmds.checkBox(PrefixTexfields[2]  ,q=True,v=True) 
    UseTarget       = cmds.checkBox(PrefixTexfields[3]  ,q=True,v=True) 
    List            = Anim.GetSelection()
    Prefix          = []
    if UseOriginal:
        Prefix.append(Original)
    if UseTarget:
        Prefix.append(Target)
    
    NewList = []
    for P in Prefix:
        for L in List:
            if(cmds.objExists(P + ":" + L)):
                NewList.append(P + ":" + L)
    if (len(NewList) > 0):  
        cmds.select(NewList)
    

def UI_SaveSelection():

    FrameLayout = cmds.frameLayout(label='Save Selection',cl = True, collapsable = True,bv=True,w=60,bgc=(1,0.5,.3),ann=" - WIP: still need to fix this... ")
    cmds.button(l='Save Selection',     c='UI.SaveSelectionButton()',w=30,ann="Saves selection list into a temporary node..")
    cmds.button(l='Select from Saved',  c='UI.SelectFromSavedButton()',w=30,ann="Selects from temporary created node that has the list of previously selected nodes")
    UI_Prefix()
    UI_TransferKeys()
    cmds.setParent( '..' )



def TransferAnimation():
    #get the info from the the ui..
    List = cmds.ls(sl=True)
    collection1 = cmds.radioCollection("radioButtonGrp_TransferAnim_How",q=True,sl=True)
    collection2 = cmds.radioCollection("radioButtonGrp_TransferAnim_TargetOrSource",q=True,sl=True)
    Text        = cmds.textField("textfield_NameSpace",q=True,text=True)
    
    if(collection1 == "Selected"):
        if List.length == 2:
            Source = List[0]
            Target = List[1]
            copyKeyframes(Source,Target)
    else:
        Target = ""
        Source = ""
        for Obj in List:
            if(collection2 == "Target"):
                Temp = Anim.RemoveNamespace(Obj)[0]
                Target = Anim.AddNamespace(Text,Temp[Temp[Temp.len-1]])
                Source = Obj
            else:
                Temp = Anim.RemoveNamespace(Obj)
                Source = Anim.AddNamespace(Text,Temp[Temp[Temp.len-1]])
                Target = Obj
            copyKeyframes(Source,Target)




def UI_NameSpace():
    PrefixTexfields = UI_PrefixTexfields()
    width = 58
    cmds.rowColumnLayout(numberOfColumns=1)
    cmds.columnLayout()
    RadioCollectionName = "radioButtonGrp_TransferAnim_How"
    collection1 = cmds.radioCollection(RadioCollectionName)
    rb1 = cmds.radioButton("Selected",label='From Selected',ann="transfer anim from first selected object to 2nd selected object")
    rb2 = cmds.radioButton("NameSpace",label='From NameSpace',ann="Transfer anim from one namespace to another: select object to tranfer ani too or from then make selections")
    cmds.setParent( '..' )
    cmds.columnLayout()
    RadioCollectionName = "radioButtonGrp_TransferAnim_TargetOrSource"
    collection1 = cmds.radioCollection(RadioCollectionName)
    rb1 = cmds.radioButton("Target",label='Target',ann="transfer anim from first selected object to 2nd selected object")
    rb2 = cmds.radioButton("Source",label='Source',ann="Transfer anim from one namespace to another: select object to tranfer ani too or from then make selections")
    cmds.setParent( '..' )
    NameSpaceTextfield = cmds.textField("textfield_NameSpace")
    cmds.textField(NameSpaceTextfield,it="Namespace",edit=True,ann="temp")
    #cmds.textField("textfield_NameSpace",edit=True,w=width)
    cmds.setParent( '..' )
def UI_TransferAnim():

    FrameLayout = cmds.frameLayout(label='Copy Anim',cl = True, collapsable = True,bv=True,w=60,ann=" - Copy Anim")
    UI_NameSpace()
    cmds.button(l='Transfer Anim',     c='UI.TransferAnimation()',w=30,ann="Copy anim from one object to another")
    cmds.setParent( '..' )


def UI_TransferKeys():
    cmds.button(l='Transfer Keys',  c='UI.Anim_TransferKeys()',w=30,bgc=(1,0.5,.3),ann="Wip.. still need to finish script.. to tranfer keys.")


def UI_Switcher():
    FrameLayout = cmds.frameLayout(label='Parent Switch',cl = True, collapsable = False,bv=True,w=60,ann=" Space/Parent switch helps: this saves position of selection and then once you have applied the space/parent switch to you can re-apply the pose/location rotation it was in")
    cmds.button(l='Save Pose'   ,   c='UI.SavePoseButton()' ,w=30,ann="saves current pose of selected objects: Tool creates a new temp node of selected objects, that can be saved and applied later")
    cmds.button(l='Set'         ,   c='Anim.SetPose(False,True)'    ,w=30,ann="Sets the saved pose - great to use with parent/space switching : Tool sets the saved pose created from the 'Save Pose' button, once the pose it set it deletes the temporary node created in 'Save Pose'")
    cmds.button(l='Wip - Lock Pose' ,   c='Anim.SavePose(True)'         ,w=30,ann="Currently not working.... ment to lock/constraint pose... ")
    cmds.setParent( '..' )  


def UI_AlteredKeyFix():
    
    FrameLayout = cmds.frameLayout(label='Anim Fixes',cl = True, collapsable = False,bv=True,w=60)
    cmds.button(l='Altered Key Fix' ,   c='Anim.AlteredKeyFix()'    ,w=30,ann="If you recieve the Altered key error, use this to fix it..... ")

    cmds.setParent( '..' )  
    

def UI_EditKeys():
    
    FrameLayout = cmds.frameLayout(label='Edit Keys',cl = True, collapsable = False,bv=True,w=60,ann="Helps for editing animation")
    UI_Switcher()
    UI_AlteredKeyFix()
    UI_SaveSelection()
    
    cmds.setParent( '..' )

def ModelPanelImagePlane_Display():
    
    OnOff = True
    Panels = cmds.getPanel( type='modelPanel')
    #print Panels
    if (cmds.modelEditor(Panels[0],q=True,imagePlane=True)):
        OnOff = False
    for Panel in Panels:
        #print Panel
        Test = cmds.modelEditor(Panel,edit=True,imagePlane=OnOff)
        #print Test


def Anim_FHS_ShiftAnims():
    ShiftKeys_Selection     = cmds.checkBox("checkBox_ShiftKeys_Selection"      ,q=True,v=True)
    ShiftKeys_FHSAnimRanges = cmds.checkBox("checkBox_ShiftKeys_FHSAnimRanges"  ,q=True,v=True)
    ShiftKeys_ShiftAmount   = cmds.textField("TextField_ShiftAmount"            ,q=True,text=True)
    ShiftKeys_StartFrame    = cmds.textField("TextField_StartFrame"             ,q=True,text=True)
    ShiftKeys_EndFrame      = cmds.textField("TextField_EndFrame"               ,q=True,text=True)

    if(ShiftKeys_FHSAnimRanges):
        Anim.FHS_ShiftAnims(ShiftKeys_ShiftAmount,ShiftKeys_StartFrame,ShiftKeys_EndFrame)
    if(ShiftKeys_Selection):
        Anim.ShiftKeys(ShiftKeys_ShiftAmount,ShiftKeys_StartFrame,ShiftKeys_EndFrame)


def UI_Anim_ShiftKeys():
    FrameLayout = cmds.frameLayout(label='Wip - Adjust Keys',cl = True, collapsable = True,bv=True)
    
    cmds.button(l='Shift Keys',     c='UI.Anim_FHS_ShiftAnims()',ann="temp")
    cmds.rowColumnLayout(numberOfColumns=2)
    Test = cmds.checkBox("checkBox_ShiftKeys_Selection",label="Selection",ann="temp")
    Test = cmds.checkBox("checkBox_ShiftKeys_FHSAnimRanges",label="FHS Anim Ranges",ann="temp")
    cmds.setParent( '..' )
    cmds.rowColumnLayout(numberOfColumns=2)
    cmds.text( label='Shift Keys Amount' )
    ShiftAmount = cmds.textField("TextField_ShiftAmount")
    cmds.textField(ShiftAmount,it="0",edit=True,ann="temp")
    #FrameLayout = cmds.frameLayout(label='Test',cl = True, collapsable = False)
    cmds.setParent( '..' )
    cmds.text( label='Effected Range' )
    cmds.rowColumnLayout(numberOfColumns=4)
    cmds.text( label='Start' )
    ShiftStart = cmds.textField("TextField_StartFrame")
    cmds.textField(ShiftStart,it="0",edit=True,ann="temp")
    cmds.text( label='End' )
    ShiftEnd = cmds.textField("TextField_EndFrame")
    cmds.textField(ShiftEnd,it="0",edit=True,ann="temp")
    cmds.setParent( '..' )
    cmds.setParent( '..' )


def UI_AnimSettings():
    cmds.button(l='Anim Settings',  c='Anim.Anim_Settings()',ann="Sets the scene for ready for Animation, sets playback to ntsc,and removes selected objects to only control curves")
    cmds.button(l='Toggle ImagePlane',  c='UI.ModelPanelImagePlane_Display()',ann="Toggles visibility of Image plane on all modelpanels")
    cmds.button(l='Refresh Iso Select',  c='Anim.Anim_IsoSelect()',ann="refreshes iso select for all panels")
def UI_Anim_SetKeys():
    FrameLayout = cmds.frameLayout(label='Set Key Types',cl = True, collapsable = False)
    cmds.rowColumnLayout(numberOfColumns=3)
    cmds.button(l='Stepped',    c='Anim.KeyTangents_Set("Stepped")',ann="sets new created keys to a Step Mode: great to start out animation and blocking - ( will not change current curves only new keys)")
    cmds.button(l='Linear',     c='Anim.KeyTangents_Set("Linear")',ann="sets new created keys to linear: great for moving from stepped to an evenly spaced interpolation - ( will not change current curves only new keys)")
    cmds.button(l='Spline',     c='Anim.KeyTangents_Set("Spline")',ann="sets new created keys to spline: great for smoothing out animation wiht smoother spline curves - ( will not change current curves only new keys)")
    cmds.setParent( '..' )
    FrameLayout = cmds.frameLayout(label='Export',cl = True, collapsable = False)
    
    cmds.button(l='Export XML',    c='Anim.XML_AnimationExporter()',ann="Export XML Animation")
    cmds.setParent( '..' )

def UI_Anim_Repose():
    FrameLayout = cmds.frameLayout(label='RePose Anim - Pose Side',cl = True, collapsable = True)
    cmds.rowColumnLayout(numberOfColumns=2)
    cmds.button(l='Left',   c='Anim.ReposeAnim("previous")',ann="temp")
    cmds.button(l='Right',  c='Anim.ReposeAnim("next")',ann="temp")
    cmds.setParent( '..' )
    cmds.setParent( '..' )


def UI_Anim_IKFK_MatchPose_Run():
    print ("MatchPose")
    Sel = cmds.ls(sl=True)

    for S in Sel:
        Temp = Anim.RemoveNamespace(S)
        NameSpace = Temp[0]

        Side = Rigging.CheckSide(Temp[2])[1][0]
        
        LimbType = S.replace(Side, "")
        LimbType = LimbType.replace(NameSpace + ":","")
        LimbType = LimbType.replace("_IK_CTRL","")
        LimbType = Rigging_IK.ReverseFootLimbs(LimbType,True)
        Limbs    = Rigging_IK.ReverseFootLimbs(LimbType)
        Suffixes = [Rigging.BASE_NodeTypes()[8],Rigging.BASE_NodeTypes()[1]]
        print (NameSpace)
        print (LimbType)
        print (Side)
        Anim.IK_FK_MatchPose(LimbType,NameSpace,Side,Limbs,Suffixes)



def UI_Anim_IKFK_MatchPose():
        cmds.button(l='IK FK MatchPose',    c='UI.UI_Anim_IKFK_MatchPose_Run()',ann= "match Pose from IK position and set the FK Position")
    
def UI_ScaleAnim_Set(Divide = False):
    Sel1 = cmds.ls(sl=True)
    Reverse = cmds.checkBox("checkBox_ScaleAnim_Reverse",q=True,v=True)
    CHARValue = cmds.checkBox("checkBox_ScaleAnim_ValueFromSelection",q=True,v=True)
    Value   = cmds.floatField("FloatField_ScaleAnimAmount",q=True,v=True)
    if CHARValue:
        Sel = cmds.ls(sl=True)
        Value = cmds.getAttr(Sel[0] +  "." + "NewScale")
        print ("got new scale value: ")
    Selection = cmds.radioCollection("radioButtonGrp_ScaleAnim_Selection",q=True,sl=True)
    if Selection == "True":
        Selection = True
    if Selection == "False":
        Selection = False
    if Divide:
        Value = 1/Value
    
    print ("My value", Value)
    print ("Selection..",Selection)
    Anim.ScaleAnim(Selection,Value,Reverse)
    cmds.select(Sel1)
    
def UI_Anim_ScaleAnim():
    FrameLayout = cmds.frameLayout(label='Scale Anim',cl = True, collapsable = True)
    #cmds.rowColumnLayout(numberOfColumns=2)
    cmds.columnLayout()
    RadioCollectionName = "radioButtonGrp_ScaleAnim_Selection"
    collection1 = cmds.radioCollection(RadioCollectionName)
    rb1 = cmds.radioButton(False,label='All Translate Animation',ann="temp")
    rb2 = cmds.radioButton(True,label='Selected Anim Curves',ann="temp")
    cmds.setParent( '..' )
    cmds.checkBox("checkBox_ScaleAnim_ValueFromSelection",label="Scale Value from Selection",ann="Object must have a New scale attribute to get the value from ( created for the rescale tool)")
    cmds.checkBox("checkBox_ScaleAnim_Reverse",label="Reverse Animation - Timeline",ann="This will reverse the animation in the timeline")
    cmds.rowColumnLayout(numberOfColumns=2)
    cmds.text( label='Scale Amount' )
    ShiftEnd = cmds.floatField("FloatField_ScaleAnimAmount",value= 1)
    #cmds.textField(ShiftEnd,it="1",edit=True)
    cmds.setParent( '..' )
    cmds.rowColumnLayout(numberOfColumns=2)
    cmds.button(l='<<< Divide', c='UI.UI_ScaleAnim_Set(True)',bgc=(0.8,0.4,0.6),ann=" select Keys in Graph editor to to Scale Animation") 
    cmds.button(l='Multiply >>>', c='UI.UI_ScaleAnim_Set()'  ,bgc=(0.6,0.8,0.6),ann=" select Keys in Graph editor to to Scale Animation") 
    cmds.setParent( '..' )
    cmds.setParent( '..' )
    
    cmds.radioCollection( RadioCollectionName, edit=True, select=rb1 )

def Anim_SelectCTRLS_getValues():
    UseNamespace     = cmds.checkBox("checkBox_SelectCTRLS_UseNameSpace"      ,q=True,v=True)
    Anim.Select_CTRLS(UseNamespace)
    
    
def UI_Anim_SelectCTRLS():
    FrameLayout = cmds.frameLayout(label='Selection',cl = True, collapsable = True)
    cmds.checkBox("checkBox_SelectCTRLS_UseNameSpace",label="by Selected Namespace",ann="Used to limit selection of controls to currently selected Rig. -Selects all objects with same namespace-")
    cmds.button(l='Select All CTRLS',  c='UI.Anim_SelectCTRLS_getValues()',ann="Selects all nodes that end with '_CTRL'")
    cmds.setParent( '..' )

def CharSetUp_Anim_UI(UIName):

    Layout = cmds.rowColumnLayout(numberOfColumns=1)#,bgc=(0.5450981020927429, 0.5490196704864502, 0.5294118285179138))
    cmds.button(l='Get Frame Count', c='UI.UI_UpdateFrameCount()',ann="prints current number of frames in the Time slider below the button, also prints half the amount of current frame count - it's perpose is if you want to quickly find out the frame time slider frame count/loop")
    UI_UpdateFrameCount()
    #cmds.text("text_FrameCount",label=str(FrameCountText),align='center')
    UI_AnimSettings()
    
    UI_Anim_SetKeys()
    cmds.separator(h=30)
    
    cmds.button(l='Anim Picker',    c='UI.CharSetUp_AnimPicker()'           ,ann= "Launches AnimSchools Anim Picker: - this tool is used to create a visual representation of the Character controls for easy selection during animation")
    cmds.button(l='Tween Machine',  c='tweenMachine.start()'                ,ann= "Launch The Tween Machine Tool - This tool is to help with speeding up inbetween poses when animating")
    cmds.button(l='Studio Library', c='UI.CharSetup_StudioLibrary()'        ,ann= "Launch Studio Library Tool - tool for Saving Character poses and animation, helps transfering animation and poses to new characters from scene to scene") 
    cmds.button(l='aTools Install', c='UI.CharSetup_aTools_launchInstall()' ,ann= "Launches aTools : another tool to help with improving animation workflow")  
    cmds.button(l='BH Ghost',       c='UI.CharSetup_BHGhost_Run()'          ,ann= "Launches BH Ghost to help 3d Ghosting tools for animation")
    cmds.button(l='MG Tools Pro',   c='UI.CharSetup_MGToolsPro_Run()'   ,ann= "Launches MG Tools Pro - tools for animation by Miguel Gao - you may need to acquire your own license")  
    CharSetup_MGToolsPro_Run 
    UI_Anim_SelectCTRLS()
    UI_EditKeys()
    UI_TransferAnim()
    UI_Anim_Repose()
    UI_Anim_IKFK_MatchPose()
    UI_Anim_ShiftKeys()
    UI_Anim_ScaleAnim()
    

    cmds.setParent( '..' )
    cmds.setParent( '..' )
    return Layout


def Skinned_CheckMaxInfluence():
    Max = cmds.intField( "Skinned_VertInfluence_Count", q=True,v=True)
    Skinning.CheckMaxInfluence(Max)

def UI_Settings_VertexColorToggle():
    FrameLayout = cmds.frameLayout(label='Vertex Color Settings',cl = True, collapsable = False,bv=True)    
    
    FrameLayout = cmds.frameLayout(label='Toggle Display',cl = True, collapsable = False,bv=True)
    cmds.text( label='vertex color')
    Layout = cmds.rowColumnLayout(numberOfColumns=2)
    cmds.button(l='ON',     c='UI.CharSetUp_VertexColorToggle(1)',bgc=(0,0.6,0.15),ann="temp")
    cmds.button(l='OFF',    c='UI.CharSetUp_VertexColorToggle(0)',bgc=(0.4,0.04,0),ann="temp")
    cmds.setParent( '..' )
    cmds.text( label='Set as Reference')
    Layout = cmds.rowColumnLayout(numberOfColumns=2)
    cmds.button(l='ON',     c='UI.CharSetUp_MakeRef(1)',bgc=(0,0.6,0.15),ann="temp")
    cmds.button(l='OFF',    c='UI.CharSetUp_MakeRef(0)',bgc=(0.4,0.04,0),ann="temp")
    cmds.setParent( '..' )
    cmds.setParent( '..' )
    cmds.setParent( '..' )

def CharSetUp_Settings_UI(UIName):
    Layout = cmds.rowColumnLayout(numberOfColumns=2)#,bgc=(0.5078432083129883, 0.4960785031318665, 0.460784387588501))
    cmds.button(l='Debug Turn On', c='UI.ImportPtvsd()',bgc=(0.3,0.1,0.1),ann="Turn on Python debug")
    cmds.separator(h=30)
    cmds.button(l='Toggle Scene Units cm/m', c='MASTER.Scene_UnitSettings_Set()',ann="temp")
    cmds.separator(h=30)

    FrameLayout = cmds.frameLayout(label='File Clean Up',cl = True, collapsable = False)
    cmds.separator(h=30)
    
    cmds.intField( "Skinned_VertInfluence_Count", minValue = 0, maxValue = 100, value = 3)
    cmds.intField( "Skinned_VertInfluence_Count", e=True)
        
    cmds.button(l='Skinned Verts over Influence Limit', c='UI.Skinned_CheckMaxInfluence()',ann="temp")
    

    cmds.separator(h=30)
    FrameLayout = cmds.frameLayout(label='Scene Fixes',cl = True, collapsable = False,bv=True)  
    cmds.button(l='Delete Unkown File Types', c='MASTER.DeleteUnkownNodes()',ann="temp")
    cmds.button(l='Fix Broken Perspective Camera', c='RenderTools.fixThePerspCamera()',ann="temp")
    cmds.setParent( '..' )
    UI_Settings_VertexColorToggle()
    cmds.setParent( '..' )
    cmds.setParent( '..' )
    return Layout
    


def CharSetUp_UI():
    
    PrintNote   = "CharSetUp_UI():"
    WindowName  = ["CharSetUpUI","Character Setup"]

    Tabs        = ["Settings","Skeleton","Rigging"]#"Skeleton SetUp",
    window      = WindowName[0]
    DockWindow  = window + "_Docked"
    IsDocked    = None
    
    MASTER.PrintCheck([PrintNote,"WindowName : ",WindowName,"Tabs : ",Tabs,"window : ",window,"DockWindow : ",DockWindow],UI_ONOFF,["*",""])
    
    #check to see if window exists
    if cmds.window(WindowName[0],exists = True):
        cmds.deleteUI(WindowName[0])
    if cmds.dockControl(DockWindow, exists=True):
        cmds.deleteUI(DockWindow)   
        
    
            
    #create Window[0.26, 0.3, 0.35]
    window  = cmds.window(WindowName[0],title=WindowName[1],iconName=WindowName[0], widthHeight=(200, 55))
    form    = cmds.formLayout()
     #"none", "top", "notop" and "full"
    tabs    = cmds.tabLayout(innerMarginWidth=5, innerMarginHeight=5,bs="full")
    cmds.formLayout( form, edit=True, attachForm=((tabs, 'top', 0), (tabs, 'left', 0), (tabs, 'bottom', 0), (tabs, 'right', 0)))
    
    LayoutTabs = []
    for Tab in Tabs:
        UIName = Tab.replace(" ", "")
        print (Tab)
        print (UIName)
        TLabel = eval ("CharSetUp_" + UIName + "_UI(UIName)")
        print (TLabel)
        cmds.tabLayout( tabs, edit=True, tabLabel=(TLabel, Tab))
    allowedAreas = ['right', 'left']
    
    dw =  cmds.dockControl(DockWindow,area='left', content=window)
    #else:
    #   #dw =  cmds.dockControl(DockWindow,area='left', content=window)
    #   dw =  cmds.dockControl(DockWindow,state=IsDocked, content=window)
    

#   workspaceControlName = WindowName[0] + 'WorkspaceControl'

#   if cmds.workspaceControl(workspaceControlName, q=True, exists=True):

#       cmds.workspaceControl(workspaceControlName, e=True, close=True )

#       cmds.deleteUI(workspaceControlName, control=True)

#   cmds.workspaceControl(workspaceControlName, dtp=[window, "right", True])    

#   

    #print DockWindow
    #show window
    cmds.showWindow(window)