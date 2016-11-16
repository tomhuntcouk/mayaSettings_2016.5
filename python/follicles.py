import pymel.all as pm

sel = pm.ls(sl=True)
src = sel.pop(0)

cpos = pm.ClosestPointOnSurface()
pm.connectAttr( src.getShape().worldSpace, cpos.inputSurface )
pm.select(None)

for obj in sel :
    cpos.inPosition.set( obj.getTranslation( space='world') )
    uv = ( cpos.u.get(), cpos.v.get() )
    print uv
    
    fol = pm.Follicle()
    src.local >> fol.inputSurface
    src.getShape().worldMatrix[0] >> fol.inputWorldMatrix
    fol.outRotate >> fol.getParent().rotate
    fol.outTranslate >> fol.getParent().translate
    
    fol.parameterU.set( uv[0] )
    fol.parameterV.set( uv[1] )

    pm.parentConstraint( fol.getParent(), obj, mo=True )

    
#pm.delete(cpos)

pm.select( src, sel )