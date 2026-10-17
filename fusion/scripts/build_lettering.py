# Lettering decals for car 601 (component 'Lettering') from CoreText SVG outlines (tools/lettering/svg/601_*,
# made by make_svgs_601.sh). Per livery, at both ends (as photographed):
#   1 light blue (2012): white "601" on the viewer's-left intermediate dash facet, "٦٠١" on the right; destination
#     board "VICTORIA" | route "2" | "النصر"; black apron "١٩٣١" + "بدء دخول الخدمة" (the car's own claim of 1931)
#   2 red (2020+): "٦٠١" left, "601" right (tp 2110423, 2168484); board "محطة الرمل" on both halves, route "٢";
#     cream side legend "الهيئة العامة لنقل الركاب بالإسكندرية", widely spaced over the middle panels (tp 1920902)
#   3 yellow works (2002): black "601" left only.
# Generic planar placement as in the GT6 build: plane, ink-box centre, ink height, reading direction (seen from
# outside) and outward direction; the mirrored/plain SVG is picked from the sketch x-axis; counters are dropped.
import math
import adsk.core, adsk.fusion
import os
ROOT = os.path.dirname(os.path.abspath(__file__))
SVG = os.path.join(ROOT, '..', '..', 'tools', 'lettering', 'svg', '')
PX = 3.7795275591

def run(_context: str):
    g = {'__file__': os.path.join(ROOT, 'common601.py')}; exec(open(g['__file__']).read(), g)
    des = g['design'](); ev = g['ev_fn'](des)
    Lt = g['comp'](des, 'Lettering'); g['wipe'](Lt)
    P, V3 = adsk.core.Point3D.create, adsk.core.Vector3D.create
    L, hw = ev('car_len'), ev('half_w')
    lv = int(round(ev('livery', '')))
    white = des.appearances.itemByName('Plastic - Matte (White)')
    black = des.appearances.itemByName('Plastic - Matte (Black)')
    cream = des.appearances.itemByName('601 cream') or white
    am = ev('bow_m_ang', 'rad'); c = ev('bow_c') / 2; m = ev('bow_m')

    def off_plane(base, d, name):
        pi = Lt.constructionPlanes.createInput(); pi.setByOffset(base, adsk.core.ValueInput.createByReal(d))
        p = Lt.constructionPlanes.add(pi); p.name = name; p.isLightBulbOn = False; return p

    def facet_plane(pt, out, name):
        """Vertical plane through model point pt with horizontal outward normal out."""
        pz = off_plane(Lt.xYConstructionPlane, pt[2], name + ' axis plane')
        sk = Lt.sketches.add(pz); sk.isVisible = False
        ln = sk.sketchCurves.sketchLines.addByTwoPoints(sk.modelToSketchSpace(P(pt[0], 40, pt[2])), sk.modelToSketchSpace(P(pt[0], 160, pt[2])))
        ang = math.atan2(out[2], -out[0]) if out[0] < 0 else math.atan2(out[2], out[0])
        for sgn in (1, -1):
            pi = Lt.constructionPlanes.createInput()
            pi.setByAngle(ln, adsk.core.ValueInput.createByReal(sgn * ang), Lt.yZConstructionPlane)
            p = Lt.constructionPlanes.add(pi); n = p.geometry.normal
            if abs(abs(n.x * out[0] + n.z * out[2]) - 1.0) < 1e-4:
                p.name = name; p.isLightBulbOn = False; return p
            p.deleteMe()
        raise RuntimeError('facet plane orientation ' + name)

    def place(pl, base, centre, h, read, out, depth, name, app):
        sk = Lt.sketches.add(pl)
        o = sk.sketchToModelSpace(P(0, 0, 0)); ux = o.vectorTo(sk.sketchToModelSpace(P(1, 0, 0)))
        uy = o.vectorTo(sk.sketchToModelSpace(P(0, 1, 0)))
        up = V3(0, 1, 0) if abs(V3(*out).y) < 0.9 else V3(*read).crossProduct(V3(*out))
        rot = math.atan2(up.dotProduct(uy), up.dotProduct(ux)) - math.pi / 2
        rx = V3(ux.x * math.cos(rot) + uy.x * math.sin(rot), ux.y * math.cos(rot) + uy.y * math.sin(rot),
                ux.z * math.cos(rot) + uy.z * math.sin(rot))
        f = SVG + base + ('_R' if rx.dotProduct(V3(*read)) > 0 else '_L') + '.svg'
        sk.importSVG(f, 0, 0, PX)
        # ink box from the curves (sketchPoints include the sketch origin, which inflated the box by the ascent)
        bbs = [cv.boundingBox for cv in sk.sketchCurves]
        x0, x1 = min(b.minPoint.x for b in bbs), max(b.maxPoint.x for b in bbs)
        y0, y1 = min(b.minPoint.y for b in bbs), max(b.maxPoint.y for b in bbs)
        sk.deleteMe()
        s = h / (y1 - y0)
        sk = Lt.sketches.add(pl); sk.name = name; sk.isComputeDeferred = True
        tc = sk.modelToSketchSpace(P(*centre))
        sk.importSVG(f, tc.x - s * (x0 + x1) / 2, tc.y - s * (y0 + y1) / 2, PX * s)
        sk.isComputeDeferred = False
        holes = set()
        def key(lp):
            pts = []
            for cv in lp.profileCurves:
                b = cv.boundingBox; pts += [b.minPoint, b.maxPoint]
            return (round(min(q.x for q in pts), 3), round(min(q.y for q in pts), 3), round(max(q.x for q in pts), 3), round(max(q.y for q in pts), 3))
        for i in range(sk.profiles.count):
            for lp in sk.profiles.item(i).profileLoops:
                if not lp.isOuter: holes.add(key(lp))
        profs = adsk.core.ObjectCollection.create()
        for i in range(sk.profiles.count):
            pr = sk.profiles.item(i)
            if key([lp for lp in pr.profileLoops if lp.isOuter][0]) not in holes: profs.add(pr)
        ext = Lt.features.extrudeFeatures
        ei = ext.createInput(profs, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        ei.setDistanceExtent(False, adsk.core.ValueInput.createByReal(depth))
        fe = ext.add(ei)
        cb = fe.bodies.item(0).boundingBox; cm = P((cb.minPoint.x + cb.maxPoint.x) / 2, (cb.minPoint.y + cb.maxPoint.y) / 2, (cb.minPoint.z + cb.maxPoint.z) / 2)
        if P(*centre).vectorTo(cm).dotProduct(V3(*out)) < 0:
            fe.deleteMe(); ei = ext.createInput(profs, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
            ei.setDistanceExtent(False, adsk.core.ValueInput.createByReal(-depth)); fe = ext.add(ei)
        fe.name = name
        if abs(rot) > 1e-4:
            bodies = adsk.core.ObjectCollection.create()
            for b in fe.bodies: bodies.add(b)
            mm = adsk.core.Matrix3D.create(); mm.setToRotation(rot, ux.crossProduct(uy), P(*centre))
            mi = Lt.features.moveFeatures.createInput2(bodies); mi.defineAsFreeMove(mm)
            Lt.features.moveFeatures.add(mi).name = name + ' upright'
        for b in fe.bodies:
            b.name = name
            if app: b.appearance = app
        sk.isVisible = False
        return fe.bodies.count

    nb = 0; D = 0.03
    numc = black if lv == 3 else white
    for tag, sx in (('A', 1), ('B', -1)):
        X = (lambda x: x) if sx > 0 else (lambda x: L - x)
        # intermediate dash facets (end-A plan: from (0, +/-c) back to (m sin am, +/-(c + m cos am)))
        def mid_facet(sz, frac, grow):
            px = m * math.sin(am) * frac; pz = sz * (c + m * math.cos(am) * frac)
            out = (-sx * math.cos(am), 0, sz * math.sin(am))
            pt = (X(px) + out[0] * grow, 0, pz + out[2] * grow)
            return pt, out
        def read_dir(sz):
            # along the facet towards the viewer's right (+z at end A, -z at end B)
            return (sz * math.sin(am), 0, sx * math.cos(am))
        hy = 146.0
        left_sz = -sx                     # viewer's left side of the dash
        dash_nums = {1: (('num601', left_sz), ('numar601', -left_sz)), 2: (('numar601', left_sz), ('num601', -left_sz)),
                     3: (('num601', left_sz),)}[lv]
        for base, sz in dash_nums:
            pt, out = mid_facet(sz, 0.5, 0.02)
            pl = facet_plane(pt, out, 'Dash plane %s %s' % (tag, base))
            h = 13.0 if base == 'num601' else 15.0
            nb += place(pl, '601_' + base.replace('num601', 'num').replace('numar601', 'numar'), (pt[0], hy, pt[2]), h,
                        read_dir(sz), out, D, 'Decal %s %s' % (tag, base), numc)
        # destination board texts on the board's intermediate facets (outer face of the board)
        gb = ev('roof_ovh') + 1.0 + 2.5 + 0.02
        yb = ev('board_bot') + ev('board_h') / 2
        if lv == 1:
            texts = (('victoria', left_sz, 10.5), ('nasr', -left_sz, 17.0))
        elif lv == 2:
            texts = (('raml', left_sz, 15.0), ('raml', -left_sz, 15.0))
        else:
            texts = ()
        for base, sz, h in texts:
            pt, out = mid_facet(sz, 0.5, gb)
            pl = facet_plane(pt, out, 'Board plane %s %s %d' % (tag, base, sz))
            nb += place(pl, '601_' + base, (pt[0], yb, pt[2]), h, read_dir(sz), out, D, 'Decal %s board %s' % (tag, base), white)
        # route number on the route-box glass
        if lv in (1, 2):
            xr = X(-(ev('roof_ovh') + 1.0 + 12.4))
            pr = off_plane(Lt.yZConstructionPlane, xr, 'Route plane ' + tag)
            nb += place(pr, '601_route2' if lv == 1 else '601_routear2', (xr, yb + 2.0, 0), 15.0, (0, 0, sx), (-sx, 0, 0), D,
                        'Decal %s route' % tag, white)
        # apron lettering (light-blue era)
        if lv == 1:
            ga = ev('apron_out') + 0.02
            xa = X(-ga)
            pa = off_plane(Lt.yZConstructionPlane, xa, 'Apron plane ' + tag)
            nb += place(pa, '601_1931', (xa, 68.0, left_sz * 20.0), 12.0, (0, 0, sx), (-sx, 0, 0), D, 'Decal %s 1931' % tag, white)
            pt, out = mid_facet(-left_sz, 0.5, ga)
            pl = facet_plane(pt, out, 'Apron plane mid ' + tag)
            nb += place(pl, '601_since', (pt[0], 70.0, pt[2]), 9.0, read_dir(-left_sz), out, D, 'Decal %s since' % tag, white)
    # side legend (red era): centred on the car, upper part of the lower panels
    if lv == 2:
        for sz in (1, -1):
            zp = sz * (hw + 0.9 + 0.02)
            ps = off_plane(Lt.xYConstructionPlane, zp, 'Side plane %d' % sz)
            nb += place(ps, '601_apta', (L / 2, 163.0, zp), 13.0, (sz * 1.0, 0, 0) if sz < 0 else (1.0, 0, 0), (0, 0, sz), D,
                        'Decal side legend %d' % sz, cream)
    print('decal bodies', nb)
