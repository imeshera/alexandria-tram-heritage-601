# Activates the 601 document and sets a camera. _context: iso | isoL | isoB | left | right | front | rear | top |
# interior | platform | roof | bogie | front34 | end_b | fit. Model units cm; car centre x = car_len / 2.
import adsk.core, adsk.fusion
DOC = 'Alexandria Heritage Tram 601'
def run(_context: str):
    app = adsk.core.Application.get()
    d = [x for x in app.documents if x.name == DOC or x.name.startswith(DOC + ' v')][0]; d.activate()
    vp = app.activeViewport; cam = vp.camera
    P, V = adsk.core.Point3D.create, adsk.core.Vector3D.create
    mode = (_context or 'iso').strip()
    cx = 662.0; tgt = P(cx, 190, 0)
    eyes = {'iso': P(-700, 700, 1400), 'isoL': P(-700, 700, -1400), 'isoB': P(2000, 650, 1300),
            'left': P(cx, 190, 5000), 'right': P(cx, 190, -5000), 'front': P(-5000, 190, 0), 'rear': P(6500, 190, 0),
            'top': P(cx, 5000, 1), 'low': P(-300, 60, 900)}
    special = {'interior': (P(1120, 235, -25), P(300, 200, 5), 1.0),         # standing in the saloon aisle near end B, looking to A
               'platform': (P(118, 245, -55), P(0, 170, 40), 1.1),          # on platform A looking at the controller / front
               'bogie': (P(330, 80, 380), P(264, 45, 0), 0.75),
               'roof': (P(-150, 720, 650), P(380, 390, 0), 0.7),
               'front34': (P(-800, 160, 260), P(60, 200, 0), 0.5),        # 2012 Commons-like front three-quarter
               'end_b': (P(2100, 230, -250), P(1260, 220, 0), 0.5)}
    if mode in special:
        e, t_, ang = special[mode]
        # gotcha: going from an orthographic preset straight to an interior eye renders blank; apply twice
        for _ in range(2):
            cam = vp.camera
            cam.isFitView = False; cam.cameraType = adsk.core.CameraTypes.PerspectiveCameraType
            cam.eye = e; cam.target = t_; cam.upVector = V(0, 1, 0); cam.perspectiveAngle = ang
            vp.camera = cam; vp.refresh()
        print('view', mode); return
    if mode in eyes:
        cam.isFitView = False
        cam.target = tgt; cam.eye = eyes[mode]; cam.upVector = V(0, 1, 0)
        cam.cameraType = adsk.core.CameraTypes.PerspectiveCameraType if mode.startswith('iso') or mode == 'low' else adsk.core.CameraTypes.OrthographicCameraType
        cam.perspectiveAngle = 0.4
        vp.camera = cam
    vp.fit()
    print('view', mode)
