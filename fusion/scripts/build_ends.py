# Cab ends of car 601 (component 'Ends'), both ends from the same code (x -> car_len - x for end B):
#  - 5-facet bowed end (corner / intermediate / centre facets, end_poly in common601.py): dash panels, cream waist
#    band, window posts, glass with rounded-corner fillets, sashes, header; facet-joint beading + dash lining
#  - corner posts, entrance steps (two treads + hangers), folded platform gates, brass grab handles
#  - apron / fender (follows the bow, grown by apron_out, returns along the sides), coupler pocket + tow bar
#  - headlight (chrome ring, lens) on the centre facet; destination board on the roof hood + route-number box; wiper
# Photos: 2012 Commons front (light blue), tp 2110423 / 1915990 head-on (red), tp 1920902 broadside.
import math
import adsk.core, adsk.fusion
import os
ROOT = os.path.dirname(os.path.abspath(__file__))

def run(_context: str):
    g = {'__file__': os.path.join(ROOT, 'common601.py')}; exec(open(g['__file__']).read(), g)
    des = g['design'](); ev = g['ev_fn'](des)
    C = g['comp'](des, 'Ends'); g['wipe'](C); tb = g['TB'](C)
    L, hw, t = ev('car_len'), ev('half_w'), ev('wall_t')
    bb_, waist, fwb, fwt, eave = ev('body_bot'), ev('waist_h'), ev('fwin_bot'), ev('fwin_top'), ev('eave_h')
    e0, e1 = ev('ent_x0'), ev('ent_x1')

    for tag, sx in (('A', 1), ('B', -1)):
        X = (lambda x: x) if sx > 0 else (lambda x: L - x)
        def fbox(name, a, b, y0, y1, d0, d1, s0=0.0, s1=1.0, ext=0.0):
            """Box on facet a->b (plan, end-A coords), from fraction s0..s1 (+ext cm each side), heights y0..y1,
            depth d0..d1 inward from the facet line (negative = outward)."""
            dx, dz = b[0] - a[0], b[1] - a[1]; Lf = math.hypot(dx, dz); ux, uz = dx / Lf, dz / Lf
            nx, nz = -uz, ux                      # candidate normal; make it point inward (+x for end A)
            if nx < 0: nx, nz = -nx, -nz
            sm = (s0 + s1) / 2; dm = (d0 + d1) / 2
            px = a[0] + dx * sm + nx * dm; pz = a[1] + dz * sm + nz * dm
            ln = Lf * (s1 - s0) + 2 * ext
            tb.box(name, X(px), (y0 + y1) / 2, pz, ln, y1 - y0, abs(d1 - d0), ax=(sx * ux, 0, uz), ay=(0, 1, 0))
            return Lf
        def fchamfer(a, b, s, y, r):
            """Rounded-corner fill: a square of side r turned 45 deg in the facet plane, centred on the glass corner."""
            dx, dz = b[0] - a[0], b[1] - a[1]; Lf = math.hypot(dx, dz); ux, uz = dx / Lf, dz / Lf
            nx, nz = -uz, ux
            if nx < 0: nx, nz = -nx, -nz
            px = a[0] + dx * s + nx * t * 0.6; pz = a[1] + dz * s + nz * t * 0.6
            c45 = math.sqrt(0.5)
            tb.box('Window post', X(px), y, pz, r * 0.72, r * 0.72, t * 0.8,
                   ax=(sx * ux * c45, c45, uz * c45), ay=(-sx * ux * c45, c45, -uz * c45))
        F = g['facets'](ev)
        wins = {'centre': ev('fwin_c_w'), 'mid': 38.0, 'corner': 20.0}
        for i, (a, b, kind) in enumerate(F):
            Lf = math.hypot(b[0] - a[0], b[1] - a[1])
            fbox('Dash', a, b, bb_, waist, 0, t, ext=0.6)
            fbox('Waist band', a, b, waist, fwb, -1.0, t, ext=0.6)
            fbox('Header', a, b, fwt, eave, 0, t, ext=0.6)
            w = wins[kind]; pf = (Lf - w) / 2 / Lf
            fbox('Window post', a, b, fwb, fwt, 0, t, 0.0, pf, ext=0.3)
            fbox('Window post', a, b, fwb, fwt, 0, t, 1 - pf, 1.0, ext=0.3)
            fbox('Glass', a, b, fwb, fwt, t * 0.55, t * 0.55 + 0.6, pf, 1 - pf, ext=0.5)
            # sash (varnished frame inside the opening) + rounded-corner fillets
            s3 = 3.0 / Lf
            fbox('Window sash', a, b, fwb, fwb + 3.0, t * 0.3, t * 0.9, pf, 1 - pf)
            fbox('Window sash', a, b, fwt - 3.0, fwt, t * 0.3, t * 0.9, pf, 1 - pf)
            fbox('Window sash', a, b, fwb, fwt, t * 0.3, t * 0.9, pf, pf + s3)
            fbox('Window sash', a, b, fwb, fwt, t * 0.3, t * 0.9, 1 - pf - s3, 1 - pf)
            r = 9.0 if kind == 'centre' else 6.0
            for yy in (fwb, fwt):
                for ss in (pf, 1 - pf):
                    fchamfer(a, b, ss, yy, r)
            # dash beading (top + bottom strips) and lining (inset rectangle, 1.5 cm, painted per livery)
            fbox('Dash beading', a, b, waist - 2.0, waist, -0.8, 0.5, ext=0.6)
            fbox('Dash beading', a, b, bb_, bb_ + 2.5, -0.8, 0.5, ext=0.6)
            li = 6.0 / Lf
            fbox('Dash lining', a, b, waist - 9.0, waist - 7.5, -0.15, 0.2, li, 1 - li)
            fbox('Dash lining', a, b, bb_ + 8.0, bb_ + 9.5, -0.15, 0.2, li, 1 - li)
            fbox('Dash lining', a, b, bb_ + 8.0, waist - 7.5, -0.15, 0.2, li, li + 1.5 / Lf)
            fbox('Dash lining', a, b, bb_ + 8.0, waist - 7.5, -0.15, 0.2, 1 - li - 1.5 / Lf, 1 - li)
        P5 = g['end_poly'](ev)
        for (px, pz) in P5[1:-1]:                 # vertical beading on the facet joints
            tb.cyl('Dash beading', (X(px - 0.3), bb_, pz), (X(px - 0.3), waist, pz), 1.0)
        # corner posts (side junction -> entrance) and saloon-side grab handles
        for sz in (1, -1):
            q = P5[0] if sz > 0 else P5[-1]
            x0c = q[0]
            tb.box('Corner post', X((x0c + e0) / 2), (bb_ + eave) / 2, sz * (hw - t / 2), e0 - x0c + 0.5, eave - bb_, t)
            tb.box('Corner post', X((x0c + e0) / 2 + 0.5), (bb_ + 9.0) / 2 + 0.0, sz * (hw - t / 2 + 0.6), e0 - x0c, 9.0, t)
            for xh in (e0 + 3.5, e1 - 3.5):
                tb.cyl('Grab handle', (X(xh), 100.0, sz * (hw + 3.0)), (X(xh), 225.0, sz * (hw + 3.0)), 1.4)
                for yh in (100.0, 225.0):
                    tb.cyl('Grab handle', (X(xh), yh, sz * (hw - 1.0)), (X(xh), yh, sz * (hw + 3.0)), 1.0)
            # steps: upper tread just outside the body line, lower tread further out; side hangers
            s1h, s2h = ev('step1_h'), ev('step2_h')
            xa, xb = e0 + 2.0, e1 - 2.0
            tb.box('Step tread', X((xa + xb) / 2), s1h - 1.5, sz * (hw + 4.0), xb - xa, 3.0, 24.0)
            tb.box('Step tread', X((xa + xb) / 2), s2h - 1.5, sz * (hw + 12.0), xb - xa, 3.0, 26.0)
            tb.box('Step riser', X((xa + xb) / 2), (s1h + ev('floor_h')) / 2, sz * (hw - 6.0), xb - xa, ev('floor_h') - s1h, 1.5)
            for xx in (xa + 1.0, xb - 1.0):
                tb.box('Step hanger', X(xx), (s2h - 3 + ev('floor_h')) / 2, sz * (hw + 8.0), 1.2, ev('floor_h') - s2h + 3, 34.0)
            # folded lattice gate parked against the corner post (open, as in service)
            for k in range(6):
                tb.cyl('Gate bar', (X(e0 + 1.5 + k * 1.3), 92.0, sz * (hw - 2.5)), (X(e0 + 1.5 + k * 1.3), 172.0, sz * (hw - 2.5)), 0.6)
            for yy in (92.0, 132.0, 172.0):
                tb.box('Gate bar', X(e0 + 4.8), yy, sz * (hw - 2.5), 8.5, 1.6, 1.6)
            tb.box('Gate bar', X(e0 + 4.8), 172.0, sz * (hw - 2.5), 8.5, 1.6, 1.6)
        # apron / fender: facets grown by apron_out, plate 4 cm thick, apron_bot .. body_bot; top cap; side returns
        ao, ab = ev('apron_out'), ev('apron_bot')
        G = g['facets'](ev, ao)
        for a, b, kind in G:
            fbox('Apron', a, b, ab, bb_ + 2.0, 0, 4.0, ext=1.2)
        for (a, b, kind), (a0, b0, k0) in zip(G, F):
            fbox('Apron top', a, b, bb_ + 0.5, bb_ + 2.5, 0, ao + 1.0, ext=1.0)
        PG = g['end_poly'](ev, ao)
        for sz, q in ((1, PG[0]), (-1, PG[-1])):
            tb.box('Apron', X((q[0] + e0 + 6) / 2), (ab + 12 + bb_ + 2) / 2, sz * (hw + ao - 2.0), e0 + 6 - q[0], bb_ + 2 - ab - 12, 4.0)
        # coupler pocket + tow bar on the centre facet of the apron
        cc = G[2]; cx_ = (cc[0][0] + cc[1][0]) / 2
        tb.box('Coupler pocket', X(cx_ - 0.4), 56.0, 0, 1.0, 11.0, 26.0)
        tb.box('Tow bar', X(cx_ - 6.0), 56.0, 0, 14.0, 5.0, 9.0)
        tb.cyl('Tow bar', (X(cx_ - 10.0), 50.0, 0), (X(cx_ - 10.0), 62.0, 0), 1.3)
        tb.box('Lifeguard', X(cx_ + 22.0), ab - 4.0, 0, 30.0, 6.0, 2 * hw - 60.0)
        # headlight on the centre facet
        c = F[2]; cxh = (c[0][0] + c[1][0]) / 2; R = ev('hl_d') / 2; hy = ev('hl_y')
        tb.cyl('Headlight ring', (X(cxh + 0.5), hy, 0), (X(cxh - 5.0), hy, 0), R)
        tb.cyl('Headlamp lens', (X(cxh - 5.0), hy, 0), (X(cxh - 5.4), hy, 0), R - 2.6)
        tb.cyl('Headlight ring', (X(cxh - 5.0), hy, 0), (X(cxh - 6.2), hy, 0), R, R - 2.2)
        # destination board on the roof hood (+ route box in the middle), following the roof overhang
        ov = ev('roof_ovh'); bbot, bh = ev('board_bot'), ev('board_h')
        GB = g['facets'](ev, ov + 1.0)
        for a, b, kind in GB:
            s0, s1 = (0.35, 1.0) if kind == 'corner' and a[1] > 0 else (0.0, 0.65) if kind == 'corner' else (0.0, 1.0)
            fbox('Destination board', a, b, bbot, bbot + bh, -2.5, 0, s0, s1, ext=0.0 if kind == 'corner' else 0.5)
            fbox('Board frame', a, b, bbot + bh - 1.5, bbot + bh, -3.2, 0, s0, s1, ext=0.0 if kind == 'corner' else 0.5)
            fbox('Board frame', a, b, bbot, bbot + 1.5, -3.2, 0, s0, s1, ext=0.0 if kind == 'corner' else 0.5)
        cb = GB[2]; xb_ = (cb[0][0] + cb[1][0]) / 2; rw = ev('route_w')
        tb.box('Route box', X(xb_ - 6.0), bbot + bh / 2 + 2.0, 0, 12.0, bh + 6.0, rw)
        tb.box('Route box glass', X(xb_ - 12.2), bbot + bh / 2 + 2.0, 0, 0.4, bh - 2.0, rw - 4.0)
        # hand wiper on the centre window (driver side)
        # hand wiper parked at ~35 deg from the top of the centre window (driver side), pivot + arm + blade
        ca, sa = math.cos(math.radians(35)), math.sin(math.radians(35))
        zp = -sx * 18.0; yp = fwt - 4.0
        tb.cyl('Wiper', (X(cxh - 1.0), yp, zp), (X(cxh - 3.0), yp, zp), 1.2)
        tb.box('Wiper', X(cxh - 1.6), yp - 20.0 * ca, zp + sx * 20.0 * sa, 40.0, 0.6, 1.0, ax=(0, ca, -sx * sa), ay=(1, 0, 0))
    tb.commit('Ends')
    print('end bodies', C.bRepBodies.count)
