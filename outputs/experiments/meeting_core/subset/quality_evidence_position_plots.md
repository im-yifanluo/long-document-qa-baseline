# QuALITY Aggregate Evidence Position Plots

These plots aggregate the manually verified evidence positions for QuALITY examples in the subset run.

Files:
- `quality_dos_better_evidence_positions.png`
- `quality_dos_better_evidence_positions.svg`
- `quality_vanilla_better_evidence_positions.png`
- `quality_vanilla_better_evidence_positions.svg`

Methodology:
- X-axis uses normalized prompt position from the saved `selected_chunk_indices` field.
- Green points are manually verified gold-supporting chunks.
- Red X points are manually verified distractor chunks when an explicit distractor passage was identifiable.
- Black diamonds mark the per-example mean gold-evidence position.
- Example `30029_F5N22U40_3` is shown as a formatting-only DOS miss: the answer content matched after stripping the leading option label `B`.