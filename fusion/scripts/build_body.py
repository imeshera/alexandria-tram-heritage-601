# Body of car 601 (component 'Body'):
#  - saloon side walls, each as two bodies: lower panelled wall (body_bot..waist_h) and the upper window wall
#    (waist_h..eave) with 11 big + 2 narrow windows with segmental-arch heads (broadside tp 1920902)
#  - saloon end bulkheads (centre sliding-door opening + one round-headed window each side; interior photo 2022)
#  - floor slab over the whole plan (bowed 5-facet ends)
#  - arched roof with cornice, cut to the bowed plan + overhang, hollowed over the saloon (wooden ceiling)
# The open platforms, cab ends (dash / posts / glass), apron and steps are in build_ends.py.
import math
import adsk.core, adsk.fusion
import os
ROOT = os.path.dirname(os.path.abspath(__file__))

def run(_context: str):
    g = {'__file__': os.path.join(ROOT, 'common601.py')}; exec(open(g['__file__']).read(), g)
    des = g['design'](); ev = g['ev_fn'](des)
    C = g['comp'](des, 'Body'); g['wipe'](C)
    P = adsk.core.Point3D.create; VR = adsk.core.ValueInput.createByReal
    ext = C.features.extrudeFeatures
    NEW, CUT = adsk.fusion.FeatureOperations.NewBodyFeatureOperation, adsk.fusion.FeatureOperations.CutFeatureOperation
    L, hw, t = ev('car_len'), ev('half_w'), ev('wall_t')
    x0, x1 = ev('ent_x1'), L - ev('ent_x1')
    bb_, sill, eave = ev('body_bot'), ev('sill_h'), ev('eave_h')
    AX = {'x': 0, 'y': 1, 'z': 2}

    def coll(items):
        oc = adsk.core.ObjectCollection.create()
        for i in items: oc.add(i)
        return oc

    def extrude(profs, a, b, axis, op=NEW, bodies=None, name=''):
        """Extrude from model coordinate a to b along axis; the sketch plane must be an origin plane normal to axis."""
        sk0 = profs[0].parentSketch
        n = sk0.xDirection.crossProduct(sk0.yDirection)
        sgn = 1 if [n.x, n.y, n.z][AX[axis]] > 0 else -1
        ei = ext.createInput(coll(profs), op)
        ei.startExtent = adsk.fusion.OffsetStartDefinition.create(VR(sgn * a))
        ei.setDistanceExtent(False, VR(sgn * (b - a)))
        if bodies: ei.participantBodies = bodies
        f = ext.add(ei); f.name = name
        return f

    def arch_window(sk, m, xa, xb, ya, yb, rise):
        Ln, Ar = sk.sketchCurves.sketchLines, sk.sketchCurves.sketchArcs
        l1 = Ln.addByTwoPoints(m(xa, ya), m(xb, ya))
        l2 = Ln.addByTwoPoints(l1.endSketchPoint, m(xb, yb - rise))
        a = Ar.addByThreePoints(l2.endSketchPoint, m((xa + xb) / 2, yb), m(xa, yb - rise))
        l3 = Ln.addByTwoPoints(a.endSketchPoint if a.endSketchPoint.geometry.distanceTo(m(xa, yb - rise)) < 1e-4 else a.startSketchPoint, l1.startSketchPoint)

    def windows():
        n = int(round(ev('n_win', ''))); p, w, x1w = ev('win_pitch'), ev('win_w'), ev('win1_x')
        W = [(ev('nwin_x'), ev('nwin_x') + ev('nwin_w'))]
        W += [(x1w + i * p, x1w + i * p + w) for i in range(n)]
        W += [(L - ev('nwin_x') - ev('nwin_w'), L - ev('nwin_x'))]
        return W

    # ---- side walls
    sk = C.sketches.add(C.xYConstructionPlane); sk.name = 'Side upper'; sk.isComputeDeferred = True
    m = lambda x, y: sk.modelToSketchSpace(P(x, y, 0))
    sk.sketchCurves.sketchLines.addTwoPointRectangle(m(x0, ev('waist_h')), m(x1, eave))
    for xa, xb in windows():
        arch_window(sk, m, xa, xb, sill, ev('win_top'), ev('arch_rise'))
    sk.isComputeDeferred = False
    big = max((sk.profiles.item(i) for i in range(sk.profiles.count)), key=lambda p: p.areaProperties().area)
    sk2 = C.sketches.add(C.xYConstructionPlane); sk2.name = 'Side lower'
    m2 = lambda x, y: sk2.modelToSketchSpace(P(x, y, 0))
    sk2.sketchCurves.sketchLines.addTwoPointRectangle(m2(x0, bb_), m2(x1, ev('waist_h')))
    for side, za, zb in (('L', hw - t, hw), ('R', -hw, -hw + t)):
        f = extrude([big], za, zb, 'z', name='Side upper ' + side); f.bodies.item(0).name = 'Side upper ' + side
        f = extrude([sk2.profiles.item(0)], za, zb, 'z', name='Side lower ' + side); f.bodies.item(0).name = 'Side lower ' + side
    sk.isVisible = sk2.isVisible = False

    # ---- bulkheads (saloon end walls)
    fl = ev('floor_h')
    for tag, xb, sgn in (('A', x0, 1), ('B', x1, -1)):
        pi = C.constructionPlanes.createInput(); pi.setByOffset(C.yZConstructionPlane, VR(xb))
        pl = C.constructionPlanes.add(pi); pl.name = 'Bulkhead plane ' + tag; pl.isLightBulbOn = False
        skb = C.sketches.add(pl); skb.name = 'Bulkhead ' + tag; skb.isComputeDeferred = True
        mb = lambda z, y: skb.modelToSketchSpace(P(xb, y, z))
        Ln = skb.sketchCurves.sketchLines
        Ln.addTwoPointRectangle(mb(-(hw - t), fl), mb(hw - t, eave))
        Ln.addTwoPointRectangle(mb(-34.0, fl), mb(34.0, fl + 188.0))           # sliding-door opening
        for s in (1, -1):
            arch_window(skb, mb, s * 44.0, s * 92.0, fl + 40.0, fl + 180.0, 8.0)
        skb.isComputeDeferred = False
        bigb = max((skb.profiles.item(i) for i in range(skb.profiles.count)), key=lambda p: p.areaProperties().area)
        ei = ext.createInput(bigb, NEW); ei.setDistanceExtent(False, VR(sgn * t))
        f = ext.add(ei)
        bx = f.bodies.item(0).boundingBox
        if (bx.minPoint.x + bx.maxPoint.x) / 2 < xb and sgn > 0 or (bx.minPoint.x + bx.maxPoint.x) / 2 > xb and sgn < 0:
            f.deleteMe(); ei = ext.createInput(bigb, NEW); ei.setDistanceExtent(False, VR(-sgn * t)); f = ext.add(ei)
        f.name = 'Bulkhead ' + tag; f.bodies.item(0).name = 'Bulkhead ' + tag
        skb.isVisible = False

    # ---- plan outline (both bowed ends) -> floor slab
    pa = g['end_poly'](ev); pb = list(reversed(g['mirror_x'](L, pa)))
    poly = pa + pb[::-1][::-1]
    poly = pa + [(L - x, z) for x, z in reversed(pa)][::-1][::-1]
    poly = pa + [(L - x, -z) for x, z in pa]          # A (+z..-z), then B (-z..+z)
    skp = C.sketches.add(C.xZConstructionPlane); skp.name = 'Plan floor'
    mp = lambda x, z: skp.modelToSketchSpace(P(x, 0, z))
    Ln = skp.sketchCurves.sketchLines
    for i in range(len(poly)):
        Ln.addByTwoPoints(mp(*poly[i]), mp(*poly[(i + 1) % len(poly)]))
    f = extrude([skp.profiles.item(0)], fl - 4.0, fl, 'y', name='Floor'); f.bodies.item(0).name = 'Floor'
    skp.isVisible = False

    # ---- roof: arched section with cornice, along X
    ov = ev('roof_ovh'); zr = hw + ov; ct, cr = ev('cornice_top'), ev('crown_h')
    sks = C.sketches.add(C.yZConstructionPlane); sks.name = 'Roof section'
    ms = lambda z, y: sks.modelToSketchSpace(P(0, y, z))
    Ln, Ar = sks.sketchCurves.sketchLines, sks.sketchCurves.sketchArcs
    l1 = Ln.addByTwoPoints(ms(-zr, eave), ms(-zr, ct))
    a = Ar.addByThreePoints(l1.endSketchPoint, ms(0, cr), ms(zr, ct))
    e2 = a.endSketchPoint if a.endSketchPoint.geometry.distanceTo(ms(zr, ct)) < 1e-4 else a.startSketchPoint
    l2 = Ln.addByTwoPoints(e2, ms(zr, eave)); Ln.addByTwoPoints(l2.endSketchPoint, l1.startSketchPoint)
    f = extrude([sks.profiles.item(0)], -ov - 30.0, L + ov + 30.0, 'x', name='Roof'); roof = f.bodies.item(0); roof.name = 'Roof'
    sks.isVisible = False
    # plan cut (outline grown by the overhang)
    po = g['end_poly'](ev, ov); polyo = po + [(L - x, -z) for x, z in po]
    skc = C.sketches.add(C.xZConstructionPlane); skc.name = 'Plan roof'
    mc = lambda x, z: skc.modelToSketchSpace(P(x, 0, z))
    Ln = skc.sketchCurves.sketchLines
    for i in range(len(polyo)):
        Ln.addByTwoPoints(mc(*polyo[i]), mc(*polyo[(i + 1) % len(polyo)]))
    Ln.addTwoPointRectangle(mc(-ov - 80.0, -zr - 40.0), mc(L + ov + 80.0, zr + 40.0))
    ring = max((skc.profiles.item(i) for i in range(skc.profiles.count)), key=lambda p: p.profileLoops.count)
    extrude([ring], eave - 10.0, cr + 20.0, 'y', op=CUT, bodies=[roof], name='Roof plan cut')
    skc.isVisible = False
    # saloon ceiling hollow (concentric inner arc, wall_t below the outer roof)
    R = (zr * zr + (cr - ct) ** 2) / (2 * (cr - ct)); yc = cr - R; zi = hw - t
    yi = yc + math.sqrt((R - t) ** 2 - zi * zi)
    skh = C.sketches.add(C.yZConstructionPlane); skh.name = 'Ceiling hollow'
    mh = lambda z, y: skh.modelToSketchSpace(P(0, y, z))
    Ln, Ar = skh.sketchCurves.sketchLines, skh.sketchCurves.sketchArcs
    l1 = Ln.addByTwoPoints(mh(-zi, eave - 2.0), mh(-zi, yi))
    a = Ar.addByThreePoints(l1.endSketchPoint, mh(0, cr - t), mh(zi, yi))
    e2 = a.endSketchPoint if a.endSketchPoint.geometry.distanceTo(mh(zi, yi)) < 1e-4 else a.startSketchPoint
    l2 = Ln.addByTwoPoints(e2, mh(zi, eave - 2.0)); Ln.addByTwoPoints(l2.endSketchPoint, l1.startSketchPoint)
    extrude([skh.profiles.item(0)], x0 + t, x1 - t, 'x', op=CUT, bodies=[roof], name='Ceiling hollow')
    skh.isVisible = False
    print('bodies', [b.name for b in C.bRepBodies], '| roof bbox x', round(roof.boundingBox.minPoint.x, 1), round(roof.boundingBox.maxPoint.x, 1))
