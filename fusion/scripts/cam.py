# Ad-hoc camera for checks: _context = "ex,ey,ez,tx,ty,tz[,angle]" (cm, perspective).
import adsk.core, adsk.fusion
DOC = 'Alexandria Heritage Tram 601'
def run(_context: str):
    app = adsk.core.Application.get()
    d = [x for x in app.documents if x.name == DOC or x.name.startswith(DOC + ' v')][0]; d.activate()
    v = [float(s) for s in _context.split(',')]
    vp = app.activeViewport; cam = vp.camera; P = adsk.core.Point3D.create
    cam.isFitView = False; cam.cameraType = adsk.core.CameraTypes.PerspectiveCameraType
    cam.eye = P(*v[0:3]); cam.target = P(*v[3:6]); cam.upVector = adsk.core.Vector3D.create(0, 1, 0)
    cam.perspectiveAngle = v[6] if len(v) > 6 else 0.6
    vp.camera = cam; vp.refresh()
