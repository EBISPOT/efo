# From EFO 3 to EFO 4 in minimal increments

Proposal, 24 September 2026. Every statement below was checked against `master` (3.94.0), the `efo-4` branch (head `05442c6`) and PR #2810 on that date. Numbers come from the repository, the release assets and the linked issues.

## 1. Where things stand

**`master` is the EFO 3 line.** It builds with the ROBOT Makefile and HermiT, imports 14 per-ontology modules (11 of them trimmed to the seeded terms, so most relations to unseeded fillers are dropped), and released 3.94.0 on 15 September with 94,312 classes and about 124,000 named `SubClassOf` axioms. All content work (imports, new terms, obsoletions) happens here, and the definitive-ID workflow only runs here.

**`efo-4` is where EFO 4 has been assembled since 4 September**, when master was reset to before the owlmake migration (PR #2811 records the reset). The branch carries:

- the owlmake build (#2768, #2788, #2789);
- the ELK release: `has_disease_location o part_of ⊑ has_disease_location`, the 267 rewritten `X or part_of some X` restrictions, the asserted union-only parents, the weekly HermiT QC job and two new QC rules (#2793);
- seven content fixes that were merged to master between 26 August and 4 September and are no longer on master: #2774, #2775, #2777, #2784, #2785, #2806, #2809.

**PR #2810 (open, against `efo-4`) is the EFO 4 layout**: one merged, sharded base import of 25 ontologies, reasoned with ELK. It produces 142,590 classes and 211,443 named `SubClassOf` axioms against about 94,400 and 123,800 on master at the time, with 0 lost and 49 gained EFO edges relative to the branch base. Three modelling PRs (#2812, #2813, #2814) are also open against `efo-4`. Issue #2800 says the next version after 3.94 is planned to be 4.0.0, and names the reason for a major version: half as many classes again and a new source layout.

What master lacks today that `efo-4` already has (verified by diffing the two branches):

| Item | master | efo-4 |
|---|---|---|
| Obsoletions tagged `obsoleted_in_version 3.94.0` | 1 | 12 |
| Property chains in `efo-edit.owl` | 3 | 4 |
| `owl:unionOf` in `efo-edit.owl` | 392 | 134 |
| UBERON/CL `part_of` rows in the anatomogram templates | 123 | 0 |
| QC rules `self-xref`, `has-disease-location-union`, `non-el-class-expression` | absent | present |
| `reasoner_hierarchy_diff.py` (release hierarchy comparison) | absent | present |
| Release-notes tooling from #2826–#2828 (`generate_release_notes.py`, run-stable reports, pinned MONDO mirror, consistency gate) | present | absent |

The structural problem is not any single change. It is that `efo-4` is a long-lived branch diverging from master in both tooling and content, so it can only land as one big merge and one big release. That is the thing that cannot be done politically.

## 2. The approach

Replace the big-bang with a sequence of ordinary monthly 3.x releases. Each release carries one bounded, reviewable step. Each step has a measured, pre-announced effect on consumers (or none) and can be reverted on its own. "EFO 4" stops being a release and becomes a milestone: the state master reaches when the last step lands. Whether that state is then tagged 4.0.0, keeps counting 3.x, or moves to date-based versions (#2780) is a separate, cosmetic decision that can be taken whenever it is convenient.

Rules that make this work:

1. **Content on master only, as now.** `efo-4` stops receiving merges from master. It becomes a source of cherry-picks and a scheduled preview build, and is deleted at the end.
2. **Every step is a normal PR against master** with the usual QC plus the release gate from Stage 0. The gate's report goes in the PR description.
3. **Consumer-visible steps ship one per release**, get a standing "Towards EFO 4" paragraph in the release notes, and are announced on efo-users one release ahead when they touch GWAS Catalog, Open Targets or Expression Atlas.
4. **Tooling-only steps must prove identical output** (`robot diff` empty against the previous pipeline) before they merge.
5. **Every step has a one-PR rollback**: a flag in `owlmake.yaml`, a seed-file revert, or a content revert.

## 3. What EFO 4 decomposes into

| Part | What it is | Where it lives today | Independently shippable? |
|---|---|---|---|
| A. Build system | Makefile/ROBOT → owlmake; jars, `get_mirrors.sh`, `odk.sh` retired | #2768, #2788, #2789 on `efo-4` | Yes, output-identical by design |
| B. Reasoner | HermiT → ELK, which needs EL-friendly axioms (property chain, union rewrites, asserted union-only parents, non-EL allowlist, weekly HermiT QC) | #2792, #2793 on `efo-4` | Yes, in three PRs |
| C. Content hygiene that relations expose | cell lines `derives_from` not `part_of`; genus on `part_of` equivalences; self-xrefs; anatomogram `part_of` on UBERON/CL; twelve wrong parents; `has component some abnormal`; head-and-neck double equivalence; craniopharyngioma location | #2774, #2775, #2777, #2784, #2785, #2806, #2809 merged on `efo-4`; #2812, #2813, #2814 open | Yes, each a small content PR |
| D. Relations and ancestors of imported terms | trimmed modules → base modules; fillers and parents arrive with the term | #2756, #2122, #2810 | Yes, one ontology per release |
| E. New source ontologies for fillers | PATO, NCBITaxon taxslim, BFO, COB, IAO, SO, NBO, MPATH, ExO, SwissLipids; prefixes EFO ignores excluded; IAO/OBI/COB domain and range stripped; BFO disjointness stripped | #2803, #2810 | Yes, one or two per release |
| F. Duplicate labels | 22 EFO terms duplicating imported terms plus 8 PATO copies, mostly obsoletion with `replaced_by` | #2804 | Yes, normal curation |
| G. Packaging | one merged import committed as 216 sorted functional-syntax shards; catalog entries; OLS root annotation `IAO:0000700`; owlmake ≥ 0.2.12 | #2810 | Yes, as the last flip |
| H. Docs, version, cleanup | README, editor docs, `efo-3-edit.owl` (70 MB), `migration2019/` (71 MB), OLS docker files, Travis/GitLab CI | partly on `efo-4` | Yes |

Explicitly **not** part of EFO 4 (per #2800): BFO's disjointness axioms and the upper-level refiling they force (the table in #2808: measurement and phenotype placement, cell lines under diseases, drug-response groupings, material versus immaterial anatomy); the audit of the 10,329 foreign class blocks in `efo-edit.owl` (#2805); the 7,302 HGNC and 6,481 MGI gene classes in the PR module; the 6,213 native Orphanet blocks.

## 4. The stages

Releases are on or about the 15th of each month. The release numbers below assume 3.95.0 is October 2026 and nothing slips. Steps marked "pairable" can share a release with the previous step when the team is comfortable.

### Stage 0. Measure before moving (3.95.0)

No ontology change. This answers the testing-strategy question raised in #2800.

- Port `src/scripts/reasoner_hierarchy_diff.py` from `efo-4` and add a **release gate** to the release PR: candidate build against the last published `efo.owl`, reporting named edges lost and gained with re-routing discounted, class count by prefix, labels and definitions changed on existing IRIs, and the obsoletion delta the notes generator already computes. A lost edge fails the gate unless the PR lists it.
- Add **consumer contract checks**: every IRI in `iri_dependencies/gwas_terms.tsv` (the GWAS Catalog trait mappings, about 110,000 rows), every ID in the anatomogram templates, the Open Targets therapeutic-area roots and the most recent EVA import batches must resolve to a live, non-obsolete class, and their ancestor sets must not shrink unless the PR says so.
- Note that `efo_otar_slim.*` and `efo_otar_profile.*` are release assets but are not built by anything in the repository. Either bring their generation into the build now or add them to the gate as an external step, so every later stage is checked on them too.
- **Preview artefact** (optional, cheap, politically useful): a scheduled workflow on `efo-4` attaches its `efo.owl` to the latest release page as `efo-4-preview.owl`, never as the `current` asset. GWAS Catalog, Open Targets and Expression Atlas can test against the target months before any step reaches them.
- **Governance**: repurpose #2800 as the roadmap issue with this checklist; each merged step ticks a box; the release notes get a standing "Towards EFO 4" section. Decide the version policy (#2780) now so that no later step depends on a major bump.

Gate: none (tooling only). Rollback: not needed.

### Stage 1. Re-land the content hygiene the reset dropped (3.95.0 and 3.96.0)

Seven small PRs that were already reviewed and merged once, cherry-picked from `efo-4` one at a time and rebased on master's current content. None changes tooling.

| PR | Change | Consumer-visible effect |
|---|---|---|
| #2785 | remove 1,138 self-referential xrefs; add the `self-xref` QC rule | none |
| #2774 | obsolete 11 measurement terms missed by the 3.77.0 OBA migration | 11 obsoletions with replacements |
| #2775 | obsolete environmental-exposure measurements replaced by ECTO | obsoletions with replacements |
| #2777 | remove wrong scar xrefs from an obsolete stub | none |
| #2784 | 62 lymphoblastoid cell lines `derives_from` blood instead of `part_of`; genus added to 10 genus-less `part_of` equivalences | none in the hierarchy; removes 66 of the 88 unsatisfiable classes that relation recovery exposes (#2767) |
| #2806 | remove EFO's 112 `part_of` assertions on UBERON/CL classes in the anatomogram components | Expression Atlas roll-up: 67 of the 112 are entailed by UBERON+CL; the 45 that are not are listed in the PR and need a heads-up |
| #2809 | remove twelve wrong parents that PATO, UBERON and PO reject; import the eight PO classes properly and OBA's root | `heart rate` and `QRS duration` leave OBA's cardiovascular grouping; GWAS trait categories derive from ancestors, so announce |

Then the three open fixes, each its own PR: #2814 (single equivalence for `head and neck disorder`), #2813 (`has modifier`, not `has component`, on 53 axioms) and #2796, resolved the way Arwa proposed in the issue thread (obsolete the two EFO craniopharyngioma subtypes in favour of the MONDO terms) rather than the relocation in #2812.

Gate: hierarchy diff per PR; the only lost edges are the ones each PR lists. Rollback: revert the PR.

### Stage 2. Swap the build system, keep the output (3.96.0, pairable with the end of Stage 1)

- Re-land the owlmake migration (#2768 with the #2788 and #2789 fixes), rebased, with `reasoner: hermit` kept so this step is plumbing only.
- Port master's newer release tooling into the plan, since `efo-4` predates it: the pinned MONDO mirror (`mondo_mirror_version.txt`), `generate_release_notes.py`, `canonicalize_basic_report.py`, the run-stable reports and `release-notes-check.yml` (#2826–#2828).
- Acceptance: `robot diff` between the Makefile build and the `om` build from the same mirrors is empty; all reports byte-identical; a dry run of `allocate-definitive-ids` on a temporary ID passes; CI green on the owlmake image.
- Keep the Makefile in the tree for one release as a fallback. Remove it together with `bin/*.jar`, `get_mirrors.sh`, `odk.sh`, `efo-3-edit.owl`, `migration2019/`, `validation_flags.owl`, `issue_1948.owl`, the OLS docker files and the Travis/GitLab CI files in a separate hygiene PR that changes no output (the `owlmake-migration` branch already contains this deletion set).

Rollback: revert the migration PR; the Makefile is still there.

### Stage 3. EL-friendly axioms, then ELK (3.97.0 → 3.98.0)

Three PRs, in order:

- **3a, still HermiT.** Add `has_disease_location o part_of ⊑ has_disease_location`, rewrite the 254 restrictions in `efo-edit.owl` and 13 in `efo_equivalent_class_axioms.owl` from `has_disease_location some (X or part_of some X)` to `has_disease_location some X`, and add `has-disease-location-union-violation.sparql`. Expected under HermiT: no lost edges; the 15 head-located inflammatory diseases may appear under `head and neck disorder` (HermiT's inverse-plus-chain bug, EBISPOT/hermit-rs#5, decides whether they do).
- **3b.** Assert the 12 cell-line and assay parents that only unions gave; fix the five wrong inferences at their source (`has_role some hormone role` on two measurements, `has component some abnormal` on two Orphanet diseases, the PATO-style equivalence on `polycythemia`).
- **3c.** Flip `reasoner: elk`; add `hermit-qc.yml` (weekly) and `non-el-class-expression-violation.sparql` with its 136-class allowlist. Expected diff is exactly the table in #2793: 31 edges gained, 10 lost, the 10 all internal to CHEBI and PR with another parent kept. Release build time drops from about 2 min 48 s to about 30 s.

Gate: the #2793 table, no more. Rollback: flip the reasoner line back.

### Stage 4. Prepare the ground for relations (3.98.0 → 3.99.0)

- **Import PATO and NCBITaxon taxslim** as ordinary modules, seeded with the 338 PATO and 69 taxon fillers listed in #2803 and their ancestors; declare `RO:0020202` and `RO:0020203`. Expected: roughly 530 new classes under `quality` and `organism`, no EFO edge changes. (#2807 did this on master and was closed only because the classes are unreferenced until relations arrive; in this plan they are referenced two releases later.)
- **Curate the duplicate labels** (#2804): 22 EFO terms that copy imported terms plus 8 PATO copies (`area`, `duration`, `size`, `temperature`, `time`, `volume`, `strain`, `recurrent`). Obsolete with `replaced_by` over two releases, with the usual deprecation notice to ArrayExpress and Expression Atlas, and scope `duplicate-label-violation.sparql` to pairs that involve an EFO or Orphanet class.
- **Audit `subclasses.csv`** (8,200 rows: 4,771 PR, 3,312 OBA): drop rows whose edge the source ontology entails once its module carries relations; keep the grouping rows EFO users depend on. Scripted, zero hierarchy change by construction.
- **Seed the OBA ancestor closure** (#2122): the 439 missing ancestors (356 OBA, 77 PATO, 3 HP, 3 BFO) so that the 9,467 OBA classes missing a direct upstream parent regain it. Expected: OBA terms move from `amount` to their real parents. Announce, since GWAS trait categories derive from ancestors.

Gate: hierarchy diff; only edges listed by each PR. Rollback: seed-file revert.

### Stage 5. Recover relations, one ontology per release (3.99.0 → about 3.104.0)

For each import X, in `owlmake.yaml`: set the filter's `trim: true` to `trim: false` (signature seeding stays), harvest X's fillers into the sibling seed files with the script from #2758, remove whole axioms that mention any prefix EFO does not yet import (never partial class expressions, so no equivalence loses a conjunct), rebuild, run ELK and the HermiT job, publish the hierarchy diff, release.

Order, smallest blast radius first, with today's class counts:

| Release | Ontologies un-trimmed | Classes today |
|---|---|---|
| 3.99.0 | ECTO, GSSO, FBbi, OBI, FBbt | 14, 16, 54, 88, 110 |
| 3.100.0 | CL, GO | 728, 775 |
| 3.101.0 | UBERON | 1,269 |
| 3.102.0 | CHEBI | 2,115 |
| 3.103.0 | HP | 2,528 |
| 3.104.0 | OBA | 17,826 |

MONDO, HANCESTRO and PR already keep their relations (custom rules without a filter step). OBA goes last because it is the largest change (equivalence axioms rise from 3,823 to 42,008 when un-trimmed) and the one users asked for, so it should arrive when every prerequisite is in place.

Storage: PR's module is already 74 MB and an un-trimmed OBA or PR module can exceed GitHub's 100 MB limit. Until Stage 7's shards, build such modules at CI time from pinned mirrors (as `mondo_import.owl` is today) or commit them gzipped.

Expected per step: new relation axioms and a few thousand ancestor and filler classes, plus new inferred EFO edges only where EFO groupings meet the newly visible logic. Stages 1, 3 and 4 exist to keep that list short: when everything was done at once in #2810, the result was 0 lost and 49 gained.

Rollback: flip `trim` back and revert the seeds for that ontology.

### Stage 6. Add the remaining source ontologies (interleaved with Stage 5, one or two per release)

BFO (disjointness stripped at mirror time, as #2810 does), COB and IAO (domain and range axioms stripped), SO, NBO, MPATH, ExO and SwissLipids (from OBA's published merged import). Each: add the source, un-exclude its prefix, add the root rows in `subclasses.csv` that #2810 uses, and check `nolabels-violation` and `no-dangling-violation` are both 0. NCIT, SIO, ENVO, CLM, CARO, CHMO, FOODON, IDO, HsapDv, RnorDv and the non-OBO IRIs stay excluded, as in #2810.

### Stage 7. Flip the packaging to the EFO 4 layout (one release)

`use_base_merging: true`, `imports/merged_import.owl` as the index plus `imports/merged/` shards (216 files, none over 10 MiB), one catalog entry per shard, the `IAO:0000700` root annotation for OLS, owlmake ≥ 0.2.12, and the fifteen import statements in `efo-edit.owl` replaced by one. This is PR #2810 rebased onto a master that already contains everything else.

Acceptance: the release is axiom-identical to the previous release built from the per-ontology modules (#2808 verified that shards and a single module give identical releases; the comparison here is against Stage 5 and 6 output), class count unchanged. Consumers see nothing except OLS showing one root. Editors see the new layout, documented in `README-editors.md`.

Rollback: keep the per-ontology modules for one release.

### Stage 8. Close out

Docs (README, CLAUDE.md, the import guide), delete the `efo-4` branch and label, tick #2800, and take the version decision: keep counting 3.x, tag 4.0.0 as a release that changes nothing, or move to dates.

## 5. Consumers and what changes for them

| Consumer | Depends on | Stages that touch it | What to say and when |
|---|---|---|---|
| GWAS Catalog | term IRIs and labels; trait categories from EFO ancestors; `gwas_terms.tsv` mappings | 1 (#2809), 3c, 4 (OBA closure), 5 (OBA) | contract check every release; one-release-ahead note when ancestors of mapped terms change |
| Open Targets | `efo_otar_slim`/`efo_otar_profile` assets; therapeutic areas from ancestors; disease IDs | 1 (#2796), 3c, 5 (HP, OBA) | bring the slim/profile build into the gate (Stage 0); announce TA membership changes |
| Expression Atlas / ArrayExpress | anatomogram components; experimental-factor categories (`area`, `time`, …) | 1 (#2806), 4 (#2804 obsoletions) | the 45 non-entailed anatomy relations and the PATO-copy obsoletions need a direct heads-up |
| OLS | `efo.owl` (348 MB today), root terms, hierarchical properties | 3c, 5, 6, 7 | file grows across Stages 5 and 6; root annotation at Stage 7; test on OLS staging each release |
| EVA / ClinVar | imported MONDO/HP terms | none beyond normal curation | contract check |
| OBO-format users (`efo.obo` is the most downloaded asset, 106 downloads for 3.94.0) | is_a axis only | 5 and 6 (size) | note the size growth; consider gzipped assets |
| Editors and agents | `efo-edit.owl` layout, `om` commands | 2, 7 | README-editors and the agent specs, already written on `efo-4` |

## 6. The gate in detail

Run in the release PR (and on demand in any PR that touches imports or logic):

1. **Hierarchy**: `reasoner_hierarchy_diff.py` candidate vs last published `efo.owl`; lost edges must be listed in the PR; gained edges are reported.
2. **Counts**: `class-count-by-prefix.tsv` delta; file sizes of `efo.owl`, `efo.obo`, `efo.json` against a budget agreed in Stage 0.
3. **Existing IRIs**: labels, definitions and `owl:deprecated` changed on IRIs present in the last release.
4. **Obsoletions**: the notes generator's delta (#2826) with replacements.
5. **Consumer contracts**: GWAS mappings, anatomogram IDs, OTAR roots, EVA batches resolve and keep their ancestors.
6. **Logic**: ELK coherent; weekly HermiT job green; `nolabels`, `no-dangling`, `duplicate-label` (EFO-scoped) at 0.
7. **Reproducibility**: the release-notes consistency gate (#2826) stays as it is: notes, reports and artefacts from one build with pinned mirrors.

## 7. Schedule (proposal)

| Release | Month | Steps | Consumer-visible change |
|---|---|---|---|
| 3.95.0 | Oct 2026 | Stage 0; Stage 1 first half (#2785, #2774, #2775, #2777, #2784) | obsoletions only |
| 3.96.0 | Nov 2026 | Stage 1 second half (#2806, #2809, #2814, #2813, #2796); Stage 2 | anatomy roll-up and two OBA groupings; build swap invisible |
| 3.97.0 | Dec 2026 | Stage 3a, 3b; hygiene deletions | none expected |
| 3.98.0 | Jan 2027 | Stage 3c (ELK); Stage 4 PATO/taxslim | the #2793 edge table; about 530 new classes |
| 3.99.0 | Feb 2027 | Stage 4 duplicates part 1, `subclasses.csv` audit, OBA closure; Stage 5 small ontologies | obsoletions; OBA parents |
| 3.100.0 | Mar 2027 | Stage 4 duplicates part 2; Stage 5 CL, GO; Stage 6 BFO, COB | relations on CL/GO terms |
| 3.101.0 | Apr 2027 | Stage 5 UBERON; Stage 6 IAO, SO | relations on anatomy |
| 3.102.0 | May 2027 | Stage 5 CHEBI; Stage 6 NBO, MPATH | relations on chemicals |
| 3.103.0 | Jun 2027 | Stage 5 HP; Stage 6 ExO, SwissLipids | relations on phenotypes |
| 3.104.0 | Jul 2027 | Stage 5 OBA | the measurement branch gets its logic back |
| 3.105.0 | Aug 2027 | Stage 7 packaging; Stage 8 | none; EFO 4 complete |

Compressed variant, if the first four releases go cleanly: fold Stage 5 into two releases (everything but OBA, then OBA with the last of Stage 6) and finish by May 2027. The per-ontology schedule above is the "tiny steps" answer; the compressed one trades three months for larger monthly diffs.

## 8. Decisions needed from the team

1. Version policy (#2780): keep 3.x throughout, dates, or a cosmetic 4.0.0 at the end.
2. Whether to publish the `efo-4-preview` asset from Stage 0.
3. #2796: obsolete the two EFO craniopharyngioma subtypes (Arwa's proposal) or relocate them (#2812).
4. Timing and wording of the #2804 obsoletions for Expression Atlas users.
5. Whether PR's HGNC and MGI gene classes stay or are excluded as OBA does (affects Stage 5's PR handling and Stage 7).
6. Per-ontology Stage 5 (recommended) or the compressed variant.
7. Who owns the consumer contract lists (GWAS, Open Targets, Expression Atlas, EVA), since they are the thing that makes each step safe to ship.
