import os, sys
import xml.etree.ElementTree as etree
import xml.dom.minidom as md

FRAMERATE = 24

ANIMDATA = """
static_0                       0     1
idle_blink_0                   5     30
idle_happy_0                   35    60
idle_sad_0                     65    90
idle_sleep_0                   100   150
reaction_feed_0                160   200
reaction_laugh_0               210   250
reaction_wake_up_0             260   300
transition_0_1                 310   350
static_1                       355   356
idle_blink_1                   360   385
idle_happy_1                   390   415
idle_sad_1                     420   450
idle_sleep_1                   460   510
reaction_feed_1                520   560
reaction_laugh_1               570   610
reaction_wake_up_1             620   660
transition_1_2                 670   710
static_2                       715   716
idle_blink_2                   720   745
idle_happy_2                   755   780
idle_sad_2                     790   820
idle_sleep_2                   830   880
reaction_feed_2                890   950
reaction_laugh_2               960   1000
reaction_wake_up_2             1010  1050
transtition_2_3                1060  1100
static_3                       1105  1106
idle_blink_3                   1110  1135
idle_happy_3                   1145  1170
idle_sad_3                     1180  1210
idle_sleep_3                   1220  1270
reaction_feed_3                1280  1326
reaction_laugh_3               1350  1390
reaction_wake_up_3             1400  1440
transition_3_4                 1450  1490
static_4                       1495  1496
idle_blink_4                   1500  1525
idle_happy_4                   1535  1560
idle_sad_4                     1570  1600
idle_sleep_4                   1610  1660
reaction_feed_4                1670  1716
reaction_laugh_4               1740  1780
reaction_wake_up_4             1790  1830
transition_4_5                 1840  1880
static_5                       1885  1886
idle_blink_5                   1900  1925
idle_happy_5                   1935  1960
idle_sad_5                     1970  2000
idle_sleep_5                   2010  2060
reaction_feed_5                2070  2116
reaction_laugh_5               2130  2170
reaction_wake_up_5             2180  2220
celebratory_5                  2230  2265
"""


TIMELINES_FILE = "/Volumes/SSD/Work/FarmHeroes/FarmHeroes_dev/mobile/res/common/lo_pet/timelines.xml"
TIMELINES_DIR = "/Volumes/SSD/Work/FarmHeroes/FarmHeroes_dev/mobile/res/common/lo_pet/timelines"
TIMELINE_SCENE = "/Volumes/SSD/Work/FarmHeroes/FarmHeroes_dev/mobile/res/common/lo_pet/scenes/pet_main_scene.xml"

ROOTDIR = "/Volumes/SSD/Work/FarmHeroes/FarmHeroes_dev/mobile/res/common/"

s_endTime = '***ENDTIME***'
s_animationName = '***ANIMATIONNAME***'
s_targetName = '***TARGENAME***'


TIMELINE_SNIPPET = """
<Timelines>
	<Timeline startTime="0" endTime="{0}">
		<Triggers>
			<AnimationTrigger time="0" animationName="{1}" targetName="{2}">			
			</AnimationTrigger>
		</Triggers>	
	</Timeline>
</Timelines>
""".format( s_endTime, s_animationName, s_targetName )



timelinesEtree = etree.parse( TIMELINES_FILE )
timelinesXML = timelinesEtree.getroot()

animdata = ANIMDATA.splitlines()
for anim in animdata :
    s = anim.split()
    if( len(s) > 0 ) :
        name = s[0]
        start = int(s[1])
        end = int(s[2])
        length = end-start
        time = str(float(length) / FRAMERATE)

        timeline = TIMELINE_SNIPPET[0:]
        timeline = timeline.replace( '***ANIMATIONNAME***', name )
        timeline = timeline.replace( s_endTime, time )
        timeline = timeline.replace( s_targetName, 'CropsieModel' )

        # create timeline file

        filename = '%s.xml' % name
        filepath = os.path.join( TIMELINES_DIR, filename )

        try :
            xml = etree.fromstring( timeline )
            tree = etree.ElementTree(xml)
        except :
            print 'Could not create etree for %s' % name

        tree.write( filepath )
        
        # add to timelines.xml

        timelineEntries = timelinesXML.findall( "Timeline[@name='%s']" % name + '_tl' )
        if( timelineEntries is not None ) :
            for entry in timelineEntries :
                print 'removing ' % entry
                timelinesXML.remove( entry )

        timelineEntryAttribs = {
            'name' : name + '_tl',
            'timeline' : filepath.replace(ROOTDIR, ''),
            'scene' : TIMELINE_SCENE.replace(ROOTDIR, '')
        }
        timelineEntryElement = etree.Element( 'Timeline', timelineEntryAttribs )
        timelinesXML.append(timelineEntryElement)


# save timelines.xml

timelinesXMLPretty = md.parseString( etree.tostring(timelinesXML) ).toprettyxml()
with open(TIMELINES_FILE, 'w') as f :
    f.write( timelinesXMLPretty )


        
        

