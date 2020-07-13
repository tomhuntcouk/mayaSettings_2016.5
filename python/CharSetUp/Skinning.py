####################################################
#
# Character UI Setup for character Rigging tools
# Creator = Leo Michalek
# Created 18.08.2016
#
#
####################################################

import maya.cmds as cmds
import maya.mel as mel
import MASTER

Skinning_ONOFF = True

def Constrain2MatchingJoints(Offset):
	List = cmds.ls(sl=True,type="transform")
	#print List
	for L in List:
	   cmds.select(cl=True)
	   cmds.joint(n=L + "_JNT")
	   cmds.matchTransform(L + "_JNT",L,pos=True)
	for L in List:
	    #print L
	    ParentNode = cmds.listRelatives(L,p=True)
	    #print ParentNode[0]
	    cmds.parent(L + "_JNT",ParentNode[0] + "_JNT")
	    PNode = cmds.parentConstraint(L + "_JNT",L,mo=Offset,weight=1)
	    SNode = cmds.scaleConstraint(L + "_JNT",L,offset=(1,1,1),weight=1)
	    cmds.parent(PNode,"Geo_Constraints")
	    cmds.parent(SNode,"Geo_Constraints")
    
    
def SkinObjects2MatchingJoints():
	List = cmds.ls(sl=True,type="transform")
	for L in List:
	   cmds.select(cl=True)
	   cmds.skinCluster (L + "_JNT",L, tsb=True )

	
def GetSkininfluence(Object,Type="VertName"):

	SC = mel.eval('findRelatedSkinCluster '+ Object)
	PrintNote = "SC = related SkinCluster query.. /n "
	MASTER.PrintCheck([PrintNote,"Object : ",Object,"SC : ",SC])

	PruneValue = 0.001
	if SC:
		cmds.skinPercent( SC, Object, pruneWeights=PruneValue )
		Verts = cmds.polyEvaluate( Object,v=True)
		PrintNote = "Verts"
		MASTER.PrintCheck([PrintNote,"Verts : ",Verts])
		VertInfluence = []
		for V in range(Verts):
			Vert 		= Object + ".vtx[" + str(V) + "]"
			#Position	= cmds.xform(Vert,q=True,ws=True,t=True)
			JNTS 		= cmds.skinPercent(SC, Vert, transform=None,query=True)
			Weight 		= cmds.skinPercent(SC, Vert, v=True,query=True)
			Influences 	= []
			PrintNote = "Vert list... "
			MASTER.PrintCheck([PrintNote,"Vert : ",V,"JNTS : ",JNTS,"Weight : ",Weight])
			if(JNTS != None):
				for W in range(len(JNTS)):
					JNTInfluence = JNTS[W].rpartition(':')[2]
					if(Weight[W]>0.0):
						Influences.append([str(JNTInfluence),Weight[W]])
				if(Type == "VertName"):
					VertInfluence.append([V,Influences])
				if(Type == "VertPosition"):
					VertInfluence.append([Position,Influences])
		return [str(Object),VertInfluence]

def UI_CheckInfluenceDone():
	window = "CheckVertComplete_UI"
	if cmds.window(window,exists = True):
		cmds.deleteUI(window)
	window = cmds.window(window,title="Check Vert influence", widthHeight=(200, 55) )
	cmds.columnLayout(bgc=(0.4,0.5,0.4),cal="center")
	cmds.text( label='No Verts where Found - Ready for export',align='center' )
	cmds.button( label='Close', command=('cmds.deleteUI(\"' + window + '\", window=True)'),align='center',bgc=(0.3,0.3,0.3) )
	cmds.setParent( '..' )
	cmds.showWindow( window )
 
def SelectMaxInfluence(Object,Max,VertInfluence):
	
	PastInfluence = []
	PastInfluenceValues = []
	for VI in VertInfluence:
	    Vert = VI[0]
	    if len(VI[1])>Max:
	        PastInfluence.append(str(Object) + ".vtx[" + str(VI[0]) + "]")
	        PastInfluenceValues.append(VI)
	#print PastInfluence
	#print PastInfluenceValues
	if PastInfluence != []:
		cmds.selectMode( component=True )
		cmds.select(PastInfluence,r=True)
	else:
		UI_CheckInfluenceDone()
		cmds.selectMode( object=True )

    
def CheckMaxInfluence(Max):
	cmds.selectMode( object=True )
	Objects = cmds.filterExpand(sm=12)
	for Object in Objects:
		CheckMaxInfluence_Object(Object,Max)
		

def CheckMaxInfluence_Object(Object,Max):		
	VertInfluence = GetSkininfluence(Object)
	if VertInfluence:
		SelectMaxInfluence(Object,Max,VertInfluence[1])
	else:
		print ("Nothing with a skin cluster selected.. Please select different object")

def SetWeights(Object,SkinCluster,WeightInfo):
	PrintNote = "SetWeights(Object,SkinCluster,WeightInfo):"
	MASTER.PrintCheck([PrintNote,"Object : ",Object,"SkinCluster : ",SkinCluster,"WeightInfo : ",WeightInfo])

	PrintNote = "Get the prefix of the influence to add back the namspace. "
	MASTER.PrintCheck(PrintNote)		
	JNTInfluences 	= cmds.skinCluster(SkinCluster,query=True,inf=True)
	JNTPrefix 		= JNTInfluences[0].rpartition(':')
	Prefix 			= str(JNTPrefix[0]) + str(JNTPrefix[1])
	
	for WeightInfoPerVert in WeightInfo:
		Values = []
		print ("weightinfoperVert")
		Vert = WeightInfoPerVert[0]
		print (Vert)
		print (WeightInfoPerVert[1])
		for Info in WeightInfoPerVert[1] :
			#print Info
			Influence 	= Prefix + Info[0]
			Value	  	= Info[1]
			Values.append([Influence,Value])
		print (Vert)
		print (Values)
		#MASTER.BreakCode()
		#cmcds.skinPercent(tv=Chest_JNT 1,SkinCluster,Pig2.vtx[142];
		cmds.skinPercent( SkinCluster, Object + ".vtx[" + str(Vert) + "]", transformValue=Values)
	#print WeightInfo

def CopyWeights_By_Position(GetList = None):
	print ("Copying Weights by Position")
	print ("--------------------------")
	Objects	= []
	if GetList == None:
		Objects 	= cmds.ls(sl=True)
	else:
		Objects = GetList
	
	print (Objects)
	cmds.copySkinWeights(ss=Objects[0],ds=Objects[1],noMirror=True,sa="closestPoint",ia=["label","name","oneToOne"])

def CopyWeights_PerVertName(GetList = None):
	print ("Copying Weights by Vert Name")
	print ("--------------------------")
	PrintNote = "CopyWeights_PerVertName(Objects = cmds.ls(sl=True)):"
	MASTER.PrintCheck([PrintNote,"GetList:",GetList],Skinning_ONOFF,["*",""])		
	Objects	= []
	if GetList == None:
		Objects 	= cmds.ls(sl=True)
	else:
		Objects = GetList
	

	#print Objects	
	if len(Objects)>1:	
		# copy 1st object paste to 2nd.
		SourceObject 	= Objects[0]
		WeightInfo 		= GetSkininfluence(SourceObject)[1]
		MASTER.PrintCheck(["WeightInfo:",WeightInfo],Skinning_ONOFF,["",""])	
		newObjects = Objects.pop(0)
		for Object in Objects:
			SkinCluster = mel.eval('findRelatedSkinCluster '+ Object)
			print ("SourceObject"),(SourceObject)
			print ("Object",Object)
			print ("SkinCluster", SkinCluster)
			print ("WeightInfo", WeightInfo)
			SetWeights(Object,SkinCluster,WeightInfo)
	else:
		PrintNote = "Selected... "
		PrintNote2 = "not enough objects selected. select at least 2 objects. 1st object as the source"
		MASTER.PrintCheck([PrintNote,"Objects:",Objects,PrintNote2],Skinning_ONOFF,["",""])		

	
def CopyWeights(Type):
	cmds.selectMode( object=True )
	Objects	= cmds.filterExpand(sm=12)
	#print "test...."
	#print Objects
	#if Type == "VertName":
	#	print Objects
	#	MASTER.BreakCode()
	#	CopyWeights_PerVertName(Objects)
	#if Type == "VertPosition":
	#	CopyWeights_PerVertPosition(Objects)
		

def SelectVertsInfluencedByJNTS():
	Sel 	= cmds.ls(sl=True)
	Geo 	= Sel[0]
	del Sel[0]
	#Select Geo then the Joints to influence
	WeightInfo 		= GetSkininfluence(Geo)[1]
	#print WeightInfo
	Verts = []
	#print Geo
	#print Sel
	for S in Sel:
		for WI in WeightInfo:
			for W in WI[1]:
				if (S == W[0]):
					Verts.append(str(Geo) + ".vtx[" + str(WI[0]) + "]")
	#print Verts
	cmds.select(Verts)
	
def ReverseNormals(Geo):
    cmds.polyNormal(Geo,normalMode=0,userNormalMode=1,ch=1)	
    
def CleanUpHistory_ReSkin(Geo = None,CopyWeightsBy_Name=True,DeleteOriginal=True,SecondMesh=None):

	Geoparent = cmds.listRelatives(Geo, p=True)
	GeoparentNew = Geoparent
	Influence_List  = cmds.skinCluster(Geo,q=True,inf=True)
	
	NewGeo = SecondMesh
	hasParent = False
	if(SecondMesh == None):
		NewGeo          = cmds.duplicate(Geo,n= Geo + "_New")[0]
		hasParent 		= bool(cmds.listRelatives(NewGeo, parent=True))
	else:
		GeoparentNew = cmds.listRelatives(NewGeo, p=True)
		
	if(hasParent):
		cmds.parent(NewGeo,w=True)
	#check to see if already has skinCluster
	if(mel.eval('findRelatedSkinCluster '+ NewGeo)):
		print ("Already Skinned")
	else:
		print ("Adding skinning")
		NewSkin         = cmds.skinCluster(NewGeo,Influence_List)
	if(CopyWeightsBy_Name):
		CopyWeights_PerVertName([Geo,NewGeo])
	else:
		SkinCluster_Source = mel.eval('findRelatedSkinCluster '+ Geo)
		SkinCluster_Destination = mel.eval('findRelatedSkinCluster '+ NewGeo)
		CopyWeights_By_Position([SkinCluster_Source,SkinCluster_Destination])

	if(DeleteOriginal):
		cmds.delete(Geo)
		if(SecondMesh == None):
			cmds.rename(NewGeo,Geo)

	print ("GEoParent: ", Geoparent)

	if(cmds.objExists(Geo)):
		if(Geoparent != cmds.listRelatives(Geo, p=True)):
			cmds.parent(Geo,Geoparent)
	if(cmds.objExists(NewGeo)):
		if(GeoparentNew != cmds.listRelatives(NewGeo, p=True)):
			cmds.parent(NewGeo,GeoparentNew)
	return NewGeo


def CombineSkinnedMesh_KeepOriginal(OriName="NewGeoName",Geo = None):
	ComboGeo = cmds.polyUniteSkinned(Geo,muv=1,ch=1)[0]
	cmds.rename(ComboGeo,OriName)
	CleanUpHistory_ReSkin(OriName,DeleteOriginal=True)
	cmds.delete(Geo)
	return OriName
