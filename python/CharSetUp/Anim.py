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
import UI
import XML_Animation_Exporter
Anim_ONOFF = True


def MatchTransforms(MoveMe,MatchMe,Trans=True,Rot=True):
	if(Trans):
		Temp = cmds.pointConstraint(MatchMe,MoveMe)
		cmds.delete(Temp)
	if(Rot):
		Temp = cmds.orientConstraint(MatchMe,MoveMe)
		cmds.delete(Temp)

		
def DistanceBetween(Object1,Object2):
	
	Loc1 = cmds.spaceLocator(n=Object1 + "_" + "DisLoc")
	Loc2 = cmds.spaceLocator(n=Object1 + "_" + "DisLoc")
	D3 = cmds.shadingNode("distanceBetween",n="TestDistance",asUtility=True)
	cmds.connectAttr(str(Loc1[0]) + ".translate",str(D3) + ".point1")
	cmds.connectAttr(str(Loc2[0]) + ".translate",str(D3) + ".point2")
	cmds.matchTransform(Loc1[0],Object1,pos=True)
	cmds.matchTransform(Loc2[0],Object2,pos=True)
	Value = cmds.getAttr(str(D3) + ".distance")
	#remove temp measuring nodes
	cmds.delete(Loc1[0],Loc2[0],D3)
	print Value
	return Value

def KeyTangets_Get():
	itt = cmds.keyTangent(g=True,q=True,itt=True)[0]
	ott = cmds.keyTangent(g=True,q=True,ott=True)[0]
	return [itt,ott]

def KeyTangents_Set(Type):
	print "Type : "
	print Type
	if(type(Type) == str ):
		if Type == "Stepped":
			cmds.keyTangent(g=True,itt="flat",ott="step")
		if Type == "Linear":
			cmds.keyTangent(g=True,itt="linear",ott="linear")
		if Type == "Spline":
			cmds.keyTangent(g=True,itt="spline",ott="spline")
	if(type(Type) == list ):
		
		cmds.keyTangent(g=True,itt=Type[0],ott=Type[1])

def Anim_Settings():
	cmds.selectType( allObjects=False )
	cmds.selectType( curve=True )
	Panels = cmds.getPanel( type='modelPanel' )
	for P in Panels:
	    cmds.modelEditor(P,e=True,allObjects=False,manipulators=True)
	    cmds.modelEditor(P,e=True,polymeshes=True,nurbsCurves=True)
	cmds.playbackOptions(v="all",l="continuous")
	cmds.currentUnit( time='ntsc' )
	
	
	

def Anim_IsoSelect():
    ActivePanels = MASTER.Get_ActivePanels()
    State = cmds.isolateSelect( ActivePanels[0], query=True,state=True)

    for Panel in ActivePanels:
    	print Panel
    	cmds.isolateSelect(Panel,state=not State)
    	#print (not State)
    	#if(not State):
    	#	print "Set Stuff"
    		#cmds.isolateSelect(Panel,addSelected=True)
    		#cmds.isolateSelect(Panel,ls=True)
    	#	cmds.isolateSelect(Panel,state=)
    		
def FHS_ShiftAnims(offset,start=0,end=10000):
	MASTER.PrintCheck(["FHS_ShiftAnims(offset,start=0,end=10000)",offset,start,end],Anim_ONOFF,["*",""])

	Node = "fhs_scene_settings"
	Attr = "range_"
	
	AttrList = cmds.listAttr(Node)
	RangeList = []
	for AL in AttrList:
	    if Attr in AL:
	        RangeList.append(AL)
	
	#print AttrList
	#print RangeList
	for i in RangeList:
		print i
		update = False
		Array = cmds.getAttr(Node + "." + str(i))
		Array2 = list(Array)
		print Array[1]
		print Array[2]
		
		if int(Array[1]) >= int(start):
			print "start"
			update = True
			print Array[1]
			print (int(Array[1]) + int(offset))
			Array2[1] = unicode(int(Array[1]) + int(offset))
  
		if int(Array[2]) >= int(start):
		  print "End"
		  update = True
		  print Array[2]
		  print (int(Array[2]) + int(offset))
		  Array2[2] = unicode(int(Array[2]) + int(offset))
		
		if update:
			print Array
			print Array2
			cmds.setAttr(Node + "." + str(i),type="stringArray",*([len(Array2)] + Array2))

			
def ShiftKeys(offset=0,start=0,end=10000):
	MASTER.PrintCheck(["ShiftKeys(offset=0,start=0,end=10000)",offset,start,end],Anim_ONOFF,["*",""])
	cmds.keyframe(time=(start,end),timeChange=offset,r=True)
	

def SaveSelectionNode():
	Node 		= "Temp_SavedSelection"
	Attribute 	= "SelectionList"
	
	return [Node,Attribute]

def GetSavedSelection():
	Node 		= SaveSelectionNode()[0]
	Attribute 	= SaveSelectionNode()[1]
	List = cmds.getAttr(Node + "." + Attribute).split(",")
	return List
	
def SaveSelection():
	TempSel	= cmds.ls(sl=True)
	TempSel = [ x.encode('ascii','ignore')  for x in TempSel]
	#print TempSel
	Prefix = TempSel[0].rpartition(':')[0]
	#print Prefix
	strList = map(str, TempSel)
	strList = map( lambda x: x.replace( Prefix + ':', ''), strList)
	#print strList
	#save list on node. 
	#create node
	Node 		= SaveSelectionNode()[0]
	Attribute 	= SaveSelectionNode()[1]
	
	if (cmds.objExists(Node)):
		cmds.delete(Node)
	cmds.createNode('transform', n=Node)
	cmds.addAttr(Node,ln=Attribute,dt="string")
	cmds.setAttr(Node + "." + Attribute,cb=True)
	cmds.setAttr(Node + "." + Attribute,keyable=True)
	#adjust strList to save cleanly by removing extra bits. 
	
	
	cmds.setAttr(Node + "." + Attribute,','.join(strList),type="string")
	
	return [Prefix,strList]
	#SelList = []
	#for List in strList:
	#    print List
	#    if((cmds.objExists(prefix[0] + ":" + List)) and (cmds.objExists(prefix[1] + ":" + List))):
	#        SelList.append(List)

	#print SelList
 
def SavePoseAnim_Node():
	Node 		= "Temp_SavePoseAnim"
	
	return Node

def RemoveNamespace(Node):
	NodeParts = Node.rpartition(':')
	return NodeParts

def AddNamespace(Namespace,Node):
	return Namespace + ":" + Node

	
def SavePose(Constrain = False,ParentSwitch = False):
	Node 	= SavePoseAnim_Node()
	sel 	= cmds.ls(sl=True,type="transform")
	if(cmds.objExists(Node)):
		cmds.delete(Node)
	cmds.createNode('transform', n=Node)
	if(Constrain):
		cmds.createNode('transform', n=Node + "_Constraints",p=Node)
	
	CTRLParts = []
	for CTRL in sel:
		NodeName = CTRL # RemoveNamespace(CTRL)
		NodeNameSuffix = NodeName # NodeName[2]
		CTRLParts.append(NodeName)
		NewNode = Node + "_" + NodeNameSuffix
		print Node
		print NewNode
		cmds.createNode('transform', n=NewNode,p=Node)
		cmds.matchTransform(NewNode,CTRL)
		if(Constrain):
			print "driver"
			print NewNode
			print ("ctrl")
			print CTRL
			Point 	= cmds.pointConstraint(NewNode,CTRL)
			Orient 	= cmds.orientConstraint(NewNode,CTRL)
			cmds.parent(Point,Node + "_Constraints")
			cmds.parent(Orient,Node + "_Constraints")
	cmds.select(sel)
	
	return sel
	
def SetPose(Constrain = False,ParentSwitch = False):
	Node 	= SavePoseAnim_Node()
	Prefix 	= "" # UI.UI_PrefixTexfields(True)
	print "Prefix : ", Prefix
	
	
	List = []
	if(cmds.objExists(Node)):
		List = cmds.listRelatives(Node,c=True)
		print List
		#List.remove(Node + "_Constraints")  
	for L in List:
		CTRL = L.replace(Node + "_", "")
		cmds.matchTransform(CTRL,L)
	cmds.delete(Node)
    	
def Old():   
    Trans  = cmds.xform(sel,q=True,ws=True,t=True)
    Rot    = cmds.xform(sel,q=True,ws=True,ro=True)
    cmds.setAttr(sel + ".Orient",0)
    cmds.setAttr(sel + ".Position",0)
    cmds.xform(sel,ws=True,t=Trans)
    cmds.xform(sel,ws=True,ro=Rot)
    
def SaveAnim(SaveAnim=False):
	SavePose()
	
def AlteredKeyFix():
	Sel = cmds.ls(sl=True)
	Min = cmds.playbackOptions(q=True,min=True)
	Max = cmds.playbackOptions(q=True,max=True)
	cmds.copyKey(option="keys")
	cmds.select(cl=True)
	
	List = []
	
	for S in Sel:
		Temp = cmds.createNode('transform')
		cmds.setKeyframe(Temp)
		List.append(Temp)
		
	cmds.select(List)
	cmds.pasteKey()
	#remove Keys
	cmds.select(Sel)
	cmds.cutKey(option="keys")
	cmds.setKeyframe(Sel)
	#transfer Keys back
	cmds.select(List)
	cmds.copyKey()
	cmds.select(Sel)
	cmds.pasteKey()
	
	#remove transform Nodes
	cmds.delete(List)
    


def ReposeAnim(Direction="previous"):
	

	#only run if at least one key is selected
	keyCount = cmds.keyframe(q=True,keyframeCount=True)
	if (keyCount != 0):	
		#loop over selected curves and process independently
		selectedCurves = cmds.keyframe(selected=True,q=True,name=True)
		for c in range(len(selectedCurves)):
			#channel to use for this pass
			channel = selectedCurves[c]
		
			#get array of key times in selection (to find closest match key)
			timeArray = cmds.keyframe(channel,selected=True,q=True,timeChange=True)
			
			#find first frame time
			lastkey = cmds.keyframe(channel,q=True,lastSelected=True)
			firstKey = lastkey[0]
			for Time in timeArray:
			    if (Time < firstKey):
    				firstKey = Time
	
			#find closest key
			endKey = timeArray[0]

			if Direction == "next":
			    endKey = timeArray[len(timeArray)-1]

			matchKey = cmds.findKeyframe(channel,time=(endKey,endKey),which=Direction)

			#get difference in values between firstKey and matchKey
			matchKey_val = cmds.keyframe(channel,time=(matchKey,matchKey),q=True, valueChange=True)
			endKey_val = cmds.keyframe (channel,time=(endKey,endKey),q=True,valueChange=True)
			delta = matchKey_val[0] - endKey_val[0]
			
			#offset values with delta
			selected = cmds.keyframe(channel,selected=True,q=True,indexValue=True)

			for i in range(len(selected)):
			    cmds.keyframe(channel,relative=True,index=(selected[i],selected[i]),valueChange=delta)


def ScaleAnim(Selection=True,ScaleValue=1,Reverse=False):
    print "Selection...",Selection
    print "reversed....",Reverse
    if (Selection):
        TimeScaleValue=1
        TimePivotValue=0
        ScalePivotValue = 0
        animCurves = cmds.keyframe(q=True,n=True,sl=True)
        print "animCurves :",animCurves
        timeSelKey = cmds.keyframe(animCurves[0],q=True,sl=True)
        print "timeSelKey :",timeSelKey
        if Reverse :
            TimeScaleValue = -1
            Min = min(timeSelKey)
            Max  = max(timeSelKey)
            print Min
            print Max
            TimePivotValue =  (Min + Max)/2
            ScaleValue=1
        else:
            NewList = []
            for Curve in animCurves:
                if "translate" in Curve:
                    NewList.append(Curve)
            
            #remove any controllers that are not translate... 
            #selectKey -rm -k -t 30 CHAR_CTRL_rotateY ;
            cmds.selectKey(clear=True)
            cmds.selectKey(NewList,k=True)
            
        #calculates the pivotpoint of the keys to be scaled
        #selectKey -hi below;
        cmds.scaleKey(timeScale=TimeScaleValue,timePivot=TimePivotValue,valueScale=ScaleValue,valuePivot=ScalePivotValue)
        #all translate keys no range entire range. 
    else:
        List = cmds.ls(type="animCurveTL")
        cmds.scaleKey(List,valueScale=ScaleValue)

def Select_CTRLS(UseNamespace=False):
    namespaces = []
    Sel = cmds.ls(sl=True)
    if (len(Sel)>0):#if more than one
        if(UseNamespace):
            #get namespace of selection
            for S in Sel:
                namespace = S.rpartition(':')[0]
                print namespace
                namespaces.append(namespace)
    if(UseNamespace == False):
        #using all namespaces to make sure we get all objects. 
        namespaces = cmds.namespaceInfo(listOnlyNamespaces=True)

    print namespaces
    mystring = [":*_CTRL",":*_SwitchCTRL"]
	# using .join to got through mystring List and Namespace list to create a list of possible selectable nodes. 
    #SelList = ",".join([ '"' + str(s) + str(m) + '"'  for m in mystring for s in namespaces])
    SelList = [str(s) + str(m) for m in mystring for s in namespaces]
    TempList = []
    for Sel in SelList:
        if cmds.objExists(Sel):
			cmds.select(Sel,add=True)
	Sel = cmds.ls(sl=True,type="transform")
	cmds.select(Sel)

def getAttName(fullname):
    parts = fullname.split('.')
    return parts[-1]

def copyKeyframes(Source,Target):
	for Obj in Objs:
		animAttributes = cmds.listAnimatable(sourceObj);
		for attribute in animAttributes:
			numKeyframes = cmds.keyframe(attribute, query=True, keyframeCount=True)
			if (numKeyframes > 0):
				cmds.copyKey(attribute)
				cmds.pasteKey(Obj, attribute=getAttName(attribute))

def SetLimbPose_FK(Limb_Settings):
	for L in Limb_Settings:
		CTRL = L[0]
		Trans = L[1]
		Attr_List = L[2]
		print "settt=========="
		print CTRL
		print Trans
		print Attr_List
		cmds.xform(CTRL,ws=True, t=Trans)	
		for Attr in Attr_List:
			cmds.setAttr(Attr[0], Attr[1])
		if(cmds.objExists(CTRL + "." + "Orient")):
			cmds.setAttr(CTRL + "." + "Orient",0)
		if(cmds.objExists(CTRL + "." + "Position")):
			cmds.setAttr(CTRL + "." + "Position",0)




def IK_FK_MatchPose(LimbType,NameSpace,Side,Limbs,Suffixes):

	IKFK_Switch = NameSpace + ":" + Side + LimbType + "_" + "SwitchCTRL"
	if(not cmds.objExists(IKFK_Switch)):
		IKFK_Switch = NameSpace + ":" + Side + LimbType + "_" + "Switch_CTRL"
	print LimbType
	print NameSpace
	print Side
	print Limbs
	print Suffixes
	print IKFK_Switch

	JNT_List = []
	CTR_List = []
	Limb_Settings	= []	
	for L in Limbs:
		Attr_Trans = ["rotate","scale"]
		Attr_Axis = ["X","Y","Z"]
		JNT = NameSpace + ":" + Side + L + "_" + Suffixes[0]
		CTRL = NameSpace + ":" + Side + L + "_" + Suffixes[1]
		
		if(cmds.objExists(JNT) and cmds.objExists(CTRL)):
			Trans = cmds.xform(JNT,q=True,ws=True, t=True)
			OtherAttr = []
			for A_T in Attr_Trans:
				for A_A in Attr_Axis:
					OtherAttr.append([CTRL + "." + A_T + A_A,cmds.getAttr(JNT + "." + A_T + A_A)])
			Limb_Settings.append([CTRL,Trans,OtherAttr])

	SetLimbPose_FK(Limb_Settings)
	SetLimbPose_FK(Limb_Settings)

	#cmds.setAttr(IKFK_Switch + "." + "IKSwitch", 1)	
	


	
	#get JointValues:
	
def XML_AnimationExporter():
    print "TEST"
    
    XML_Animation_Exporter.main_XML_Anim_Export()
	