# Operational Design Domain and Requirements Traceability

*Guide and templates for the RL lane-keeping thesis.*

---

## 1. Purpose and scope of this chapter

This chapter defines the Operational Design Domain (ODD) of the autonomous lane-keeping system presented in this thesis, derives the requirements that the system must satisfy within that ODD, and establishes the traceability links between ODD attributes, requirements, test scenarios, and safety-case evidence. It is the organising skeleton of the evaluation chapters that follow.

The ODD and its requirements together form the **safety envelope** of the system: a declaration of where the system is expected to operate correctly, what it must do inside that envelope, and what it must do when it is about to leave it. This chapter gives each of those three elements explicit, numbered, and verifiable form so that every scenario generated for training or testing maps to a concrete line of the argument.

---

## 2. The operational design domain

### 2.1 Definition and role

Following BSI PAS 1883 and ISO 34503, the ODD is the description of the operating conditions under which the system is designed to function, expressed as enumerable attributes of the environment. An ODD is **not** a statement of what the system does; it is a statement of *where* it does it. Requirements about behaviour live inside the ODD. Outside the ODD, the system may fail, and that failure is acceptable **if, and only if,** an ODD monitor detects the exit and triggers a controlled fallback.

Three practical implications follow from this definition and shape the rest of the chapter:

- **Every ODD attribute must enumerate both in-ODD values and out-of-ODD values.** A catalogue listing only what is included does not enable runtime monitoring.
- **Every scenario used in training or testing must map to a set of attributes.** A tile without an ODD mapping cannot contribute evidence to the safety case.
- **Every requirement must cite the attributes it assumes.** A requirement without ODD references is either a functional requirement or a latent assumption.

### 2.2 ODD catalogue

The catalogue below enumerates the attributes relevant to this thesis. Categories follow BSI PAS 1883: Scenery (S), Environmental (E), Dynamic (D) and Operational (O). Out-of-ODD values are included so that the ODD monitor has measurable triggers.

| ID     | Category                | Attribute                           | In-ODD values                                              | Out-of-ODD / trigger                                     |
| ------ | ----------------------- | ----------------------------------- | ---------------------------------------------------------- | -------------------------------------------------------- |
| S-1.1  | Scenery — Road type     | Number of lanes                     | 1 lane or 2 lanes                                          | 3+ lanes, unmarked path                                  |
| S-1.2  | Scenery — Road type     | Lane useful width                   | 24.5 cm ± 2 cm                                             | <20 cm or >28 cm                                         |
| S-1.3  | Scenery — Road type     | Total road width                    | 26.5 cm (single) or 52 cm (two-lane)                       | Values outside ±5% of nominal                            |
| S-2.1  | Scenery — Geometry      | Curvature radius R (centreline)     | R ≥ 30 cm (straight to tight curve)                        | R < 30 cm                                                |
| S-2.2  | Scenery — Geometry      | Arc angle of single curve segment   | 0° (straight) to 180° (U-turn)                             | Compound curves without straight relief                  |
| S-2.3  | Scenery — Geometry      | Change of curvature                 | Discrete transitions at tile boundaries                    | Continuous clothoids (not modelled)                      |
| S-2.4  | Scenery — Geometry      | Gradient and cross-slope            | 0° (flat)                                                  | Banked, inclined, or crowned surfaces                    |
| S-3.1  | Scenery — Surface       | Surface type                        | Asphalt (clean, worn, patched, wet)                        | Ice, snow, loose sand                                    |
| S-3.2  | Scenery — Surface       | Alternate surfaces                  | Dirt / gravel (limited exposure)                           | Exposed gravel > 2 m continuous                          |
| S-3.3  | Scenery — Surface       | Debris on surface                   | Leaves, light dirt, oil stains                             | Standing water, large debris > 3 cm                      |
| S-4.1  | Scenery — Markings      | Edge line continuity                | Continuous or gap ≤ 1.5 m                                  | Gap > 1.5 m or both edges missing                        |
| S-4.2  | Scenery — Markings      | Edge line width                     | 1 cm ± 20%                                                 | Outside tolerance                                        |
| S-4.3  | Scenery — Markings      | Centre line (two-lane)              | Dashed white 10+10 cm or double solid                      | Yellow markings, colour variations                       |
| S-4.4  | Scenery — Markings      | Cross markings                      | Zebra crossings, stop lines, painted arrows                | Lettered text, pictograms not listed                     |
| S-5.1  | Scenery — Intersections | Intersection type                   | T-junction, side entrance (≤ 1 per segment)                | 4-way crossings, roundabouts                             |
| S-5.2  | Scenery — Intersections | Intersection frequency              | ≤ 1 per 10 m of driven road                                | Higher density                                           |
| S-6.1  | Scenery — Obstacles     | Obstacle presence                   | Traffic cones, drain covers, fallen leaves                 | Walls, parked vehicles, poles                            |
| S-6.2  | Scenery — Obstacles     | Obstacle height                     | < 15 cm                                                    | ≥ 15 cm                                                  |
| E-1.1  | Environment — Lighting  | Illumination                        | Uniform simulated daylight                                 | Sun flare, tunnels, darkness, headlights                 |
| E-1.2  | Environment — Weather   | Weather                             | Dry or moderately wet                                      | Rain in motion, snow, fog                                |
| D-1.1  | Dynamic elements        | Other vehicles                      | None                                                       | Any other vehicle                                        |
| D-1.2  | Dynamic elements        | Pedestrians and cyclists            | None                                                       | Any pedestrian or cyclist                                |
| O-1.1  | Operational             | Longitudinal speed                  | 0.3 – 1.5 m/s (scale-model)                                | Outside range                                            |
| O-1.2  | Operational             | Mission duration                    | ≤ 10 min continuous                                        | Longer missions without reset                            |
| O-1.3  | Operational             | Sensor availability                 | Camera + odometry nominal                                  | Single-sensor degradation                                |

**Note on exclusions.** Dynamic elements (D-1.\*) and adverse weather and lighting (E-1.\*) are explicitly *out of ODD* for this thesis. This is a defensible scope provided the system detects these conditions and executes a fallback, not provided it performs well in them. The corresponding requirements (REQ-LK-020 onward) encode this detect-and-handover behaviour.

### 2.3 Mapping road modules to ODD attributes

Each texture module produced during this thesis is a concrete instantiation of a point in the ODD space. The table below maps every module to the attributes it exercises and locates it as either interior (nominal zone) or boundary (edge of an attribute's admitted range).

| Tile name                   | ODD attributes exercised                     | Position in ODD space                        |
| --------------------------- | -------------------------------------------- | -------------------------------------------- |
| `single_01_clean`           | S-1.1, S-1.2, S-1.3, S-3.1, S-4.1, S-4.2      | Centre of ODD (nominal single-lane)           |
| `single_02_worn`            | S-3.1, S-3.3, S-4.1 (partial wear)            | Interior, degraded paint + dirt               |
| `single_03_dirt_road`       | S-3.2, S-4.1 (faint)                          | Boundary — dirt surface attribute             |
| `two_same_01_clean`         | S-1.1, S-1.3, S-4.1, S-4.3                    | Centre of ODD (nominal two-lane)              |
| `two_same_02_patched`       | S-3.1 (worn), S-3.3, S-4.1 (partial)          | Interior, repair patches                      |
| `two_same_03_tee_junction`  | S-5.1 (T-junction), S-4.1 (gap at opening)    | Boundary — intersection attribute             |
| `two_opp_01_clean`          | S-1.1, S-1.3, S-4.1, S-4.3, S-4.4 (none)      | Centre of ODD (opposite-direction)            |
| `two_opp_02_wet`            | E-1.2 (wet), S-3.3                            | Interior, wet surface                         |
| `two_opp_03_side_entrance`  | S-5.1 (side entrance)                         | Boundary — intersection attribute             |
| `g1_01_zebra_crossing`      | S-4.4 (zebra + stop line)                     | Interior, transverse markings                 |
| `g1_02_lane_arrows`         | S-4.4 (arrows)                                | Interior, pictogram markings                  |
| `g2_01_sharp_curve`         | S-2.1 (R ≈ 50 cm effective)                   | Boundary — minimum curvature                  |
| `g2_02_lane_narrowing`      | S-1.2 (reduced lane), S-6.1 (cones)           | Boundary — lane-width attribute               |
| `g3_01_edge_line_gap`       | S-4.1 (gap ≈ 1.2 m)                           | Boundary — edge continuity attribute          |
| `g3_02_double_solid_centre` | S-4.3 (double solid)                          | Interior, alternate centreline style          |
| `g4_01_fallen_leaves`       | S-3.3 (leaves)                                | Interior, debris presence                     |
| `g4_02_drain_cover`         | S-6.1 (drain ≤ 15 cm)                         | Interior, static obstacle presence            |
| `curve_R030cm_A*`           | S-2.1 (R = 30 cm)                             | Boundary — minimum curvature                  |
| `curve_R050cm_A*`           | S-2.1 (R = 50 cm)                             | Interior, tight curve                         |
| `curve_R080cm_A*`           | S-2.1 (R = 80 cm)                             | Interior, moderate curve                      |
| `curve_R120cm_A*`           | S-2.1 (R = 120 cm)                            | Interior, gentle curve                        |

**Interpretation.** Tiles marked as boundary (such as `g3_01_edge_line_gap` for S-4.1, or `curve_R030cm` for S-2.1) are the ones that exercise the ODD at its limit. They are the most valuable tiles for verifying that the system degrades gracefully near the boundary and that the ODD monitor triggers correctly just beyond it. The training curriculum should weight them more heavily in later stages.

---

## 3. Requirements

### 3.1 Authoring patterns

All requirements in this thesis follow the EARS (Easy Approach to Requirements Syntax) patterns. Each requirement is a single sentence whose subject is a concrete component (policy, cage, ODD monitor, safe-stop controller, logging subsystem) and whose criterion is measurable. Requirements without a numeric or binary criterion are rejected during review.

| Pattern             | Syntax                                                  | Example (lane-keeping)                                                                                        |
| ------------------- | ------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| Ubiquitous          | The [component] shall [response].                       | The policy shall publish actions on `/cmd_proposed` at ≥ 20 Hz.                                              |
| Event-driven        | When [trigger], the [component] shall [response].       | When the lateral offset exceeds ±10 cm, the cage shall substitute the proposed action.                        |
| State-driven        | While [state], the [component] shall [response].        | While the vehicle is inside the ODD, the ODD monitor shall publish `ok=True` on `/odd/status`.              |
| Optional            | Where [feature condition], the [component] shall [...]. | Where the right edge line is missing for more than 0.2 s, the cage shall extrapolate offset from the left line. |
| Unwanted behaviour  | If [undesired condition], then the [component] shall [...]. | If both edge lines are lost for > 0.5 s, then the system shall execute a controlled stop.                   |

### 3.2 Requirement metadata

Every requirement in the catalogue carries six fields:

- **ID** of the form `REQ-LK-NNN`, assigned once and never reused.
- **Owner** — which component satisfies the requirement (policy, cage, ODD monitor, safe-stop, logging).
- **Statement** in EARS form, naming the trigger, the responsible component, and the response.
- **Verification criterion** — a pass/fail condition expressible as an inequality or a boolean test.
- **ODD attributes referenced** — the attributes whose in-ODD values the requirement assumes.
- **Verification method** — simulation, adversarial testing, unit test, formal proof, or reachability analysis.

### 3.3 Example requirement catalogue

The requirements below are representative, not exhaustive. They cover the four component categories used throughout the thesis and exercise each of the ODD attribute groups at least once.

| ID           | Owner       | Requirement                                                                                                                                   | ODD attributes        |
| ------------ | ----------- | --------------------------------------------------------------------------------------------------------------------------------------------- | --------------------- |
| REQ-LK-001   | Policy      | The policy shall maintain mean \|e_y\| ≤ 5 cm while operating on straight segments of the road (S-1.1, S-4.1).                                 | S-1.1, S-4.1          |
| REQ-LK-002   | Policy      | When the road curvature radius R is ≥ 50 cm, the policy shall maintain peak \|e_y\| ≤ 10 cm throughout the turn.                                | S-2.1                 |
| REQ-LK-003   | Policy      | While the lane width is between 20 and 28 cm, the policy shall track the centre line with mean \|e_y\| ≤ 6 cm.                                 | S-1.2                 |
| REQ-LK-010   | Cage        | When the predicted lateral offset at t+T exceeds `e_y_max`, the cage shall substitute a backup steering action before the next actuation cycle. | S-4.1, S-2.1          |
| REQ-LK-011   | Cage        | Where one edge line is missing for less than 1.5 m, the cage shall extrapolate the missing offset from the surviving edge line.                | S-4.1                 |
| REQ-LK-012   | Cage        | When the predicted distance to a static obstacle drops below `d_safe`, the cage shall substitute an action with τ ≤ 0.2.                       | S-6.1, S-6.2          |
| REQ-LK-020   | ODD monitor | If both edge lines are lost for > 0.5 s, then the ODD monitor shall declare out-of-ODD and trigger the safe-stop controller.                    | S-4.1                 |
| REQ-LK-021   | ODD monitor | If the surface classifier confidence on 'asphalt' or 'dirt' falls below 0.6 for > 1 s, then the ODD monitor shall declare out-of-ODD.          | S-3.1, S-3.2          |
| REQ-LK-022   | ODD monitor | The ODD monitor shall publish `ok/nominal` at ≥ 10 Hz on the topic `/odd/status`.                                                            | All                   |
| REQ-LK-030   | Safe-stop   | When commanded by the ODD monitor, the safe-stop controller shall bring the vehicle to v ≤ 0.05 m/s within 2 s while keeping \|e_y\| ≤ 15 cm.  | All (fallback)        |
| REQ-LK-040   | Logging     | The cage shall publish every intervention event on `/cage/interventions` with timestamp, triggering guard, and substituted action.            | All                   |
| REQ-LK-041   | Logging     | The ODD monitor shall log every ODD boundary crossing with affected attribute, timestamp, and sensor evidence.                                 | All                   |

**How to grow this table.** For each ODD attribute that does not yet appear in the right-hand column, write at least one requirement. For each requirement that does not yet name a specific owner, rewrite it. When you finish, every attribute has at least one requirement and every requirement has exactly one owner. This is the completeness check that should happen before the thesis defence.

---

## 4. Traceability

### 4.1 What traceability buys

A traceability matrix is the audit trail that connects every line of the argument: ODD attribute → requirement → test case → tile used → evidence → safety-case node. Its presence allows a reviewer to follow any claim in the safety case back to its ODD anchor, and forward to the evidence that supports it. Its absence makes the safety case unfalsifiable.

### 4.2 Traceability matrix

The matrix below illustrates the structure using ten representative chains. The full matrix is maintained as a living spreadsheet (see appendix) and updated whenever a requirement, tile, or test case is added or modified.

| ODD attr.        | Requirement               | Tile(s)                                                                 | Test case                     | GSN evidence             |
| ---------------- | ------------------------- | ----------------------------------------------------------------------- | ----------------------------- | ------------------------ |
| S-1.1            | REQ-LK-001                | `single_01_clean`, `two_same_01_clean`, `two_opp_01_clean`               | TC-001 nominal driving         | E1 coverage grid         |
| S-2.1            | REQ-LK-002                | `curve_R050cm_A*`, `curve_R080cm_A*`, `g2_01_sharp_curve`                | TC-010 curve tracking          | E1 coverage grid         |
| S-3.1 / S-3.3    | REQ-LK-001                | `single_02_worn`, `two_same_02_patched`, `g4_01_fallen_leaves`           | TC-020 degraded surface        | E1, E3 intervention log  |
| S-3.2            | REQ-LK-021                | `single_03_dirt_road`                                                    | TC-030 dirt-road ODD monitor   | E5 reachability proof    |
| S-4.1            | REQ-LK-010, REQ-LK-011     | `g3_01_edge_line_gap`                                                    | TC-040 edge gap fallback       | E3, E4 zero departures   |
| S-4.3            | REQ-LK-001 (regression)    | `g3_02_double_solid_centre`                                              | TC-041 double-line regression  | E3                       |
| S-4.4            | REQ-LK-001                | `g1_01_zebra_crossing`, `g1_02_lane_arrows`                              | TC-050 transverse markings     | E3                       |
| S-5.1            | REQ-LK-010, REQ-LK-011     | `two_same_03_tee_junction`, `two_opp_03_side_entrance`                   | TC-060 junction handling       | E3, E4                   |
| S-6.1 / S-6.2    | REQ-LK-012                | `g4_02_drain_cover`, `g2_02_lane_narrowing` (cones)                      | TC-070 static obstacle clearance | E3, E5                 |
| E-1.2            | REQ-LK-021 (out-of-ODD)    | `two_opp_02_wet` (boundary), rain scenario (out)                         | TC-080 wet-road boundary       | E2 adversarial           |

**Reading the matrix.** Each row is a single verifiable claim: the ODD attribute bounds the scope, the requirement states the expected behaviour, the tile(s) provide the stimulus, the test case records the outcome, and the GSN evidence node consumes the result. A gap in any column signals incomplete argument.

---

## 5. How to use this chapter

### 5.1 Workflow during thesis writing

Three steps, in order:

- **Freeze the ODD catalogue before writing requirements.** The catalogue is the vocabulary everything else uses; changing it mid-writing invalidates downstream sections.
- **Write requirements per component, not per scenario.** Every requirement has exactly one owner. If you find yourself writing "the system shall …", decompose it into one requirement per responsible component.
- **Populate the traceability matrix as you write evaluation chapters.** When a test case is defined, its row in the matrix is completed. Empty cells mean untested requirements; extra cells mean untraced evidence.

### 5.2 Where to place this material in the thesis

This chapter is a dedicated chapter of the thesis, typically positioned after the state-of-the-art and before the system design. A suggested placement in the draft is:

- **New chapter: "Operational Design Domain and Requirements"** — insert after the literature review / state-of-the-art chapter and before the system architecture chapter.
- **Sections 2.2 and 2.3** integrate directly with the methodology chapter's discussion of scenario generation.
- **Section 3.3** is referenced by every subsequent chapter — each evaluation result cites the requirement ID it addresses.
- **Section 4.2 (traceability matrix)** belongs in an appendix; the main chapter references it by forward pointer.

### 5.3 Living-document conventions

Two conventions keep this material maintainable across thesis revisions:

- **Stable IDs.** ODD attribute IDs (S-\*, E-\*, D-\*, O-\*) and requirement IDs (REQ-LK-\*) are assigned once and never reused, even if the attribute or requirement is deleted. A deleted item is marked as such; its ID is retired, not recycled.
- **Single source of truth.** The traceability matrix is the single source of truth. If a requirement exists in the matrix, it exists in the thesis; if it does not, it does not. This avoids the common failure mode where different chapters disagree on the set of requirements.

---

## Appendix A. Glossary

- **ODD** — Operational Design Domain. The declared range of conditions under which the system is designed to function.
- **SOTIF** — Safety Of The Intended Functionality (ISO 21448). Addresses hazards arising from the intended behaviour of a system in specified conditions.
- **EARS** — Easy Approach to Requirements Syntax. Five authoring patterns (ubiquitous, event-driven, state-driven, optional, unwanted behaviour) used throughout this thesis.
- **GSN** — Goal Structuring Notation. A graphical notation for structuring safety arguments into goals, strategies and evidence.
- **UL 4600** — Standard for safety cases for autonomous products. Cited in the safety-argument chapter.
- **Cage** — Synonym for safety filter or shield. A rule-based component that certifies or substitutes the learned policy's actions.
- **Tile** — A single PNG texture representing a scenery segment. The atomic unit of scenario construction in this thesis.
