# Four-legged mobile base — concept and feasibility

**Status: early layout only. Do not print the layout or order its actuators as a completed design.** The Fusion model in `outputs/quadruped-layout-concept-not-printable.f3d` consists of rectangular space-claim components, not functioning leg parts. It has no motor pockets, bearings, fasteners, feet, real chassis, arm adapter, Fusion joints, electronics, control code, or gait. There has been no load analysis, slicing, physical build, or walking test.

## Purpose and approach

Carry the SO-101 follower on a four-legged base. First establish stable, slow indoor walking with the arm folded and secured; treat stationary manipulation as a later, separately tested mode. A trained or programmed gait and a controller are required in addition to legs. The arm reference is a desktop design, so its desk clamp cannot simply be used as a mobile mount.

The preferred development path is to adapt a documented open quadruped rather than invent a motor and bearing interface from dimensions alone. The layout explores the proportions of [SpotMicroESP32](https://github.com/michaelkubina/SpotMicroESP32), a 12-servo, four-legged printed robot. The author explicitly labels it work in progress, describes limitations in the electronics and software, and says its basic MG996R servos are weak for walking. The upstream repository points to community gait implementations; neither those nor the original mechanics have been tested with our arm. Its GPL-3.0 license applies to its materials. [Stanford Pupper v3](https://github.com/HandsOnRobotics/pupper-v3-documentation) is another documented quadruped using more capable actuators, at higher complexity and cost; it too has no verified payload rating for this combination here.

## What the Fusion layout contains

- Body envelope: 207.5 × 78 × 30 mm; 30 mm thickness is a visualization assumption, not the reference chassis design.
- Four shoulder envelopes and eight simple upper/lower link envelopes, with joint-center lengths of 111.1 mm and 118.5 mm. The 207.5 mm longitudinal spacing, 78 mm body width, 60.5 mm lateral offset and link lengths come from the [SpotMicroESP32 kinematics notes](https://github.com/michaelkubina/SpotMicroESP32/tree/master/kinematics). The chosen pose and rectangular cross sections are approximations.
- A 150 × 110 × 6 mm top plate envelope is an arbitrary space claim, not an SO-101-compatible mounting interface. The arm itself is not included.
- These solids intersect at idealized joint centers and have no moving joints. They are intentionally unsuitable for fabrication and do not represent the real referenced chassis or hardware.

## Why actuator choice remains open

A real SO-101 follower adds substantial mass and a high, moving center of gravity. A Hiwonder SO-101 variant is listed at about 704 g, but that is not a measurement of our particular printed arm and servo kit. Battery, camera, mount, wiring and computer add more weight. In addition, static stability and joint loading change as the arm reaches outward. Neither candidate's ability to carry this arm has been established.

For scale only: if a hypothetical 4 kg total robot shares its weight equally across three stance legs, the average vertical foot force is about 13.1 N per leg. At an illustrative 40 mm perpendicular joint lever arm, that one force contributes about 0.52 N·m at that joint. Real stance forces are unequal, joint leverage changes with pose, and acceleration, impacts, link weight, efficiency and thermal duty increase requirements. This is not a motor specification or proof of feasibility. Establish the full mass/center-of-mass budget and worst-case joint torques before selecting motors or the battery and regulator.

## Development gates

1. **Measure the real arm** with all motors, fasteners, controller, wiring and camera. Determine its folded envelope, center of mass, and desired stationary work poses. Decide on mass limits and stowage.
2. **Choose and verify the quadruped platform and actuators:** obtain physical motor dimensions and continuous torque/thermal/current data, not just stall ratings. Model three-leg stance, uneven load distribution, reaching moments, and dynamic margins; verify a power budget.
3. **Bring real CAD into Fusion:** use the chosen quadruped's complete source model and confirmed hardware, create proper joints and joint limits, build a mechanically attached arm adapter on structural members, and check the arm/leg/camera/battery clearances throughout motion. The current layout is not this step.
4. **Design power and controls:** matched supply rails for the arm and legs, correctly rated wiring/connectors and protective devices, battery protection and a physical motor-power disconnect. Develop a watchdog and a tested safe response to communication loss or fall; power removal can cause the robot and payload to collapse.
5. **Fabricate and inspect:** print motor fit coupons and a single leg first; verify servo fit, bearings, horn interfaces, fasteners and printed strength. Slice all parts for the actual Bambu model and material. Verify assembly and safe working load before committing to all four legs.
6. **Bring up incrementally:** secure the robot on a support stand for individual joint tests and calibrated limits; verify a static stand and controlled weight transfer on the floor with an accessible disconnect. Only then test slow tethered walking in a clear area. Add a representative inert mass before trying the arm, then the secured arm, checking temperature and balance each time. Do not run a gait or manipulate objects near people, pets, stairs, or desk edges during early tests.

## References

- [SpotMicroESP32 project, BOM and caveats](https://github.com/michaelkubina/SpotMicroESP32)
- [SpotMicroESP32 kinematics dimensions](https://github.com/michaelkubina/SpotMicroESP32/tree/master/kinematics)
- [Stanford Pupper v3 project documentation](https://github.com/HandsOnRobotics/pupper-v3-documentation)
- [Hiwonder SO-101 product specifications](https://www.hiwonder.com/products/lerobot-so-101?variant=42198960210007) — comparative mass only, not a specification for this build.
