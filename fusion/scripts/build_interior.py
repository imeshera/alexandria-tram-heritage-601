# Interior of car 601 (component 'Interior') after the transphoto 1702830 saloon view (2022) and the 2007 Parris
# photos: varnished wood throughout, arched wooden ceiling with carlines, maroon curtains gathered at every post on a
# brass rail, pendant lanterns + wall lamps, framed photos on the ceiling coves, glazed sliding bulkhead doors,
# grey linoleum with aisle strips + trap doors. Platforms: drum controller (left of the driver), hand-brake column
# with wheel (right), stool, gong pedal, cab rail, stanchions.
# Seats: walkover wooden-slat benches, 2+1 (doubles on +z, singles on -z), one row per big window, as two instanced
# components 'Seat double' / 'Seat single' placed as root occurrences, all set for travel towards end A.
import math
import adsk.core, adsk.fusion
import os
ROOT = os.path.dirname(os.path.abspath(__file__))

def seat(g, des, name, width, S):
    root = des.rootComponent; C = None
    for o in root.occurrences:
        if o.component.name == name: C = o.component
    if C is None:
        C = root.occurrences.addNewComponent(adsk.core.Matrix3D.create()).component; C.name = name
    g['wipe'](C); tb = g['TB'](C)
    # local: origin on the floor at the wall end of the seat; the seat spans z = 0..S*width (wall side at z = 0);
    # passengers face -X (travel towards end A); the walkover back leans over +X.
    d, sy = 44.0, 44.0
    for k in range(6):
        tb.box('Seat slat', -d / 2 + 3.5 + k * 7.4, sy - 0.4 * k / 5, S * width / 2, 6.0, 2.0, width - 4.0)
    tb.box('Seat slat', -d / 2 + 1.0, sy - 2.5, S * width / 2, 2.4, 5.0, width - 4.0)
    bt = math.radians(16)
    xb0 = 8.0
    for k in range(7):
        r = 6.0 + k * 7.2
        tb.box('Back slat', xb0 + r * math.sin(bt), sy + 4.0 + r * math.cos(bt), S * width / 2, 1.8, 6.0, width - 6.0,
               ax=(math.cos(bt), -math.sin(bt), 0), ay=(math.sin(bt), math.cos(bt), 0))
    for zz in (S * 2.5, S * (width - 2.5)):
        # walkover arms: pivot at the seat side, rising to the back
        tb.box('Back rail', xb0 / 2 + 2.0, sy + 8.0, zz, 3.0, 16.0, 2.5, ax=(0.6, 0.8, 0), ay=(-0.8, 0.6, 0))
        top = (xb0 + 54.0 * math.sin(bt), sy + 4.0 + 54.0 * math.cos(bt))
        tb.box('Back rail', (xb0 + top[0]) / 2, (sy + 4.0 + top[1]) / 2, zz, 2.5, 54.0, 2.5,
               ax=(math.sin(bt), math.cos(bt), 0), ay=(math.cos(bt), -math.sin(bt), 0))
    # aisle-end cast standard + wall bracket
    za = S * (width - 1.5)
    tb.box('Seat standard', 0, sy / 2 - 1.0, za, d - 6.0, 6.0, 2.0)
    tb.box('Seat standard', -d / 2 + 6.0, sy / 2, za, 4.0, sy - 2.0, 2.0)
    tb.box('Seat standard', d / 2 - 6.0, sy / 2, za, 4.0, sy - 2.0, 2.0)
    tb.box('Seat standard', 0, 1.0, za, d - 4.0, 2.0, 5.0)
    tb.box('Seat standard', 0, sy - 3.0, za, d - 6.0, 3.0, 2.5)
    tb.box('Seat bracket', 0, sy - 6.0, S * 1.5, d - 10.0, 6.0, 3.0)
    gx, gy = xb0 + 58.0 * math.sin(bt), sy + 4.0 + 58.0 * math.cos(bt)
    for dx in (-5.0, 5.0):                     # inverted-U chrome handle on the aisle end of the back
        tb.cyl('Grab handle', (gx + dx * math.cos(bt), gy - dx * math.sin(bt), za - S * 1.0), (gx + dx * math.cos(bt) + 2.0 * math.sin(bt), gy - dx * math.sin(bt) + 7.0, za - S * 1.0), 0.9)
        tb.sphere('Grab handle', (gx + dx * math.cos(bt) + 2.0 * math.sin(bt), gy - dx * math.sin(bt) + 7.0, za - S * 1.0), 0.9)
    tb.cyl('Grab handle', (gx - 5.0 * math.cos(bt) + 2.0 * math.sin(bt), gy + 5.0 * math.sin(bt) + 7.0, za - S * 1.0),
           (gx + 5.0 * math.cos(bt) + 2.0 * math.sin(bt), gy - 5.0 * math.sin(bt) + 7.0, za - S * 1.0), 0.9)
    tb.commit(name)
    return C

def place(des, C, mats):
    root = des.rootComponent
    occs = [o for o in root.occurrences if o.component == C]
    while len(occs) < len(mats):
        occs.append(root.occurrences.addExistingComponent(C, adsk.core.Matrix3D.create()))
    for o in occs[len(mats):]:
        o.deleteMe()
    for o, m in zip(occs, mats):
        o.transform2 = m

def run(_context: str):
    g = {'__file__': os.path.join(ROOT, 'common601.py')}; exec(open(g['__file__']).read(), g)
    des = g['design'](); ev = g['ev_fn'](des); root = des.rootComponent
    I = g['comp'](des, 'Interior'); g['wipe'](I); tb = g['TB'](I)
    L, hw, t = ev('car_len'), ev('half_w'), ev('wall_t'); hi = hw - t
    x0, x1 = ev('ent_x1'), L - ev('ent_x1')
    fl, sill, eave, ct, cr = ev('floor_h'), ev('sill_h'), ev('eave_h'), ev('cornice_top'), ev('crown_h')
    zr = hw + ev('roof_ovh'); Rr = (zr * zr + (cr - ct) ** 2) / (2 * (cr - ct)); yc = cr - Rr
    ceil_y = lambda z: yc + math.sqrt(max(0.0, (Rr - t) ** 2 - z * z))
    n = int(round(ev('n_win', ''))); p, w, xw = ev('win_pitch'), ev('win_w'), ev('win1_x')
    nx0, nw = ev('nwin_x'), ev('nwin_w')
    W = [(nx0, nx0 + nw)] + [(xw + i * p, xw + i * p + w) for i in range(n)] + [(L - nx0 - nw, L - nx0)]
    posts = [(W[i][1] + W[i + 1][0]) / 2 for i in range(len(W) - 1)]

    def beam(name, a, b, wd, ht):
        d = [b[i] - a[i] for i in range(3)]; ln = math.sqrt(sum(v * v for v in d)); u = tuple(v / ln for v in d)
        tb.box(name, (a[0] + b[0]) / 2, (a[1] + b[1]) / 2, (a[2] + b[2]) / 2, ln, wd, ht, ax=u, ay=(1.0, 0, 0) if abs(u[0]) < 0.5 else (0, 1.0, 0))

    for sz in (1, -1):
        tb.box('Window ledge', L / 2, sill + 0.5, sz * (hi - 3.0), x1 - x0 - 2 * t, 2.5, 7.0)
        tb.box('Window ledge', L / 2, ev('waist_h') - 25.0, sz * (hi - 1.0), x1 - x0 - 2 * t, 3.0, 2.0)      # dado moulding
        tb.cyl('Curtain rail', (x0 + t, 280.0, sz * (hi - 4.0)), (x1 - t, 280.0, sz * (hi - 4.0)), 0.8)
        for xp in posts + [x0 + t + 6.0, x1 - t - 6.0]:
            tb.box('Curtain', xp, 236.0, sz * (hi - 5.0), 13.0, 86.0, 6.0)
            tb.box('Curtain', xp, 229.0, sz * (hi - 5.5), 9.0, 10.0, 7.5)               # tie-back gather
        for k, xp in enumerate(posts):
            if k % 2 == 0:
                tb.box('Lamp fitting', xp, 283.0, sz * (hi - 2.0), 6.0, 6.0, 4.0)
                tb.cyl('Lamp fitting', (xp, 283.0, sz * (hi - 3.0)), (xp, 283.0, sz * (hi - 12.0)), 1.0)
                tb.sphere('Lamp', (xp, 283.0, sz * (hi - 15.0)), 5.5)
            # framed photo on the ceiling cove, tilted to follow the arch
            zc = sz * (hi - 22.0); yv = ceil_y(abs(zc)) - 3.0
            if k % 2 == 1:
                tb.box('Picture frame', xp + p / 2, yv, zc, 36.0, 26.0, 1.2, ax=(1, 0, 0), ay=(0, 0.55, -sz * 0.83))
                tb.box('Picture', xp + p / 2, yv - 0.6 * 0.83, zc + sz * 0.6 * 0.55 * 0, 30.0, 20.0, 1.2, ax=(1, 0, 0), ay=(0, 0.55, -sz * 0.83))
    # carlines (ceiling ribs) at every post, following the inner roof arc in 8 chords
    for xp in posts + [x0 + t + 2.0, x1 - t - 2.0]:
        for k in range(8):
            za = -hi + 2 * hi * k / 8; zb = -hi + 2 * hi * (k + 1) / 8
            beam('Ceiling rib', (xp, ceil_y(za) - 2.0, za), (xp, ceil_y(zb) - 2.0, zb), 4.0, 4.0)
    for xl in (L / 2 - 350.0, L / 2, L / 2 + 350.0):                                 # pendant lanterns
        tb.cyl('Lamp fitting', (xl, ceil_y(0) - 1.0, 0), (xl, ceil_y(0) - 22.0, 0), 0.8)
        tb.cyl('Lamp fitting', (xl, ceil_y(0) - 22.0, 0), (xl, ceil_y(0) - 26.0, 0), 7.0, 3.0)
        tb.sphere('Lamp', (xl, ceil_y(0) - 33.0, 0), 8.5)
    # floor: aisle strips + trap doors
    for zz in (-10.0, 30.0):
        tb.box('Floor strip', L / 2, fl + 0.2, zz, x1 - x0 - 2 * t, 0.4, 3.0)
    for xt in (ev('bogie_a_x'), ev('bogie_b_x')):
        tb.box('Trap door', xt, fl + 0.15, 10.0, 80.0, 0.3, 36.0)
    # bulkheads: sliding doors (closed), glazing in the side windows, sign
    for tag, xb, sgn in (('A', x0, 1), ('B', x1, -1)):
        xd = xb + sgn * (t + 2.0)
        tb.box('Bulkhead door', xd, fl + 94.0, 0, 3.0, 188.0, 70.0)
        tb.box('Door glass', xd + sgn * 0.0, fl + 140.0, 0, 3.6, 70.0, 50.0)
        tb.cyl('Door handle', (xd + sgn * 2.0, fl + 100.0, 28.0), (xd + sgn * 2.0, fl + 120.0, 28.0), 1.0)
        for s in (1, -1):
            tb.box('Door glass', xb + sgn * t / 2, fl + 108.0, s * 68.0, 0.6, 134.0, 48.0)
        tb.box('Sign', xb + sgn * (t + 0.6), fl + 196.0, 0, 0.6, 9.0, 46.0)
        # platform: drum controller (driver's left = +z at end A, -z at end B), brake column (right), stool, gong
        xe = 0.0 if tag == 'A' else L
        Xp = (lambda x: x) if tag == 'A' else (lambda x: L - x)
        zl = 38.0 if tag == 'A' else -38.0
        tb.box('Controller', Xp(32.0), fl + 52.0, zl, 22.0, 104.0, 26.0)
        tb.cyl('Controller', (Xp(21.0), fl + 6.0, zl), (Xp(21.0), fl + 100.0, zl), 13.0)          # rounded drum front
        tb.cyl('Controller top', (Xp(26.0), fl + 100.0, zl), (Xp(26.0), fl + 104.0, zl), 15.5)
        tb.cyl('Reverser key', (Xp(36.0), fl + 104.0, zl - 6.0), (Xp(36.0), fl + 110.0, zl - 6.0), 1.0)
        tb.box('Reverser key', Xp(39.0), fl + 110.0, zl - 6.0, 8.0, 1.5, 2.0)
        for k in range(5):                                                                      # notch plate
            a = math.radians(-60 + k * 30)
            tb.box('Controller top', Xp(26.0 - 13.0 * math.cos(a)), fl + 104.6, zl + 13.0 * math.sin(a), 1.0, 0.6, 2.0)
        tb.cyl('Controller handle', (Xp(26.0), fl + 104.0, zl), (Xp(26.0), fl + 111.0, zl), 1.6)
        tb.box('Controller handle', Xp(20.0), fl + 111.5, zl + 3.0, 16.0, 2.0, 3.0, ax=(0.89 * (1 if tag == 'A' else -1), 0, 0.45), ay=(0, 1, 0))
        tb.cyl('Controller handle', (Xp(12.0), fl + 111.5, zl + 7.0), (Xp(12.0), fl + 117.0, zl + 7.0), 1.6)
        tb.cyl('Brake column', (Xp(30.0), fl, -zl), (Xp(30.0), fl + 100.0, -zl), 3.0)
        tb.cyl('Brake wheel', (Xp(30.0), fl + 101.0, -zl), (Xp(30.0), fl + 103.0, -zl), 17.0)
        tb.cyl('Brake column', (Xp(30.0), fl + 103.0, -zl), (Xp(30.0), fl + 108.0, -zl), 2.5)
        tb.cyl('Stool post', (Xp(72.0), fl, 0), (Xp(72.0), fl + 62.0, 0), 2.0)
        tb.cyl('Driver stool', (Xp(72.0), fl + 62.0, 0), (Xp(72.0), fl + 67.0, 0), 17.0)
        tb.cyl('Gong', (Xp(46.0), fl, 4.0), (Xp(46.0), fl + 2.5, 4.0), 4.0)
        tb.cyl('Cab rail', (Xp(26.0), 196.0, -70.0), (Xp(26.0), 196.0, 70.0), 1.2)
        for zz in (-70.0, 70.0):
            tb.cyl('Cab rail', (Xp(26.0), 196.0, zz), (Xp(18.0), 196.0, zz * 1.05), 1.0)
        for sz in (1, -1):
            tb.cyl('Stanchion', (Xp(ev('ent_x1') - 8.0), fl, sz * (hw - 14.0)), (Xp(ev('ent_x1') - 8.0), eave, sz * (hw - 14.0)), 1.6)
    tb.commit('Interior')
    # seats: one row per big window, doubles on +z (wall side), singles on -z
    sd = seat(g, des, 'Seat double', 98.0, -1); ss = seat(g, des, 'Seat single', 52.0, 1)
    md, ms = [], []
    for i in range(n):
        xc = xw + i * p + w / 2
        m = adsk.core.Matrix3D.create(); m.translation = adsk.core.Vector3D.create(xc, fl, hi - 1.0); md.append(m)
        m2 = adsk.core.Matrix3D.create(); m2.translation = adsk.core.Vector3D.create(xc, fl, -(hi - 1.0)); ms.append(m2)
    place(des, sd, md); place(des, ss, ms)
    if des.snapshots.hasPendingSnapshot:
        des.snapshots.add()
    print('interior bodies', I.bRepBodies.count, '| seats', len(md) + len(ms))
