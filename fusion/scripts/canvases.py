# Calibrated photo underlay for car 601 (component 'Underlays'): the transphoto 1920902 broadside resampled to
# 100 px/m by references/notes/photogrammetry/underlay_601.py, on a plane at z = +2.6 m (between a viewer of the
# +z side and the car), 45 % opacity, so it overlays the model in the 'left' view. _context 'hide' switches it off.
import adsk.core, adsk.fusion
import os
ROOT = os.path.dirname(os.path.abspath(__file__))
DER = os.path.join(ROOT, '..', '..', 'references', 'images', 'derived', '')   # gitignored; see references/notes/photogrammetry
# name, file, z offset cm, mm/px, u0 px, v0 px (from top) of the model origin, w, h
CANVASES = [('601 broadside tp1920902', 'derived_601_broadside_100pxm.jpg', 260.0, 10.0, 67.5, 666.0, 1462, 822)]

def run(_context: str):
    g = {'__file__': os.path.join(ROOT, 'common601.py')}; exec(open(g['__file__']).read(), g)
    des = g['design']()
    C = g['comp'](des, 'Underlays')
    for i in range(C.canvases.count - 1, -1, -1): C.canvases.item(i).deleteMe()
    for i in range(C.constructionPlanes.count - 1, -1, -1): C.constructionPlanes.item(i).deleteMe()
    vis = (_context or '').strip() != 'hide'
    for name, fn, off, s, u0, v0, iw, ih in CANVASES:
        pi = C.constructionPlanes.createInput(); pi.setByOffset(C.xYConstructionPlane, adsk.core.ValueInput.createByReal(off))
        pl = C.constructionPlanes.add(pi); pl.name = 'Underlay plane ' + name; pl.isLightBulbOn = False
        ci = C.canvases.createInput(DER + fn, pl)
        W, H = iw * s / 10.0, ih * s / 10.0
        uo, vo = u0 / iw, 1.0 - v0 / ih
        m = adsk.core.Matrix2D.create()
        m.setCell(0, 0, W); m.setCell(0, 2, -W * uo); m.setCell(1, 1, H); m.setCell(1, 2, -H * vo)
        ci.transform = m; ci.opacity = 45; ci.isDisplayedThrough = False
        cv = C.canvases.add(ci); cv.name = name; cv.isLightBulbOn = vis
    print('canvases', C.canvases.count, 'visible' if vis else 'hidden')
