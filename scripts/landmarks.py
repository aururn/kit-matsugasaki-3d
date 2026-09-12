"""Building-specific forms observed in architect / official campus photographs.
Executed in build_campus namespace. No third-party 3D meshes are copied.
"""
def curtain(mx,a,b,z0,z1,step=1.5,door=False):
    length=math.dist(a,b);theta=math.atan2(b[1]-a[1],b[0]-a[0]);cs=math.cos(theta);sn=math.sin(theta)
    n=max(1,round(length/step));w=length/n
    def part(u,v,z,ww,dd,hh,mat):mx.box((a[0]+u*cs-v*sn,a[1]+u*sn+v*cs,z),(ww,dd,hh),mat,theta)
    part(length/2,.16,(z0+z1)/2,length,.012,z1-z0,glass)
    for j in range(n+1):part(j*w,.06,(z0+z1)/2,.06,.11,z1-z0,white)
    for zz in [z0,z1]:part(length/2,.06,zz,length,.11,.06,white)
    if door:
        for xx in [-.12,.12]:part(length/2+xx,-.07,z0+1.1,.027,.08,.40,frames)
        part(length/2,.05,z0+2.35,min(3,length),.10,.08,white)

def perforated_screen(mx,a,b,z0,z1):
    length=math.dist(a,b);theta=math.atan2(b[1]-a[1],b[0]-a[0]);cs=math.cos(theta);sn=math.sin(theta)
    cols=max(1,round(length/.42));cw=length/cols;rows=max(1,round((z1-z0)/.125));rh=(z1-z0)/rows
    for row in range(rows):
        z=z0+(row+.5)*rh
        for j in range(cols):
            u=(j+.5)*cw
            # Two narrow openings per unit, staggered in alternating rows.
            u+=cw*.22 if row%2 else 0
            if u>length:continue
            mx.box((a[0]+u*cs,a[1]+u*sn,z),(cw*.67,.18,rh*.72),brown,theta)
    for zz in [z0,z1]:mx.beam((a[0],a[1],zz),(b[0],b[1],zz),.045,grey)

def kithouse(b):
    mx=Mesh(b['name'],buildcols);x0,x1=-239.1,-198.9;y0,y1=-71.8,-44.8;h=7.5;floor=3.6
    # Main pavilion and the glazed southern return make the mapped L footprint.
    for xa,xb,ya,yb in [(x0,x1,y0,y1),(-216.5,x1,-91.5,y0)]:
        mx.box(((xa+xb)/2,(ya+yb)/2,.25),(xb-xa,yb-ya,.48),concrete)
        mx.box(((xa+xb)/2,(ya+yb)/2,floor),(xb-xa,yb-ya,.18),white)
        mx.box(((xa+xb)/2,(ya+yb)/2,h),(xb-xa,yb-ya,.16),grey)
        pp=[(xa,ya),(xb,ya),(xb,yb),(xa,yb)]
        for a,c in zip(pp,pp[1:]+pp[:1]):
            curtain(mx,a,c,.48,floor-.08,1.5,True)
            ln=math.dist(a,c);theta=math.atan2(c[1]-a[1],c[0]-a[0])
            # Glass sits behind the perforated brickwork at the upper storey.
            curtain(mx,a,c,floor+.12,h-.1,1.5)
            direction=Vector((c[0]-a[0],c[1]-a[1]))/ln
            for st,en in [(0,ln*.18),(ln*.55,ln*.74)]:
                p1=Vector(a)+direction*st;p2=Vector(a)+direction*en;perforated_screen(mx,p1,p2,floor+.15,h-.05)
            for st,en in [(ln*.18,ln*.55),(ln*.74,ln)]:
                center=Vector(a)+direction*((st+en)/2)
                mx.box((center.x,center.y,(floor+h)/2),(en-st,.23,h-floor),brown,theta)
        # The furniture and ceiling are visible through the lower curtain wall.
        for xx in range(int(xa)+3,int(xb)-2,4):
            for yy in range(int(ya)+3,int(yb)-2,5):
                mx.box((xx,yy,.98),(1.6,.8,.07),timber)
                for dx in [-.65,.65]:mx.beam((xx+dx,yy,.48),(xx+dx,yy,.95),.025,frames)
    # Four continuous gables, with east-facing rooflights documented by the designer.
    bay=(x1-x0)/4
    for j in range(4):
        xa=x0+j*bay;xb=xa+bay;ridge=xa+bay*.55;zt=h+3.2
        mx.face([(xa,y0,h),(xa,y1,h),(ridge,y1,zt),(ridge,y0,zt)],grey)
        mx.face([(ridge,y0,zt),(ridge,y1,zt),(xb,y1,h),(xb,y0,h)],glass)
        for yy in [y0,y1]:mx.face([(xa,yy,h),(xb,yy,h),(ridge,yy,zt)],white)
        for yy in [y0+i*(y1-y0)/12 for i in range(13)]:
            mx.beam((ridge,yy,zt+.02),(xb,yy,h+.02),.045,white)
            mx.beam((xa,yy,h+.02),(ridge,yy,zt+.02),.022,white)
    # Terrace, open stair, handrails and exterior tables in the L-shaped courtyard.
    mx.box((-222,-82,.24),(6,18,.32),timber)
    for yy in [-92,-92.7,-93.4]:mx.box((-222,yy,.21),(6,.65,.18),timber)
    sx=-219.0;bottom=-84.8;run=11.6;steps=22
    for i in range(steps):
        yy=bottom+(i+.5)*run/steps;z=.42+(i+1)*(floor-.42)/steps
        mx.box((sx,yy,z),(2.4,run/steps,.10),white)
        if i%3==0:
            for xx in [sx-1.22,sx+1.22]:mx.beam((xx,yy,z),(xx,yy,z+1),.022,white)
    for xx in [sx-1.22,sx+1.22]:
        mx.beam((xx,bottom,.45),(xx,bottom+run,floor),.085,white)
        mx.beam((xx,bottom,1.45),(xx,bottom+run,floor+1),.028,white)
    mx.box((sx,-72.5,floor),(3.3,2.3,.15),timber)
    for xx in [-223]:
        for yy in [-78,-83,-88]:
            mx.box((xx,yy,1.0),(2.8,.75,.08),timber)
            for off in [-.9,.9]:
                mx.box((xx,yy+off,.65),(2.8,.42,.10),timber)
                for dx in [-1.1,1.1]:mx.beam((xx+dx,yy+off,.35),(xx+dx,yy+off,.62),.028,white)
    ob=mx.finish();ob['building_name']=b['name'];ob['source_osm_way']=b['osm_id'];ob['evidence']='Architect photographs: k-associates.com/works/kit-house; four gables, perforated brickwork, glazed lower floor, open stair'
    label(b['name'],(-218,-60,h+5),1.8)
    return ob

def rounded_rect(x0,y0,x1,y1,r,steps=10):
    pts=[]
    for cx,cy,start in [(x1-r,y1-r,0),(x0+r,y1-r,90),(x0+r,y0+r,180),(x1-r,y0+r,270)]:
        for j in range(steps+1):
            a=math.radians(start+j*90/steps);pts.append((cx+r*math.cos(a),cy+r*math.sin(a)))
    return pts

def anniversary_hall(b):
    mx=Mesh('60th Anniversary Hall - curved upper volume',eastcols)
    x0,y0,x1,y1=16.9,-18.4,53.4,8.7;zmid=3.8;h=8.2
    # Brick plinth and glazed recesses carry the white cantilevered upper storey.
    mx.box((35.3,-4.85,.23),(37.2,28,.42),concrete)
    mx.box((42,-7,1.97),(19,22,3.5),brown)
    curtain(mx,(18,-17),(31,-17),.42,3.7,1.3,True)
    curtain(mx,(18,7),(18,-17),.42,3.7,1.5)
    curtain(mx,(32,7),(18,7),.42,3.7,1.4,True)
    for yy in [-15,-8,-1,6]:mx.beam((18.3,yy,.3),(18.3,yy,zmid),.09,white)
    pts=rounded_rect(x0,y0,x1,y1,2.0)
    for a,c in zip(pts,pts[1:]+pts[:1]):
        mx.face([(a[0],a[1],zmid),(c[0],c[1],zmid),(c[0],c[1],h),(a[0],a[1],h)],white)
        mx.beam((a[0],a[1],h+.07),(c[0],c[1],h+.07),.065,white)
    # White fins curve around the western and southern upper frontage.
    for yy in [y0+2+i*.18 for i in range(int((y1-y0-4)/.18))]:mx.box((x0-.10,yy,6.0),(.10,.035,3.25),white)
    for xx in [x0+2+i*.18 for i in range(int((x1-x0-4)/.18))]:mx.box((xx,y0-.10,6.0),(.035,.10,3.25),white)
    # Shallow four-sided roof with rounded eaves, lower than an ordinary gable.
    top=[(x0+7,y0+7,h+1.65),(x1-7,y0+7,h+1.65),(x1-7,y1-7,h+1.65),(x0+7,y1-7,h+1.65)]
    lower=[(x0,y0,h),(x1,y0,h),(x1,y1,h),(x0,y1,h)]
    for i in range(4):j=(i+1)%4;mx.face([lower[i],lower[j],top[j],top[i]],grey)
    mx.face(top,grey)
    # Signature slim dark vertical blade at the entry end.
    mx.box((23.5,8.82,8.0),(.75,.34,10),grey)
    mx.box((23.5,8.62,11.2),(.51,.045,1.4),dark)
    for i in range(4):mx.box((26.0,9.25+i*.32,.34-i*.07),(5.0,.70,.12),concrete)
    mx.box((19.4,-7.5,3.10),(5.8,6.0,.13),white)
    for xx in [17,21.6]:mx.beam((xx,-10.2,.2),(xx,-10.2,3.1),.045,white)
    ob=mx.finish();ob['building_name']=b['name'];ob['source_osm_way']=b['osm_id'];ob['evidence']='ks-architects.com work 89 photographs; rounded upper volume, white screen, brick plinth, shallow roof and entrance blade'
    label(b['name'],(35,-4,12),1.8);return ob

def center_hall(b):
    mx=Mesh('Center Hall - stepped brick facade',buildcols)
    p=b['points'];x0=min(x for x,y in p);x1=max(x for x,y in p);y0=min(y for x,y in p);y1=max(y for x,y in p)
    cx=(x0+x1)/2;cy=(y0+y1)/2
    # Auditorium has a tall, largely blank envelope, and descending lobby roofs.
    mx.box((cx,cy+2,5.8),(x1-x0-7,y1-y0-7,11.6),brown)
    for xx in [x0+3,x1-3]:mx.box((xx,cy,7.2),(6,y1-y0,14.4),brown)
    front=y0-1
    for k,(width,depth,height) in enumerate([(x1-x0-12,7.5,8.7),(x1-x0-8,5.8,5.1)]):
        yy=front-k*3.0
        mx.box((cx,yy+depth/2,height-.48),(width,depth,.90),brown)
        mx.box((cx,yy+depth/2,height+.03),(width+.25,depth+.25,.12),concrete)
        curtain(mx,(cx-width/2,yy),(cx+width/2,yy),.4,height-1.0,1.3,k==1)
        for side in [-1,1]:curtain(mx,(cx+side*width/2,yy),(cx+side*width/2,yy+depth),.4,height-1.0,1.3)
        for zz in ([5.6,6.5,7.3] if k==0 else [1.1,2.3,3.5]):mx.box((cx,yy-.015,zz),(width,.10,.055),frames)
        for xx in [cx-width/2,cx,cx+width/2]:mx.box((xx,yy-.04,(height-.4)/2),(.38,.44,height-.4),concrete)
    for xx in [x0+3,x1-3]:mx.box((xx,cy,14.48),(6.2,y1-y0+.2,.16),concrete)
    for j in range(5):mx.box((x1-6.15,cy-2+j*.42,9.8),(.02,.20,1.6),dark)
    mx.box((cx,front-5.1,.22),(24,6,.25),pathmat)
    ob=mx.finish();ob['building_name']=b['name'];ob['source_osm_way']=b['osm_id'];ob['evidence']='KIT official open campus photograph: blank brick towers and stepped entrance volume; approximate dimensions'
    label(b['name'],(cx,cy,17),1.8);return ob

def custom_landmark(b):
    if b['style']=='kithouse':return kithouse(b)
    if b['name']=='60th Anniversary Hall':return anniversary_hall(b)
    if b['name']=='60th Hall annex':return 'merged'
    if b['style']=='auditorium':return center_hall(b)
    return None
