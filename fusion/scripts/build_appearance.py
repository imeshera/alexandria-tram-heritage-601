# Livery + materials for car 601. The 'livery' user parameter selects the scheme (colours sampled from the dated
# photos, slightly greyed for a lived-in look):
#   1 (default) light blue / cream, c. 2007-2019: light-blue dash + lower panels, cream window band, posts and rails,
#     black apron, maroon destination board with a rust route box, aluminium dash beading (2012 Commons front,
#     2007 Parris front)
#   2 red / cream after the 2020 restoration: red dash + lower panels with cream lining, cream upper, blue-grey apron,
#     red board (UTM 2023, transphoto 2022-2025)
#   3 yellow works / shunting car, 2002 (TramTravels, Mustafa Kamel depot)
# Painting is per body (the shell is built as separate colour bodies); faces facing the inside of the car get the
# varnished-wood interior. Faces are re-read after each write (setting an appearance can reorder body.faces).
import adsk.core, adsk.fusion
import os
ROOT = os.path.dirname(os.path.abspath(__file__))

LIVERIES = {  # lower/dash, upper/cream, cornice, roof, apron, board, route box, dash beading, lining, solebar
    1: ((96, 164, 206), (232, 222, 192), (92, 118, 128), (122, 124, 118), (34, 34, 36), (112, 42, 46), (168, 108, 78),
        (196, 198, 196), (96, 164, 206), (40, 42, 44)),
    2: ((196, 34, 16), (232, 221, 196), (118, 120, 118), (116, 118, 114), (108, 128, 140), (194, 38, 22), (194, 38, 22),
        (232, 221, 196), (232, 221, 196), (44, 52, 60)),
    3: ((220, 158, 46), (226, 212, 184), (104, 96, 86), (106, 100, 90), (52, 52, 50), (60, 60, 58), (60, 60, 58),
        (220, 158, 46), (220, 158, 46), (46, 44, 40)),
}

def run(_context: str):
    g = {'__file__': os.path.join(ROOT, 'common601.py')}; exec(open(g['__file__']).read(), g)
    des = g['design'](); ev = g['ev_fn'](des); base = g['base']
    app = adsk.core.Application.get()
    lib = app.materialLibraries.itemByName('Fusion Appearance Library')
    root = des.rootComponent
    lv = int(round(ev('livery', '')))
    lo, up, cor, rf, apr, brd, rbx, bead, lin, sol = LIVERIES.get(lv, LIVERIES[1])

    def lib_app(name):
        a = des.appearances.itemByName(name)
        return a if a else des.appearances.addByCopy(lib.appearances.itemByName(name), name)

    def custom(name, src, rgb):
        a = des.appearances.itemByName(name)
        if not a:
            a = des.appearances.addByCopy(lib.appearances.itemByName(src), name)
        for i in range(a.appearanceProperties.count):
            p = a.appearanceProperties.item(i)
            if isinstance(p, adsk.core.ColorProperty) and any(k in p.id.lower() for k in ('color', 'albedo', 'diffuse')):
                v = p.value
                if v and (v.red, v.green, v.blue) == tuple(rgb): continue
                try: p.value = adsk.core.Color.create(rgb[0], rgb[1], rgb[2], 255)
                except Exception: pass
        return a
    PG = 'Paint - Enamel Glossy (Yellow)'
    A_lo = custom('601 lower', PG, lo); A_up = custom('601 cream', PG, up); A_cor = custom('601 cornice', PG, cor)
    A_rf = custom('601 roof canvas', 'Paint - Metallic (Dark Grey)', rf); A_apr = custom('601 apron', PG, apr)
    A_brd = custom('601 board', PG, brd); A_rbx = custom('601 route box', PG, rbx); A_bead = custom('601 dash beading', PG, bead)
    A_lin = custom('601 lining', PG, lin); A_sol = custom('601 solebar', 'Paint - Metallic (Dark Grey)', sol)
    A_uf = custom('601 underframe', 'Paint - Metallic (Dark Grey)', (40, 40, 38))
    A_lino = custom('601 linoleum', 'Plastic - Matte (Yellow)', (92, 88, 80))
    A_curt = custom('601 curtain', 'Plastic - Matte (Yellow)', (118, 22, 32))
    A_blind = custom('601 blind', 'Plastic - Matte (Yellow)', (236, 232, 220))
    A_wood = lib_app('Mahogany'); A_ceil = lib_app('Cherry'); A_dwood = lib_app('Walnut')
    A_glass, A_rub, A_chr = lib_app('Glass (Clear)'), lib_app('Rubber - Hard'), lib_app('Chrome')
    A_brass, A_stl, A_rough = lib_app('Brass - Polished'), lib_app('Steel - Satin'), lib_app('Steel - Rough')
    A_wht, A_blk, A_red = lib_app('Plastic - Matte (White)'), lib_app('Plastic - Matte (Black)'), lib_app('Glass (Red)')
    A_ins = custom('601 insulator', 'Plastic - Matte (Yellow)', (150, 92, 60))
    A_tower = custom('601 tower grey', 'Paint - Metallic (Dark Grey)', (128, 132, 134))

    def comp(name):
        r = [o.component for o in root.occurrences if o.component.name == name]
        return r[0] if r else None

    L = ev('car_len'); pl = ev('plat_len'); eave, ct = ev('eave_h'), ev('cornice_top')
    def inward(fc):
        p = fc.pointOnFace; ok, n = fc.evaluator.getNormalAtPoint(p)
        d = adsk.core.Vector3D.create(min(max(p.x, pl + 60.0), L - pl - 60.0) - p.x, 190.0 - p.y, -p.z)
        if d.length < 1e-6: return False, n
        d.normalize()
        return n.dotProduct(d) > 0.35, n

    def paint_faces(bd, rule):
        for it in range(8):
            nf = 0
            for i in range(bd.faces.count):
                fc = bd.faces.item(i); w = rule(fc)
                if w and (fc.appearance is None or fc.appearance.id != w.id):
                    fc.appearance = w; nf += 1
            if nf == 0: break

    shell = {'Side upper': A_up, 'Side lower': A_lo, 'Dash': A_lo, 'Waist band': A_up, 'Header': A_up,
             'Window post': A_up, 'Corner post': A_up}
    parts_only = (_context or '').strip() == 'parts'      # skip the slow per-face shell pass
    import time; t0 = time.time()
    LOG = open(g['SCRATCH'] + 'appearance601.log', 'w')
    def log(*x):
        LOG.write('%6.1f ' % (time.time() - t0) + ' '.join(str(v) for v in x) + '\n'); LOG.flush()
    for cname in ('Body',) if parts_only else ('Body', 'Ends'):
        Cc = comp(cname)
        log('component', cname, Cc.bRepBodies.count if Cc else None)
        if not Cc: continue
        for bd in Cc.bRepBodies:
            n_ = base(bd.name)
            if n_[-2:] in (' L', ' R'): n_ = n_[:-2]
            if n_ in shell:
                if parts_only: continue
                out = shell[n_]
                if bd.appearance is None or bd.appearance.id != out.id: bd.appearance = out
                paint_faces(bd, lambda fc, out=out: A_wood if inward(fc)[0] else out)
            elif n_.startswith('Bulkhead'):
                bd.appearance = A_wood
            elif n_ == 'Floor':
                bd.appearance = A_uf
                paint_faces(bd, lambda fc: A_lino if fc.evaluator.getNormalAtPoint(fc.pointOnFace)[1].y > 0.9 else None)
            elif n_ == 'Roof':
                bd.appearance = A_rf
                def rr(fc):
                    ins, n = inward(fc)
                    if ins or n.y < -0.5: return A_ceil
                    if abs(n.y) < 0.5 and fc.centroid.y < ct + 1.0: return A_cor
                    return A_rf
                paint_faces(bd, rr)
            else:
                a = {'Glass': A_glass, 'Window sash': A_dwood, 'Dash beading': A_bead, 'Dash lining': A_lin,
                     'Apron': A_apr, 'Apron top': A_apr, 'Coupler pocket': A_blk, 'Tow bar': A_uf, 'Lifeguard': A_uf,
                     'Headlight ring': A_chr, 'Headlamp lens': A_glass, 'Destination board': A_brd, 'Board frame': A_uf,
                     'Route box': A_rbx, 'Route box glass': A_rbx, 'Wiper': A_blk, 'Step tread': A_rough,
                     'Step riser': A_uf, 'Step hanger': A_uf, 'Gate bar': A_up, 'Grab handle': A_brass}.get(n_)
                if a: bd.appearance = a

    def paint(cname, rule):
        Cc = comp(cname)
        if not Cc: return
        for bd in Cc.bRepBodies:
            a = rule(base(bd.name))
            if a and (bd.appearance is None or bd.appearance.id != a.id): bd.appearance = a

    paint('Side Details', lambda n: {'Waist rail': A_up, 'Bottom rail': A_up, 'Eave moulding': A_up, 'Panel beading': A_up,
                                     'Panel lining': A_lin, 'Window sash': A_dwood, 'Sash rail': A_dwood, 'Glass': A_glass,
                                     'Solebar': A_sol, 'Solebar bracket': A_sol, 'Rivet': A_sol}.get(n))
    paint('Underframe', lambda n: A_uf if n not in ('Resistor grille',) else A_rough)
    paint('Bogie', lambda n: A_stl if n in ('Wheel', 'Axle', 'Axlebox lid') else A_rough if n == 'Brake shoe' else A_uf)
    paint('Roof Equipment', lambda n: A_ins if n == 'Insulator' else A_rough if n == 'Collector strip' else
          A_blk if n in ('Roof cable', 'Pantograph spring') else A_dwood if n == 'Roof walkway' else
          A_rf if n in ('Roof batten', 'Rain gutter') else A_tower)
    seat = lambda n: A_wood if n in ('Seat slat', 'Back slat', 'Back rail') else A_chr if n == 'Grab handle' else A_uf
    paint('Seat double', seat); paint('Seat single', seat)
    paint('Interior', lambda n: {'Ceiling rib': A_dwood, 'Window ledge': A_dwood, 'Curtain': A_curt, 'Curtain rail': A_brass,
                                 'Lamp': A_blind, 'Lamp fitting': A_brass, 'Bulkhead door': A_dwood, 'Door glass': A_glass,
                                 'Door handle': A_brass, 'Floor strip': A_stl, 'Controller': A_blk,
                                 'Controller top': A_brass, 'Controller handle': A_brass, 'Brake column': A_uf,
                                 'Brake wheel': A_blk, 'Driver stool': custom('601 stool', PG, (150, 34, 30)), 'Reverser key': A_brass, 'Stool post': A_stl, 'Stanchion': A_brass,
                                 'Gong': A_brass, 'Sign': A_blind, 'Picture': custom('601 photo print', 'Plastic - Matte (Yellow)', (176, 170, 158)), 'Picture frame': A_blk, 'Bell cord': A_dwood,
                                 'Cab rail': A_brass, 'Trap door': A_lino}.get(n))
    for i in range(des.appearances.count - 1, -1, -1):
        a = des.appearances.item(i)
        if a.name.startswith('601') and not a.isUsed:
            try: a.deleteMe()
            except Exception: pass
    log('done'); LOG.close()
    print('livery', lv, '| appearances', des.appearances.count)
