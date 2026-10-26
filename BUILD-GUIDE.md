# Build your desk-mounted SO-101 robot arm

A practical guide for printing one SO-101 **follower** arm, attaching it to a desk, and connecting it to a Mac. The follower is the powered arm that moves objects. A separate leader arm is optional and is useful for recording demonstrations for AI training.

**Project status:** This guide builds the published SO-101 design from The Robot Studio and Hugging Face. The files have not been sliced or physically tested on your printer, and the Fusion assembly is an imported static reference with no joints. Your actual desk, clamps, camera, servos, and print settings still need fit checks. Nothing has been purchased or printed yet.

## The big picture

1. Buy the follower hardware and choose a camera.
2. Print a small fit gauge, then the arm parts.
3. Give each motor its own ID, assemble the arm, and clamp it to the desk.
4. Connect power and USB, calibrate the joints, and test the gripper.
5. Add an overhead camera. For AI tasks, collect demonstrations and train or adapt a compatible policy.

## 1. Parts and tools

The easiest way to avoid incompatible fasteners is an **SO-101 follower motor/electronics kit without printed parts**, whose listing explicitly includes the items below. The [upstream parts list and kit vendors](https://github.com/TheRobotStudio/SO-ARM100#sourcing-parts) is the source of truth for supported hardware. Confirm the contents with the seller; some listings contain a leader-and-follower pair or printed parts as well.

| Item | Quantity | What to check |
|---|---:|---|
| Feetech STS3215 follower servos | 6 | All six should be the same follower type: **1/345 (C001)**. Choose one voltage version and match its power supply. They need the appropriate drive and passive horns, horn screws, mounting screws, and three-pin bus cables. |
| Compatible serial bus servo adapter | 1 | The upstream BOM uses a Waveshare bus-servo adapter. Confirm it supports these Feetech servos and has a USB data connection. [Example from upstream BOM](https://www.amazon.com/dp/B0CTMM4LWK/). |
| Power supply | 1 | Upstream uses **5 V for its 7.4 V motors**; its 12 V follower option uses **12 V, at least 5 A**. Match the exact adapter input, barrel size/polarity, and seller's motor/board specifications. USB alone does not power the servos. A leader's 7.4 V motors must not be connected to a 12 V supply. |
| USB data cable | 1 | Match the controller and Mac ports; use a data-capable cable, not charging-only. An adapter may be needed. |
| Desk clamps | 2 | Choose clamps with enough opening for your measured desk thickness and enough reach to engage the base's clamp tabs. Add protective pads. The [upstream BOM example](https://www.amazon.com/dp/B092L925J4/) is a starting point, not proof of fit for your desk. |
| PLA+ filament | As needed | Upstream's recommended starting material. Confirm the printer and work's approved material profile. |
| USB webcam | 1 | A fixed overhead view is a good first camera. The [upstream overhead mount](reference/SO-ARM100/Optional/Overhead_Cam_Mount_Webcam/README.md) is designed around a [specific webcam](https://www.amazon.com/dp/B082X91MPP); verify the exact listing and physical fit. A different webcam may need a separate mount. |
| Tools | 1 set | #0 and #1 Phillips screwdrivers, flush cutters, support-removal tools, ruler or calipers, and eye protection. |

The assembly uses M2×6 and M3×6 fasteners in specific positions. The exact loose screw and cable quantities have **not** been reconciled against a particular kit. Check the kit packing list against the [illustrated assembly instructions](https://huggingface.co/docs/lerobot/main/so101) before ordering; do not use the fasteners modeled in the Fusion reference as a purchasing count. The upstream BOM lists about $122 for follower components as an illustrative figure, excluding the camera, printing, shipping, and tax; it is not a current quote.

**Optional leader arm:** A second, manually moved arm makes demonstration recording easier. It needs its own controller, supply, printed leader parts, and mixed-ratio 7.4 V motors. Buy a kit explicitly for an SO-101 leader rather than six follower motors. It is not needed for the first follower-only test below.

## 2. Choose the files

- **Follower print layout:** [Ender_Follower_SO101.stl](reference/SO-ARM100/STL/SO101/Follower/Ender_Follower_SO101.stl). This is the upstream combined plate, not an articulated model.
- **Fit gauge:** [Gauge_0.STL](reference/SO-ARM100/STL/Gauges/Gauge_0.STL) and, if useful, [Gauge_tight_1.STL](reference/SO-ARM100/STL/Gauges/Gauge_tight_1.STL).
- **Individual replacements:** [SO-101 individual STL parts](reference/SO-ARM100/STL/SO101/Individual/). Use the upstream README's follower/common list to identify the required parts; do not print leader-only parts.
- **Fusion reference:** [SO101-reference-static.f3d](outputs/SO101-reference-static.f3d). Use it to inspect component relationships; use the STL files for slicing. It does not simulate movement.
- **Optional webcam mount:** [mount instructions and STL folder](reference/SO-ARM100/Optional/Overhead_Cam_Mount_Webcam/README.md). Its parts are separate and require their own orientation and fit checks.

The reference files are from upstream SO-ARM100 commit `a758567c3978dfeefe282ede0500085a48fe8f78`; the repository includes its license and attribution.

## 3. Print the fit gauge first

1. Confirm the exact Bambu printer, build plate, nozzle and filament with the workplace printer operator. Clean and prepare the plate according to the printer's instructions.
2. In Bambu Studio select that printer, plate, filament profile, and nozzle. Import `Gauge_0.STL` at its original scale; the files are in millimeters.
3. Upstream's baseline is PLA+, a **0.4 mm nozzle, 0.2 mm layer height, and 15% infill**. Use the approved filament temperatures and plate settings in the printer's profile. Slice and inspect the preview before printing.
4. Once cool, remove the gauge and try your actual STS3215 servo in it. It should seat without excessive force or obvious slop. If it does not, consult the [upstream gauge instructions](https://github.com/TheRobotStudio/SO-ARM100#printing-the-parts), adjust the printer profile or print the alternate gauge, and repeat. Do not scale the whole arm to compensate for one bad fit.

## 4. Slice and print the follower

1. Import `Ender_Follower_SO101.stl` into a new Bambu Studio project. It is already arranged by upstream as a combined follower plate. Keep its scale at 100% and preserve the supplied orientation.
2. The mesh's measured bounding box is approximately **216.4 × 215.3 × 87 mm**. That is a geometry measurement, not a successful Bambu slice. Check that the exact printer's usable area, bed exclusions, brim and supports all fit. If they do not, use the individual STL files and arrange them on multiple plates without changing their scale.
3. Start with the same upstream PLA+/0.4 mm/0.2 mm/15% settings as the gauge. Upstream recommends supports where needed for overhangs and specifically avoiding support inside horizontal screw holes. Use Bambu Studio's support painting/blocking and **inspect the sliced layers**, especially holes and motor pockets. Part orientation and supports affect strength and fit.
4. Slice; review each layer, bed adhesion, part collisions, filament estimate and time. Resolve errors before submitting the job through your workplace's approved workflow. Save the resulting 3MF project so settings are reproducible.
5. Let the parts cool. Remove them and carefully remove supports; do not gouge bearing surfaces or crack thin sections. Inspect for layer separation, warped mating faces, blocked holes and poor adhesion. Reprint suspect parts. Test each servo in its pocket before fastening it.

No slicer project or print has yet been validated for your specific printer. The optional camera mount contains pieces up to roughly 242 mm in one dimension; orient, split plates if needed, and check bed fit separately.

## 5. Install the software and assign motor IDs

Do this before the final mechanical assembly so you can connect **one servo at a time**. The steps below follow the current [SO-101 guide](https://huggingface.co/docs/lerobot/main/so101) and [installation guide](https://huggingface.co/docs/lerobot/main/installation); software and commands can change. The cited `main` documentation may describe newer features than a stable PyPI release.

1. Install [Miniforge](https://github.com/conda-forge/miniforge) for your Mac if you do not already have Conda. Open a new Terminal and create a separate Python 3.12 environment:

   ```bash
   conda create -n lerobot python=3.12
   conda activate lerobot
   conda install -c conda-forge ffmpeg
   python -m pip install 'lerobot[core_scripts,feetech]'
   ```

   Follow the installation guide for the current platform and version if dependencies fail; it describes an Intel Mac video-decoding exception. Activate the environment whenever you open a new shell. These commands have not been run against your future robot.

2. With no servo attached yet, connect the matching supply and the controller's USB **data** cable. For the upstream Waveshare board, the SO-101 guide specifies its two jumpers on channel **B (USB)**; confirm this against your exact board.
3. Find the port:

   ```bash
   lerobot-find-port
   ```

   Disconnect the USB cable when prompted and reconnect it afterward. Write down the resulting `/dev/tty.usbmodem…` port; the example in the official guide is not your port.
4. Start motor setup with your actual port, for example:

   ```bash
   lerobot-setup-motors --robot.type=so101_follower --robot.port=/dev/tty.usbmodemYOUR_PORT
   ```

   **Follow each prompt exactly.** Connect only the named motor to the controller, with no other motor daisy-chained, and press Enter to assign its ID and baud rate. Label the motor before moving to the next. Start with the gripper when prompted. Avoid connecting/disconnecting servo cables under power: turn the supply off before changing the motor, then restore it before proceeding.

   | ID | Joint |
   |---:|---|
   | 1 | shoulder pan / base rotation |
   | 2 | shoulder lift |
   | 3 | elbow flex |
   | 4 | wrist flex |
   | 5 | wrist roll |
   | 6 | gripper |

   If the setup program or connection fails, stop: check supply voltage, board jumpers, USB data cable, port, and that exactly one motor is connected. Do not proceed with duplicate or unknown IDs.

## 6. Assemble the follower

Use the photos and videos in the [official SO-101 assembly guide](https://huggingface.co/docs/lerobot/main/so101) alongside these checkpoints. They show the exact orientations; this summary does not replace those images. Power off and disconnect the adapter while assembling. Fit a bus cable into each motor as it is installed where access would otherwise be difficult.

1. **Base and shoulder pan (ID 1):** Fit the drive and passive horns as shown in the guide, using the specified horn screw. Install motor 1 in the base, secure the motor and holder, then attach the shoulder component to the horns. Check that the base rotates freely without wires catching.
2. **Shoulder lift (ID 2):** Install its horns and servo in the shoulder holder. Secure the upper arm to the horns. Confirm both sides are fully seated and the link swings without binding.
3. **Elbow (ID 3):** Install its servo and horns, then attach the forearm. Keep the motor cable accessible and check the motion path.
4. **Wrist flex (ID 4):** Fit the wrist motor holder and motor, then attach the wrist assembly as shown.
5. **Wrist roll (ID 5):** Fit this motor in the wrist holder and install the specified single horn. Secure the wrist assembly to motor 4.
6. **Gripper (ID 6):** Attach the follower gripper body to motor 5's horn. Install motor 6 and its horns, then the moving jaw. Check that the jaws move without rubbing or a trapped cable.
7. **Controller and cables:** Fit the controller mounting plate and route the three-pin leads through the provided guides. With power off, daisy-chain the motors and connect the shoulder-pan motor to the board. Use the connector orientation and cable supplied for the exact servos; do not force or reverse a plug. Leave service loops at moving joints and check that cables cannot pull tight or enter the gripper.

Use the guide's M2×6 and M3×6 screws in the specified holes. Tighten gently: stripped plastic or a cracked mount is a reason to replace the part. Check that screw lengths cannot bottom out or damage a motor.

## 7. Mount the arm to the desk

1. Measure the desktop thickness and the clear space beneath its edge. Choose a solid section of desk with room for the arm's motion and its cables. Avoid thin, hollow, damaged or unsupported surfaces.
2. Place the base flat and use **two suitable external clamps**, engaging the printed base's intended clamp tabs, with protective pads. The upstream arm is designed for this arrangement; a custom clamp has not been designed or tested here.
3. Tighten both clamps evenly. With power off, gently check that the base cannot rock, slide, or lift; inspect the desk and printed tabs for flex or cracks. Move the arm by hand through its intended working area without forcing the servos or joints. Verify it cannot hit the desk, monitor, cables, or a person. Reposition or improve the mounting if it moves.
4. Provide a physical way to remove power quickly, and support the arm before removing power: the joints can relax and the arm or object can fall. Keep fingers clear of the gripper and joints.

## 8. Connect, calibrate, and test

1. Confirm the six unique IDs and cable chain, matching power-supply voltage and polarity, and a secure desk mount. Clear the workspace. Support the arm so it cannot fall if torque is disabled. Keep the power disconnect within reach.
2. Connect the controller to the Mac by USB and its matching supply. Re-run `lerobot-find-port` if the port changed. Then calibrate using the **same arm ID** you will use for control:

   ```bash
   lerobot-calibrate \
     --robot.type=so101_follower \
     --robot.port=/dev/tty.usbmodemYOUR_PORT \
     --robot.id=desk_follower
   ```

3. Follow the prompts and the official calibration video: put the joints near their middle positions, then slowly move each through its **physically safe** range as prompted. Do not drive or force a joint into a hard stop. Save the calibration. If it binds or travels in an unexpected direction, stop and resolve the assembly or cabling first.
4. **Follower-only connection and gripper check:** The following example uses the current `SO101Follower` Python API. It has not been tested on your physical arm. Keep the gripper empty, hands clear, and arm supported. Connecting may enable torque and the arm may move; disconnecting may release torque. Start with the gripper approximately mid-range. Replace the port and run this only after calibration:

   ```bash
   python - <<'PY'
   import time
   from lerobot.robots.so_follower import SO101Follower, SO101FollowerConfig

   robot = SO101Follower(SO101FollowerConfig(
       port='/dev/tty.usbmodemYOUR_PORT',
       id='desk_follower',
       max_relative_target=3.0,
   ))
   try:
       robot.connect(calibrate=False)
       pos = robot.get_observation()['gripper.pos']
       print('Current gripper position:', pos)
       if not 10 <= pos <= 90:
           print('Gripper is near an endpoint; skipping the movement.')
       else:
           print('Sending one small gripper position change.')
           print('Command applied:', robot.send_action({'gripper.pos': pos + 3.0}))
           time.sleep(1)
   finally:
       if robot.is_connected:
           robot.disconnect()
   PY
   ```

   Keep a hand near the power disconnect, not the arm. Stop on unexpected motion, noise or a strained cable. This uses a small change in the gripper's normalized 0–100 range; `max_relative_target` limits the requested step but is **not** a collision detector or emergency stop. If imports differ, consult the [current API reference](https://huggingface.co/docs/lerobot/main/api/robots) for your installed version rather than guessing. If a script fails during connection, power off after safely supporting the arm and diagnose before retrying.
5. Once that succeeds, perform supervised, small movements one joint at a time using a supported control interface. Do not command full-speed, maximum reach, or a payload until clearances and the mount have been checked. Servo stall torque is not a safe working-payload rating.

## 9. Add vision and work toward a desk task

**Camera:** Mount a USB webcam above the workspace with a stable, independent stand or the upstream printed mount designed for its specified model. Confirm that it cannot fall or obstruct the arm. In QuickTime Player on the Mac, choose **File → New Movie Recording**, select the webcam in the camera menu, and check the image. Aim for a clear view of the gripper, object, and destination. The upstream mount suggests 640 × 480 at 30 fps as a starting point; test what your actual camera and software support. Do not assume an unverified webcam fits that printed mount.

**First AI task:** Start with one light, easy-to-grasp object and one marked bin inside the arm's reachable area. Keep the camera fixed. In LeRobot the typical sequence is **teleoperate → record → train or adapt → evaluate**. The [real-world robot tutorial](https://huggingface.co/docs/lerobot/main/getting_started_real_world_robot) walks through demonstrations and training. A compatible teleoperator is needed to collect demonstrations; the optional SO-101 leader is the most direct documented path. Cameras, joint calibration, and action formats need to match the dataset and policy. Expect iteration and supervised failures: a language instruction does not automatically produce a reliable general-purpose desk organizer.

For a leader, use its own 7.4 V supply, assign and calibrate its motors independently using the official guide, and note its port. Then, with both arms securely mounted and ready to stop, the documented teleoperation pattern is:

```bash
lerobot-teleoperate \
  --robot.type=so101_follower \
  --robot.port=/dev/tty.usbmodemFOLLOWER_PORT \
  --robot.id=desk_follower \
  --teleop.type=so101_leader \
  --teleop.port=/dev/tty.usbmodemLEADER_PORT \
  --teleop.id=desk_leader
```

Replace both ports with the discovered values. Start from the calibrated middle pose and move slowly with the workspace clear. Consult the [LeRobot cheat sheet](https://huggingface.co/docs/lerobot/main/cheat-sheet) for version-specific camera and recording options; keep datasets local if desired by setting the appropriate `push_to_hub` option.

## Troubleshooting

| Symptom | Check first |
|---|---|
| Servo does not fit a print | Recheck the fit gauge, scale, material shrinkage, orientation and supports; reprint before forcing it. |
| Serial port missing | Confirm a data-capable USB cable, reconnect the board and rerun `lerobot-find-port`; check board USB jumper settings. |
| Motor setup cannot find one motor | Check correct supply and polarity, one motor connected, connector seating, and ID/baud setup. Power off before rewiring. |
| Arm behaves oddly after assembly | Stop and support it; confirm motor IDs, cable order, correct horns and calibration. Check mechanical binding with power off. |
| Arm or base shifts | Stop, remove power after supporting the arm, and improve the clamp contact or desk support before testing again. |
| Camera absent or poor view | Check Mac camera permissions and QuickTime input selection; reposition the camera and lighting, then keep placement fixed for the dataset. |

## Primary references

- [SO-101 source, BOM and printing guidance](https://github.com/TheRobotStudio/SO-ARM100)
- [Hugging Face SO-101 assembly and calibration](https://huggingface.co/docs/lerobot/main/so101)
- [LeRobot installation](https://huggingface.co/docs/lerobot/main/installation)
- [LeRobot real-world robot workflow](https://huggingface.co/docs/lerobot/main/getting_started_real_world_robot)
- [SO follower API and configuration](https://huggingface.co/docs/lerobot/main/api/robots)
