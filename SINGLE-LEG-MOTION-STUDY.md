# Single-leg Fusion linkage study

**Prototype only; not a walking simulation or a print-ready assembly.** This isolated leg is derived from `reference/quadruped-v2/leg_v2.step`, by Miguel Ayuso Parrilla. The reference contains overlapping mirrored alternatives; see [placement provenance](QUADRUPED-PLACEMENT-STUDY.md) for the source and license.

[Open the revised motor-shaft prototype in Fusion](outputs/single-leg-motor-shafts-PROTOTYPE.f3d). A small grounded fixture named `Diagnostic datum` is a CAD test datum, not a physical part. The model also retains hidden source geometry, including a hidden alternative fork and hidden original shaft bodies, and an unconnected servo occurrence. Hidden parts still exist in the file. It is not a bill of materials or an assembly to manufacture.

## What was built and tested

A prior import with hierarchical coxa geometry would not drive its yaw joint, even when the other joints were suppressed. A healthy timeline indicator did not establish that the joint could move. Copying the visible source bodies into a flat, rigid coxa component allowed the diagnostic yaw pivot to drive. The femur and tibia were also flattened into separate rigid components, omitting identified mirrored alternatives. This is a workaround for this particular imported model, not a diagnosis of Fusion's underlying solver behavior.

Six as-built revolute joints connect the datum, coxa, femur, tibia, knee crank and connecting rod. The knee crank and rod were separated from their source bodies, and the rod was connected at both ends to form a planar closed linkage. The axes were inferred from the modeled cylindrical features. In the reference coordinate system, the hip and knee flex axes are parallel to X at approximately Y = 0 and −100 mm, Z = 43.55 mm; the interpreted yaw axis is parallel to Z at X = Y = 0. The crank pivot is at Y = −39.5 mm, Z = 43.55 mm, and its rod pin is at Y = −39.5 mm, Z = 67.55 mm. The distal rod pin is at Y = −100 mm, Z = 67.55 mm. These are CAD interpretations that need checking against the physical parts.

In Fusion, individual drives from the source pose gave:

- Yaw at +8° and −8° moved the coxa, femur, tibia, crank and rod together.
- Hip flex at +8° and −8° moved the femur and its downstream components while leaving the coxa fixed.
- Crank commands of +10°, −10°, +20° and −20° moved the tibia, crank and rod. The knee joint reported the opposite angle modulo 360°; for example, a +20° crank drive produced a 340° knee reading. This is the sign convention of these joint definitions, not a validated motor command.
- Each test was reset to zero. The timeline reported no unhealthy elements. After export and reopening, all six joints were present; yaw +8°, hip +8° and crank +10° were repeated successfully and reset.

These checks establish limited geometric solver behavior in an isolated pose. They do **not** validate servo limits, real-world horn indexing, forces, the body connection, control signals, or the full robot. The actual rod ends may permit movement that the simplified planar pivots do not represent. No load simulation or complete range sweep has been performed.

## Interference checks and fork selection

The isolated reference contains both `front fork` and `back fork` at the same position. Fusion calculated a 241.235 mm³ intersection between those two bodies. Inspection of the full quadruped reference showed that each leg has only one fork; the full model includes a back fork paired with the same unmirrored femur variant selected for this diagnostic leg. The revised prototype hides the front fork while retaining it in the file. This is an interpretation of the imported reference, not a verified manufacturing configuration.

Before selecting a fork, cross-component interference was sampled at the reference pose, hip ±10° and ±20°, and knee crank ±10° and ±20°. The complete results are in [single-leg-interference-samples.json](outputs/single-leg-interference-samples.json). Four overlaps appeared in the reference pose; several occur at modeled shaft or fastener interfaces but have not been resolved or confirmed intentional. The hip positions introduced additional intersections involving the forks and femur bodies.

With the front fork hidden, a focused check tested the back fork against the visible flattened femur bodies at 5° increments from −45° to +45°, returning to the source pose between samples. It found intersections at every sampled angle from −45° through −15°; at −15° the reported intersection was 0.0258 mm³, while at −20° four body pairs intersected. No solid intersections were reported for these particular body pairs at the sampled angles from −10° through +45°. See [the extended results](outputs/back-fork-hip-clearance-extended.json) and [the initial focused scan](outputs/back-fork-hip-clearance-samples.json). The revised F3D was reopened with all six joints and the fork visibility intact; a +10° crank drive still moved the knee.

The checks used Fusion solid-interference analysis with coincident faces excluded and bounding boxes to select candidate pairs. The focused check covers only the back fork and femur, and all checks are discrete positions, not a continuous sweep. They do not establish usable clearance, minimum gap, a safe joint limit, or clearance to omitted parts, wiring and the chassis. Investigate the remaining overlaps and verify actual hardware before using the leg.

## Servo output shafts

The first flattened model placed each servo output shaft in the same rigid component as its stationary housing. To represent the moving outputs more accurately, the revised prototype copies the modeled hip shaft into the femur component and the modeled knee shaft into the crank component, then hides the original shaft bodies. The hidden originals remain in the model; this is not a cleaned-up production assembly. Shaft and horn geometry, spline engagement, and real servo behavior still require confirmation.

After the change, a cross-component interference check at the source pose found two intersections: the modeled femur nut with the tibia (2.8265 mm³) and the modeled knee servo housing with the crank horn (20.2371 mm³). Their significance is unresolved. The two previously reported shaft-to-horn intersections are now inside their respective rigid moving components and were not included in this cross-component check; their disappearance from the report does not prove physical fit. At hip −20°, the four back-fork-to-femur intersections remained; at +20°, only the two reference-pose intersections were reported in this limited selection. Results are in [motor-shafts-interference-samples.json](outputs/motor-shafts-interference-samples.json).

The revised archive was reopened: six joints were present, the original shaft bodies were hidden, the copied shafts were visible, and a −10° crank test produced a +10° knee reading. Fusion reported no unhealthy timeline elements. This is not a whole-assembly or physical clearance verification.

[The earlier hierarchical joint study](outputs/single-leg-joint-study-INCOMPLETE.f3d) is retained for comparison: its yaw did not drive, and its rod was not constrained. [The intermediate flattened-pivot study](outputs/single-leg-flat-joints-PROTOTYPE.f3d) predates the closed linkage; [the first linkage study](outputs/single-leg-linkage-PROTOTYPE.f3d) still displays both fork alternatives. [The back-fork study](outputs/single-leg-back-fork-PROTOTYPE.f3d) predates the shaft correction.

## Remaining work

- Verify handed parts, shaft and horn mounting, actual fasteners and pivot locations against the purchased hardware. Replace the diagnostic datum with a real chassis interface and account for the unconnected source servo.
- Establish measured joint limits and motor directions, evaluate interference throughout useful motion, and validate the linkage and printed joints with physical fit and supported tests.
- Replicate validated mechanisms to all four legs, connect the arm through a real load-carrying mount, add arm joints and limits, and test whole-robot clearances and motion.
- Complete the load, stability, electrical, firmware, slicing and physical commissioning work described in [BUILD-READINESS.md](BUILD-READINESS.md). The isolated CAD motion is not evidence of strength, safe power, stable walking, or AI manipulation.
