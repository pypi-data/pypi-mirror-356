# Additional CLI Design Considerations

This document outlines additional technical considerations for the Patronus CLI implementation based on deeper analysis of the codebase and the prompt management system architecture.

## Critical Implementation Requirements

### 1. PromptProvider Integration

**Current State**: The `LocalPromptProvider` in `src/patronus/prompts/clients.py` is currently a placeholder that returns `None`.

**CLI Approach**: The CLI should use the PromptProvider pattern from the SDK for all operations, including write operations like future `push` commands. This ensures consistency and allows the CLI to write to the resource directory through the same interface.

**Implementation Notes**:
- CLI should implement the LocalPromptProvider as part of the CLI work
- CLI operations should go through the provider interface for consistency
- The provider should return properly constructed `LoadedPrompt` objects with all required fields
- Write operations (future push commands) can also use the provider pattern

### 2. Enhanced Storage Format

Based on the `LoadedPrompt` model, the local storage needs to capture more information than initially specified:

```python
@dataclasses.dataclass
class LoadedPrompt(BasePrompt):
    prompt_definition_id: str      # UUID of the prompt definition
    project_id: str               # UUID of the project  
    project_name: str
    
    name: str
    description: Optional[str]
    
    revision_id: str              # UUID of the revision
    revision: int                 # Sequential revision number
    body: str
    normalized_body_sha256: str   # Hash for change detection
    metadata: Optional[dict[str, Any]]
    labels: list[str]             # Labels applied to this revision
    created_at: datetime.datetime
```

**Recommended Enhanced Storage Structure**:
```
.patronus/
├── info.yaml
└── <project_name>/
    └── prompts/
        └── <prompt_name_with_slashes>/  # Supports nested directories
            ├── definition.json          # Prompt definition metadata
            ├── description.txt
            └── revisions/
                ├── v1/
                │   ├── prompt.txt
                │   ├── metadata.json    # User metadata only
                │   └── revision.json    # System metadata (IDs, hash, timestamp)
                ├── v2/
                └── v4/
```

**Note**: Prompt names can contain slashes (e.g., "percival/chat/general/instructions/about") and should be stored in nested directory structures reflecting this hierarchy.

**revision.json Structure**:
```json
{
  "revision_id": "uuid-of-revision",
  "revision": 4,
  "normalized_body_sha256": "abc123...",
  "labels": ["prod", "stable"],
  "created_at": "2024-01-15T10:30:00Z"
}
```

**definition.json Structure**:
```json
{
  "prompt_definition_id": "uuid-of-definition",
  "project_id": "uuid-of-project",
  "name": "percival/chat/general/instructions/about",
  "latest_revision": 4
}
```

### 3. Normalized Body Hash for Change Detection

The system uses SHA-256 hashes of normalized prompt bodies for duplicate detection and change tracking.

**CLI Implementation**:
- Import and use `calculate_normalized_body_hash()` from `patronus.prompts.models`
- Store hash in `revision.json` for local change detection
- Use hash to avoid redundant downloads when body hasn't changed
- The `tidy` command can use hashes to identify truly identical revisions

### 4. Template Engine Handling

The CLI should not be opinionated about template engines - this is a user concern handled in their application code.

**CLI Approach**:
- CLI does not manage or store template engine information
- Template engine selection is handled by users in their SDK usage
- CLI focuses on prompt content and metadata storage only

### 5. Provider System Integration

The CLI should integrate cleanly with the existing provider configuration:

**Default Provider Order**: `["local", "api"]`
- Local provider checks CLI-managed storage first
- API provider used as fallback
- CLI should not interfere with this order

**Provider Factory Compatibility**:
- CLI's LocalPromptProvider implementation should be compatible with the existing provider factory pattern
- Consider how CLI updates affect cached prompts in the SDK

### 6. SDK Cache Interaction

The CLI should not be concerned with SDK caching behavior:

**CLI Approach**:
- CLI operations are independent of SDK cache state
- SDK manages its own cache lifecycle
- No need for CLI to consider or manage SDK caches

### 7. Error Type Compatibility

The CLI should use the same error types as the SDK for consistency:

**Import and Use Existing Errors**:
```python
from patronus.prompts.clients import (
    PromptNotFoundError,
    PromptProviderError,
    PromptProviderConnectionError,
    PromptProviderAuthenticationError,
)
```

**CLI-Specific Error Mapping**:
- Network issues → `PromptProviderConnectionError`
- Authentication failures → `PromptProviderAuthenticationError`
- File system errors → `PromptProviderError`
- Missing prompts → `PromptNotFoundError`

### 8. Project Structure and Entry Points

**pyproject.toml Updates Required**:
```toml
[project.scripts]
patronus = "patronus.cli.main:main"

[tool.hatch.metadata.hooks.uv-dynamic-versioning]
dependencies = [
    # ... existing dependencies ...
    "click>=8.0.0",
]
```

**CLI Module Structure**:
```
src/patronus/cli/
├── __init__.py
├── main.py          # Main CLI entry point
├── commands/
│   ├── __init__.py
│   ├── prompts.py   # Prompt management commands
│   └── common.py    # Shared command utilities
├── storage/
│   ├── __init__.py
│   ├── manager.py   # Storage operations
│   └── models.py    # Local storage models
└── providers/
    ├── __init__.py
    └── local.py     # LocalPromptProvider implementation
```

### 9. Configuration Usage

The CLI should use the SDK's configuration system directly:

**Configuration Priority** (same as SDK):
1. CLI arguments
2. Environment variables (`PATRONUS_*`)
3. `patronus.yaml` file
4. Default values

**Resource Directory Handling**:
- Use `resource_dir` from config (default: `./patronus`)
- Support `--resource-dir` global flag override
- Use SDK's configuration without modification

### 10. API Client Setup

**Direct API Client Usage**:
- CLI should NOT use `patronus.init()` or the context module to avoid unnecessary overhead
- CLI should create its own `patronus_api.Client` instance directly for faster boot time
- Avoid setting up tracing exporters and other SDK infrastructure not needed by CLI

**Minimal Client Setup**:
```python
from patronus.config import config
import patronus_api

cfg = config()
client = patronus_api.Client(
    api_key=cfg.api_key,
    base_url=cfg.api_url,
    timeout=cfg.timeout_s
)
```

**Forward Compatibility**:
- Design storage format to be extensible for future prompt features
- Consider how new prompt metadata fields would be handled
- Plan for backward compatibility with existing storage formats

### 11. Concurrency and File Locking

**File System Safety**:
- Multiple CLI processes could modify storage simultaneously
- Consider file locking for critical operations (info.yaml updates)
- Atomic file operations where possible (write to temp, then move)

**Progress Reporting**:
- For large operations, show progress without cluttering output
- Consider `rich` library for enhanced progress bars and formatting
- Support quiet mode for automation/scripting

### 12. Testing Strategy Considerations

**Test Data Management**:
- Mock API responses for integration tests
- Test storage format compatibility
- Validate LocalPromptProvider integration
- Test configuration inheritance

**Cross-Platform Compatibility**:
- File path handling (Windows vs Unix)
- Line ending consistency in stored files
- Unicode handling in prompt content

## Implementation Phases

### Phase 1: Core CLI (Current PRD)
- Basic `pull` and `tidy` commands
- Essential storage format
- Configuration integration

### Phase 2: Provider Integration
- Complete LocalPromptProvider implementation
- SDK integration testing
- Cache behavior documentation

### Phase 3: Enhanced Features
- Progress reporting improvements with `rich`
- Quiet mode for automation
- Advanced error handling
- Performance optimizations

## Dependencies

**Required New Dependencies**:
- `click>=8.0.0` for CLI framework
- `rich` for enhanced output formatting and progress bars
- Consider `typing-extensions` compatibility for older Python versions

**Optional Dependencies**:
- File locking library for concurrent access safety
- `tqdm` (already a dependency) for progress bars

## Backward Compatibility

**Storage Format Evolution**:
- Design storage format to be backward compatible
- Include version information in `info.yaml`
- Plan migration strategy for format changes

**SDK Integration**:
- Ensure CLI doesn't break existing SDK workflows
- Maintain compatibility with existing `patronus.yaml` configurations
- Test with various SDK usage patterns

---

This document should be considered alongside the main PRD to ensure a complete and robust CLI implementation that integrates seamlessly with the existing Patronus SDK architecture.