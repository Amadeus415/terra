# Quadruped + SO-101: build readiness

**Not ready to order, print as a complete robot, or power on.** This is an engineering assessment of the imported references, not a claim that the physical robot has been built. The existing Fusion assembly is a static placement study and lacks a structural connection, joints, motion limits, complete electrical design and a validated gait for the added arm. Use [QUADRUPED-PLACEMENT-STUDY.md](QUADRUPED-PLACEMENT-STUDY.md) for the actual model and source provenance.

A separate [single-leg linkage study](SINGLE-LEG-MOTION-STUDY.md) now has diagnostic joints and sampled interference results. It is not integrated into the full assembly. The focused hip study found intersections in some sampled positions, and other modeled overlaps remain unresolved.

An [arm-mount study](ARM-MOUNT-STUDY.md) explores a plate and four side supports around existing chassis holes, checks simplified bolt envelopes, and provides a gravity-only estimate based on upstream SO-101 simulation inertias. Side-bolt overlaps and the arm attachment remain unresolved; neither the concept nor the estimates establish a structural load path or demonstrate that the chassis can carry the arm.

A separate [Fusion support study](SUPPORT-SIMULATION.md) was solved using a placeholder material and illustrative load. It does not represent the complete mount or establish printed-part strength.

## Mechanical and stability findings

The quadruped has four 3-actuator legs. The arm's modeled base floats about 4.48 mm above the nearest measured body in this particular CAD pose. No suitable load-carrying bracket or positive stow restraint has been modeled. The arm's mass and its center of mass in the actual stowed position are unknown. It is not established that the chosen quadruped or its actuators can carry the arm.

In the reference pose, the approximate X–Z centers of the modeled TPU foot bounding boxes (mm) are `(−89, −91.25)`, `(89, −91.25)`, `(−89, 102.35)` and `(89, 102.35)`. These are **bounding-box centers**, not measured contact patches. Their centroid is `(0, 5.55)` mm. A three-foot support triangle has that centroid on its diagonal edge: a robot whose projected combined center of mass happened to be there would have essentially zero idealized static margin when any one foot is lifted. That is not a measurement of the actual robot's mass distribution; it illustrates why a walking controller must plan weight shifts and why placing an arm high on the chassis matters.

For a reproducible static geometry check only, run `python3 tools/support_margin.py X_MM Z_MM` with measured, combined center-of-mass coordinates in the Fusion reference coordinate frame. It calculates signed distances from that point to four-foot and three-foot support polygon edges. Positive is inside, negative is outside. It assumes fixed, coplanar point contacts and vertical gravity; it cannot assess gait dynamics, tip recovery, traction, joint limits, or motor loads. Use it for analysis, never to authorize operation. Its geometric calculations were checked for central, boundary, outside and collinear cases; the robot itself was not tested.

## Actuators and power are not yet specified

The V2 STEP assembly names twelve leg servos as DS3225MG. The [manufacturer's DS3225 datasheet](https://www.dsservo.com/d_file/DS3225%20datasheet.pdf) lists 4.8–6.8 V operating range and 2.3 A stall current at 6.8 V for the documented variant. Twelve times that figure is **27.6 A**, an illustrative simultaneous-stall sum for those leg motors alone. This is neither a normal operating current nor a selected fuse, battery or regulator rating. Other DS3225 variants/listings have different current and torque figures; confirm the exact SKU, travel, measured current and mechanical horn before selecting it. Stall torque is not a continuous-duty rating, and the source has not been validated with the arm attached.

The SO-101 follower uses a separate serial-bus controller and requires a supply matched to its actual servo variant: the upstream guide uses a 5 V supply for the 7.4 V option, or a 12 V supply for its 12 V follower option. Do not connect those motors to a mismatched leg rail. The onboard computer also needs an appropriately specified supply. A real power design must account for regulator input range, surge and sustained loads, wiring, connectors, overcurrent protection, battery protection, grounding and shutdown behavior. No schematic, component values or wiring ratings have been verified for this combined robot.

## Original walking firmware audit

The creator's [Arduino source at revision d6291b5](https://github.com/miguelasd688/4-legged-robot-model/blob/d6291b50db6d05c437b78ec836df243db6f21e8b/arduino-code/arduino_com.ino) is a reference, not approved firmware for this project. In the inspected `loop()`, `moveServos` is invoked each cycle whether or not a new complete command arrived. In `recvWithStartEndMarkers()`, parsed values are assigned to individual `pulseN` variables as fields arrive; the displayed code does not implement a complete-frame atomic commit or a command-age timeout. The servo array is attached during startup and commands are written from initially zero-valued globals before a validated frame is required. Do not assume safe startup, calibrated joint limits or a safe communication-loss response.

Before hardware operation, design and verify a controller that (1) validates complete commands and calibrated per-joint limits, (2) starts in a deliberately disarmed state, (3) handles loss of host/controller communications with a **tested** response, and (4) has an independent physical way to remove motor power. Detaching PWM or removing torque may cause the arm and robot to collapse, so the actual safe response needs supported testing; holding the last position is not inherently safe either. The arm controller, leg controller, stow interlock and battery protection must be considered together. No replacement firmware has been implemented or tested here.

## Required completion evidence

1. Confirm exact leg hardware, available continuous actuator data, printed material and printer. Measure the completed arm with electronics and cables, and measure the combined center of mass for stowed and manipulation positions.
2. Design the mount against actual load-bearing chassis interfaces, fasteners and measured arm base; verify fastener access, fit, strength, clearances and a stow restraint. Model actual hardware, then create and validate leg and arm joints with real limits in Fusion.
3. Model conservative three-leg stance and manipulator-reach loads, choose actuators and a matched power architecture, and verify thermal and electrical margins. Complete a schematic and component-specific BOM; reconcile source CAD and purchased servo geometry.
4. Build and test controller behavior including startup, joint limits, malformed input, connection loss, stop behavior and arm/leg coordination before applying motor power to an assembled robot.
5. Slice fit coupons and a first leg for the actual printer and filament. Inspect physical fits, layer strength and hardware. Only then slice the remaining parts and assemble with the upstream instructions.
6. Commission on a support stand: individual actuators, calibration, movement bounds, harnesses and current/temperature. Progress to unloaded static support and controlled weight shifts, then restrained low-speed walking with an inert payload, then the physically secured arm. Keep people, pets, stairs, and edges clear. Do not manipulate objects while walking until the combined system has passed its own validation.

No purchases, physical printing, assembly, powered tests, code deployment or gait trials have been performed.
