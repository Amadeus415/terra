# SO-101 arm and quadruped research

This project contains a guide to a desk-mounted SO-101 follower arm and exploratory Fusion studies for carrying it on a four-legged base.

**The walking robot is not ready to print or operate.** It has not been assembled or physically tested, and its mount, actuators, power, controls and gait are not validated. The images and CAD concepts are studies, not a completed build.

- [Desktop arm build guide](BUILD-GUIDE.md) and [design notes](DESIGN-NOTES.md)
- [Walking-robot build readiness](BUILD-READINESS.md) and [quadruped placement study](QUADRUPED-PLACEMENT-STUDY.md)
- [Single-leg motion and interference study](SINGLE-LEG-MOTION-STUDY.md)
- [Arm mount and load study](ARM-MOUNT-STUDY.md) and [Fusion support simulation](SUPPORT-SIMULATION.md)
- [Early quadruped layout concept](QUADRUPED-CONCEPT.md)

The upstream SO-101 print files and license are pinned in the `reference/SO-ARM100` Git submodule. Clone with:

```bash
git clone --recurse-submodules https://github.com/Amadeus415/robotics_terra.git
```

For an existing clone, run `git submodule update --init --recursive`. Open the guides from the local checkout to use their links to submodule files. On GitHub, browse the upstream submodule or the [SO-101 repository](https://github.com/TheRobotStudio/SO-ARM100) directly. Quadruped source attribution and terms are recorded in the [placement study](QUADRUPED-PLACEMENT-STUDY.md).
