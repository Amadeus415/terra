# Desktop robotics arm

A build guide and Fusion reference for a desk-mounted SO-101 follower arm, based on The Robot Studio and Hugging Face's published design. Start with [BUILD-GUIDE.md](BUILD-GUIDE.md). The [design notes](DESIGN-NOTES.md) record what has and has not been verified.

The arm has not been printed, assembled, or physically tested for this project. The Fusion archive is a static reference, not an articulated or custom-validated design.

The upstream print files and license are pinned in the `reference/SO-ARM100` Git submodule. Clone with:

```bash
git clone --recurse-submodules https://github.com/Amadeus415/robotics_terra.git
```

For an existing clone, run `git submodule update --init --recursive`. Open the guide from the local checkout to use its links to files inside the submodule. On GitHub, browse the upstream submodule or the [SO-101 repository](https://github.com/TheRobotStudio/SO-ARM100) directly.
