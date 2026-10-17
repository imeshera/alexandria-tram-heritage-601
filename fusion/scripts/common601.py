# Shared helpers for the car 601 build scripts. Exec'd by each 601 script:
#   g = {'__file__': os.path.join(ROOT, 'common601.py')}; exec(open(g['__file__']).read(), g)
# Re-uses the GT6 helpers (comp, wipe, TB, base, ev_fn) from common.py, but points design() at the 601 doc.
import math
import adsk.core, adsk.fusion
import os
ROOT = os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(ROOT, 'common.py')).read())
DOC = 'Alexandria Heritage Tram 601'
import tempfile
SCRATCH = os.path.join(tempfile.gettempdir(), '')   # progress logs

def end_poly(ev, grow=0.0):
    """Plan outline of the bowed end A, from the +z body side to the -z body side, in cm (x, z).
    5 facets: corner (bow_k_ang), intermediate (bow_m, bow_m_ang), centre (bow_c), mirrored.
    grow > 0 offsets the outline outward (roof overhang, apron) by moving each facet along its normal."""
    hw = ev('half_w'); c = ev('bow_c') / 2; m = ev('bow_m')
    am, ak = ev('bow_m_ang', 'rad'), ev('bow_k_ang', 'rad')
    q1 = (0.0, c); q2 = (m * math.sin(am), c + m * math.cos(am))
    dz = hw - q2[1]; q3 = (q2[0] + dz * math.tan(ak), hw)
    half = [q3, q2, q1]
    pts = half + [(x, -z) for x, z in reversed(half)]
    if grow:
        # offset polygon (+z side to -z side); outward normal of segment a->b is to the left in (x,z) going -z..
        segs = list(zip(pts[:-1], pts[1:]))
        lines = []
        for a, b in segs:
            dx, dz = b[0] - a[0], b[1] - a[1]; L = math.hypot(dx, dz); nx, nz = dz / L, -dx / L   # outward = -x side
            if nx > 0: nx, nz = -nx, -nz
            lines.append(((a[0] + nx * grow, a[1] + nz * grow), (dx / L, dz / L)))
        out = []
        # first and last vertices sit on the body side line z = +/-(hw + grow)
        def inter(l1, l2):
            (p, d), (q, e) = l1, l2
            den = d[0] * e[1] - d[1] * e[0]
            t = ((q[0] - p[0]) * e[1] - (q[1] - p[1]) * e[0]) / den
            return (p[0] + d[0] * t, p[1] + d[1] * t)
        side_p = (((0.0, hw + grow), (1.0, 0.0)), ((0.0, -(hw + grow)), (1.0, 0.0)))
        out.append(inter(side_p[0], lines[0]))
        for i in range(len(lines) - 1):
            out.append(inter(lines[i], lines[i + 1]))
        out.append(inter(lines[-1], side_p[1]))
        pts = out
    return pts

def facets(ev, grow=0.0):
    """End-A facets as (a, b, kind) plan segments from +z to -z; kind = corner | mid | centre."""
    p = end_poly(ev, grow); kinds = ['corner', 'mid', 'centre', 'mid', 'corner']
    return [(p[i], p[i + 1], kinds[i]) for i in range(5)]

def mirror_x(L, pts):
    return [(L - x, z) for x, z in pts]


def save(msg):
    """Guarded save of the 601 document only."""
    app = adsk.core.Application.get()
    d = [x for x in app.documents if x.name == DOC or x.name.startswith(DOC + ' v')]
    if not d: raise RuntimeError('doc not open')
    doc = d[0]
    if doc.dataFile is None or doc.dataFile.parentProject.name != PROJECT:
        raise RuntimeError('save guard: parent project is not ' + PROJECT)
    doc.activate()
    return doc.save(msg)
