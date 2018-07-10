"""import pymel.all as pm

crvs = pm.ls(type=pm.nodetypes.AnimCurveTA)

for crv in crvs :
    plug = crv.listConnections(plugs=True)[0]
    plugname = 'Char:' + plug.name()
    newplug = pm.PyNode(plugname)
    crv.output >> newplug
"""