# Exploratory Fusion support study

**Not a qualification test.** The study isolates the front-right raised side support from the quadruped mount concept. It does not model the chassis, plate, bolt, friction, preload, other supports, arm, impact, or walking. The load, fixture and material are illustrative assumptions, not measured conditions or safety limits. Do not use its results to approve the robot for printing or operation.

[Local Fusion study archive](outputs/raised-support-fusion-study-10N-RESULTS-NOT-INCLUDED.f3d) contains the corrected setup. When reopened, the archive retained the 10 N load, fixture and material but **did not contain the solved results**. The cloud document named `Robot arm - exploratory support simulation - NOT VALIDATED` was saved to Fusion's Default Project with the user's explicit authorization and is where the completed result was observed.

## Setup

- Source geometry: one `CONCEPT drilled support R 1` from the raised v4 mount; exported as [STEP](outputs/raised-front-support-SIMULATION-ONLY.step). It is not the full assembly.
- Study: Fusion Linear Static Stress. Its default gravity load is suppressed.
- Material: Fusion library `ABS Plastic`, a placeholder. No actual material, layer orientation, infill, or printed-part properties have been measured. An isotropic bulk material does not capture printed-layer strength.
- Constraint: the entire modeled 3.4 mm chassis-side cylindrical hole face is fixed in X, Y and Z. This idealizes an infinitely rigid connection and can artificially stiffen the part; a real bolt and chassis are not represented.
- Load: a 10 N downward force in the model's Y direction, distributed over the top horizontal support face (area approximately 676.9 mm²). This is an illustrative test load, not a derived maximum or a verified share of robot weight.
- Precheck: Fusion reported the prepared study ready. That checks setup completeness, not physical validity. The study was scheduled using the Solve dialog, which showed zero credits required.

An earlier setup mistakenly used −10 Fusion internal force units, which Fusion formats as **−0.1 N**, not −10 N. Its solve completed, but it must not be used to assess the intended 10 N case. The original `Force1` is now suppressed; the active `10 N downward - illustrative` load uses −1000 internal units, which Fusion formats as **−10.0 N**. The corrected study was resubmitted at zero credits. The [earlier local archive](outputs/raised-support-fusion-study-PROTOTYPE.f3d) contains the incorrect 0.1 N setup and is retained only as history.

## Corrected solve result

Fusion reported the corrected 10 N study complete and its results up to date. In the Safety Factor result, Fusion displayed a **minimum modeled value of 5.66**, using the library ABS yield-strength criterion. [Result view](outputs/support-10N-fusion-result.png). This number belongs only to this isolated, homogeneous-material, fixed-hole, single-load model; it is not a safety factor for the printed part, its fasteners, the chassis or the walking robot. It does not justify reducing material or proceeding to a physical build. The screenshot and the cloud result are evidence of the solve; the local archive preserves the setup, not its cloud results.

## Sideways load case

A cloned study, `10 N sideways support study - NOT VALIDATED`, uses the same support, material, and fully fixed hole but applies **+10 N in X** to the same top face. The downward case is suppressed in the clone. Fusion's unit formatter confirmed the active force as 10 N; the precheck reported ready. The original downward study remains unchanged. The [two-study local archive](outputs/raised-support-two-load-cases-SETUP.f3d) preserves setups rather than cloud results.

Fusion reported the sideways solve complete and displayed a **minimum modeled safety factor of 1.009** against its target of 2.0. [Result view](outputs/support-sideways-10N-fusion-result.png). Under these particular assumptions it is much more demanding than the downward case; this is a warning about the concept, not a measured failure load. The fixed hole and sharp geometric features may create mesh-sensitive local stresses, and actual printing, fastener load distribution and walking forces remain unknown. The side support is being revised; do not interpret either result as approval to print or operate the robot.

The subsequent [8 mm-wall support concept](ARM-MOUNT-STUDY.md#thicker-support-iteration) was tested in a separate Fusion Linear Static Stress study with the same nominal **+10 N X force**, ABS library material, and fully fixed side-hole face. Fusion reported the solve complete and displayed a **minimum modeled safety factor of 3.075**. [Result view](outputs/thick-support-sideways-10N-fusion-result.png). The top face carrying the distributed force increased from approximately 676.9 to 788.9 mm², and the support geometry and load centroid changed, so this is an approximate comparison, not an isolated measurement of wall-thickness effects. The result does not account for the actual print, chassis, bolts, contacts, walking loads or mesh convergence and does not validate the design.

The revised cloud study is `Robot arm - thicker support simulation - NOT VALIDATED` in Fusion's Default Project. The [local setup archive](outputs/thick-support-sideways-study-SETUP.f3d) was reopened with the 10 N load, fixed-hole selection and ABS material intact; like the other local archives, it did not contain the cloud result. A longer side-bolt envelope and the earlier small lower-shell overlaps remain unresolved.

Sharp corners and the fully fixed hole can produce mesh-sensitive stress concentrations. A useful follow-up needs measured material properties for the actual print, contact and fastener models, credible loads across stowed, manipulation and walking configurations, mesh-convergence checks, and physical testing. A single successful solve cannot establish strength or safety.
