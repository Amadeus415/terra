"""Build a NON-STRUCTURAL Fusion fit study from the saved placement reference.

Run with Fusion's Python API. Dimensions are provisional; this is not a print file.
"""
import adsk.core
import adsk.fusion


def run(_context: str):
    app = adsk.core.Application.get()
    base_path = '/Users/colenba/Documents/ChatGPT/robotics_terra/outputs/quadruped-so101-placement-study.f3d'
    app.importManager.importToNewDocument(app.importManager.createFusionArchiveImportOptions(base_path))
    d = adsk.fusion.Design.cast(app.activeProduct)
    root = d.rootComponent
    arm = next(o for o in root.occurrences if o.name.startswith('SO101 - placement'))
    m = adsk.core.Matrix3D.create()
    m.setWithArray([1, 0, 0, 0, 0, 0, 1, 8, 0, -1, 0, 0, 0, 0, 0, 1])
    arm.transform2 = m
    if d.snapshots.hasPendingSnapshot:
        d.snapshots.add()

    plate_occ = root.occurrences.addNewComponent(adsk.core.Matrix3D.create())
    plate = plate_occ.component
    plate.name = 'CONCEPT arm plate 120x100 - NOT VALIDATED'
    pi = plate.constructionPlanes.createInput()
    pi.setByOffset(plate.xZConstructionPlane, adsk.core.ValueInput.createByReal(8.0384))
    plane = plate.constructionPlanes.add(pi)
    sketch = plate.sketches.add(plane)
    sketch.name = 'Plate interface layout - candidates only'

    def plate_point(x, z):
        return sketch.modelToSketchSpace(adsk.core.Point3D.create(x/10, 8.0384, z/10))

    sketch.sketchCurves.sketchLines.addTwoPointRectangle(plate_point(-60, -60), plate_point(60, 40))
    for x, z in [(-31.75, -45.42), (31.75, -45.42), (-27.78, 24.35), (27.78, 24.35)]:
        sketch.sketchCurves.sketchCircles.addByCenterRadius(plate_point(x, z), 0.26)
    for side in [-1, 1]:
        for z in [-34, 24]:
            sketch.sketchCurves.sketchCircles.addByCenterRadius(plate_point(side*51.5, z), 0.17)
    profile = max((sketch.profiles.item(i) for i in range(sketch.profiles.count)), key=lambda p: p.areaProperties().area)
    ext = plate.features.extrudeFeatures
    i = ext.createInput(profile, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    i.setDistanceExtent(False, adsk.core.ValueInput.createByReal(-0.4))
    ext.add(i)
    print(plate.name, 'volume mm3', round(plate_occ.bRepBodies.item(0).volume*1000, 3))

    for side in [-1, 1]:
        for number, side_z, top_z, width in [(1, -24.65, -34, 28), (2, 24, 24, 12)]:
            occurrence = root.occurrences.addNewComponent(adsk.core.Matrix3D.create())
            c = occurrence.component
            c.name = 'CONCEPT thick drilled support %s %s - NOT VALIDATED' % ('L' if side < 0 else 'R', number)
            start_z = side_z - width/2
            pi = c.constructionPlanes.createInput()
            pi.setByOffset(c.xYConstructionPlane, adsk.core.ValueInput.createByReal(start_z/10))
            sketch = c.sketches.add(c.constructionPlanes.add(pi))
            sketch.name = 'L-shaped support section'
            points = [(36, 72.384), (56.5, 72.384), (56.5, 10.5), (64.5, 10.5), (64.5, 76.384), (36, 76.384)]
            for n, (x, y) in enumerate(points):
                xx, yy = points[(n+1) % len(points)]
                p = sketch.modelToSketchSpace(adsk.core.Point3D.create(side*x/10, y/10, start_z/10))
                q = sketch.modelToSketchSpace(adsk.core.Point3D.create(side*xx/10, yy/10, start_z/10))
                sketch.sketchCurves.sketchLines.addByTwoPoints(p, q)
            ex = c.features.extrudeFeatures
            i = ex.createInput(sketch.profiles.item(0), adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
            i.setDistanceExtent(False, adsk.core.ValueInput.createByReal(width/10))
            ex.add(i)

            pi = c.constructionPlanes.createInput()
            pi.setByOffset(c.yZConstructionPlane, adsk.core.ValueInput.createByReal(side*5.65))
            sk = c.sketches.add(c.constructionPlanes.add(pi))
            sk.name = 'Side clearance hole 3.4mm'
            center = sk.modelToSketchSpace(adsk.core.Point3D.create(side*5.65, 1.45, side_z/10))
            sk.sketchCurves.sketchCircles.addByCenterRadius(center, 0.17)
            i = ex.createInput(sk.profiles.item(0), adsk.fusion.FeatureOperations.CutFeatureOperation)
            i.setDistanceExtent(False, adsk.core.ValueInput.createByReal(side*0.8))
            ex.add(i)

            pi = c.constructionPlanes.createInput()
            pi.setByOffset(c.xZConstructionPlane, adsk.core.ValueInput.createByReal(7.2384))
            sk = c.sketches.add(c.constructionPlanes.add(pi))
            sk.name = 'Top clearance hole 3.4mm'
            center = sk.modelToSketchSpace(adsk.core.Point3D.create(side*5.15, 7.2384, top_z/10))
            sk.sketchCurves.sketchCircles.addByCenterRadius(center, 0.17)
            i = ex.createInput(sk.profiles.item(0), adsk.fusion.FeatureOperations.CutFeatureOperation)
            i.setDistanceExtent(False, adsk.core.ValueInput.createByReal(0.4))
            ex.add(i)
            print(c.name, 'volume mm3', round(occurrence.bRepBodies.item(0).volume*1000, 3))

    print('Arm transform', arm.transform2.asArray())
    print('Timeline errors', [(e.index, e.name, e.healthState) for e in d.timeline if e.healthState not in [adsk.fusion.FeatureHealthStates.HealthyFeatureHealthState, adsk.fusion.FeatureHealthStates.UnknownFeatureHealthState]])
    output = '/Users/colenba/Documents/ChatGPT/robotics_terra/outputs/quadruped-raised-support-v5-thick-CONCEPT.f3d'
    print('Exported', d.exportManager.execute(d.exportManager.createFusionArchiveExportOptions(output)), output)
