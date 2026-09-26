## ADDED Requirements

### Requirement: Transcription cost is measured at what it is billed for
Cost measurements of Tier-2 transcription runs SHALL report a price-weighted figure computed from a
per-model price table, SHALL reconstruct output tokens from context growth rather than from logged
usage, and SHALL read per-turn usage from persisted subagent transcripts where they exist. Raw token
volume MAY be reported alongside, and any comparison MUST state which of the two metrics it uses.

Logged `output_tokens` in Claude Code transcripts is a stream-start snapshot and undercounts output
by orders of magnitude on long replies; the plan meter weights usage approximately by API price, not
by raw volume. A cost model fitted to raw volume with logged output optimizes cache reads, the
cheapest token class, and cannot see thinking, the most expensive one.

#### Scenario: A run is re-scored
- **WHEN** `pipeline/measure_session.py` reports on a session with subagent transcripts
- **THEN** it prints, per subagent and in total, cache reads, cache writes by TTL, fresh input and
  reconstructed output, with the API-price cost of each and each one's share of the total
- **AND** it prints the raw-volume total separately, labelled as such

#### Scenario: Output is reconstructed
- **WHEN** a turn's logged `output_tokens` is smaller than the next turn's context growth minus the
  tool results fed into it
- **THEN** the reconstructed figure is used, and the visible/thinking split is reported as an
  estimate

#### Scenario: The instrument is checked against known answers
- **WHEN** the reconstruction is changed
- **THEN** its tests include a transcript whose true output is known, and the reconstructed total
  falls within 5% of it
