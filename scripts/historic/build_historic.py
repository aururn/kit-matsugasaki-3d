"""Photo-calibrated KIT historic main building, revision 2. See RESEARCH.md."""
from pathlib import Path
import os, json, math, random
ROOT=Path(__file__).resolve().parents[2]
(ROOT/'build').mkdir(exist_ok=True)
os.environ['OPTIX_CACHE_PATH']=str(ROOT/'build/cache')
(ROOT/'build/cache').mkdir(exist_ok=True)
# Reuse only low-level mesh helpers, never the old building geometry.
exec((ROOT/'scripts/historic/mesh_helpers.py').read_text(encoding='utf-8-sig'))
from mathutils import Matrix
random.seed(724)
OUT=ROOT
for material in list(bpy.data.materials):
    if material.users==0:bpy.data.materials.remove(material)
def basic(name,c,rough=.6,metal=0):return mat(name,c,rough,metal)

def weathered(name,c,rough=.8,noise_scale=14,bump_strength=.2,bump_distance=.02):
    m=basic(name,c,rough);ns=m.node_tree.nodes;lk=m.node_tree.links;p=ns.get('Principled BSDF')
    g=ns.new('ShaderNodeNewGeometry');nt=ns.new('ShaderNodeTexNoise');nt.inputs['Scale'].default_value=noise_scale;nt.inputs['Detail'].default_value=4
    lk.new(g.outputs['Position'],nt.inputs['Vector'])
    ramp=ns.new('ShaderNodeValToRGB');ramp.color_ramp.elements[0].position=.15;ramp.color_ramp.elements[0].color=tuple(v*.55 for v in c)+(1,)
    ramp.color_ramp.elements[1].position=.85;ramp.color_ramp.elements[1].color=tuple(v*1.2 for v in c)+(1,)
    lk.new(nt.outputs['Fac'],ramp.inputs[0]);lk.new(ramp.outputs[0],p.inputs['Base Color'])
    bu=ns.new('ShaderNodeBump');bu.inputs['Strength'].default_value=bump_strength;bu.inputs['Distance'].default_value=bump_distance
    lk.new(nt.outputs['Fac'],bu.inputs['Height']);lk.new(bu.outputs[0],p.inputs['Normal']);return m

tile=basic('01 Scratched ochre ceramic tile | metric running bond',(.28,.16,.085),.86)
ns=tile.node_tree.nodes;lk=tile.node_tree.links;p=ns.get('Principled BSDF')
tc=ns.new('ShaderNodeTexCoord');sep=ns.new('ShaderNodeSeparateXYZ');lk.new(tc.outputs['UV'],sep.inputs[0])
br=ns.new('ShaderNodeTexBrick');br.inputs['Scale'].default_value=1;br.inputs['Brick Width'].default_value=.225;br.inputs['Row Height'].default_value=.065
br.inputs['Color1'].default_value=(.32,.185,.090,1);br.inputs['Color2'].default_value=(.46,.295,.155,1);br.inputs['Mortar'].default_value=(.185,.175,.145,1)
br.inputs['Mortar Size'].default_value=.0024;br.inputs['Mortar Smooth'].default_value=.001;lk.new(tc.outputs['UV'],br.inputs[0])
noise=ns.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=1.2;noise.inputs['Detail'].default_value=5;lk.new(tc.outputs['UV'],noise.inputs[0])
mix=ns.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=.33;lk.new(br.outputs['Color'],mix.inputs[1]);lk.new(noise.outputs['Fac'],mix.inputs[2]);lk.new(mix.outputs[0],p.inputs['Base Color'])
scratch=ns.new('ShaderNodeTexWave');scratch.wave_type='BANDS';scratch.bands_direction='X';scratch.inputs['Scale'].default_value=165;scratch.inputs['Distortion'].default_value=2;scratch.inputs['Detail Scale'].default_value=12
lk.new(tc.outputs['UV'],scratch.inputs['Vector'])
bu1=ns.new('ShaderNodeBump');bu1.inputs['Strength'].default_value=.22;bu1.inputs['Distance'].default_value=.0012;lk.new(scratch.outputs[0],bu1.inputs['Height'])
bu2=ns.new('ShaderNodeBump');bu2.invert=True;bu2.inputs['Strength'].default_value=.45;bu2.inputs['Distance'].default_value=.008
lk.new(br.outputs['Fac'],bu2.inputs['Height']);lk.new(bu1.outputs[0],bu2.inputs['Normal']);lk.new(bu2.outputs[0],p.inputs['Normal'])
stone=weathered('02 Weathered pale stone',(.39,.38,.32),noise_scale=18,bump_distance=.007)
roof=weathered('03 Oxidised dark coping',(.075,.085,.075),noise_scale=13,bump_distance=.005)
frame=weathered('04 Thin aged aluminium frames',(.57,.61,.57),rough=.36,noise_scale=80,bump_distance=.001)
teal=weathered('05 Blue green painted entrance joinery',(.10,.25,.255),rough=.4,noise_scale=45,bump_distance=.001)
dark=basic('06 Interior deep shadow',(.025,.028,.024),.96)
roomwall=weathered('07 Room plaster',(.55,.53,.44),noise_scale=40,bump_distance=.003)
blind=weathered('08 Pale grey roller blinds',(.45,.49,.46),noise_scale=130,bump_distance=.0008)
bronze=basic('09 Oxidised bronze',(.20,.18,.095),.5,.6)
glass=basic('10 Optical window glass',(.86,.94,.96),.075)
gp=glass.node_tree.nodes.get('Principled BSDF');gp.inputs['Transmission Weight'].default_value=.97;gp.inputs['IOR'].default_value=1.46
glassAlt=glass.copy();glassAlt.name='11 Slightly dusty window glass';glassAlt.node_tree.nodes.get('Principled BSDF').inputs['Roughness'].default_value=.16
concrete=weathered('12 Rough grey concrete',(.27,.28,.26),noise_scale=45,bump_distance=.018)
soil=weathered('13 Dry earth / moss',(.072,.086,.035),noise_scale=32,bump_distance=.032)
grass=weathered('14 Sparse grass',(.085,.12,.038),noise_scale=55,bump_distance=.025)
bark=weathered('15 Fibrous palm bark',(.070,.048,.024),noise_scale=75,bump_distance=.035)
leafm=[]
for i,c in enumerate([(.055,.11,.025),(.080,.16,.035),(.12,.19,.04),(.035,.080,.018),(.17,.20,.045)]):
    m=weathered('Leaf '+str(i),c,rough=.52,noise_scale=65,bump_distance=.001)
    m.node_tree.nodes.get('Principled BSDF').inputs['Subsurface Weight'].default_value=.045
    leafm.append(m)
deadleaf=weathered('Dry palm fronds',(.15,.105,.035),noise_scale=80,bump_distance=.005)
asphalt=basic('Poly Haven asphalt_01 / 2K PBR',(.16,.16,.15),.9)
ns=asphalt.node_tree.nodes;lk=asphalt.node_tree.links;p=ns.get('Principled BSDF');uv=ns.new('ShaderNodeTexCoord')
for ch,socket in [('Diffuse','Base Color'),('Rough','Roughness')]:
    im=ns.new('ShaderNodeTexImage');im.image=bpy.data.images.load(str(ROOT/'assets/textures'/('asphalt_'+ch+'.jpg')))
    if ch!='Diffuse':im.image.colorspace_settings.name='Non-Color'
    lk.new(uv.outputs['UV'],im.inputs['Vector']);lk.new(im.outputs['Color'],p.inputs[socket])
im=ns.new('ShaderNodeTexImage');im.image=bpy.data.images.load(str(ROOT/'assets/textures'/'asphalt_nor_gl.jpg'));im.image.colorspace_settings.name='Non-Color'
lk.new(uv.outputs['UV'],im.inputs[0]);normal=ns.new('ShaderNodeNormalMap');normal.inputs['Strength'].default_value=.4;lk.new(im.outputs[0],normal.inputs['Color']);lk.new(normal.outputs[0],p.inputs['Normal'])

# Metric box-projected UVs. Unlike Generated coordinates, courses keep their size
# across wall fragments and turn the corner correctly.
old_cube=cube
def cube(name,loc,dims,material,bevel=0):
    obj=old_cube(name,loc,dims,material,bevel)
    mesh=obj.data;uv=mesh.uv_layers.new(name='Metric projection')
    scale=1/4 if material==asphalt else 1
    for poly in mesh.polygons:
        n=poly.normal;axis=max(range(3),key=lambda i:abs(n[i]))
        for li in poly.loop_indices:
            co=mesh.vertices[mesh.loops[li].vertex_index].co+Vector(loc)
            pair=(co.y,co.z) if axis==0 else (co.x,co.z) if axis==1 else (co.x,co.y)
            uv.data[li].uv=(pair[0]*scale,pair[1]*scale)
    return obj
def localpoint(origin,u,z,theta=0,v=0):
    return Vector(origin)+Vector((math.cos(theta)*u-math.sin(theta)*v,math.sin(theta)*u+math.cos(theta)*v,z))
def panel(name,origin,loc,dims,material,theta=0,bev=0):
    pos=localpoint(origin,loc[0],loc[2],theta,loc[1]);o=cube(name,pos,dims,material,bev);o.rotation_euler.z=theta;return o
def line(name,pts,r,material):
    cu=bpy.data.curves.new(name,'CURVE');cu.dimensions='3D';cu.resolution_u=1;cu.bevel_depth=r;cu.bevel_resolution=2
    sp=cu.splines.new('POLY');sp.points.add(len(pts)-1)
    for p0,p1 in zip(sp.points,pts):p0.co=(*p1,1)
    ob=bpy.data.objects.new(name,cu);COL.objects.link(ob);cu.materials.append(material);return ob

WIN_RECORD=[]
def glazing(name,origin,u,z,w=2.04,h=2.63,theta=0,vent=False,curtain=True):
    # Window plane is recessed 12 cm behind the masonry; the wall itself has a void.
    def part(s,loc,dims,m,bev=0):return panel(name+' / '+s,origin,(loc[0]+u,loc[1],loc[2]+z),dims,m,theta,bev)
    for x in [-w/2,w/2]:part('perimeter vertical',(x,.07,0),(.045,.065,h),frame,.006)
    for zz in [-h/2,h/2]:part('perimeter horizontal',(0,.07,zz),(w,.065,.045),frame,.006)
    part('central fine mullion',(0,.045,0),(.032,.065,h),frame,.004)
    # Large middle lights with shallow upper/lower lights, matching photo.
    bars=[-h*.29,h*.05,h*.26]
    for zz in bars:part('horizontal sash',(0,.042,zz),(w,.07,.036),frame,.003)
    for a,b in zip([-h/2]+bars,bars+[h/2]):
        for s in [-1,1]:part('individual glass light',(s*w*.25,.095,(a+b)/2),(w*.5-.038,.008,b-a-.036),glassAlt if random.random()<.12 else glass)
    part('dark lintel reveal',(0,.05,h/2+.035),(w+.09,.29,.08),roof)
    part('slender sill',(0,-.01,-h/2-.055),(w+.11,.27,.09),stone,.008)
    # Closed room boxes give glass genuine depth and differing reflections.
    part('room back wall',(0,2.4,0),(w+.5,.08,h+.55),roomwall)
    for s in [-1,1]:part('room side',(s*(w/2+.22),1.25,0),(.08,2.4,h+.55),roomwall)
    part('room ceiling',(0,1.25,h/2+.22),(w+.5,2.4,.08),roomwall)
    part('room floor',(0,1.25,-h/2-.22),(w+.5,2.4,.08),dark)
    if curtain:
        length=random.choice([.2,.4,.9,1.3,h-.12,h-.18])
        part('partly lowered blind',(0,.29,h/2-length/2-.03),(w-.10,.018,length),blind)
        part('blind lower bar',(0,.285,h/2-length-.03),(w-.06,.035,.026),frame)
    if vent:
        part('square exhaust panel',(-w*.29,.005,h*.37),(.39,.10,.35),stone)
        o=part('small exhaust hood',(-w*.29,-.075,h*.36),(.31,.30,.045),roof);o.rotation_euler.x=.35
    WIN_RECORD.append({'name':name,'u':u,'z':z,'w':w,'h':h})

def facade(name,origin,length,height,windows,theta=0,thick=.36,skip_glazing=()):
    # Partition wall into real solid strips around openings, no black decals.
    cuts=sorted(set([0,height]+[round(w[1]-w[3]/2,5) for w in windows]+[round(w[1]+w[3]/2,5) for w in windows]))
    for a,b in zip(cuts,cuts[1:]):
        mid=(a+b)/2;spans=sorted([(u-w/2,u+w/2) for u,z,w,h in windows if z-h/2<mid<z+h/2])
        last=0
        for lo,hi in spans+[(length,length)]:
            if lo>last:panel(name+' masonry',origin,((last+lo)/2,thick/2,mid),(lo-last,thick,b-a),tile,theta)
            last=max(last,hi)
    for i,(u,z,w,h) in enumerate(windows):
        if i not in skip_glazing:glazing(name+' window '+str(i+1),origin,u,z,w,h,theta,vent=(random.random()<.19))

H=14.2;L=json.loads((ROOT/'data/camera-calibration.json').read_text())['left_wing_length_m'];CW=8.4;HALF=L+CW/2
ZS=[2.62,7.25,11.60]
collection('A Main historic facade / measured image ratios')
for side in [-1,1]:
    x0=-HALF if side<0 else CW/2
    wins=[(L*(i+.5)/7,z,2.08,2.57 if j else 2.77) for i in range(7) for j,z in enumerate(ZS)]
    facade(('South' if side<0 else 'North')+' front wing',(x0,0,0),L,H,wins)
cube('Main roof deck',(0,5.5,H-.24),(2*HALF,11,.16),concrete)
for x0 in [-HALF+9.2,8.5]:
    length=HALF-9.2-8.5
    facade('Main wing courtyard return',(x0+length,11,0),length,H,[(length*(i+.5)/3,z,1.8,2.57) for i in range(3) for z in ZS],math.pi)
for y in [0,11]:cube('Dark narrow roof coping',(0,y,H+.02),(2*HALF+.07,.13,.075),roof,.008)
for x in [-HALF,HALF]:cube('Narrow corner roof coping',(x,5.5,H+.02),(.13,11.1,.075),roof,.008)
for s in [-1,1]:
    for i in [1,3,5]:
        x=s*(CW/2+L*(i+.1)/7)
        line('Facade rainwater downpipe',[(x,-.13,.4),(x,-.13,H-.35),(x,-.25,H-.2)],.042,bronze)
        cube('Rainwater hopper',(x,-.14,H-.28),(.23,.23,.30),roof,.012)
        for z in [1.1,4.3,8.7,12.6]:cube('Pipe fixing',(x,-.10,z),(.16,.18,.03),bronze)
    for i in [1,5]:cube('Roof chimney',(s*(6+i*3.5),6,H+.75),(.65,.65,1.5),concrete,.025)
cube('Low dark foundation',(0,-.02,.22),(2*HALF,.15,.43),roof,.012)
print('Front facade complete',flush=True)

collection('B Projecting entrance / open doors and canopy')
TH=14.52;TY=-2.9
tower_wins=[(u,z,1.64,2.57) for u in [1.90,4.20,6.50] for z in [7.25,11.60]]+[(4.2,2.24,3.95,3.86)]
facade('Projecting entrance front',(-CW/2,TY,0),CW,TH,tower_wins,skip_glazing=[6])
for side in [-1,1]:
    origin=(side*CW/2,TY if side>0 else 0,0);theta=side*math.pi/2
    facade('Entrance bay side',origin,2.9,TH,[(1.45,z,1.58,2.57) for z in [7.25,11.60]],theta)
    for z in [7.25,11.60]:
        for x in [-1.15,1.15]:cube('Short pale separator between upper lights',(x,TY-.03,z),(.16,.10,2.83),stone,.006)
cube('Tower flat roof',(0,-1.45,TH-.1),(CW,2.9,.2),concrete)
for y in [TY,.0]:cube('Tower thin dark coping',(0,y,TH+.025),(CW+.07,.15,.065),roof,.008)
for x in [-CW/2,CW/2]:cube('Tower side coping',(x,-1.45,TH+.025),(.14,2.95,.065),roof,.008)
# Recessed stone surround and original blue transom framing.
for side in [-1,1]:
    cube('Portal stone jamb',(side*2.08,TY-.08,2.24),(.20,.40,3.98),stone,.01)
    cube('Blue outer portal stile',(side*1.86,TY+.12,2.23),(.15,.14,3.77),teal,.008)
cube('Portal stone head',(0,TY-.08,4.23),(4.36,.40,.18),stone,.01)
cube('Blue doorway transom upper',(0,TY+.09,4.09),(3.85,.15,.15),teal,.008)
cube('Blue doorway transom lower',(0,TY+.09,3.35),(3.85,.15,.15),teal,.008)
cube('Transom glass',(0,TY+.17,3.72),(3.65,.008,.65),glass)
for x in [-.94,0,.94]:cube('Transom upright',(x,TY+.065,3.72),(.07,.12,.67),teal,.006)
for x in [-1.44,-.47,.47,1.44]:
    for z in [3.56,3.84]:cube('Transom decorative horizontal',(x,TY+.01,z),(.66,.035,.023),teal)
    for dx in [-.28,.28]:cube('Transom decorative vertical',(x+dx,TY+.01,3.72),(.022,.035,.32),teal)
# Glazed sidelights.
for side in [-1,1]:
    x=side*1.56
    cube('Sidelight glass',(x,TY+.15,1.86),(.54,.008,2.8),glass)
    for dx in [-.31,0,.31]:cube('Sidelight vertical',(x+dx,TY+.10,1.86),(.055,.11,2.92),teal)
    for z in [.43,.94,1.52,2.09,2.66,3.29]:cube('Sidelight cross rail',(x,TY+.10,z),(.65,.11,.05),teal)
# Two open leaves, shallow glass lights and worn paint.
for side in [-1,1]:
    angle=side*math.radians(66);hinge=(side*1.22,TY+.08,.0);direction=-side;u=direction*.55
    for dx in [-.53,.53]:panel('Open blue door stile',hinge,(u+dx,0,1.86),(.12,.12,2.95),teal,angle,.015)
    for z,hh in [(.46,.19),(.96,.12),(3.24,.17)]:panel('Open blue door rail',hinge,(u,0,z),(1.17,.12,hh),teal,angle,.01)
    panel('Open door lower solid panel',hinge,(u,.012,.72),(.95,.065,.4),teal,angle)
    panel('Open door glass',hinge,(u,.015,2.08),(.95,.008,2.06),glass,angle)
    for dx in [-.30,0,.30]:panel('Open leaf fine glazing bar',hinge,(u+dx,-.06,2.07),(.025,.04,2.06),teal,angle)
    for z in [1.18,1.86,2.55]:panel('Open leaf sash',hinge,(u,-.062,z),(.99,.04,.03),teal,angle)
    pt=localpoint(hinge,u+direction*.33,1.60,angle,-.12)
    line('Door bronze pull',[pt,pt+Vector((0,0,.28))],.019,bronze)
cube('Entrance floor',(0,.2,.24),(3.95,6.4,.20),stone)
for s in [-1,1]:cube('Entrance internal plaster side',(s*2.14,.5,2.7),(.23,6.8,5.0),roomwall)
cube('Entrance internal ceiling',(0,.6,4.8),(4.2,7,.18),roomwall)
cube('Interior backdrop',(0,6.7,3),(4.2,.2,6),dark)
for i in range(14):cube('Visible indicative interior stair',(0,.9+i*.30,.37+i*.145),(3.4,.32,.16),stone,.014)
for i in range(3):cube('Entrance worn step',(0,TY-.45-i*.33,.29-i*.09),(4.3+i*.2,.83,.12),stone,.015)
# Deep, dark concrete canopy with accurate shallow frieze and diagonal brackets.
cube('Main entrance canopy',(0,TY-.79,4.79),(5.65,2.12,.22),stone,.025)
cube('Dark weathered canopy top',(0,TY-.79,4.93),(5.66,2.14,.07),roof,.018)
cube('Canopy carved front frieze',(0,TY-1.84,4.64),(5.67,.16,.31),stone,.014)
cube('Canopy underside blue glazing',(0,TY-.75,4.63),(5.03,1.74,.045),glassAlt)
for x in [-2.43,-1.60,-.80,0,.8,1.6,2.43]:cube('Canopy underside ribs',(x,TY-.76,4.53),(.10,1.98,.15),stone,.008)
for side in [-1,1]:
    for d in [0,.14,.28]:
        x=side*(2.09+d)
        line('Canopy projecting support',[(x,TY-.04,3.62),(x,TY-1.68,4.48)],.065,stone)
for i in range(23):
    x=-2.65+i*.232
    pts=[(x-.10,TY-1.927,4.52),(x-.10,TY-1.927,4.74),(x+.10,TY-1.927,4.74),(x+.10,TY-1.927,4.57),(x-.045,TY-1.927,4.57),(x-.045,TY-1.927,4.68),(x+.035,TY-1.927,4.68)]
    line('Carved Greek key on canopy',pts,.013,roof)
for side in [-1,1]:
    cube('Entry wall lamp',(side*2.81,TY-.15,2.96),(.18,.17,.27),bronze,.016)
    cube('Heritage / office plaque',(side*2.70,TY-.023,1.79),(.33,.045,.23),bronze,.012)
print('Entrance complete',flush=True)

def ribbon_glazing(name,origin,start,end,z,theta):
    """Continuous projected band, with shared jambs rather than nested windows."""
    width=end-start; h=2.88; count=10; bay=width/count
    def part(s,u,v,zz,w,d,hh,m):return panel(name+' / '+s,origin,(u,v,zz),(w,d,hh),m,theta,.004)
    # Entire glazing plane projects from the original masonry.
    for zz in [z-h/2,z+h/2]:part('continuous metal perimeter',(start+end)/2,-.25,zz,width,.09,.065,frame)
    for i in range(count+1):part('structural mullion',start+i*bay,-.26,z,.075,.15,h,frame)
    for i in range(count):
        c=start+(i+.5)*bay
        for f in [-1/6,1/6]:part('slender sash vertical',c+bay*f,-.285,z,.037,.065,h,frame)
        # Deep main light and shallow opening lights, observed in renovation photos.
        cuts=[-h/2,-.84,.91,h/2]
        for zz in cuts[1:-1]:part('sash transom',c,-.29,z+zz,bay,.08,.045,frame)
        for j in range(3):
            u=c+(j-1)*bay/3
            for a,b in zip(cuts,cuts[1:]):part('separate glass light',u,-.225,z+(a+b)/2,bay/3-.055,.01,b-a-.045,glass)
        part('room back',c,2.8,z,bay,.12,h+.4,roomwall)
        part('room floor',c,1.3,z-h/2-.04,bay,3.0,.08,dark)
        part('room ceiling',c,1.3,z+h/2+.04,bay,3.0,.08,roomwall)
        length=[.42,.72,.20,1.48,.3,1.05,.25,1.72,.55,.22][i]
        part('roller blind',c,.12,z+h/2-length/2-.03,bay-.12,.02,length,blind)
    for u in [start,end]:part('end reveal',u,-.06,z,.12,.5,h,stone)

def secondary_door(name,origin,u,theta):
    """Recessed closed glazed pair, clear threshold and continuous accessible landing."""
    def part(s,x,y,z,w,d,h,m):return panel(name+' / '+s,origin,(u+x,y,z),(w,d,h),m,theta,.009)
    w=2.25; top=2.88; bottom=.18
    for x in [-w/2,w/2]:part('stone jamb',x,0,(top+bottom)/2,.15,.44,top-bottom+.20,stone)
    part('stone lintel',0,0,top,w+.25,.44,.15,stone)
    for x in [-w/2+.10,0,w/2-.10]:part('painted stile',x,.13,1.46,.075,.11,2.56,teal)
    for x in [-.52,.52]:
        part('door glass',x,.17,1.65,.96,.012,2.08,glass)
        part('kick panel',x,.13,.43,.97,.07,.42,teal)
        for z0 in [.68,2.32,2.74]:part('door horizontal rail',x,.12,z0,1.01,.10,.065,teal)
        part('pull handle',x*.24,.025,1.32,.026,.06,.32,bronze)
    part('room darkness',0,2,1.6,2.5,.1,3.0,dark)
    part('landing',0,-.83,.07,3.0,1.95,.12,stone)
    part('canopy',0,-.49,3.24,3.1,1.55,.16,stone)
    part('canopy dark flashing',0,-.49,3.34,3.12,1.57,.04,roof)
    for x in [-1.08,1.08]:
        a=localpoint(origin,u+x,2.64,theta,0);b=localpoint(origin,u+x,3.13,theta,-1.1)
        line(name+' canopy bracket',[a,b],.042,bronze)
    part('wall light',1.45,-.12,2.32,.16,.18,.22,bronze)

collection('C E shaped returns / continuous window bands')
# Heritage record confirms E shape. Return and hall lengths remain approximations.
RETURN=49.0
for side in [-1,1]:
    outerx=side*HALF;theta=side*math.pi/2
    org=(outerx,0 if side>0 else RETURN,0)
    # Two conventional corner bays, followed by the long modernist ribbon.
    wins=[]
    for z in ZS:
        for y in [2.35,6.65]:wins.append(((y if side>0 else RETURN-y),z,2.08,2.57 if z>3 else 2.77))
    for i in range(10):
        y=12.0+i*3.5
        if i!=5:wins.append(((y if side>0 else RETURN-y),2.40,2.75,1.85))
    # The upper strip openings are divided only by slender mullions.
    skip=[]
    start,end=(9.6,46.25) if side>0 else (RETURN-46.25,RETURN-9.6)
    for z in [7.25,11.6]:
        skip.append(len(wins));wins.append(((start+end)/2,z,end-start,2.88))
    door_u=29.5 if side>0 else RETURN-29.5
    skip.append(len(wins));wins.append((door_u,1.52,2.25,2.72))
    facade('South return' if side<0 else 'North return',org,RETURN,H,wins,theta,skip_glazing=skip)
    for z in [7.25,11.6]:ribbon_glazing('South ribbon' if side<0 else 'North ribbon',org,start,end,z,theta)
    secondary_door('South side entrance' if side<0 else 'North side entrance',org,door_u,theta)
    for z in [5.70,10.05,13.11]:
        cube('Ribbon window projecting horizontal lip',(outerx+side*.23,27.925,z),(.60,36.8,.15),stone,.05)
    cube('Projected tiled ribbon spandrel',(outerx+side*.14,27.925,9.43),(.36,36.65,1.42),tile,.035)
    for y in [9.60,46.25]:cube('Ribbon end rounded pier',(outerx+side*.05,y,9.43),(.42,.35,7.48),tile,.13)
    cube('Return roof slab',(side*(HALF-4.6),RETURN/2,H-.18),(9.2,RETURN,.18),concrete)
    endorg=(side*(HALF-4.6)-4.6,RETURN,0)
    endwins=[(u,z,1.75,2.55) for u in [2.1,7.1] for z in ZS]
    endwins.append((4.6,1.52,2.25,2.72))
    facade('Rear end elevation',(endorg[0]+9.2,RETURN,0),9.2,H,endwins,math.pi,skip_glazing=[6])
    secondary_door('Rear return entrance',(endorg[0]+9.2,RETURN,0),4.6,math.pi)
    cube('Return roof thin coping',(outerx,RETURN/2,H+.02),(.14,RETURN,.08),roof,.009)
    for y in [8.1,47.3]:
        x=outerx+side*.20
        line('Return downpipe',[(x,y,.2),(x,y,13.5),(x,y+.15,13.8)],.043,bronze)
    # Rear courtyard fenestration is indicative and clearly separated in collection.
    inner_theta=-side*math.pi/2;inner_origin=(side*(HALF-9.2),RETURN if side>0 else 0,0)
    inner_wins=[(y,z,2.0,2.57) for y in range(4,46,4) for z in ZS]
    facade('Indicative courtyard elevation',inner_origin,RETURN,H,inner_wins,inner_theta)
for y in [11.0,37.0]:cube('Rear lecture hall end wall',(0,y,4.85),(17.0,.36,9.7),tile)
cube('Lecture hall roof',(0,24.0,9.80),(17.2,26.2,.18),roof,.03)
for side in [-1,1]:
    hall_windows=[(y-11,5.8,1.6,3.5) for y in range(14,36,4)]
    facade('Indicative hall elevation',(side*8.5,11 if side>0 else 37,0),26,9.7,hall_windows,side*math.pi/2)
print('E shape and ribbon glazing complete',flush=True)

collection('D Site / asphalt, curved planting margins')
cube('Continuous asphalt ground',(0,12,-.11),(260,240,.2),asphalt)
def ground_patch(name,points,z,material):
    me=bpy.data.meshes.new(name);me.from_pydata([(x,y,z) for x,y in points],[],[tuple(range(len(points)))])
    me.materials.append(material);o=bpy.data.objects.new(name,me);COL.objects.link(o);return o
for side in [-1,1]:
    pts=[(side*x,y) for x,y in [(5.0,-.05),(HALF+3.1,-.05),(HALF+3.1,44),(HALF+4.7,44),(HALF+4.7,-2.3),(HALF+4.5,-3.1),(HALF+3.8,-3.9),(HALF+2.7,-4.3),(7,-4.3),(5.8,-3.8),(5.0,-2.8)]]
    ground_patch('Grass planting island',pts,.055,grass)
    line('Curved stone curb',[(x,y,.095) for x,y in pts]+[(pts[0][0],pts[0][1],.095)],.075,concrete)
    cube('Inner courtyard soil',(side*14.5,26,.015),(11,28,.035),soil)
for i in range(5):
    for j in range(3):cube('Entry paving slabs',(-2.25+i*.9,-3.28-j*.73,.06),(.89,.72,.075),stone,.007)

collection('E Botanical geometry / fan palms and small leaves')
def foliage_object(name,verts,faces,indices=None,materials=leafm):
    me=bpy.data.meshes.new(name);me.from_pydata(verts,[],faces)
    for m in materials:me.materials.append(m)
    if indices:
        for f,mi in zip(me.polygons,indices):f.material_index=mi
    ob=bpy.data.objects.new(name,me);COL.objects.link(ob);return ob
def leaf_patch(verts,faces,indices,center,axis,length,width,mi):
    d=Vector(axis).normalized();across=d.cross(Vector((0,0,1)))
    if across.length<.05:across=d.cross(Vector((1,0,0)))
    across.normalize();c=Vector(center);up=d.cross(across).normalized()
    v=[c-d*length*.45,c-d*length*.15+across*width,c+d*length*.22+across*width*.72,c+d*length*.55,c+d*length*.22-across*width*.72,c-d*length*.15-across*width,c+up*width*.2]
    start=len(verts);verts.extend(v)
    for j in range(6):faces.append((start+j,start+(j+1)%6,start+6));indices.append(mi)
def shrub(x,y,rx,ry,h,seed):
    rng=random.Random(seed);vs=[];fs=[];idx=[]
    ico('Dense shaded interior of shrub',(x,y,.38*h),(.84*rx,.84*ry,.48*h),leafm[3],3)
    # Distributed elliptical leaves, with clustered rather than spherical silhouette.
    for k in range(4400):
        az=rng.uniform(0,math.tau);el=rng.uniform(-.1,math.pi/2);rr=rng.uniform(.83,1.07)
        px=x+math.cos(az)*math.cos(el)*rx*rr;py=y+math.sin(az)*math.cos(el)*ry*rr;pz=.14+math.sin(el)*h*rr
        leaf_patch(vs,fs,idx,(px,py,pz),(math.cos(az)+rng.uniform(-1,1),math.sin(az)+rng.uniform(-1,1),rng.uniform(-.35,.8)),rng.uniform(.045,.11),rng.uniform(.017,.032),rng.randrange(len(leafm)))
    foliage_object('Azalea shrub / individual leaves',vs,fs,idx)
    for i in range(6):beam('Azalea woody branch',(x,y,.05),(x+rng.uniform(-rx*.6,rx*.6),y+rng.uniform(-ry*.6,ry*.6),h*.62),.017,bark)
def palm(x,y,h,seed):
    rng=random.Random(seed);vs=[];fs=[];idx=[]
    # Continuous tapered, slightly irregular fibrous trunk.
    tv=[];tf=[];rings=65;segments=14;lean=rng.uniform(-.22,.22)
    for j in range(rings):
        z=j/(rings-1)*h;r=.12+(.006*math.sin(j*1.9))+.02*j/rings
        for k in range(segments):
            a=k*math.tau/segments;rr=r*rng.uniform(.93,1.1);tv.append((x+math.cos(a)*rr+lean*z/h,y+math.sin(a)*rr,z))
    for j in range(rings-1):
        for k in range(segments):tf.append((j*segments+k,j*segments+(k+1)%segments,(j+1)*segments+(k+1)%segments,(j+1)*segments+k))
    foliage_object('Rough fibrous palm trunk',tv,tf,materials=[bark])
    for k in range(55):
        az=rng.uniform(0,math.tau);z=rng.uniform(h*.45,h-.4);rr=.16
        line('Hanging trunk fibres',[(x+math.cos(az)*rr,y+math.sin(az)*rr,z),(x+math.cos(az)*.24,y+math.sin(az)*.24,z-.23),(x+math.cos(az)*.19,y+math.sin(az)*.19,z-.45)],.006,deadleaf)
    for k in range(27):
        az=k*2.39996+rng.uniform(-.16,.16);elev=rng.uniform(-.55,.9);stemlen=rng.uniform(.50,.95)
        radial=Vector((math.cos(az),math.sin(az),0));tangent=Vector((-math.sin(az),math.cos(az),0))
        root=Vector((x+lean,y,h));hub=root+radial*stemlen+Vector((0,0,elev*.6))
        line('Palm slender petiole',[root,root.lerp(hub,.6)+Vector((0,0,.12)),hub],.012,leafm[1])
        for j in range(29):
            a=(j-14)/14*1.08;d=radial*math.cos(a)+tangent*math.sin(a);length=rng.uniform(.63,.91)*(1-.13*abs(j-14)/14)
            sid=Vector((-d.y,d.x,0));start=len(vs)
            # The pleated fan is continuous near the hub and splits into drooping fingers.
            for t in [0,.27,.55,.80,1.0]:
                center=hub+d*(length*t)+Vector((0,0,.12*math.sin(math.pi*t)+elev*.35*t-.38*t*t))
                width=.009 if t==0 else (.029 if t<.8 else .015)*(1-t*.75)
                vs.extend([center-sid*width,center+Vector((0,0,.011*(1-t))),center+sid*width])
            mi=rng.randrange(4)
            for t in range(4):
                for a1,b1 in [(0,1),(1,2)]:fs.append((start+t*3+a1,start+t*3+b1,start+(t+1)*3+b1,start+(t+1)*3+a1));idx.append(mi)
    foliage_object('Pleated fan palm canopy',vs,fs,idx)
    # Triangular wooden supports and dark ties visible in the photographs.
    if seed%3!=0:
        for k in range(3):
            a=k*math.tau/3
            beam('Palm support stake',(x+math.cos(a)*.47,y+math.sin(a)*.47,.05),(x+math.cos(a)*.09,y+math.sin(a)*.09,h*.50),.036,stone)
for side in [-1,1]:
    for i in range(9):
        x=side*(6.8+i*2.6);y=-2.0+random.uniform(-.75,.7)
        palm(x,y,random.uniform(5.5,7.1),100+i+int(side)*10)
    for i in range(5):
        y=8+i*7.2
        if abs(y-29.5)>3.0:palm(side*(HALF+2.0),y,random.uniform(5.5,6.6),300+i+int(side)*10)
    for i in range(7):shrub(side*(7.0+i*3.85),-3.30,random.uniform(1.1,1.6),.75,random.uniform(.75,1.2),500+i+int(side)*10)
    for i in range(7):
        y=2.6+i*6.2
        if abs(y-29.5)>3.0:shrub(side*(HALF+3.1),y,1.0,1.2,.9,700+i+int(side)*10)
    ramppts=[(side*(HALF+.15),28,.18),(side*(HALF+5.0),28,.035),(side*(HALF+5.0),31,.035),(side*(HALF+.15),31,.18)]
    me=bpy.data.meshes.new('Side entrance accessible path');me.from_pydata(ramppts,[],[(0,1,2,3)]);me.materials.append(stone)
    ob=bpy.data.objects.new('Side entrance clear approach',me);COL.objects.link(ob)
# Irregular grass blades in front of the palm trunks.
gv=[];gf=[];gi=[]
for i in range(24000):
    side=random.choice([-1,1]);x=side*random.uniform(5.2,HALF+2);y=random.uniform(-4.1,-.1)
    a=random.random()*math.tau;h=random.uniform(.025,.15);base=Vector((x,y,.055));s=Vector((math.cos(a),math.sin(a),0))*.008;start=len(gv)
    gv.extend([base-s,base+s,base+Vector((.025*math.cos(a),.025*math.sin(a),h))]);gf.append((start,start+1,start+2));gi.append(random.randrange(5))
foliage_object('Fine grass blades',gv,gf,gi)
print('Botanical geometry complete',flush=True)

collection('F Background trees / reflection context')
def tree(x,y,h,seed):
    rng=random.Random(seed);beam('Background tree trunk',(x,y,0),(x+.25,y,h*.72),.26,bark)
    vv=[];ff=[];ii=[]
    for j in range(14):
        a=rng.random()*math.tau;r=rng.uniform(1.5,3.8);z=rng.uniform(h*.5,h*.88)
        end=Vector((x+math.cos(a)*r,y+math.sin(a)*r,z))
        beam('Natural tree branch',(x,y,h*.4),end,.065,bark)
        for k in range(700):
            az=rng.random()*math.tau;el=rng.uniform(-math.pi/2,math.pi/2);radius=rng.uniform(.5,1.9)
            center=end+Vector((math.cos(az)*math.cos(el)*radius,math.sin(az)*math.cos(el)*radius,math.sin(el)*radius*.8))
            leaf_patch(vv,ff,ii,center,(rng.uniform(-1,1),rng.uniform(-1,1),rng.uniform(-.8,.8)),rng.uniform(.11,.23),rng.uniform(.03,.065),rng.randrange(4))
    foliage_object('Background tree leaves',vv,ff,ii)
for i,(x,y,h) in enumerate([(-44,8,12),(-44,27,13),(-42,52,12),(44,8,12),(45,33,13),(38,55,12),(-20,62,14),(12,63,13)]):tree(x,y,h,900+i)

collection('G Exterior details / cycles, drainage, fixtures')
rubber=basic('Bicycle rubber',(.014,.016,.014),.87)
bikepaint=basic('Bicycle dark red enamel',(.17,.023,.015),.32,.45)
def bicycle(x,y,angle):
    def pt(u,z,v=0):return localpoint((x,y,0),u,z,angle,v)
    for u in [-.58,.58]:
        ring=[pt(u+.35*math.cos(t*math.tau/48),.36+.35*math.sin(t*math.tau/48)) for t in range(49)]
        line('Bicycle tyre',ring,.024,rubber)
        line('Wheel metal rim',[pt(u+.325*math.cos(t*math.tau/48),.36+.325*math.sin(t*math.tau/48)) for t in range(49)],.006,frame)
        for i in range(12):line('Wheel spoke',[pt(u,.36),pt(u+.32*math.cos(i*math.tau/12),.36+.32*math.sin(i*math.tau/12))],.0016,frame)
    points=[(-.58,.36),(-.23,.80),(.05,.36),(.42,.89),(.58,.36)]
    for a,b in [(0,1),(1,2),(0,2),(1,3),(2,3),(3,4)]:line('Cycle frame',[pt(*points[a]),pt(*points[b])],.018,bikepaint)
    line('Cycle handlebar',[pt(.42,.89),pt(.44,1.12),pt(.44,1.12,.24)],.012,frame)
    line('Saddle post',[pt(-.23,.80),pt(-.25,.94)],.018,frame)
    panel('Bicycle saddle',(x,y,0),(-.25,0,.96),(.25,.17,.045),rubber,angle,.015)
    line('Bicycle kickstand',[pt(.02,.35),pt(-.08,.03,.23)],.008,frame)
for x,y,a in [(-5.2,-.60,.08),(-6.7,-.55,-.08),(5.3,-.7,.1),(6.9,-.6,-.15)]:bicycle(x,y,a)
for s in [-1,1]:
    for x in [7,20,31]:
        cube('Storm drain grate',(s*x,-4.60,.012),(.58,.32,.035),roof)
        for i in range(11):cube('Drain slots',(s*x-.25+i*.05,-4.60,.031),(.014,.25,.003),dark)
    cube('Discrete campus sign support',(s*17,-3.85,.65),(.045,.055,1.3),frame)
    cube('Discrete campus sign',(s*17,-3.85,1.17),(1.30,.065,.27),roof,.01)
    x=s*10.8
    line('Flag pole',[(x,-3.5,0),(x,-3.5,14.8)],.035,frame)
    ico('Flag pole finial',(x,-3.5,14.85),(.065,.065,.075),frame,2)
cube('Subtle road marking',(12,-8,.006),(1.75,.08,.007),stone)
print('Site detail complete',flush=True)

collection('H Calibrated cameras and physical daylight')
scene=bpy.context.scene
world=bpy.data.worlds.new('Poly Haven overcast daylight / HDRI');world.use_nodes=True;scene.world=world
wn=world.node_tree.nodes;wl=world.node_tree.links;env=wn.new('ShaderNodeTexEnvironment');env.image=bpy.data.images.load(str(ROOT/'assets/textures'/'overcast.hdr'))
mapping=wn.new('ShaderNodeMapping');mapping.inputs['Rotation'].default_value.z=math.radians(110);coords=wn.new('ShaderNodeTexCoord');wl.new(coords.outputs['Generated'],mapping.inputs['Vector']);wl.new(mapping.outputs[0],env.inputs[0]);wl.new(env.outputs[0],wn.get('Background').inputs['Color']);wn.get('Background').inputs['Strength'].default_value=.65
def camera(name,loc,target,lens):
    data=bpy.data.cameras.new(name);obj=bpy.data.objects.new(name,data);COL.objects.link(obj);obj.location=loc;obj.rotation_euler=(Vector(target)-obj.location).to_track_quat('-Z','Y').to_euler();data.lens=lens;data.clip_end=1000;return obj
cal=json.loads((ROOT/'data/camera-calibration.json').read_text());cc=cal['camera_local'];R=Matrix(cal['rotation_world_to_cv'])
photo=camera('01 Photograph matched camera',(cc[0]-HALF,cc[1],cc[2]),(0,0,8),cal['focal_pixels']*36/1504)
photo.rotation_euler=(R.transposed()@Matrix.Diagonal((1,-1,-1))).to_euler()
ground=camera('02 Ground level exterior',(-49,-32,3.0),(-6.0,4.0,7.0),28)
detail=camera('03 Entrance and side glazing',(-15,-22,3.1),(0,-1.7,6.4),39)
aerial=camera('04 E plan overview',(-78,-65,70),(0,20,3),46)
scene.camera=photo;scene.render.engine='CYCLES';scene.cycles.samples=160;scene.cycles.use_denoising=True;scene.cycles.max_bounces=9;scene.cycles.transmission_bounces=8
scene.render.resolution_x=2400;scene.render.resolution_y=1596;scene.render.resolution_percentage=100
scene.render.image_settings.file_format='PNG';scene.view_settings.view_transform='AgX';scene.view_settings.exposure=.35
try:scene.view_settings.look='AgX - Medium High Contrast'
except Exception:pass
scene.unit_settings.system='METRIC'
try:
    prefs=bpy.context.preferences.addons['cycles'].preferences;prefs.compute_device_type='OPTIX';prefs.get_devices()
    for device in prefs.devices:device.use=device.type=='OPTIX'
    if any(d.use for d in prefs.devices):scene.cycles.device='GPU'
except Exception as e:print('GPU fallback:',e,flush=True)
for area in bpy.context.screen.areas:
    if area.type=='VIEW_3D':
        area.spaces.active.region_3d.view_perspective='CAMERA';area.spaces.active.clip_end=1000;area.spaces.active.shading.color_type='MATERIAL'
scene['Accuracy']='Reference reconstructed exterior, not a measured survey. E shape confirmed by heritage record. Window count checked using rectified photo. Rear lengths, courtyard and interiors are approximate.'
note=bpy.data.texts.new('START HERE - sources and accuracy');note.write('KIT HISTORIC MAIN BUILDING / REVISION 3\nPhoto references and methodology: see SOURCES.md and README.md beside this file.\nThe heritage record confirms the E shaped plan and projecting ribbon windows on the return facades.\nFront facade has seven window bays on each side, revised using a rectified reference photo.\nDark coping, recessed glazing, blinds, rainwater pipes and an open blue doorway replace the earlier generic approximations.\nCamera 01 uses manual vanishing-point calibration of the 2007 reference; not a photogrammetric survey.\nOverall height 14.2m is a scale assumption, not a verified measurement. Rear lengths, lecture hall and internal spaces remain approximate.\nPoly Haven asphalt_01 and kloofendal_overcast_puresky are CC0 and packed into this file.\n')
scene.render.film_transparent=False
bpy.ops.file.pack_all()
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'build/kit_building_3_v3.blend'))
summary={'objects':len(scene.objects),'mesh_objects':sum(o.type=='MESH' for o in scene.objects),'vertices':sum(len(o.data.vertices) for o in scene.objects if o.type=='MESH'),'front_window_bays_per_wing':7,'estimated_front_width':2*HALF,'assumed_height_m':H,'gpu':scene.cycles.device,'reference_camera':cal}
(ROOT/'reports/model-info.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
preview='--preview' in sys.argv
views=[(photo,'photo-matched'),(ground,'exterior'),(detail,'entrance'),(aerial,'overview')]
sidecam=camera('05 South ribbon and secondary entrance',(-49,38,4),(-HALF,25,6.6),30)
views.append((sidecam,'side-windows'))
if '--build-only' in sys.argv:views=[]
if preview:
    views=views[:1];scene.render.resolution_percentage=55;scene.cycles.samples=32
for c,fn in views:
    scene.camera=c;scene.render.filepath=str(ROOT/'build'/(fn+('-preview' if preview else '')+'.png'));bpy.ops.render.render(write_still=True)
scene.camera=photo
if not preview:bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'build/kit_building_3_v3.blend'))
print('KIT_V3_COMPLETE',json.dumps({k:v for k,v in summary.items() if k!='reference_camera'}),flush=True)
