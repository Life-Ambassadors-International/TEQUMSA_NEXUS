# TEQUMSA Codex Integration Guide

## Overview

This document provides a comprehensive guide for integrating OpenAI Codex functionality into the TEQUMSA AGI Interface. The integration uses a feature-flagged approach with ethical safeguards and git subtree management for external dependencies.

## Architecture

### Feature Flag Pattern

The Codex integration uses environment-based feature flags for safe deployment:

```bash
# Enable Codex integration
export TEQUMSA_CODEX_ENABLED=true

# Disable Codex integration (default)
unset TEQUMSA_CODEX_ENABLED
# or
export TEQUMSA_CODEX_ENABLED=false
```

### Git Subtree Management

External Codex dependencies are managed via git subtree to maintain source code integrity:

```bash
# TODO: Add subtree when ready
git subtree add --prefix=external/codex https://github.com/openai/codex-integration main --squash

# Update subtree
git subtree pull --prefix=external/codex https://github.com/openai/codex-integration main --squash
```

## Setup and Installation

### Prerequisites

- Python 3.11+
- pytest testing framework
- Git subtree support

### Development Environment

1. **Clone and setup the repository**:
```bash
git clone https://github.com/Life-Ambassadors-International/TEQUMSA_OPEN.git
cd TEQUMSA_OPEN
```

2. **Install testing dependencies**:
```bash
pip install pytest pytest-mock pytest-cov
```

3. **Verify scaffold installation**:
```bash
python3 -c "from backend.codex_adapter import get_codex_status; print(get_codex_status())"
```

## Usage

### Basic Integration

```python
from backend.codex_adapter import CodexAdapter, is_codex_available

# Check if Codex is available
if is_codex_available():
    adapter = CodexAdapter()
    
    # Generate code
    result = adapter.generate("def fibonacci(n):")
    print(result)
else:
    print("Codex integration not available")
```

### Status Checking

```python
from backend.codex_adapter import get_codex_status

status = get_codex_status()
print(f"Feature flag enabled: {status['feature_flag_enabled']}")
print(f"Subtree available: {status['subtree_available']}")
print(f"Fully available: {status['fully_available']}")

if not status['fully_available']:
    print(f"Reason: {status['reason']}")
```

### Capabilities Query

```python
from backend.codex_adapter import CodexAdapter

adapter = CodexAdapter()
capabilities = adapter.get_capabilities()

if capabilities['available']:
    print(f"Supported languages: {capabilities['languages']}")
    print(f"Max tokens: {capabilities['max_tokens']}")
    print(f"Features: {capabilities['features']}")
```

## Testing

### Running Integration Tests

```bash
# Run all Codex integration tests
pytest tests/integration/test_codex_adapter.py -v

# Run with coverage
pytest tests/integration/test_codex_adapter.py --cov=backend.codex_adapter --cov-report=term-missing

# Run specific test categories
pytest tests/integration/test_codex_adapter.py::TestCodexAdapterDisabled -v
pytest tests/integration/test_codex_adapter.py::TestCodexAdapterFullyEnabled -v
```

### Test Coverage

The integration test suite covers:

- ✅ Feature flag disabled state (default)
- ✅ Feature flag enabled but subtree missing
- ✅ Full integration with simulated subtree
- ✅ Input validation and error handling
- ✅ Edge cases and integration patterns

### Manual Testing

```bash
# Test disabled state (default)
python3 -c "
from backend.codex_adapter import CodexAdapter
adapter = CodexAdapter()
print('Status:', adapter.get_status())
try:
    adapter.generate('test')
except RuntimeError as e:
    print('Expected error:', e)
"

# Test enabled state without subtree
TEQUMSA_CODEX_ENABLED=true python3 -c "
from backend.codex_adapter import CodexAdapter
adapter = CodexAdapter()
print('Status:', adapter.get_status())
"
```

## Configuration

### Environment Variables

| Variable | Values | Default | Description |
|----------|--------|---------|-------------|
| `TEQUMSA_CODEX_ENABLED` | `true`/`false` | `false` | Enable/disable Codex integration |

### Directory Structure

```
external/
├── SOURCE_LOCK.md          # External dependency tracking
└── codex/                  # TODO: Git subtree (not yet added)
    ├── README.md
    ├── __init__.py
    └── ...

backend/
├── codex_adapter.py        # Pure stdlib adapter
└── ...

tests/
└── integration/
    └── test_codex_adapter.py  # Comprehensive test suite
```

## Ethics and Consent

### Consent Validation

The adapter includes placeholder consent validation:

```python
adapter = CodexAdapter()

# Check user consent before code generation
if adapter.validate_consent(user_id="user123"):
    result = adapter.generate(prompt)
else:
    # Handle consent rejection
    pass
```

### Ethical Safeguards

- **Feature flag control**: Integration can be quickly disabled
- **Consent validation**: User consent required for AI code generation
- **Input validation**: Prompt sanitization and validation
- **Error handling**: Graceful degradation when service unavailable

## Troubleshooting

### Common Issues

1. **"Feature flag disabled" error**:
   ```bash
   export TEQUMSA_CODEX_ENABLED=true
   ```

2. **"Subtree not available" error**:
   - The external/codex directory needs to be added via git subtree
   - Currently in scaffold phase - subtree not yet integrated

3. **Import errors**:
   ```bash
   # Ensure backend directory is in Python path
   export PYTHONPATH="${PYTHONPATH}:$(pwd)/backend"
   ```

### Debugging

Enable verbose logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

from backend.codex_adapter import CodexAdapter
adapter = CodexAdapter()
print(adapter.get_status())
```

## Development Roadmap

### Current Status: Scaffold Phase ✅

- ✅ Feature flag pattern implemented
- ✅ Pure stdlib adapter created
- ✅ Comprehensive test suite
- ✅ Documentation and setup guides
- ✅ Ethical safeguards framework

### Next Steps: Integration Phase

- [ ] Add actual Codex API subtree via git subtree
- [ ] Implement real API calls replacing placeholder methods
- [ ] Add OpenAI API key configuration
- [ ] Implement rate limiting and error handling
- [ ] Add consent management system
- [ ] Enable automated PR workflows

### Future Enhancements

- [ ] Multi-language code generation support
- [ ] Code completion and refactoring features
- [ ] Integration with TEQUMSA consciousness simulation
- [ ] Performance monitoring and analytics
- [ ] Advanced ethical guardrails

## Security Considerations

- **API Key Management**: Secure storage of OpenAI API credentials
- **Input Sanitization**: Validation of user prompts
- **Output Filtering**: Content filtering for generated code
- **Audit Logging**: Track all code generation requests
- **Rate Limiting**: Prevent API abuse

## Support

For technical issues or questions:

1. Review the [troubleshooting section](#troubleshooting)
2. Check test suite output: `pytest tests/integration/test_codex_adapter.py -v`
3. Review integration status: `python3 -c "from backend.codex_adapter import get_codex_status; print(get_codex_status())"`
4. Consult the main [Claude.md](../Claude.md) documentation
5. Submit issues via GitHub issue tracker

---

**Note**: This integration is currently in scaffold phase. The git subtree integration and real API implementation are pending future development phases.