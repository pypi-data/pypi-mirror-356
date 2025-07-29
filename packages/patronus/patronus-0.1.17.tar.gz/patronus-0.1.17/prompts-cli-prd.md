# Patronus CLI - Prompt Management PRD

## Overview

This document outlines the requirements for adding CLI functionality to the Patronus Python SDK, specifically focusing on prompt management commands. The CLI will provide `patronus prompts pull` and `patronus prompts tidy` commands to manage local prompt storage and synchronization with the Patronus platform.

## Goals

- Enable offline/local prompt management workflow
- Provide version control-like experience for prompt management
- Integrate seamlessly with existing Patronus SDK configuration and storage
- Support project-based prompt organization
- Maintain data consistency between local storage and Patronus platform

## Non-Goals (For This Phase)

- `patronus prompts push` command
- `patronus prompts sync` command  
- Interactive command modes
- Label creation/modification via CLI
- Multiple output formats (JSON, table, etc.)
- Dry-run functionality

## Architecture

### CLI Framework
- Use Click framework for command structure
- Integrate with existing Patronus SDK authentication and configuration
- Share storage layer with SDK (no separate CLI-specific storage)

### Command Structure
```
patronus prompts pull [OPTIONS] [PROMPT_NAME]
patronus prompts tidy [OPTIONS]
```

## Authentication & Configuration

### Authentication
- Reuse existing SDK authentication mechanism
- Support `PATRONUS_API_KEY` environment variable
- Support `patronus.yaml` configuration file
- Follow same precedence: function params > env vars > yaml > defaults

### Configuration
- Share configuration system with SDK (`patronus.config`)
- Support global `--resource-dir` flag with fallback to config
- Default resource directory: `.patronus/`

## Commands Specification

### `patronus prompts pull`

**Purpose**: Download prompts from Patronus platform to local storage

**Syntax**: 
```bash
patronus prompts pull [OPTIONS] [PROMPT_NAME]
```

**Options**:
- `--project-name TEXT`: Target specific project
- `--all-projects`: Pull from all accessible projects  
- `--name-prefix TEXT`: Filter prompts by name prefix
- `--all-revisions`: Pull all revisions (default: latest + labeled only)
- `--revision INTEGER`: Pull specific revision
- `--label TEXT`: Pull revisions with specific label
- `--resource-dir PATH`: Override resource directory (global flag)
- `-v, --verbose`: Verbose output

**Behavior**:

1. **Project Resolution**:
   - If `--all-projects` specified: iterate through all accessible projects
   - If `--project-name` specified: use that project
   - If neither specified: use project from `patronus.yaml` config
   - If no project available: error with clear message

2. **Project Validation**:
   - Verify project ID matches stored info in `info.yaml`
   - If project ID mismatch: error (suggests account change)
   - If project doesn't exist: error unless special flag provided (future)

3. **Prompt Filtering**:
   - If `PROMPT_NAME` specified: pull only that prompt
   - If `--name-prefix` specified: pull prompts starting with prefix
   - If `--label` specified: pull all revisions with that label
   - Otherwise: pull all prompts in project

4. **Revision Selection**:
   - Default: latest revision + any labeled revisions
   - If `--all-revisions`: pull every revision
   - If `--revision`: pull only that specific revision
   - If `--label`: pull revision(s) with that label

5. **Error Handling**:
   - Abort entire operation on any failure (no partial success)
   - Clear error messages with actionable guidance
   - Verbose mode shows detailed operation progress

**Examples**:
```bash
# Error - requires project specification
patronus prompts pull

# Pull all prompts in Global project (latest + labeled)
patronus prompts pull --project-name Global

# Pull all revisions for Global project
patronus prompts pull --project-name Global --all-revisions

# Pull from all projects
patronus prompts pull --all-projects

# Pull prompts with name prefix (from config project)
patronus prompts pull --name-prefix my-agent

# Pull specific prompt
patronus prompts pull percival/chat/general/instructions/about

# Pull revisions with specific label
patronus prompts pull --label dev
```

### `patronus prompts tidy`

**Purpose**: Clean up local prompt storage by removing unlabeled, non-latest revisions

**Syntax**:
```bash
patronus prompts tidy [OPTIONS]
```

**Options**:
- `--resource-dir PATH`: Override resource directory (global flag)
- `-v, --verbose`: Verbose output

**Behavior**:

1. **Project Validation**:
   - For each project in local storage, verify project still exists
   - Verify project ID matches (detect account changes)
   - If project doesn't exist or ID mismatch: abort with error message
   - Recommend manual cleanup or special flag for deleted accounts

2. **Label Synchronization**:
   - Query current labels for each prompt from API
   - Update local `info.yaml` with current label mappings
   - If label moved to different revision: update info, allow pulling new revision
   - Remove labels that no longer exist (with warning message)

3. **Revision Cleanup**:
   - Identify revisions that are neither latest nor labeled
   - Remove these revision directories and files
   - Update `info.yaml` to reflect changes
   - Preserve `description.txt` files (update if changed on platform)

4. **Reporting**:
   - Print summary of actions taken
   - In verbose mode: show each file/directory operation
   - Report any warnings (moved labels, deleted labels, etc.)

**Examples**:
```bash
# Clean up current resource directory
patronus prompts tidy

# Clean up with verbose output
patronus prompts tidy -v

# Clean up custom resource directory  
patronus prompts tidy --resource-dir ./my-prompts
```

## File Structure

### Local Storage Layout
```
.patronus/
├── info.yaml                    # Project and prompt metadata
└── <project_name>/
    └── prompts/
        └── <prompt_name>/
            ├── description.txt   # Prompt description
            ├── v1/
            │   ├── prompt.txt    # Prompt body
            │   └── metadata.json # Revision metadata
            ├── v2/
            └── v4/              # Latest revision
                ├── prompt.txt
                └── metadata.json
```

### info.yaml Structure
```yaml
# This file is automatically managed by Patronus CLI
# Do not edit manually as changes will be overwritten

projects:
  - name: "default"
    id: "80649637-4a6f-44b0-a11b-614081864f23"
  - name: "percival" 
    id: "135f3c52-b27a-4bed-a578-e616320d9d86"

prompts:
  - name: "percival/chat/general/instructions/about"
    project_name: "percival"
    labels:
      - name: "dev"
        points_to:
          version: "v11"
      - name: "prod"
        points_to:
          version: "v4"
```

### metadata.json Structure
```json
{
  "temperature": 0.7,
  "tone": "helpful"
}
```

## Error Handling

### Error Categories
1. **Configuration Errors**: Missing API key, invalid config file
2. **Authentication Errors**: Invalid API key, network issues
3. **Project Errors**: Project not found, ID mismatch, access denied
4. **Prompt Errors**: Prompt not found, invalid revision/label
5. **File System Errors**: Permission issues, disk space, corrupted files

### Error Messages
- Clear, actionable error messages
- Include suggested remediation steps
- In verbose mode: include technical details and stack traces
- Consistent error codes for automation/scripting

### Exit Codes
- `0`: Success
- `1`: General error
- `2`: Configuration error
- `3`: Authentication error
- `4`: Project/prompt not found
- `5`: File system error

## Global Flags

### `--resource-dir PATH`
- Override default resource directory
- Falls back to `PATRONUS_RESOURCE_DIR` env var
- Falls back to `resource_dir` in `patronus.yaml`
- Default: `.patronus/`
- Applied to all commands

### `-v, --verbose`
- Enable verbose output
- Show detailed operation progress
- Include API request/response details
- Show file system operations

## Future Considerations

### Planned Extensions
- `patronus prompts push` command
- `patronus prompts sync` command  
- Support for deleted/migrated accounts (`--allow-deleted-projects`)
- Multiple name prefix support
- Interactive selection modes

### Integration Points
- Share all storage and configuration with SDK
- Maintain compatibility with SDK prompt loading
- Support for SDK's prompt provider system
- Integration with experiment tracking

## Implementation Notes

### Dependencies
- Click for CLI framework
- Existing Patronus SDK for API client and configuration
- PyYAML for configuration file handling
- Rich/typer for enhanced CLI output (optional)

### Testing Strategy
- Unit tests for each command and major functions
- Integration tests with mock API responses
- File system operation tests with temporary directories
- Configuration precedence tests
- Error condition tests

### Performance Considerations
- Concurrent downloads for multiple prompts
- Incremental updates (only download changed content)
- Progress indicators for long operations
- Efficient file system operations

## Success Metrics

- Users can successfully manage prompts offline
- Seamless integration with existing SDK workflows
- Clear, actionable error messages reduce support burden
- File structure supports version control workflows
- Consistent behavior across different operating systems