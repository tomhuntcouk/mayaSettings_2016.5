####################################################
#
# Character UI Setup for character Rigging tools
# Creator = Leo Michalek
# Created 18.08.2016
#
#
####################################################

import maya.cmds as cmds
import os
import UI
import sys

from inspect import currentframe, getframeinfo
ONOFF_Global = True

def BreakCode(frameinfo):
	base=os.path.basename(frameinfo.filename)
	print "------------Break Code Exit : -----------"
	print "Line Number : ",frameinfo.lineno
	print "Script file : ", base 
	print "Path        : ", frameinfo.filename 
	print "-----------------------------------------"
	sys.exit()
	
def Get_Selected():
	Selection= []
	TSel = cmds.ls( selection=True )
	for T in TSel:
		Selection.append(T)
	return Selection

def StringToList(Variable):
	PrintCheck(Variable)
	PrintCheck( type(Variable))
	if(str(type(Variable)) == "<type 'str'>"):
		PrintCheck( "Changing" )
		Variable = [Variable]
	PrintCheck( "Return")
	PrintCheck( Variable)
	PrintCheck( type(Variable))
	return Variable

def PrintLine(Text,i,Size):
	if(Text != "" and Text != False):
		Line = Text[i]
		for T in range(Size):
			Line = Line + Text[i]
		print Line
	
def PrintCheck(Text,ONOFF=True,SeperatorType=False):
	ONOFF_Global = UI.CharSetUp_Set_Print()
	#print "Print Checking..."
	#print Text
	#print type(Text)
	Size	= 40
	if(ONOFF_Global):
		PrintLine(SeperatorType,0,Size)
		if (str(type(Text))== "<type 'list'>"):
			for T in Text:
				print T
		else:
			print Text
			
		PrintLine(SeperatorType,1,Size)
		
def Scene_UnitSettings_Set(U=0,Toggle=True):
	
	Unit = [["cm",100,3],["m",1,2]]
	Grid = [4,1]

	if Toggle:
		CUnit = cmds.currentUnit(query=True,linear=True)
		
		if CUnit == Unit[0][0]:
		   U = 1
	    
	cmds.currentUnit(linear=Unit[U][0])
	cmds.grid(da=True,dab=True,ddl=True,dgl=True,dol=False,dpl=False,d=2,sp=Grid[1]*Unit[U][1],size=Grid[0]*Unit[U][1])
	cmds.displayColor("grid" ,Unit[U][2]) 

	PrintCheck(Unit[U][0] + "--- has been set for Unit Size.. " )
	
	
def Get_ActivePanels():
	viewPanels    = cmds.getPanel(type="modelPanel")
	visiblePanels = cmds.getPanel(visiblePanels=True)
	ActivePanels  = list( set(viewPanels) & set(visiblePanels) ) 
	return ActivePanels


def DeleteUnkownNodes():
	Nodes = cmds.ls(type="unknown")
	for n in Nodes:
		cmds.lockNode(n,l=False)
		cmds.delete(n)
		
def ReplaceShapeNode(NodeWithShapeNode,TargetNode):
	print "test"
	
def ProgressBar_Run(WindowName,List,ProgressControl):
    # Create a custom progressBar in a windows ...
	print "Length of List :"
	print len(List)
	cmds.window(WindowName,q=True,exists=True)
	if cmds.window(WindowName,q=True,exists=True):
		#print "innnnnnn"

		cmds.progressBar(ProgressControl, edit=True, step=1)
	else:
		WindowName = cmds.window(WindowName)
		cmds.columnLayout()
		ProgressControl = cmds.progressBar(maxValue=len(List), width=300)
		cmds.showWindow( WindowName )

	StepValue = cmds.progressBar(ProgressControl, q=True,pr=True)
	print "StepValue :",StepValue,len(List)
	if StepValue == len(List)-2:
		cmds.deleteUI( WindowName, window=True )

	return [WindowName,ProgressControl]
    
def UI_Complete(Window):
	if cmds.window(Window,exists = True):
		cmds.deleteUI(Window)
	Window = cmds.window(Window,title=Window, widthHeight=(200, 55) )
	cmds.columnLayout(bgc=(0.4,0.5,0.4),cal="center")
	cmds.text( label='Congratulations ' + Window + ' Script completed',align='center' )
	cmds.button( label='Close', command=('cmds.deleteUI(\"' + Window + '\", window=True)'),align='center',bgc=(0.3,0.3,0.3) )
	cmds.setParent( '..' )
	cmds.showWindow( Window )