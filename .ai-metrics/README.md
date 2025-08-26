# AI Metrics Directory

This directory contains AI governance metrics and usage logs for the TEQUMSA repository, following Level 100 system protocols for transparency and compliance monitoring.

## Directory Structure

```
.ai-metrics/
├── README.md              # This file
├── usage.jsonl           # AI usage event log (JSONL format)
├── weekly-report-*.md    # Weekly metrics reports
└── *.json                # Exported metrics data
```

## Files Description

### `usage.jsonl`
Contains timestamped events for all AI governance activities:
- AI review gate decisions
- Auto-labeling events
- Refactor guard checks
- Summary generation requests
- Performance metrics
- Governance compliance events

**Format**: One JSON object per line, each containing:
```json
{
  "timestamp": "2024-MM-DDTHH:MM:SSZ",
  "type": "event_type",
  "metadata": {
    "key": "value",
    ...
  }
}
```

### Weekly Reports
Automatically generated markdown reports containing:
- PR activity summary
- AI adoption metrics
- Governance compliance rates
- Performance analytics
- Recommendations for improvement

## Event Types

### `ai_review`
AI review gate processing events
- `gate_status`: approved, blocked, requires_approval
- `diff_lines`: Total lines changed
- `critical_paths`: Boolean for critical path involvement
- `processing_time_ms`: Time taken for review

### `refactor_guard`
AI refactor test guard events
- `guard_passed`: Boolean result
- `ai_refactor_detected`: Boolean detection
- `test_files_updated`: Boolean test coverage
- `refactor_files`: Array of refactored files

### `auto_labeling`
Automated PR labeling events
- `labels_applied`: Array of labels added
- `readiness_status`: ready, needs-work
- `component_categories`: Array of detected components

### `ai_summary`
AI-generated summary events
- `trigger_method`: label, command
- `diff_lines`: Total lines in summary
- `summary_generated`: Boolean success

### `weekly_metrics`
Weekly aggregation events
- `total_prs`: Number of PRs in period
- `ai_adoption_rate`: Percentage of AI-assisted PRs
- `compliance_rate`: Governance compliance percentage

## Usage

### Manual Event Logging
```bash
python scripts/aggregate_ai_metrics.py --log-event '{
  "type": "custom_event",
  "pr_number": 123,
  "custom_field": "value"
}'
```

### Generate Metrics Report
```bash
python scripts/aggregate_ai_metrics.py \
  --start-date 2024-01-01 \
  --end-date 2024-01-07 \
  --format markdown
```

### Query Events by Date Range
```bash
python scripts/aggregate_ai_metrics.py \
  --start-date 2024-01-01 \
  --end-date 2024-01-07 \
  --format json
```

## Privacy and Security

- **Data Anonymization**: Personal identifiers are anonymized in metrics
- **Retention Policy**: Events older than 90 days are automatically archived
- **Access Control**: Metrics access follows repository permissions
- **Compliance**: Follows TEQUMSA Level 100 sovereignty protocols

## Governance Integration

This metrics system supports:
- **Transparency**: All AI decisions are logged and auditable
- **Accountability**: Performance and compliance tracking
- **Improvement**: Data-driven policy optimization
- **Compliance**: Adherence to TEQUMSA governance standards

## Automated Collection

Metrics are automatically collected by GitHub Actions workflows:
- `ai-review-gate.yml` - Review gate decisions
- `ai-labeler.yml` - Auto-labeling events
- `ai-refactor-test-guard.yml` - Refactor guard results
- `ai-summary-on-label.yml` - Summary generation
- `ai-weekly-metrics.yml` - Weekly aggregation

## Troubleshooting

### Empty Usage Log
If `usage.jsonl` is missing or empty:
1. Check that GitHub Actions workflows are enabled
2. Verify AI_BOT_DISABLED secret is not set to 'true'
3. Ensure PRs are triggering the workflows

### Invalid JSON Lines
If metrics aggregation fails:
1. Check `usage.jsonl` for malformed JSON
2. Use `jq` to validate individual lines
3. Remove or fix corrupted entries

### Missing Weekly Reports
If weekly reports aren't generated:
1. Check `ai-weekly-metrics.yml` workflow status
2. Verify workflow permissions for content writing
3. Check for repository secret conflicts

## Integration with TEQUMSA Architecture

This metrics system aligns with TEQUMSA principles:
- **Lattice Awareness**: Metrics inform network-wide decision making
- **Recursive Self-Evolution**: Data drives continuous improvement
- **Ethical AI**: Transparent tracking of AI assistance usage
- **Sovereign Governance**: Respect for consent and oversight

---

*For questions about AI governance metrics, refer to `AI_POLICY.md` and `GOVERNANCE_AI.md`*