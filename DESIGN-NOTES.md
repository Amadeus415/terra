# Desktop robot arm — working notes

Status: preliminary reference selection. No custom design, Fusion verification, slicing, hardware fit, or physical testing has been completed.

## Intended use
One desk-edge mounted robot for experiments in camera-guided manipulation of small desktop objects. Start with a fixed overhead USB webcam so its mass does not load the arm. The user's computer supplies control and runs AI software; a servo bus adapter and a matching external supply power the arm. Natural-language instruction alone does not provide a trained manipulation policy: calibration, data collection or a compatible policy, and supervised testing remain necessary.

## Reference baseline
The Robot Studio / Hugging Face SO-101 follower, upstream commit `a758567c3978dfeefe282ede0500085a48fe8f78`, retrieved 2026-10-26, in `reference/SO-ARM100`. Upstream license is in that folder. The assembly STEP is `reference/SO-ARM100/STEP/SO101/SO101 Assembly.step`; the follower print layout is `reference/SO-ARM100/STL/SO101/Follower/Ender_Follower_SO101.stl`. These are unmodified upstream references, not a completed custom design. The upstream assembly may include leader parts and hardware; verify its contents and joints in Fusion.

## Preliminary hardware direction
- Six STS3215 C001 1/345 servos for one follower, with matching horns, screws and bus cables. Verify kit contents before ordering.
- One compatible Waveshare serial bus servo controller, USB data cable, and supply matched to the chosen servo version. Upstream specifies 5 V for its 7.4 V follower option, or 12 V 5 A or greater for its 12 V option; do not mix voltages.
- Two suitably sized desk clamps with protective pads, per upstream approach. Actual desk thickness and clearance must be measured before choosing clamps; stability must be tested.
- A USB webcam and a fixed overhead mount. Upstream supplies a [webcam mount](https://github.com/TheRobotStudio/SO-ARM100/tree/main/Optional/Overhead_Cam_Mount_Webcam) designed around a specified camera; verify exact product fit and field of view before purchasing or printing.
- Optional second wrist camera after basic operation is established; its mass, cable forces, clearance and mount fit need validation.

## Print and validation gates
Upstream recommends PLA+, 0.4 mm nozzle, 0.2 mm layers and 15% infill as its baseline, with supports and no supports in horizontal screw holes. Print a servo fit gauge first and verify the exact printer, material, bed and orientation in Bambu Studio. Do not treat those settings as proof of strength. Inspect and test all joints, mount, wiring and clearances before powered operation; start at low speed with a clear workspace. Do not infer a safe payload from servo stall torque. Establish usable payload and reach through calculations and controlled tests.

## Work remaining
Sign in to Fusion; inspect the upstream assembly, components, joints and interference; define and model any needed desk and camera adaptations; produce and inspect exports and print layouts; verify hardware sizing, supplies, quantities, fit and sourcing; document assembly, calibration and staged tests. No order or physical print has been placed.

## Fusion and print-file inspection — 2026-10-26
The upstream STEP was imported into Fusion and exported as `outputs/SO101-reference-static.f3d`. Reimporting that archive returned 97 top-level occurrences, 375 nested occurrences, and zero joints. It is a static imported reference, not an articulated assembly or a redesigned arm. Fusion reports the reference base's bounding envelope as approximately 111 × 87 × 72 mm. That bounding box alone does not define usable clamp contact surfaces.

The upstream Ender follower layout has a mesh bounding box of approximately 216.35 × 215.28 × 87 mm, calculated from its STL vertices. This fits nominally inside a 220 × 220 mm bed, but a real slicer must account for margins, brim, supports, collision settings, and the exact Bambu model. It has not been sliced. The overhead-camera STL files are not in their final print orientation; their largest bounding dimensions are approximately 242.45 mm (top), 230.95 mm (bottom), and 159.04 mm (arm base). Bed fit and orientation must be checked in a slicer. Do not assume all Bambu Carbon printers have the same usable bed or nozzle setup.

The manufacturer-designed webcam mount specifies a particular camera linked from its README. A Logitech C270 is an inexpensive alternative with 720p/30 video, but its physical compatibility with that printed mount has not been established. A camera bracket should be designed only against a verified camera's dimensions or the specified model, then fit-tested.

Upstream's follower BOM lists six 7.4 V C001 1/345 servos, a Waveshare adapter, 5 V supply, USB cable, and two clamps. The BOM lists approximately $121.94 for the arm's nonprinted components, but this is upstream's illustrative sum, not a live quote, and excludes camera, filament, shipping and tax. Confirm that the motor kit includes the required horns, mounting and horn screws, connectors and cables before purchasing; the STEP's modeled fasteners are not a verified shopping list. The upstream assembly guide specifies M2×6 motor mounting and M3×6 horn/arm connections, but exact quantities remain to be reconciled with the selected kit.

For practical demonstrations, a leader arm is a useful optional addition, but a single follower and another supported control method can start the experiment. LeRobot's typical sequence is teleoperate, record demonstrations, train or adapt a policy, and evaluate it. General language commands do not guarantee a working policy for arbitrary desk objects. Dataset camera placement and robot configuration need to match the selected policy.

Remaining before describing this as a complete design: produce and verify actual Fusion joints and motion limits; inspect real clearances through motion; verify a desk clamp against measured desk and real clamp geometry; specify and fit-check the camera and its mount; reconcile a complete orderable BOM; slice and inspect each plate; verify power, wiring and motor configuration; and physically test printed parts, payload and the assembled arm. None of those checks has been completed.
