# Roof equipment of car 601 (component 'Roof Equipment'):
#  - two lattice pantograph towers (4 angle-iron legs splayed onto the cornice, rings at foot / mid / deck,
#    X-bracing on all faces, deck frame) at tower_a_x / tower_b_x - the Raml wire was raised for the 4.8 m
#    double-deckers, so the old cars carry their pantographs on towers (tp 1920902, 2012 Commons front)
#  - a diamond pantograph on each deck (insulators, base frame, lower + upper arms, pan head with horns, springs);
#    panto_a_up / panto_b_up set the height above folded (2024 broadside: A raised, B folded)
#  - roof cables down a leg into the roof, lightning arrester, transverse roof seam battens following the arch,
#    roof walkway boards between the towers, rain gutters on the cornice.
import math
import adsk.core, adsk.fusion
import os
ROOT = os.path.dirname(os.path.abspath(__file__))

def run(_context: str):
    g = {'__file__': os.path.join(ROOT, 'common601.py')}; exec(open(g['__file__']).read(), g)
    des = g['design'](); ev = g['ev_fn'](des)
    C = g['comp'](des, 'Roof Equipment'); g['wipe'](C); tb = g['TB'](C)
    L, hw = ev('car_len'), ev('half_w'); ov = ev('roof_ovh'); zr = hw + ov
    ct, cr = ev('cornice_top'), ev('crown_h')
    Rr = (zr * zr + (cr - ct) ** 2) / (2 * (cr - ct)); yc = cr - Rr
    roof_y = lambda z: yc + math.sqrt(max(0.0, Rr * Rr - z * z))

    def beam(name, p, q, w=5.0, h=5.0):
        d = [q[i] - p[i] for i in range(3)]; ln = math.sqrt(sum(v * v for v in d)); u = tuple(v / ln for v in d)
        up = (1.0, 0, 0) if abs(u[1]) > 0.9 else (0, 1.0, 0)
        tb.box(name, (p[0] + q[0]) / 2, (p[1] + q[1]) / 2, (p[2] + q[2]) / 2, ln, w, h, ax=u, ay=up)

    def lerp(p, q, s): return tuple(p[i] + (q[i] - p[i]) * s for i in range(3))

    def tower(tx, up):
        fl, fw = ev('tower_foot_l') / 2, ev('tower_foot_w') / 2
        dl, dw, th = ev('tower_deck_l') / 2, ev('tower_deck_w') / 2, ev('tower_h')
        feet = {(sx, sz): (tx + sx * fl, roof_y(fw) + 2.0, sz * fw) for sx in (-1, 1) for sz in (-1, 1)}
        deck = {(sx, sz): (tx + sx * dl, th, sz * dw) for sx in (-1, 1) for sz in (-1, 1)}
        for k in feet:
            beam('Tower leg', feet[k], deck[k], 6.0, 6.0)
            tb.box('Tower foot', feet[k][0], feet[k][1] - 1.0, feet[k][2], 16.0, 3.0, 16.0)
        levels = [0.0, 0.5, 1.0]
        ring = lambda s: {k: lerp(feet[k], deck[k], s) for k in feet}
        order = [(-1, -1), (1, -1), (1, 1), (-1, 1)]
        for s in levels:
            r = ring(s)
            for i in range(4):
                beam('Tower ring', r[order[i]], r[order[(i + 1) % 4]], 5.0, 5.0)
        for s0, s1 in zip(levels[:-1], levels[1:]):
            r0, r1 = ring(s0), ring(s1)
            for i in range(4):
                a, b = order[i], order[(i + 1) % 4]
                beam('Tower brace', r0[a], r1[b], 3.5, 1.0); beam('Tower brace', r0[b], r1[a], 3.5, 1.0)
        # deck: cross members + plate
        for sx in (-0.33, 0.33):
            beam('Tower deck', (tx + sx * 2 * dl, th, -dw), (tx + sx * 2 * dl, th, dw), 5.0, 5.0)
        beam('Tower deck', (tx - dl, th, 0), (tx + dl, th, 0), 5.0, 5.0)
        # pantograph on insulators
        bl, bw = 100.0, 70.0; y0 = th + 4.0
        for sx in (-1, 1):
            for sz in (-1, 1):
                for k in range(3):
                    tb.cyl('Insulator', (tx + sx * bl / 2, y0 + k * 4.0, sz * bw / 2), (tx + sx * bl / 2, y0 + k * 4.0 + 2.6, sz * bw / 2), 6.5 - k * 0.3)
                tb.cyl('Insulator', (tx + sx * bl / 2, y0, sz * bw / 2), (tx + sx * bl / 2, y0 + 13.0, sz * bw / 2), 3.0)
        yb = y0 + 14.0
        tb.box('Pantograph base', tx, yb + 2.0, bw / 2, bl + 10.0, 4.0, 5.0); tb.box('Pantograph base', tx, yb + 2.0, -bw / 2, bl + 10.0, 4.0, 5.0)
        tb.box('Pantograph base', tx - bl / 2, yb + 2.0, 0, 5.0, 4.0, bw); tb.box('Pantograph base', tx + bl / 2, yb + 2.0, 0, 5.0, 4.0, bw)
        hf = 22.0; h = hf + up                   # pan head height above the base frame
        yk = yb + 4.0 + h * 0.5; yt = yb + 4.0 + h
        half = math.sqrt(max(100.0, 100.0 ** 2 - (h * 0.5) ** 2))  # diamond arms of fixed length 1.0 m
        half = min(half, 85.0)
        for sz in (-1, 1):
            z = sz * 30.0
            beam('Pantograph frame', (tx - half, yb + 4.0, z), (tx, yk, z * 0.9), 2.8, 2.8)
            beam('Pantograph frame', (tx + half, yb + 4.0, z), (tx, yk, z * 0.9), 2.8, 2.8)
            beam('Pantograph frame', (tx, yk, z * 0.9), (tx - half * 0.9, yt, z * 0.7), 2.2, 2.2)
            beam('Pantograph frame', (tx, yk, z * 0.9), (tx + half * 0.9, yt, z * 0.7), 2.2, 2.2)
            tb.cyl('Pantograph spring', (tx - half * 0.55, yb + 6.0, z), (tx - 8.0, yk - 4.0, z), 1.6)
        beam('Pantograph frame', (tx, yk, -28.0), (tx, yk, 28.0), 2.4, 2.4)
        for sx in (-1, 1):
            beam('Pantograph frame', (tx + sx * half * 0.9, yt, -22.0), (tx + sx * half * 0.9, yt, 22.0), 2.0, 2.0)
            beam('Pantograph frame', (tx + sx * half * 0.9, yt, 0), (tx + sx * 14.0, yt + 4.0, 0), 1.6, 1.6)
        for sx in (-1, 1):
            beam('Collector strip', (tx + sx * 13.0, yt + 5.0, -72.0), (tx + sx * 13.0, yt + 5.0, 72.0), 4.0, 3.0)
        for sz in (-1, 1):
            beam('Pantograph horn', (tx, yt + 5.0, sz * 72.0), (tx, yt - 10.0, sz * 92.0), 2.0, 2.0)
            beam('Pantograph horn', (tx - 13.0, yt + 5.0, sz * 72.0), (tx + 13.0, yt + 5.0, sz * 72.0), 1.8, 1.8)
        # cable from the pantograph base down the A-side leg into the roof
        f = feet[(-1, 1)]; d_ = deck[(-1, 1)]
        tb.cyl('Roof cable', (d_[0] + 3, d_[1], d_[2] - 3), (f[0] + 6, f[1] + 2, f[2] - 6), 1.4)
        tb.cyl('Roof cable', (f[0] + 6, f[1] + 2, f[2] - 6), (f[0] + 60, roof_y(f[2] - 20) + 2, f[2] - 20), 1.4)
        tb.cyl('Lightning arrester', (tx + fl + 25.0, roof_y(40.0), 40.0), (tx + fl + 25.0, roof_y(40.0) + 16.0, 40.0), 5.0)
        tb.cyl('Insulator', (tx + fl + 25.0, roof_y(40.0) + 16.0, 40.0), (tx + fl + 25.0, roof_y(40.0) + 22.0, 40.0), 7.0)

    tower(ev('tower_a_x'), ev('panto_a_up'))
    tower(ev('tower_b_x'), ev('panto_b_up'))
    # roof seam battens (canvas roof over boards) every window pitch, following the arch in 10 chords
    x0, x1 = ev('ent_x1'), L - ev('ent_x1')
    nseg = 10; xs = x0
    while xs <= x1 + 1:
        for k in range(nseg):
            za = -zr + 4 + (2 * zr - 8) * k / nseg; zb = -zr + 4 + (2 * zr - 8) * (k + 1) / nseg
            beam('Roof batten', (xs, roof_y(za) + 0.6, za), (xs, roof_y(zb) + 0.6, zb), 3.0, 1.2)
        xs += ev('win_pitch')
    for sz in (1, -1):
        tb.box('Rain gutter', L / 2, ct - 1.0, sz * (zr - 1.5), L - 70.0, 2.5, 3.0)
    # walkway boards between the towers (centre line)
    wa, wb_ = ev('tower_a_x') + ev('tower_foot_l') / 2 + 10, ev('tower_b_x') - ev('tower_foot_l') / 2 - 10
    for zz in (-14.0, 0.0, 14.0):
        tb.box('Roof walkway', (wa + wb_) / 2, cr + 3.0, zz, wb_ - wa, 2.5, 12.0)
    for xx in [wa + k * (wb_ - wa) / 6 for k in range(7)]:
        tb.box('Roof walkway', xx, cr + 1.0, 0, 5.0, 2.5, 44.0)
    tb.commit('Roof Equipment')
    print('roof bodies', C.bRepBodies.count)
