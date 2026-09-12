"""KIT Building 3: editable, photograph-informed exterior study (not a survey)."""
import bpy, bmesh, math, random, json, sys
from pathlib import Path
from mathutils import Vector

OUT = Path(__file__).resolve().parent
random.seed(1930)
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
for col in list(bpy.data.collections):
    if col.name != 'Collection': bpy.data.collections.remove(col)
base = bpy.data.collections.get('Collection'); base.name = '00 Architecture'
COL = base
def collection(name):
    global COL
    COL = bpy.data.collections.new(name); bpy.context.scene.collection.children.link(COL)
def move(obj):
    for c in list(obj.users_collection): c.objects.unlink(obj)
    COL.objects.link(obj)
    return obj
def mat(name, color, rough=.6, metal=0):
    m=bpy.data.materials.new(name); m.diffuse_color=(*color,1); m.use_nodes=True
    p=m.node_tree.nodes.get('Principled BSDF'); p.inputs['Base Color'].default_value=(*color,1)
    p.inputs['Roughness'].default_value=rough; p.inputs['Metallic'].default_value=metal
    return m
brick=mat('Warm brown ceramic tile / procedural metric courses',(.39,.235,.13))
n=brick.node_tree.nodes; l=brick.node_tree.links; p=n.get('Principled BSDF')
geo=n.new('ShaderNodeNewGeometry'); sep=n.new('ShaderNodeSeparateXYZ'); comb=n.new('ShaderNodeCombineXYZ')
l.new(geo.outputs['Position'],sep.inputs[0]); l.new(sep.outputs['X'],comb.inputs['X']); l.new(sep.outputs['Z'],comb.inputs['Y']); l.new(sep.outputs['Y'],comb.inputs['Z'])
bt=n.new('ShaderNodeTexBrick'); bt.inputs['Color1'].default_value=(.34,.205,.105,1); bt.inputs['Color2'].default_value=(.50,.325,.19,1)
bt.inputs['Mortar'].default_value=(.235,.205,.155,1); bt.inputs['Scale'].default_value=1
bt.inputs['Mortar Size'].default_value=.0035; bt.inputs['Mortar Smooth'].default_value=.002
bt.inputs['Brick Width'].default_value=.235; bt.inputs['Row Height'].default_value=.065
l.new(comb.outputs[0],bt.inputs['Vector']); l.new(bt.outputs['Color'],p.inputs['Base Color'])
bump=n.new('ShaderNodeBump'); bump.inputs['Strength'].default_value=.38; bump.inputs['Distance'].default_value=.013
l.new(bt.outputs['Fac'],bump.inputs['Height']); l.new(bump.outputs[0],p.inputs['Normal'])
stone=mat('Aged warm limestone',(.52,.51,.40)); darkstone=mat('Concrete roof / weathered',(.23,.25,.23))
frame=mat('Painted ivory metal window frames',(.68,.73,.70),.32,.32)
glass=mat('Blue grey reflective glass',(.145,.245,.29),.20,.50)
glass2=mat('Alternate slightly pale glass',(.28,.37,.38),.25,.38)
teal=mat('Historic blue green entry doors',(.12,.29,.29),.38,.25)
dark=mat('Recess and interior shadow',(.035,.046,.04))
bronze=mat('Aged bronze hardware',(.28,.22,.09),.32,.72)
paving=mat('Light grey stone paving',(.43,.46,.44)); asphalt=mat('Dark grey access road',(.17,.19,.18))
soil=mat('Planting soil',(.09,.085,.055)); grass=mat('Grass',(.20,.29,.10))
bark=mat('Palm trunk',(.19,.14,.075)); leaves=[mat('Palm leaf '+str(i),c) for i,c in enumerate([(.12,.24,.06),(.21,.32,.08),(.28,.36,.105)])]
shrubm=mat('Azalea leaves',(.095,.20,.065)); blossoms=[mat('Azalea flower '+str(i),c) for i,c in enumerate([(.59,.075,.28),(.77,.16,.40),(.49,.065,.28)])]
def cube(name, loc, dims, material, bevel=0):
    x,y,z=[v/2 for v in dims]
    me=bpy.data.meshes.new(name)
    me.from_pydata([(-x,-y,-z),(-x,-y,z),(-x,y,-z),(-x,y,z),(x,-y,-z),(x,-y,z),(x,y,-z),(x,y,z)],[],[(2,6,4,0),(5,7,3,1),(4,5,1,0),(3,7,6,2),(1,3,2,0),(6,7,5,4)])
    o=bpy.data.objects.new(name,me);COL.objects.link(o);o.location=loc
    if material:o.data.materials.append(material)
    if bevel:
        m=o.modifiers.new('Small softened edges','BEVEL'); m.width=bevel; m.segments=2
        o.modifiers.new('Weighted corner normals','WEIGHTED_NORMAL')
    return o
def cyl(name,loc,r,depth,material,vertices=12):
    vs=[(r*math.cos(i*math.tau/vertices),r*math.sin(i*math.tau/vertices),z) for z in [-depth/2,depth/2] for i in range(vertices)]
    fs=[tuple(reversed(range(vertices))),tuple(range(vertices,2*vertices))]
    fs.extend([(i,(i+1)%vertices,(i+1)%vertices+vertices,i+vertices) for i in range(vertices)])
    me=bpy.data.meshes.new(name);me.from_pydata(vs,[],fs);me.materials.append(material)
    o=bpy.data.objects.new(name,me);COL.objects.link(o);o.location=loc;return o
def beam(name,a,b,r,material):
    v=Vector(b)-Vector(a);o=cyl(name,(Vector(a)+Vector(b))/2,r,v.length,material)
    o.rotation_euler=v.to_track_quat('Z','Y').to_euler();return o
ico_cache={}
def ico(name,loc,scale,material,sub=1):
    key=(material.name,sub)
    if key not in ico_cache:
        me=bpy.data.meshes.new(name);bm=bmesh.new();bmesh.ops.create_icosphere(bm,subdivisions=sub,radius=1);bm.to_mesh(me);bm.free();me.materials.append(material)
        for f in me.polygons:f.use_smooth=True
        ico_cache[key]=me
    o=bpy.data.objects.new(name,ico_cache[key]);COL.objects.link(o);o.location=loc;o.scale=scale
    return o
def window(name,x,y,z,w=1.95,h=2.55,rotation=0):
    # Local facade axes, with the exterior in negative local Y.
    parent=bpy.data.objects.new(name,None);COL.objects.link(parent);parent.location=(x,y,z);parent.rotation_euler.z=rotation
    def part(suffix,loc,dims,material,bev=0):
        o=cube(name+' / '+suffix,loc,dims,material,bev);o.parent=parent;return o
    part('deep reveal',(0,.18,0),(w+.16,.16,h+.14),dark)
    part('glass',(0,-.025,0),(w-.15,.035,h-.16),glass2 if random.random()<.18 else glass)
    for dx in [-w/2,w/2]: part('jamb',(dx,-.075,0),(.07,.12,h),frame,.012)
    for dz in [-h/2,h/2]: part('frame',(0,-.075,dz),(w+.06,.12,.07),frame,.012)
    part('central mullion',(0,-.10,0),(.055,.10,h),frame)
    for dz in [-h/6,h/6]:part('transom',(0,-.105,dz),(w,.09,.055),frame)
    # Secondary narrow top lights, visible in the source photo.
    for dz in [-h/6+.25,h/6+.25]:part('vent light',(0,-.11,dz),(w,.085,.04),frame)
    part('stone sill',(0,-.07,-h/2-.11),(w+.25,.45,.15),stone,.025)
    part('brick lintel',(0,.045,h/2+.10),(w+.22,.18,.13),brick)
    return parent
