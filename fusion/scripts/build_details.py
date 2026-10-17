# Side details of car 601 (component 'Side Details'): waist + bottom rails, panel beading on the post lines,
# panel lining (cream inset line, red era), side window sashes / sash rails / glass, eave moulding, solebars with
# brackets. Underframe equipment (component 'Underframe'): cross-bearers, centre sills, air reservoir, resistor
# grid box, compressor, brake cylinder, battery box, sandboxes + pipes, brake rodding. Positions: tp 1920902.
import math
import adsk.core, adsk.fusion
import os
ROOT = os.path.dirname(os.path.abspath(__file__))

def run(_context: str):
    g = {'__file__': os.path.join(ROOT, 'common601.py')}; exec(open(g['__file__']).read(), g)
    des = g['design'](); ev = g['ev_fn'](des)
    C = g['comp'](des, 'Side Details'); g['wipe'](C); tb = g['TB'](C)
    L, hw, t = ev('car_len'), ev('half_w'), ev('wall_t')
    x0, x1 = ev('ent_x1'), L - ev('ent_x1')
    bb_, rb, waist, sill, wt, eave = ev('body_bot'), ev('rail_bot_h'), ev('waist_h'), ev('sill_h'), ev('win_top'), ev('eave_h')
    n = int(round(ev('n_win', ''))); p, w, xw = ev('win_pitch'), ev('win_w'), ev('win1_x')
    nx0, nw = ev('nwin_x'), ev('nwin_w')
    W = [(nx0, nx0 + nw)] + [(xw + i * p, xw + i * p + w) for i in range(n)] + [(L - nx0 - nw, L - nx0)]
    posts = [x0 + 9.0] + [(W[i][1] + W[i + 1][0]) / 2 for i in range(len(W) - 1)] + [x1 - 9.0]
    for sz in (1, -1):
        zo = sz * hw
        def sbox(name, xa, xb, ya, yb, d0, d1):
            """box on the side, x xa..xb, y ya..yb, from d0 to d1 outward of the body surface (cm)."""
            tb.box(name, (xa + xb) / 2, (ya + yb) / 2, zo + sz * (d0 + d1) / 2, xb - xa, yb - ya, abs(d1 - d0))
        sbox('Waist rail', x0, x1, waist, sill, -0.5, 1.4)
        sbox('Waist rail', x0, x1, sill - 1.2, sill + 0.6, -t + 1.0, 2.0)          # sill nosing
        sbox('Bottom rail', x0, x1, bb_, bb_ + rb, -0.5, 1.4)
        sbox('Eave moulding', x0, x1, eave - 3.0, eave, -0.5, 1.6)
        for xp in posts:
            sbox('Panel beading', xp - 1.2, xp + 1.2, bb_ + rb, waist, -0.5, 0.9)
        for xa, xb in zip(posts[:-1], posts[1:]):          # inset lining on each lower panel
            a, b = xa + 5.0, xb - 5.0; ya, yb = bb_ + rb + 5.0, waist - 5.0
            if b - a < 8: continue
            sbox('Panel lining', a, b, ya, ya + 1.2, -0.3, 0.15); sbox('Panel lining', a, b, yb - 1.2, yb, -0.3, 0.15)
            sbox('Panel lining', a, a + 1.2, ya, yb, -0.3, 0.15); sbox('Panel lining', b - 1.2, b, ya, yb, -0.3, 0.15)
        for xa, xb in W:                                    # window sashes, sash rail, glass
            sbox('Window sash', xa, xb, sill, sill + 3.5, -t * 0.85, -t * 0.25)
            sbox('Window sash', xa, xa + 3.0, sill, wt, -t * 0.85, -t * 0.25)
            sbox('Window sash', xb - 3.0, xb, sill, wt, -t * 0.85, -t * 0.25)
            sbox('Window sash', xa, xb, wt - 9.0, wt - 5.5, -t * 0.85, -t * 0.25)
            sbox('Sash rail', xa, xb, 248.0, 251.0, -t * 0.85, -t * 0.25)
            sbox('Glass', xa + 1.0, xb - 1.0, sill + 1.0, wt - 1.0, -t * 0.6, -t * 0.6 + 0.5)
        # solebar + brackets
        tb.box('Solebar', L / 2, (ev('solebar_bot') + bb_) / 2, sz * (hw - 7.0), x1 - x0 + 70.0, bb_ - ev('solebar_bot'), 10.0)
        tb.box('Solebar', L / 2, ev('solebar_bot') + 1.0, sz * (hw - 9.0), x1 - x0 + 70.0, 2.0, 14.0)
        for xp in posts:
            tb.box('Solebar bracket', xp, (ev('solebar_bot') + bb_) / 2 - 2, sz * (hw - 1.5), 6.0, bb_ - ev('solebar_bot') - 4, 3.0)
            tb.cyl('Rivet', (xp, bb_ - 6.0, sz * (hw - 0.2)), (xp, bb_ - 6.0, sz * (hw + 0.6)), 0.9)
    tb.commit('Side Details')

    U = g['comp'](des, 'Underframe'); g['wipe'](U); ub = g['TB'](U)
    sb = ev('solebar_bot'); fl = ev('floor_h')
    for xx in [40.0 + k * (L - 80.0) / 12 for k in range(13)]:
        ub.box('Cross bearer', xx, sb + 8.0, 0, 8.0, 12.0, 2 * hw - 16.0)
    for zz in (-38.0, 38.0):
        ub.box('Centre sill', L / 2, sb + 6.0, zz, L - 80.0, 14.0, 6.0)
    # air reservoir (visible side, x 6.97-8.44), resistor grid box (5.91-6.53), compressor (~4.7-5.1)
    ub.cyl('Air reservoir', (697.0, 53.0, 62.0), (844.0, 53.0, 62.0), 17.0)
    for xx in (697.0, 844.0):
        ub.sphere('Air reservoir', (xx, 53.0, 62.0), 17.0)
    for xx in (720.0, 820.0):
        ub.box('Hanger', xx, (53.0 + sb) / 2 + 8, 62.0, 4.0, sb - 53.0 + 10, 36.0)
    ub.box('Resistor box', 622.0, 50.0, 55.0, 62.0, 36.0, 60.0)
    for k in range(10):
        ub.box('Resistor grille', 596.0 + k * 5.4, 48.0, 85.4, 2.0, 26.0, 1.2)
    ub.box('Resistor box', 622.0, 50.0, -55.0, 62.0, 36.0, 60.0)
    ub.box('Compressor', 490.0, 52.0, 50.0, 46.0, 34.0, 40.0)
    ub.cyl('Compressor', (468.0, 52.0, 30.0), (468.0, 52.0, 72.0), 14.0)
    ub.cyl('Brake cylinder', (560.0, 56.0, -30.0), (610.0, 56.0, -30.0), 12.0)
    ub.box('Battery box', 890.0, 52.0, -62.0, 70.0, 34.0, 44.0)
    ub.box('Controller cable duct', L / 2, sb - 3.0, -20.0, L - 300.0, 6.0, 12.0)
    for xs in (ev('bogie_a_x') - 115.0, ev('bogie_b_x') + 115.0):
        for sz in (1, -1):
            ub.box('Sandbox', xs, sb - 12.0, sz * 75.0, 26.0, 26.0, 22.0)
            ub.cyl('Sand pipe', (xs, sb - 25.0, sz * 75.0), (xs + (32.0 if xs < L / 2 else -32.0) * 0, 10.0, sz * 68.0), 1.5)
    for zz in (-20.0, 20.0):
        ub.cyl('Brake rod', (ev('bogie_a_x') + 40.0, 48.0, zz), (ev('bogie_b_x') - 40.0, 48.0, zz), 1.3)
    ub.commit('Underframe')
    print('side details', C.bRepBodies.count, '| underframe', U.bRepBodies.count)
