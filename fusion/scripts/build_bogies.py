# Running gear of car 601: equalizer-bar bogie (outside axleboxes in pedestal jaws, low equalizer bars with coil
# springs, bolster on spring nests + spring plank, two nose-suspended motors with gear cases, clasp-free single
# brake shoes inboard of the wheels with brake beams, sand pipes). One component 'Bogie', two root occurrences at
# bogie_a_x / bogie_b_x (B turned 180 deg). Local frame: origin at the bogie centre on top of rail.
# Wheel 830 mm, wheelbase 1.52 m (V, tp 1920902 broadside: axleboxes + rims).
import math
import adsk.core, adsk.fusion
import os
ROOT = os.path.dirname(os.path.abspath(__file__))

def run(_context: str):
    g = {'__file__': os.path.join(ROOT, 'common601.py')}; exec(open(g['__file__']).read(), g)
    des = g['design'](); ev = g['ev_fn'](des); root = des.rootComponent
    C = None
    for o in root.occurrences:
        if o.component.name == 'Bogie': C = o.component
    if C is None:
        C = root.occurrences.addNewComponent(adsk.core.Matrix3D.create()).component; C.name = 'Bogie'
    g['wipe'](C); tb = g['TB'](C)
    R = ev('wheel_d') / 2; wb = ev('bogie_wb'); b2 = ev('back_to_back') / 2; tw = ev('tread_w')
    fz = ev('gauge') / 2 + 14.0                      # side-frame / axlebox centre plane
    yt = R + 30.0                                    # side-frame top bar centre
    for sx in (-1, 1):
        x = sx * wb / 2
        for sz in (-1, 1):
            zi, zo = sz * b2, sz * (b2 + tw)
            tb.cyl('Wheel', (x, R, zi), (x, R, zo), R)
            tb.cyl('Wheel', (x, R, zi - sz * 0.0), (x, R, zi + sz * 2.8), R + 2.6)           # flange
            tb.cyl('Wheel centre', (x, R, zi + sz * 2.0), (x, R, zi + sz * 6.0), R - 6.0)     # disc / spoked centre
            tb.cyl('Wheel hub', (x, R, zi - sz * 4.0), (x, R, zo + sz * 2.0), 12.0)
            tb.box('Axlebox', x, R, sz * fz, 26.0, 28.0, 20.0)
            tb.box('Axlebox lid', x, R, sz * (fz + 10.5), 20.0, 20.0, 1.5)
            for dx in (-15.5, 15.5):                                                       # pedestal jaws
                tb.box('Pedestal', x + dx, (R - 18.0 + yt) / 2, sz * fz, 4.0, yt - R + 22.0, 8.0)
            tb.cyl('Axlebox spring', (x, R + 14.0, sz * fz), (x, yt - 4.0, sz * fz), 6.0)
            # brake shoe + hanger inboard of the wheel (towards the bogie centre)
            xb = x - sx * (R + 3.5)
            tb.box('Brake shoe', xb, R - 2.0, sz * (b2 + tw / 2), 4.0, 30.0, tw - 2.0)
            tb.box('Brake hanger', xb - sx * 2.0, R + 22.0, sz * (b2 + tw / 2), 3.0, 34.0, 3.0)
        tb.cyl('Axle', (x, R, -(fz + 6.0)), (x, R, fz + 6.0), 7.0)
        tb.box('Brake beam', x - sx * (R + 6.5), R - 2.0, 0, 6.0, 8.0, 2 * (b2 + tw))
        # nose-suspended motor inboard of each axle, gear case on the +z end, nose on the transom
        xm = x - sx * 36.0
        tb.cyl('Traction motor', (xm, R + 2.0, -42.0), (xm, R + 2.0, 42.0), 23.0)
        tb.cyl('Traction motor', (xm, R + 2.0, -46.0), (xm, R + 2.0, -42.0), 18.0)
        tb.box('Gear case', x - sx * 16.0, R, 52.0, 52.0, 44.0, 12.0)
        tb.box('Motor nose', xm - sx * 26.0, R + 16.0, 0, 14.0, 10.0, 30.0)
        tb.box('Motor terminal box', xm, R + 26.0, -20.0, 18.0, 8.0, 16.0)
    for sz in (-1, 1):
        tb.box('Side frame', 0, yt, sz * fz, wb + 46.0, 8.0, 6.0)
        tb.box('Side frame', 0, yt - 7.0, sz * fz, wb - 40.0, 3.0, 8.0)
        for sx in (-1, 1):                                                                 # frame end drops
            tb.box('Side frame', sx * (wb / 2 + 21.0), yt - 6.0, sz * fz, 4.0, 18.0, 6.0)
        # equalizer bar: under both axleboxes, dropping between them, coil springs up to the frame
        ye = R - 20.0; yd = R - 30.0
        for sx in (-1, 1):
            a = (sx * wb / 2, ye, sz * fz); b = (sx * 42.0, yd, sz * fz)
            dx, dy = b[0] - a[0], b[1] - a[1]; ln = math.hypot(dx, dy)
            tb.box('Equalizer', (a[0] + b[0]) / 2, (a[1] + b[1]) / 2, sz * fz, ln + 3.0, 4.0, 5.0, ax=(dx / ln, dy / ln, 0), ay=(-dy / ln, dx / ln, 0))
            tb.cyl('Equalizer spring', (sx * 46.0, yd + 2.0, sz * fz), (sx * 46.0, yt - 4.0, sz * fz), 5.5)
            tb.box('Spring cap', sx * 46.0, yt - 4.5, sz * fz, 12.0, 1.5, 12.0)
        tb.box('Equalizer', 0, yd, sz * fz, 84.0, 4.0, 5.0)
        # bolster spring nest and spring plank
        for dx in (-11.0, 11.0):
            tb.cyl('Bolster spring', (dx, yd + 4.0, sz * (fz - 12.0)), (dx, R + 10.0, sz * (fz - 12.0)), 8.0)
        tb.cyl('Sand pipe', (sz * 0 - (wb / 2 + R * 0.7), yt - 4.0, sz * (b2 + tw / 2)), (-(wb / 2 + R * 0.35), 3.0, sz * (b2 + tw / 2)), 1.4)
        tb.cyl('Sand pipe', ((wb / 2 + R * 0.7), yt - 4.0, sz * (b2 + tw / 2)), ((wb / 2 + R * 0.35), 3.0, sz * (b2 + tw / 2)), 1.4)
    tb.box('Spring plank', 0, R - 28.0, 0, 34.0, 4.0, 2 * fz - 6.0)
    tb.box('Bolster', 0, R + 14.0, 0, 34.0, 10.0, 2 * fz - 2.0)
    tb.cyl('Centre bearing', (0, R + 19.0, 0), (0, R + 24.0, 0), 20.0)
    for sx in (-1, 1):
        tb.box('Transom', sx * 30.0, yt - 2.0, 0, 8.0, 12.0, 2 * fz - 4.0)
    tb.commit('Bogie')
    # place two root occurrences
    occs = [o for o in root.occurrences if o.component == C]
    while len(occs) < 2:
        occs.append(root.occurrences.addExistingComponent(C, adsk.core.Matrix3D.create()))
    for o, x, rot in zip(occs, (ev('bogie_a_x'), ev('bogie_b_x')), (0.0, math.pi)):
        m = adsk.core.Matrix3D.create()
        m.setToRotation(rot, adsk.core.Vector3D.create(0, 1, 0), adsk.core.Point3D.create(0, 0, 0))
        m.translation = adsk.core.Vector3D.create(x, 0, 0)
        o.transform2 = m
    if des.snapshots.hasPendingSnapshot:
        des.snapshots.add()
    print('bogie bodies', C.bRepBodies.count)
