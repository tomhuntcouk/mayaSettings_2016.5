import pymel.all as pm

olddir = pm.fileDialog2(cap='Select Current Directory', ds=2, fm=3, okc="Select")[0]
newdir = pm.fileDialog2(cap='Select New Directory', ds=2, fm=3, okc="Select")[0]

files = pm.ls(type='file')

# repl = '/Volumes/GoogleDrive/My Drive/PNG/'
# add = 'map/map 3.0/'

# olddir = '/Volumes/GoogleDrive/My Drive/PNG/Assets'
# newdir = '/Volumes/SSD/Work/FarmHeroes/FarmHeroes_art/Game/map/map 3.0/Assets/test'


olddirlist = olddir.split(os.sep)[::-1]
newdirlist = newdir.split(os.sep)[::-1]

commondirs = []
for i, newd in enumerate(newdirlist) :
    oldd = olddirlist[i]
    if( newd == oldd ) :
        commondirs.append(newd)
    else :
        break
        
if( len(commondirs) > 0 ) :
    commondirs = commondirs[::-1]
    commonpath = os.path.join(*commondirs)
else :
    commonpath = ''


for f in files :
    isreference = pm.core.system.referenceQuery( f, isNodeReferenced=True)
    if isreference :
        continue        
    
    fpath = f.fileTextureName.get()
    fname = os.path.basename(fpath)
    
    ws = pm.core.system.Workspace.getPath()
    relpath = newdir.replace( ws, '' )[1:]
    
    newpath = os.path.join( relpath, fname )
    f.setAttr( 'fileTextureName', newpath)