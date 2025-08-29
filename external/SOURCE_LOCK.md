# External Sources Lock File

## Codex Integration Source

**Status**: Placeholder - Subtree not yet added

### Git Subtree Configuration
```bash
# TODO: Add subtree when ready
# git subtree add --prefix=external/codex https://github.com/openai/codex-integration main --squash
```

### Current Configuration
- **Commit SHA**: `codex` (placeholder)
- **Source Repository**: TBD (OpenAI Codex integration repository)
- **Branch/Ref**: main
- **Last Updated**: TBD

### Setup Requirements

#### Python Environment
- **Python Version**: 3.11+
- **Package Manager**: pip
- **Virtual Environment**: Recommended

#### Dependencies
```bash
# Core testing framework (minimal)
pip install pytest

# Integration testing requirements
pip install pytest-mock
pip install pytest-cov
```

### Integration Testing

#### Test Suite Location
- Path: `tests/integration/test_codex_adapter.py`
- Framework: pytest
- Status: Feature flag intentionally disabled by default

#### Running Tests
```bash
# Run integration tests (will show disabled state)
pytest tests/integration/ -v

# Run with coverage
pytest tests/integration/ --cov=. --cov-report=term-missing

# Run specific codex tests
pytest tests/integration/test_codex_adapter.py -v
```

### Summary

This file tracks external source dependencies for the TEQUMSA project. The Codex integration is currently in scaffold phase with:

- ✅ Feature flag pattern implemented
- ✅ Integration test framework ready
- ✅ Adapter interface defined
- ⚠️ Subtree integration pending
- ⚠️ API implementation placeholder

**Next Steps**:
1. Add actual Codex subtree repository
2. Implement real API integration
3. Enable feature flag after testing
4. Add consent/ethics validation hooks