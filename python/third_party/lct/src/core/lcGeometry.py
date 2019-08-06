
import pymel.core as pm

class Geometry():
  ''' '''
  def __init__(self, *args, **kwargs):
    ''' '''

  @classmethod
  def getAllGeometry(cls, *args, **kwargs):
    return cls.filterForGeometry(pm.ls(tr=True))

  @classmethod
  def getTransformsFromShapes(cls, shapes, *args, **kwargs):
    ''' '''
    return [ pm.PyNode(shape).getParent() for shape in shapes ]

  @classmethod
  def getVertsFromSelection(cls, sel, *args, **kwargs):
    ''' retains current selection, returns vert list flattented '''
    verts = pm.polyListComponentConversion(sel, tv=True)
    pm.select(verts, r=True)
    verts = pm.ls(sl=True, flatten=True)
    pm.select(sel, r=True)

    return verts

  @classmethod
  def getMeshSelectionType(cls, sel, *args, **kwargs):
    ''' '''
    if sel[0].nodeType() == 'mesh':
      componentType = sel[0].split('.')[1].split('[')[0]
      return componentType
    else:
      return 'mesh'

  @classmethod
  def switchSelectType(cls, type, *args, **kwargs):
    ''' '''
    if type == 'mesh':
      pm.selectMode(object=True)
    if type == 'vtx':
      pm.selectType(ocm=True, alc=False)
      pm.selectType(ocm=True, polymeshVertex=True)
    if type == 'e':
      pm.selectType(ocm=True, alc=False)
      pm.selectType(ocm=True, polymeshEdge=True)
    if type == 'f':
      pm.selectType(ocm=True, alc=False)
      pm.selectType(ocm=True, polymeshFace=True)

  @classmethod
  def filterForGeometry(cls, sel, *args, **kwargs):
    ''' filter the list for only geometry '''
    #This has problems, only works for selections from the viewport, as in things with transforms
    try:
      return [ obj for obj in sel if obj.getShape() and obj.getShape().nodeType() == 'mesh' ]
    except:
      return None

  @classmethod
  def checkMultipleShapes(cls, transform, *args, **kwargs):
    ''' '''
    shapes = pm.listRelatives(transform, fullPath=True, shapes=True)
    if len(shapes)>1:
      return None
    else:
      return shapes[0]

  @classmethod
  def fixNamespaceNames(cls, *args, **kwargs):
    ''' '''
    sel = pm.ls(sl=True)
    if sel:
      for obj in sel:
        if obj.find(':') != -1:
          newName = obj.split(':')[1]
          pm.rename(sel, newName)

  @classmethod
  def consolidateVerts(cls, vertGrpList, *args, **kwargs):
    ''' '''
    consolidated = []
    for verts in vertGrpList:
      for vert in verts:
        consolidated.append(vert)
    return consolidated


  # relaxVerts() and shrinkWrap() inspired by oaRelaxVerts.mel by Oleg Alexander
  @classmethod
  def relaxVerts(cls, verts, mesh, progBar='', *args, **kwargs):
    ''' '''
    if verts:
      pm.polyAverageVertex(verts, i=1)
      cls.shrinkWrap(verts, mesh, progBar)
    else:
      pm.warning('No verts selected')

  @classmethod
  def shrinkWrap(cls, verts, mesh, progBar='', *args, **kwargs):
    ''' '''
    scaleFactor = 1
    loc = pm.spaceLocator()

    pm.geometryConstraint(mesh, loc)
    pm.progressBar(progBar, edit=True, isInterruptable=True, maxValue = len(verts), vis=True)

    if verts:
      tmpPos = verts[0].getPosition(space='world')
      if len(tmpPos)==4:
        scaleFactor = 1/tmpPos[3]

    for vert in verts:
      if pm.progressBar(progBar, query=True, isCancelled=True):
        pm.progressBar(progBar, edit=True, vis=False)
        break
      else:
        currentVert = ((vert.split('.')[1]).lstrip('vtx[')).rstrip(']')

        vertPos = pm.pointPosition(vert, w=True)

        pm.move(loc, [vertPos[0], vertPos[1], vertPos[2] ], ws=True)

        locPos = pm.pointPosition(loc)

        pm.move(vert, [locPos[0], locPos[1], locPos[2] ], ws=True)

        pm.progressBar(progBar, edit=True, step=1)

    pm.progressBar(progBar, edit=True, vis=False)
    pm.progressBar(progBar, edit=True, endProgress=True)

    pm.delete(loc)

    pm.select(vert.split('.')[0], r=True)
    pm.delete(ch=True)

  @classmethod
  def weldVertContext(cls):
    ''' '''
    if not pm.scriptCtx('vertWeldCustom', exists=True):
      weldVert = pm.scriptCtx('vertWeldCustom', t='Weld Verts', tss=1, fcs='weldVertCustom($Selection1)', esl=1, snp='Select a Vertex, click a second vertex to weld to, Hold CTRL to merge to middle', ssp='Click a second vertex to weld to, Hold CTRL to merge to middle', setDoneSelectionPrompt='Select only one vertex to start', sat=1, ssc=2, sac=1, pv=1, euc=0, tct='edit', ts=lambda *args: cls.weldVertexToolStart() )
      cls.weldVertexContextToolStart()
      pm.setToolTo(weldVert)

  @classmethod
  def weldVertexContextToolStart(cls):
    ''' '''
    sel = pm.ls(dag=True, type='mesh')
    pm.select(cl=True)
    for item in sel:
      pm.mel.doMenuComponentSelection(item, 'pv')

  @classmethod
  def weldVertCustom(cls, sel, *args, **kwargs):
    ''' '''

class UV():
    def __init__(self, aspect = [1,1]):
      """ """ 
      self.aspect = aspect
        
    @classmethod    
    def grabShell(cls, *args, **kwargs):
      ''' from a selection of UV's selects the shell '''
      pm.polySelectConstraint(type=0x0010, shell=True, border=False, mode=2)    #select the uv shell
      pm.polySelectConstraint(shell=False, border=False, mode=0)                #reset the selection constraint
        
    def move(self, uvw, *args, **kwargs):
      ''' moves a selection of uv's '''
      pm.polyEditUV(uValue=uvw[0],vValue=uvw[1])

    def moveShell(self, uvw, *args, **kwargs):
      ''' moves the shell of a selection of uv's '''
      pm.polyEditUVShell(uValue=uvw[0],vValue=uvw[1])

    def rotate(self, angle, pivot, aspect, *args, **kwargs):
      scaleDownU = float(aspect[0])/float(aspect[1])
      scaleUpU = float(aspect[1])/float(aspect[0])
      pm.polyEditUV(pivotU=pivot[0], pivotV=pivot[1], r=False, scaleU=scaleDownU)
      pm.polyEditUV(pivotU=pivot[0], pivotV=pivot[1], a=angle)
      pm.polyEditUV(pivotU=pivot[0], pivotV=pivot[1], r=False, scaleU=scaleUpU)
     
    def rotateShell(self, angle, pivot, aspect, *args, **kwargs):    
      scaleDownU = float(aspect[0])/float(aspect[1])
      scaleUpU = float(aspect[1])/float(aspect[0])
      pm.polyEditUVShell(pivotU=pivot[0], pivotV=pivot[1], r=False, scaleU=scaleDownU)
      pm.polyEditUVShell(pivotU=pivot[0], pivotV=pivot[1], a=angle)
      pm.polyEditUVShell(pivotU=pivot[0], pivotV=pivot[1], r=False, scaleU=scaleUpU)

    def scale(self, uv, pivot, *args, **kwargs): 
      pm.polyEditUV(pivotU=pivot[0], pivotV=pivot[1], scaleU=uv[0], scaleV=uv[1])
  
    def scaleShell(self, uv, pivot, *args, **kwargs):
      pm.polyEditUVShell(pivotU=pivot[0], pivotV=pivot[1], scaleU=uv[0], scaleV=uv[1])
        
    def getBoundingBoxCenter(self, *args, **kwargs):
      """Get the center point of the UV's bounding box"""
      uvBB = pm.polyEvaluate(boundingBoxComponent2d=True)
      uvCenter=[((uvBB[0][1]+uvBB[0][0])/2),((uvBB[1][1]+uvBB[1][0])/2)]
      return uvCenter
    
    def getBoundingBoxCenterShell(self, *args, **kwargs):
      """Get the center point of the UV shell's bounding box"""
      self.grabShell()
      uvBB = pm.polyEvaluate(boundingBoxComponent2d=True)
      uvCenter=[((uvBB[0][1]+uvBB[0][0])/2),((uvBB[1][1]+uvBB[1][0])/2)]
      return uvCenter
    
    @classmethod
    def getUVSets(cls, *args, **kwargs):
      """ """
      return pm.polyUVSet(query=True, allUVSets=True)
    
    @classmethod
    def removeExtraSets(cls, obj, *args, **kwargs):
      """ remove all uv sets except for the default one """
      for i in pm.polyUVSet(obj, query=True, allUVSetsIndices=True)[1:]:
        name = pm.getAttr(obj+'.uvSet['+str(i)+'].uvSetName')
        pm.polyUVSet(obj, delete=True, uvSet=name)
        
